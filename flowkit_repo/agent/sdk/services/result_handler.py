"""Shared result parsing + DB update helpers for SDK direct execution and background processor."""

from __future__ import annotations
from typing import TYPE_CHECKING

from agent.db import crud
from agent.worker._parsing import _is_error, _extract_media_id, _extract_output_url

if TYPE_CHECKING:
    from agent.sdk.models.media import GenerationResult


def parse_result(raw: dict, req_type: str) -> GenerationResult:
    """Parse a raw FlowClient/OperationService response into a GenerationResult."""
    from agent.sdk.models.media import GenerationResult

    if _is_error(raw):
        error_msg = raw.get("error")
        if not error_msg:
            data = raw.get("data", {})
            if isinstance(data, dict):
                ef = data.get("error", "Unknown error")
                error_msg = ef.get("message", str(ef)[:200]) if isinstance(ef, dict) else str(ef)
            else:
                error_msg = "Unknown error"
        return GenerationResult(success=False, error=str(error_msg), raw=raw)

    media_id = _extract_media_id(raw, req_type)
    url = _extract_output_url(raw, req_type)
    return GenerationResult(success=True, media_id=media_id, url=url, raw=raw)


async def apply_scene_result(
    scene_id: str | None,
    req_type: str,
    orientation: str,
    result: GenerationResult,
) -> None:
    """Update scene DB fields after a successful generation.

    Handles cascade: image regen clears video+upscale, video regen clears upscale.
    This is the shared version of processor.py's _update_scene_from_result.
    """
    if not scene_id or not result.success:
        return

    p = "vertical" if orientation == "VERTICAL" else "horizontal"
    updates = {}

    if req_type in ("GENERATE_IMAGE", "REGENERATE_IMAGE", "EDIT_IMAGE"):
        updates.update({
            f"{p}_image_media_id": result.media_id,
            f"{p}_image_url": result.url,
            f"{p}_image_status": "COMPLETED",
            # Cascade: clear downstream
            f"{p}_video_media_id": None, f"{p}_video_url": None, f"{p}_video_status": "PENDING",
            f"{p}_upscale_media_id": None, f"{p}_upscale_url": None, f"{p}_upscale_status": "PENDING",
        })
        # Chain cascade: update parent's end_scene_media_id so its video
        # transitions to this child's new image
        scene = await crud.get_scene(scene_id)
        if scene and scene.get("parent_scene_id") and result.media_id:
            await crud.update_scene(
                scene["parent_scene_id"],
                **{f"{p}_end_scene_media_id": result.media_id},
            )
    elif req_type in ("GENERATE_VIDEO", "REGENERATE_VIDEO", "GENERATE_VIDEO_REFS"):
        updates.update({
            f"{p}_video_media_id": result.media_id,
            f"{p}_video_url": result.url,
            f"{p}_video_status": "COMPLETED",
            # Cascade: clear upscale
            f"{p}_upscale_media_id": None, f"{p}_upscale_url": None, f"{p}_upscale_status": "PENDING",
        })
        # Auto-download and sync to project output folder
        scene = await crud.get_scene(scene_id)
        if scene and result.url:
            import os, shutil, urllib.request, json
            from agent.utils.slugify import slugify

            pid = scene.get("_project_id") or scene.get("project_id")
            project = await crud.get_project(pid) if pid else None
            proj_name = project.get("name") if project else "vox_project"
            proj_dir = os.path.join("..", "out", slugify(proj_name))

            if os.path.exists(os.path.dirname(os.path.abspath(proj_dir))):
                clips_dir = os.path.join(proj_dir, "clips")
                os.makedirs(clips_dir, exist_ok=True)
                order = scene.get("display_order", 0)
                dest_path = os.path.join(clips_dir, f"clip_{order+1:02d}.mp4")

                try:
                    if result.url.startswith("file://"):
                        local_src = result.url.replace("file://", "").lstrip("/")
                        if os.path.exists(local_src):
                            shutil.copy(local_src, dest_path)
                    elif result.url.startswith("http"):
                        urllib.request.urlretrieve(result.url, dest_path)

                    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 0:
                        bpath = os.path.join(proj_dir, "beats.json")
                        if os.path.exists(bpath):
                            with open(bpath, encoding="utf-8") as f:
                                bdoc = json.load(f)
                            beats_list = bdoc.get("beats", [])
                            if order < len(beats_list):
                                beats_list[order]["clip_path"] = os.path.abspath(dest_path)
                                beats_list[order]["video_url"] = result.url
                                with open(bpath, "w", encoding="utf-8") as f:
                                    json.dump(bdoc, f, ensure_ascii=False, indent=2)
                except Exception as e:
                    pass

    elif req_type == "UPSCALE_VIDEO":
        updates.update({
            f"{p}_upscale_media_id": result.media_id,
            f"{p}_upscale_url": result.url,
            f"{p}_upscale_status": "COMPLETED",
        })

    if updates:
        await crud.update_scene(scene_id, **updates)


async def apply_character_result(
    character_id: str,
    result: GenerationResult,
) -> None:
    """Update character DB fields after a successful reference image generation."""
    if not result.success:
        return
    updates = {}
    if result.media_id:
        updates["media_id"] = result.media_id
    if result.url:
        updates["reference_image_url"] = result.url
    if updates:
        await crud.update_character(character_id, **updates)
