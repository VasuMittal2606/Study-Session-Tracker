# Study Session Tracker

A command-line Python application for tracking study sessions, storing records in CSV format, and generating statistics.

## Features

- Add, list, update, and delete study sessions
- Weekly statistics and other reports
- Goal tracking and progress
- JSON configuration
- File logging

## Project Structure

```
study_tracker/
├── main.py
├── sessions.csv
├── config.json
├── tracker.log
├── modules/
│   ├── storage.py
│   ├── analytics.py
│   └── logger_setup.py
└── README.md
```

`sessions.csv`, `config.json`, and `tracker.log` are created automatically on first use.

## Usage

Run commands from the project root:

```
python main.py add
python main.py list
python main.py update
python main.py delete
python main.py stats
python main.py goal
python main.py config
```

## Statistics

- Total study hours and sessions
- Hours per subject
- Most studied subject
- Sessions per day
- Daily study hours
- Weekly summary (Monday–Sunday)
- Goal progress (overall and weekly)

## Configuration

`config.json` stores values such as:

```json
{
    "goal_hours": 25,
    "default_subject": "DSA",
    "weekly_goal": 18
}
```

Actions are written to `tracker.log`.
