from etl.extract.daily_input import extract_daily_data
from etl.validation.daily_validation import validate_daily_data
from etl.transform.daily_transform import transform_daily_data
from etl.load.postgres_loader import load_daily_data
from etl.config.logging_config import setup_logging
from etl.utils.file_handler import move_file
import os
from etl.utils.retry import retry_operation
import time
import logging

from etl.config.settings import (
    RAW_FOLDER,
    PROCESSED_FOLDER,
    FAILED_FOLDER,
    USER_ID,
    MAX_RETRY_ATTEMPTS,
    RETRY_DELAY
)


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

        # Load with retry
        def load_operation():
            load_daily_data(
                transformed_data,
                USER_ID
            )

        retry_operation(
            load_operation,
            max_attempts=MAX_RETRY_ATTEMPTS,
            delay=RETRY_DELAY
        )

        logger.info("Load completed")

        return True

    except Exception:

        logger.exception(
            "File processing failed: %s",
            file_path
        )

        return False


def run_pipeline():
    start_time = time.time()

    logger.info("Starting MyDataHub Batch ETL")

    json_files = sorted(
        RAW_FOLDER.glob("*.json")
    )

    logger.info(
        "Found %s JSON files",
        len(json_files)
    )

    successful_files = []
    failed_files = []

    for file_path in json_files:

        success = process_file(file_path)

        if success:

            move_file(
                file_path,
                PROCESSED_FOLDER
            )

            successful_files.append(
                file_path.name
            )

            logger.info(
                "File moved to processed: %s",
                file_path.name
            )

        else:

            move_file(
                file_path,
                FAILED_FOLDER
            )

            failed_files.append(
                file_path.name
            )

            logger.info(
                "File moved to failed: %s",
                file_path.name
            )


    execution_time = time.time() - start_time

    total_files = len(json_files)
    successful_count = len(successful_files)
    failed_count = len(failed_files)

    success_rate = (
        (successful_count / total_files) * 100
        if total_files > 0
        else 0
    )

    logger.info("=" * 50)
    logger.info("BATCH PIPELINE SUMMARY")
    logger.info("=" * 50)

    logger.info("Total files: %s", total_files)
    logger.info("Successful files: %s", successful_count)
    logger.info("Failed files: %s", failed_count)
    logger.info("Success rate: %.2f%%", success_rate)
    logger.info("Execution time: %.2f seconds", execution_time)

    if failed_files:
        logger.info(
            "Failed files list: %s",
            failed_files
        )

    logger.info("=" * 50)

if __name__ == "__main__":
    run_pipeline()