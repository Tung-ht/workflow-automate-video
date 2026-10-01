#!/usr/bin/env python3
import sqlite3
import uuid
import json
import os

db_path = os.path.join(os.path.dirname(__file__), "..", "flowkit_repo", "flow_agent.db")
state_path = os.path.join(os.path.dirname(__file__), "..", "flowkit_repo", "agent", "active_project.json")

pid = "0ea717be-3424-4a7e-b4d9-6637ac32f1b1"
pname = "Blackprint - SR-71 Fuel Leak"
vid = str(uuid.uuid4())

conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("INSERT OR REPLACE INTO project (id, name, description, material, status, user_paygate_tier, created_at, updated_at) VALUES (?, ?, ?, 'realistic', 'ACTIVE', 'PAYGATE_TIER_ONE', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)", (pid, pname, 'Blackprint Short'))
c.execute("INSERT OR REPLACE INTO video (id, project_id, title, orientation, status, created_at, updated_at) VALUES (?, ?, ?, 'VERTICAL', 'DRAFT', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)", (vid, pid, 'SR-71 Fuel Leak Short'))
conn.commit()
conn.close()

with open(state_path, "w") as f:
    json.dump({"project_id": pid}, f, indent=2)

print(f"Successfully registered and set active project {pid} with video {vid}")
