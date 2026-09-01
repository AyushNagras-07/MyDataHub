from etl.extract.daily_input import extract_daily_data
from etl.validation.daily_validation import validate_daily_data
from etl.transform.daily_transform import transform_daily_data
from etl.load.postgres_loader import load_daily_data
from etl.config.logging_config import setup_logging
from pathlib import Path

import logging


DATA_DIRECTORY = "/home/ayush/MyDataHub/etl/data/raw"
USER_ID = 1


setup_logging()

logger = logging.getLogger(__name__)


def process_file(file_path):

    logger.info("Processing file: %s", file_path)

    try:

        # Extract
        data = extract_daily_data(file_path)
        logger.info("Extract completed")

        # Validate
        if not validate_daily_data(data):
            logger.error("Validation failed")
            return False

        logger.info("Validation passed")

        # Transform
        transformed_data = transform_daily_data(data)
        logger.info("Transformation completed")

        # Load
        load_daily_data(
            transformed_data,
            USER_ID
        )

        logger.info("Load completed")

        logger.info(
            "File processed successfully: %s",
            file_path
        )

        return True

    except Exception as error:
        logger.exception(
            "File processing failed: %s",
            error
        )

        return False


def run_pipeline():

    logger.info("Starting MyDataHub Batch ETL")

    data_directory = Path(DATA_DIRECTORY)

    json_files = sorted(
        data_directory.glob("*.json")
    )

    logger.info(
        "Found %s JSON files",
        len(json_files)
    )

    successful_files = 0
    failed_files = []

    for file_path in json_files:

        result = process_file(file_path)

        if result:
            successful_files += 1
        else:
            failed_files.append(file_path.name)

    logger.info(
        "Batch completed | Successful: %s | Failed: %s",
        successful_files,
        failed_files
    )

if __name__ == "__main__":
    run_pipeline()