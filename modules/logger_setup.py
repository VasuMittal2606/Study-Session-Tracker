# SETS UP FILE LOGGING FOR THE STUDY SESSION TRACKER
# WRITES ACTIONS AND ERRORS TO tracker.log

import logging
from pathlib import Path

LOG_FILE = Path("tracker.log")


def setup_logger():
    logger = logging.getLogger("study_tracker")
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger
