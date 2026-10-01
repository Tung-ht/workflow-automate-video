#!/usr/bin/env python3
"""
Provider abstraction — the pluggable media backend the pipeline stages talk to.

Atlas Cloud is the default and, for now, the only backend. Stages call a Provider
(submit_image/video/audio, remove_bg, get_status, upload, download) instead of a
concrete client, so adding a backend is: subclass Provider + one registry entry.
Pick a backend per project with beats.json `{"provider": "atlas_cloud"}` (default).

The layer is a thin in-process wrapper — zero extra network hops, so it does NOT
slow the pipeline; the only cost is the API latency, which is unchanged.
"""
import os
import time
from abc import ABC, abstractmethod

import atlas_cloud


class ProviderError(RuntimeError):
    pass


class Provider(ABC):
    """The surface the stages need. get_status normalizes every backend's polling
    response to {status: pending|completed|failed, output: <url|None>, error}."""
    name = "base"

    @abstractmethod
    def submit_image(self, model, prompt, **params): ...
    @abstractmethod
    def submit_video(self, model, prompt, **params): ...
    @abstractmethod
    def submit_audio(self, model, **params): ...
    @abstractmethod
    def remove_bg(self, model, image_url, **params): ...
    @abstractmethod
    def get_status(self, job_id): ...
    @abstractmethod
    def upload(self, path): ...
    @abstractmethod
    def download(self, url, dest): ...


class AtlasCloudProvider(Provider):
    """Wraps the atlas_cloud client — identical behavior to calling it directly."""
    name = "atlas_cloud"

    def submit_image(self, model, prompt, **params):
        raise PermissionError("Atlas Cloud image generation is STRICTLY BANNED by channel rules. Use flowkit (Google Flow) only.")

    def submit_video(self, model, prompt, **params):
        raise PermissionError("Atlas Cloud video generation is STRICTLY BANNED by channel rules. Use flowkit (Google Flow) only.")

    def submit_audio(self, model, **params):
        return atlas_cloud.submit_media(model, **params)

    def remove_bg(self, model, image_url, **params):
        body = {"model": model, "image": image_url, **params}
        return atlas_cloud._post("/model/generateImage", body)["data"]["id"]

    def get_status(self, job_id):
        try:
            d = atlas_cloud._get(f"/model/prediction/{job_id}").get("data", {})
        except atlas_cloud.AtlasCloudError as e:
            return {"status": "failed", "output": None, "error": str(e)}
        st = d.get("status")
        if st in ("completed", "succeeded"):
            out = d.get("outputs") or d.get("output")
            out = out[0] if isinstance(out, list) else out
            return {"status": "completed", "output": out, "error": None}
        if st == "failed":
            return {"status": "failed", "output": None, "error": d.get("error", "")}
        return {"status": "pending", "output": None, "error": None}

    def upload(self, path):
        return atlas_cloud.upload(path)

    def download(self, url, dest):
        return atlas_cloud.download(url, dest)


class FlowkitProvider(AtlasCloudProvider):
    """Routes image and video generation to FlowKit (Google Flow) instead of Atlas Cloud."""
    name = "flowkit"

    def __init__(self):
        super().__init__()
        import os
        self.base_url = os.getenv("FLOWKIT_API_URL", "http://127.0.0.1:8100/api")
        self.project_id = None
        self.video_id = None

    def _req_post(self, path, json_data):
        import urllib.request, json
        req = urllib.request.Request(self.base_url + path, data=json.dumps(json_data).encode(), headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
            
    def _req_get(self, path):
        import urllib.request, json
        req = urllib.request.Request(self.base_url + path)
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
            
    def _ensure_project(self):
        if not self.project_id:
            try:
                active = self._req_get("/active-project")
                if active and active.get("project_id"):
                    self.project_id = active["project_id"]
                    self.video_id = active.get("video_id")
            except Exception:
                pass
        if not self.project_id:
            res = self._req_post("/projects", {"name": "Vox Director", "story": "Vox generated", "characters": [], "material": "realistic"})
            self.project_id = res["id"]
            res = self._req_post("/videos", {"project_id": self.project_id, "title": "Vox Video"})
            self.video_id = res["id"]

    def submit_image(self, model, prompt, **params):
        self._ensure_project()
        res = self._req_post("/scenes", {
            "video_id": self.video_id,
            "display_order": 0,
            "prompt": prompt,
            "video_prompt": "",
            "character_names": [],
            "chain_type": "ROOT"
        })
        scene_id = res["id"]
        
        aspect = str(params.get("aspect_ratio") or params.get("ratio") or params.get("aspect") or "16:9")
        if aspect == "9:16" or aspect.upper() == "VERTICAL":
            orientation = "VERTICAL"
        else:
            orientation = "HORIZONTAL"
            
        req = self._req_post("/requests", {
            "type": "GENERATE_IMAGE",
            "scene_id": scene_id,
            "project_id": self.project_id,
            "video_id": self.video_id,
            "orientation": orientation
        })
        rid = req["id"]
        return "flowkit:" + rid + ":" + scene_id

    def submit_video(self, model, prompt, **params):
        self._ensure_project()
        res = self._req_post("/scenes", {
            "video_id": self.video_id,
            "display_order": 0,
            "prompt": "",
            "video_prompt": prompt,
            "character_names": [],
            "chain_type": "ROOT"
        })
        scene_id = res["id"]
        
        image_url = params.get("image")
        if image_url:
            import urllib.request, json
            req = urllib.request.Request(f"{self.base_url}/scenes/{scene_id}", 
                                         data=json.dumps({
                                             "_image_url": image_url,
                                             "vertical_image_url": image_url,
                                             "horizontal_image_url": image_url
                                         }).encode(), 
                                         headers={"Content-Type": "application/json"}, 
                                         method="PATCH")
            try:
                urllib.request.urlopen(req)
            except Exception as e:
                print(f"[flowkit] PATCH scene image_url failed: {e}")
                
        aspect = str(params.get("aspect_ratio") or params.get("ratio") or params.get("aspect") or "16:9")
        if aspect == "9:16" or aspect.upper() == "VERTICAL":
            orientation = "VERTICAL"
        else:
            orientation = "HORIZONTAL"
            
        req = self._req_post("/requests", {
            "type": "GENERATE_VIDEO",
            "scene_id": scene_id,
            "project_id": self.project_id,
            "video_id": self.video_id,
            "orientation": orientation
        })
        rid = req["id"]
        return "flowkit:" + rid + ":" + scene_id

    def get_status(self, job_id):
        if not str(job_id).startswith("flowkit:"):
            return super().get_status(job_id)
            
        _, rid, scene_id = job_id.split(":", 2)
        
        try:
            req = self._req_get(f"/requests/{rid}")
        except Exception as e:
            return {"status": "failed", "output": None, "error": str(e)}
            
        status = req.get("status")
        if status == "COMPLETED":
            out_url = req.get("output_url")
            if out_url:
                return {"status": "completed", "output": out_url, "error": None}
            
            try:
                scene = self._req_get(f"/scenes/{scene_id}")
            except Exception as e:
                return {"status": "failed", "output": None, "error": str(e)}
                
            req_type = req.get("type", "")
            if req_type == "GENERATE_IMAGE":
                out = scene.get("horizontal_image_url") or scene.get("vertical_image_url") or scene.get("_image_url")
            else:
                out = scene.get("horizontal_video_url") or scene.get("vertical_video_url") or scene.get("_video_url")
            
            if out:
                return {"status": "completed", "output": out, "error": None}
            else:
                return {"status": "failed", "output": None, "error": "completed but no url found"}
                
        elif status == "FAILED":
            return {"status": "failed", "output": None, "error": req.get("error_message", "flowkit generation failed")}
        else:
            return {"status": "pending", "output": None, "error": None}


_REGISTRY = {"atlas_cloud": AtlasCloudProvider, "flowkit": FlowkitProvider}

def get_provider(name=None):
    """Return a Provider instance by name (default 'flowkit')."""
    name = (name or "flowkit").lower()
    if name not in _REGISTRY:
        raise ProviderError(f"unknown provider '{name}'; available: {list(_REGISTRY)}")
    return _REGISTRY[name]()


def run_jobs(prov, specs, *, initial_pids=None, on_submit=None, on_done=None, poll_s=5, stall_s=600, max_retries=1, deadline_s=7200, max_concurrent=4):
    """Submit + poll a batch of jobs, limiting concurrent requests to `max_concurrent`.
    Resubmits any that FAIL (including initial submit) or STALL up to `max_retries` times.
    Calls `on_submit(key, pid)` immediately upon job submission.
    Calls `on_done(key, output)` incrementally as jobs finish."""
    st = {}
    done = {}
    initial_pids = initial_pids or {}
    pending_keys = list(specs.keys())
    active_keys = set()
    deadline = time.time() + deadline_s

    while (pending_keys or active_keys) and time.time() < deadline:
        # Fill concurrent slots
        while pending_keys and len(active_keys) < max_concurrent:
            key = pending_keys.pop(0)
            
            if key in initial_pids:
                pid = initial_pids[key]
                st[key] = {"pid": pid, "t": time.time(), "tries": 0}
                active_keys.add(key)
                print(f"[{key}] resumed {pid}")
                continue

            st.setdefault(key, {"pid": None, "t": 0, "tries": 0})
            try:
                pid = specs[key]()
                st[key]["pid"] = pid
                st[key]["t"] = time.time()
                active_keys.add(key)
                print(f"[{key}] submitted {pid}")
                if on_submit:
                    on_submit(key, pid)
            except Exception as e:
                st[key]["tries"] += 1
                if st[key]["tries"] <= max_retries:
                    st[key]["t"] = time.time()  # record time of failure for backoff
                    active_keys.add(key)
                    print(f"[{key}] INITIAL submit FAILED: {e} -> will retry later")
                else:
                    print(f"[{key}] FAILED to submit (out of retries): {e}")
                    done[key] = None

        time.sleep(poll_s)
        now = time.time()

        for key in list(active_keys):
            s = st[key]
            
            # Handle jobs waiting to be resubmitted due to initial submit failure
            if s["pid"] is None:
                if now - s["t"] > poll_s * 2:  # wait a bit before retry
                    s["tries"] += 1
                    try:
                        s["pid"] = specs[key]()
                        s["t"] = time.time()
                        print(f"[{key}] resubmit #{s['tries']} ({s['pid']})")
                        if on_submit:
                            on_submit(key, s["pid"])
                    except Exception as e:
                        if s["tries"] <= max_retries:
                            s["t"] = time.time()
                            print(f"[{key}] resubmit FAILED: {e} -> will retry later")
                        else:
                            print(f"[{key}] resubmit FAILED (out of retries): {e}")
                            active_keys.remove(key)
                            done[key] = None
                continue

            try:
                r = prov.get_status(s["pid"])
            except Exception as e:
                r = {"status": "failed", "output": None, "error": str(e)}

            status = r["status"]
            if status == "completed":
                done[key] = r["output"]
                active_keys.remove(key)
                print(f"[{key}] done -> {r['output']}")
                if on_done:
                    on_done(key, r["output"])
            elif status == "failed" or (status == "pending" and now - s["t"] > stall_s):
                why = f"failed ({r.get('error', 'unknown error')})" if status == "failed" else f"stalled>{int(stall_s)}s"
                print(f"[{key}] {why}")
                if s["tries"] < max_retries:
                    s["tries"] += 1
                    try:
                        s["pid"] = specs[key]()
                        s["t"] = time.time()
                        print(f"[{key}] -> resubmit #{s['tries']} ({s['pid']})")
                        if on_submit:
                            on_submit(key, s["pid"])
                    except Exception as e:
                        s["pid"] = None
                        s["t"] = time.time()
                        print(f"[{key}] resubmit FAILED: {e} -> will retry later")
                elif status == "failed":
                    done[key] = None
                    active_keys.remove(key)
                    print(f"[{key}] FAILED permanently: {(r.get('error') or '')[:120]}")
                elif status == "pending":
                    print(f"[{key}] STALLED and out of retries, marking failed to free slot.")
                    done[key] = None
                    active_keys.remove(key)
            else:
                elapsed = int(now - s["t"])
                print(f"[{key}] status: {status} (elapsed: {elapsed}s)")
                    
    for key in specs:
        done.setdefault(key, None)
    return done
