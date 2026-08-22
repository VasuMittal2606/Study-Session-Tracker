# HANDLES CSV SESSION STORAGE AND JSON CONFIGURATION
# USED BY MAIN AND ANALYTICS

import csv
import json
from pathlib import Path

filename = "sessions.csv"
CONFIG_FILE = Path("config.json")
fields = ["subject", "topic", "duration", "date"]

DEFAULT_CONFIG = {
    "goal_hours": 25,
    "default_subject": "DSA",
    "weekly_goal": 18,
}


def load_config():
    if (not CONFIG_FILE.exists()) or (CONFIG_FILE.stat().st_size == 0):
        save_config(DEFAULT_CONFIG.copy())
        return DEFAULT_CONFIG.copy()

    with CONFIG_FILE.open("r", encoding="utf-8") as config_file:
        stored = json.load(config_file)

    config = DEFAULT_CONFIG.copy()
    config.update(stored)
    return config


def save_config(config):
    with CONFIG_FILE.open("w", encoding="utf-8") as config_file:
        json.dump(config, config_file, indent=4)
    return config


def read_sessions():
    file = Path(filename)
    if (not file.exists()) or (file.stat().st_size == 0):
        return []

    with open(filename, "r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)


def _write_sessions(rows):
    with open(filename, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def csv_storing(data_dict):
    file = Path(filename)
    header_needed = (not file.exists()) or (file.stat().st_size == 0)

    with open(filename, "a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        if header_needed:
            writer.writeheader()
        writer.writerow(data_dict)

    print("Session Saved Successfully")
    return data_dict


def list_sessions():
    rows = read_sessions()
    if not rows:
        print("No study sessions found yet")
        return []

    print("\n--- Saved Sessions ---")
    print(f"{'#':<4} {'Date':<12} {'Subject':<16} {'Topic':<24} {'Hours'}")
    for index, row in enumerate(rows, start=1):
        print(
            f"{index:<4} {row.get('date', ''):<12} {row.get('subject', ''):<16} "
            f"{row.get('topic', ''):<24} {row.get('duration', '')}"
        )
    return rows


def delete_session(index):
    rows = read_sessions()
    if index < 1 or index > len(rows):
        print("Invalid session number")
        return None

    removed = rows.pop(index - 1)
    _write_sessions(rows)
    print("Session Deleted Successfully")
    return removed


def update_session(index, updates):
    rows = read_sessions()
    if index < 1 or index > len(rows):
        print("Invalid session number")
        return None

    row = rows[index - 1]
    for key, value in updates.items():
        if key in fields and value not in (None, ""):
            row[key] = value
    rows[index - 1] = row
    _write_sessions(rows)
    print("Session Updated Successfully")
    return row
