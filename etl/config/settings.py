from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


# Data folders
RAW_FOLDER = BASE_DIR / "data" / "raw"

PROCESSED_FOLDER = BASE_DIR / "data" / "processed"

FAILED_FOLDER = BASE_DIR / "data" / "failed"


# Pipeline configuration
USER_ID = 1


# Retry configuration
MAX_RETRY_ATTEMPTS = 3

RETRY_DELAY = 2