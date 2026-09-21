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

def mark_absentees(date=None):
    """Flag every student with no record for `date` as Absent."""
    data = load_data()
    date = date or datetime.now().strftime("%Y-%m-%d")
    seen = {r["student_id"] for r in data["records"] if r["date"] == date}
    count = 0
    for s in data["students"]:
        if s["student_id"] not in seen:
            data["records"].append({"student_id": s["student_id"], "date": date,
                                    "status": "Absent",
                                    "timestamp": datetime.now().isoformat(timespec="seconds")})
            count += 1
    save_data(data)
    return count

def school_days(data):
    return sorted({r["date"] for r in data["records"]})

def attendance_rate(student_id, data=None):
    data = data or load_data()
    days = school_days(data)
    if not days:
        return 0.0
    attended = sum(1 for r in data["records"]
                   if r["student_id"] == student_id and r["status"] in ("Present", "Late"))
    return attended / len(days) * 100

def longest_absence_streak(student_id, data=None):
    data = data or load_data()
    status_by_day = {r["date"]: r["status"] for r in data["records"] if r["student_id"] == student_id}
    best = current = 0
    for day in school_days(data):
        if status_by_day.get(day, "Absent") == "Absent":
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best

def chronic_absentees(threshold=85):
    data = load_data()
    result = []
    for s in data["students"]:
        rate = attendance_rate(s["student_id"], data)
        if rate < threshold:
            result.append((s["name"], s["student_id"], round(rate, 1),
                           longest_absence_streak(s["student_id"], data)))
    return result
