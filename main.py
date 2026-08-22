# THIS IS THE MAIN ENTRY POINT FOR THIS PROJECT
# THIS IS WHERE ALL OPERATIONS WILL BE HANDLED

import argparse as agp
from datetime import date

import modules.analytics as analytics
import modules.logger_setup as logger_setup
import modules.storage as storage

logger = logger_setup.setup_logger()

parser = agp.ArgumentParser(description="--- Study Session Tracker ---")
parser.add_argument(
    "command",
    choices=["add", "delete", "update", "list", "stats", "config", "goal"],
    help="Action to be taken",
)
arg = parser.parse_args()
command = arg.command


def _read_duration(prompt="Duration(in hrs) : "):
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return None
        try:
            value = float(raw)
            if value <= 0:
                print("Duration must be greater than 0")
                continue
            return value
        except ValueError:
            print("Wrong Time, try again")


def inp():
    config = storage.load_config()
    default_subject = config.get("default_subject", "")

    subject = input(f"Subject [Default ({default_subject})] : ").strip()
    if not subject:
        subject = default_subject
    if not subject:
        print("Subject is required")
        return None

    topic = input("Topic : ").strip()
    session_date = input(f"Date [{date.today().isoformat()}] (YYYY-MM-DD) : ").strip()
    if not session_date:
        session_date = date.today().isoformat()
    else:
        try:
            date.fromisoformat(session_date)
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD")
            return None

    duration = _read_duration()
    if duration is None:
        print("Duration is required")
        return None

    return {
        "subject": subject,
        "topic": topic,
        "date": session_date,
        "duration": duration,
    }


def _choose_session():
    rows = storage.list_sessions()
    if not rows:
        return None
    try:
        index = int(input("Session number : ").strip())
    except ValueError:
        print("Enter a valid number")
        return None
    return index


def handle_config():
    config = storage.load_config()
    print("\n--- Current Config ---")
    for key, value in config.items():
        print(f"{key}: {value}")

    print("\nPress Enter to keep the current value.")
    default_subject = input(f"Default subject [{config['default_subject']}] : ").strip()
    goal_raw = input(f"Overall goal hours [{config['goal_hours']}] : ").strip()
    weekly_raw = input(f"Weekly goal hours [{config['weekly_goal']}] : ").strip()

    if default_subject:
        config["default_subject"] = default_subject
    if goal_raw:
        try:
            config["goal_hours"] = float(goal_raw)
        except ValueError:
            print("Invalid overall goal. Keeping previous value.")
    if weekly_raw:
        try:
            config["weekly_goal"] = float(weekly_raw)
        except ValueError:
            print("Invalid weekly goal. Keeping previous value.")

    storage.save_config(config)
    print("Config Saved Successfully")
    logger.info(f"Config updated: {config}")


def handle_goal():
    config = storage.load_config()
    if storage.read_sessions():
        analytics.print_goal_progress(analytics.goal_progress())
    else:
        print("No study sessions found yet. Goals can still be updated.")
        print(f"Overall goal hours: {config['goal_hours']}")
        print(f"Weekly goal hours: {config['weekly_goal']}")

    change = input("Update goals? (y/n) : ").strip().lower()
    if change != "y":
        return

    goal_raw = input(f"Overall goal hours [{config['goal_hours']}] : ").strip()
    weekly_raw = input(f"Weekly goal hours [{config['weekly_goal']}] : ").strip()
    if goal_raw:
        try:
            config["goal_hours"] = float(goal_raw)
        except ValueError:
            print("Invalid overall goal. Keeping previous value.")
    if weekly_raw:
        try:
            config["weekly_goal"] = float(weekly_raw)
        except ValueError:
            print("Invalid weekly goal. Keeping previous value.")

    storage.save_config(config)
    print("Goals Saved Successfully")
    logger.info(
        f"Goals updated: goal_hours={config['goal_hours']}, weekly_goal={config['weekly_goal']}"
    )


def Handler(command):
    storage.load_config()

    if command == "add":
        data = inp()
        if data is None:
            logger.warning("Add session cancelled due to invalid input")
            return
        storage.csv_storing(data)
        logger.info(f"Session added: {data}")

    elif command == "list":
        storage.list_sessions()
        logger.info("Listed sessions")

    elif command == "delete":
        index = _choose_session()
        if index is None:
            return
        removed = storage.delete_session(index)
        if removed:
            logger.info(f"Session deleted: {removed}")

    elif command == "update":
        index = _choose_session()
        if index is None:
            return
        print("Leave a field empty to keep its current value.")
        subject = input("New subject : ").strip()
        topic = input("New topic : ").strip()
        session_date = input("New date (YYYY-MM-DD) : ").strip()
        if session_date:
            try:
                date.fromisoformat(session_date)
            except ValueError:
                print("Invalid date. Use YYYY-MM-DD")
                return
        duration = _read_duration("New duration(in hrs) : ")
        updates = {
            "subject": subject,
            "topic": topic,
            "date": session_date,
        }
        if duration is not None:
            updates["duration"] = duration
        updated = storage.update_session(index, updates)
        if updated:
            logger.info(f"Session updated: {updated}")

    elif command == "stats":
        for key, label in analytics.stat_choices.items():
            print(f"{key}. {label}")
        choice = input("Choice for stat : ").strip()
        analytics.manage_analytics(choice)
        logger.info(f"Stats viewed: option {choice}")

    elif command == "goal":
        handle_goal()

    elif command == "config":
        handle_config()


Handler(command)
