# WEEKLY REPORTS AND STATISTICS
# TOTAL STUDY HOURS/SESSIONS  ||  HOURS PER SUBJECT  ||  MOST STUDIED SUBJECT
# SESSIONS PER DAY  ||  DAILY STUDY HOURS  ||  WEEKLY SUMMARY  ||  GOAL PROGRESS

import csv
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

try:
    import modules.storage as storage
except ImportError:
    import storage

filename = storage.filename
file_path = Path(filename)


def check():
    if (not file_path.exists()) or (file_path.stat().st_size == 0):
        print("No study sessions found yet")
        return False
    return True


def _parse_date(value):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def current_week_range(today=None):
    today = today or date.today()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    return start, end


def _add_subject_hours(bucket, labels, subject, duration):
    key = subject.strip().casefold()
    if key not in labels:
        labels[key] = subject.strip()
    bucket[key] += duration


def _named_hours(bucket, labels):
    return {labels[key]: hours for key, hours in bucket.items()}


def get_stats():
    total_sessions = 0
    total_hours = 0.0
    sub_hours = defaultdict(float)
    subject_labels = {}
    daily_hours = defaultdict(float)
    sessions_per_day = defaultdict(int)

    with open(filename, "r", newline="", encoding="utf-8") as csv_data:
        data = csv.DictReader(csv_data)
        for row in data:
            total_sessions += 1
            duration = float(row["duration"])
            total_hours += duration
            _add_subject_hours(sub_hours, subject_labels, row["subject"], duration)
            day = row["date"]
            daily_hours[day] += duration
            sessions_per_day[day] += 1

    return {
        "total_sessions": total_sessions,
        "total_hours": total_hours,
        "subject_hours": _named_hours(sub_hours, subject_labels),
        "daily_hours": dict(sorted(daily_hours.items())),
        "sessions_per_day": dict(sorted(sessions_per_day.items())),
    }


def most_studied_sub(stats):
    sub_wise_stats = stats["subject_hours"]
    if not sub_wise_stats:
        return {"Subjects": [], "Hours": 0}

    max_hours = max(sub_wise_stats.values())
    max_sub = {"Subjects": [], "Hours": max_hours}
    for sub, hrs in sub_wise_stats.items():
        if hrs == max_hours:
            max_sub["Subjects"].append(sub)
    return max_sub


def weekly_summary():
    start, end = current_week_range()
    week_hours = 0.0
    week_sessions = 0
    sub_hours = defaultdict(float)
    subject_labels = {}
    daily_hours = defaultdict(float)

    for row in storage.read_sessions():
        session_date = _parse_date(row.get("date"))
        if session_date is None or session_date < start or session_date > end:
            continue
        duration = float(row["duration"])
        week_hours += duration
        week_sessions += 1
        _add_subject_hours(sub_hours, subject_labels, row["subject"], duration)
        daily_hours[row["date"]] += duration

    return {
        "week_start": start.isoformat(),
        "week_end": end.isoformat(),
        "hours": week_hours,
        "sessions": week_sessions,
        "subject_hours": _named_hours(sub_hours, subject_labels),
        "daily_hours": dict(sorted(daily_hours.items())),
    }


def goal_progress():
    config = storage.load_config()
    stats = get_stats()
    week = weekly_summary()
    total_goal = float(config.get("goal_hours", 0))
    weekly_goal = float(config.get("weekly_goal", 0))
    total_hours = stats["total_hours"]
    week_hours = week["hours"]

    return {
        "total_hours": total_hours,
        "goal_hours": total_goal,
        "total_percent": (total_hours / total_goal * 100) if total_goal else 0,
        "week_hours": week_hours,
        "weekly_goal": weekly_goal,
        "week_percent": (week_hours / weekly_goal * 100) if weekly_goal else 0,
        "week_start": week["week_start"],
        "week_end": week["week_end"],
    }


def _print_mapping(title, mapping, value_label="Hours"):
    print(title)
    if not mapping:
        print("  No data yet")
        return
    for key, value in mapping.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f} {value_label}")
        else:
            print(f"  {key}: {value} {value_label}")


def print_basic_stats(stats):
    print("Total Study hours : ", round(stats["total_hours"], 2))
    print("Total Study sessions : ", stats["total_sessions"])


def print_most_studied(stats):
    result = most_studied_sub(stats)
    subjects = ", ".join(result["Subjects"]) or "None"
    print(f"Most Studied Subject(s): {subjects}")
    print(f"Hours: {result['Hours']:.2f}")


def print_weekly(week):
    print(f"Weekly Summary ({week['week_start']} to {week['week_end']})")
    print(f"  Sessions: {week['sessions']}")
    print(f"  Hours: {week['hours']:.2f}")
    _print_mapping("  Hours per subject this week:", week["subject_hours"])
    _print_mapping("  Daily hours this week:", week["daily_hours"])


def print_goal_progress(progress):
    print("Goal Progress")
    print(
        f"  Overall: {progress['total_hours']:.2f} / {progress['goal_hours']:.2f} hrs "
        f"({progress['total_percent']:.1f}%)"
    )
    print(
        f"  This week ({progress['week_start']} to {progress['week_end']}): "
        f"{progress['week_hours']:.2f} / {progress['weekly_goal']:.2f} hrs "
        f"({progress['week_percent']:.1f}%)"
    )
    if progress["total_hours"] >= progress["goal_hours"] and progress["goal_hours"] > 0:
        print("  Overall goal achieved.")
    if progress["week_hours"] >= progress["weekly_goal"] and progress["weekly_goal"] > 0:
        print("  Weekly goal achieved.")


stat_choices = {
    "1": "Basic Stats",
    "2": "Most Studied subject",
    "3": "Hours per subject",
    "4": "Sessions per day",
    "5": "Daily study hours",
    "6": "Weekly summary",
    "7": "Goal progress",
    "8": "All stats",
}


def manage_analytics(choice):
    if not check():
        return

    stats = get_stats()

    if choice == "1":
        print_basic_stats(stats)
    elif choice == "2":
        print_most_studied(stats)
    elif choice == "3":
        _print_mapping("Hours per subject:", stats["subject_hours"])
    elif choice == "4":
        _print_mapping("Sessions per day:", stats["sessions_per_day"], "session(s)")
    elif choice == "5":
        _print_mapping("Daily study hours:", stats["daily_hours"])
    elif choice == "6":
        print_weekly(weekly_summary())
    elif choice == "7":
        print_goal_progress(goal_progress())
    elif choice == "8":
        print_basic_stats(stats)
        print_most_studied(stats)
        _print_mapping("Hours per subject:", stats["subject_hours"])
        _print_mapping("Sessions per day:", stats["sessions_per_day"], "session(s)")
        _print_mapping("Daily study hours:", stats["daily_hours"])
        print_weekly(weekly_summary())
        print_goal_progress(goal_progress())
    else:
        print("Wrong choice, Try again")


if __name__ == "__main__":
    manage_analytics("8")
