# AUTOMATED STUDY SESSION TRACKER 
Track study sessions in subjects, hours,topic, date

# Project Structure
study_tracker/
│
├── main.py
├── sessions.csv
├── config.json
├── tracker.log
├── modules/
│   ├── storage.py
│   ├── analytics.py
│   └── logger_setup.py
└── README.md

# MODE
CLI BASED (TKINTER LATER)

# REQUIRED MODULES : 
csv | json | logging | datetime | collections | argparse | pathlib

# FEATURES : 
ADD/DELETE/UPDATE SESSIONS  ||  TRACK WEEKLY REPORT(AND VARIOUS STATISTICS)  ||  SET GOALS AND ACHIEVE THEM (FUTURE SCOPE)  ||  

# STATISTICS
TOTAL STUDY HOURS/SESSIONS  ||  HOURS PER SUBJECT  ||  MOST STUDIED SUBJECT  ||  SESSIONS PER DAY  ||  DAILY STUDY HOURS  ||  WEEKLY SUMMARY  ||  GOAL PROGRESS  ||

# WORKFLOW 
  User
    ↓
  main.py
    ↓
  storage.py
    ↓
  sessions.csv

# For statistics:
  main.py
    ↓
  analytics.py
    ↓
  sessions.csv
    ↓
  Results

# For configuration:
  main.py
    ↓
 config.json

# For logging:
 main.py
   ↓
 logging module
   ↓
 tracker.log


