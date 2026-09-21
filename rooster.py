import json, os
from datetime import datetime

LOG_FILE = "attendance_log.json"

def load_data():
    if not os.path.exists(LOG_FILE):
        return {"students": [], "records": []}
    with open(LOG_FILE) as f:
        return json.load(f)

def save_data(data):
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_student(name, student_id):
    data = load_data()
    if any(s["student_id"] == student_id for s in data["students"]):
        return False  # duplicate ID
    data["students"].append({"student_id": student_id, "name": name})
    save_data(data)
    return True

def check_in(student_id, status):
    if status not in ("Present", "Late"):
        return "Status must be Present or Late."
    data = load_data()
    if not any(s["student_id"] == student_id for s in data["students"]):
        return "Student not found."
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    # update today's record if it exists, otherwise append
    for r in data["records"]:
        if r["student_id"] == student_id and r["date"] == today:
            r["status"], r["timestamp"] = status, now.isoformat(timespec="seconds")
            save_data(data)
            return "Record updated."
    data["records"].append({"student_id": student_id, "date": today,
                            "status": status, "timestamp": now.isoformat(timespec="seconds")})
    save_data(data)
    return "Checked in."

def todays_checkins():
    data = load_data()
    today = datetime.now().strftime("%Y-%m-%d")
    names = {s["student_id"]: s["name"] for s in data["students"]}
    return [(names.get(r["student_id"], "?"), r["student_id"], r["status"], r["timestamp"])
            for r in data["records"]
            if r["date"] == today and r["status"] in ("Present", "Late")]
