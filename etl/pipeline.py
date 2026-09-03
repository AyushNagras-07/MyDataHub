from etl.extract.daily_input import extract_daily_data
from etl.validation.daily_validation import validate_daily_data
from etl.transform.daily_transform import transform_daily_data
from etl.load.postgres_loader import load_daily_data
from etl.config.logging_config import setup_logging
from pathlib import Path
from etl.utils.file_handler import move_file
import os
from etl.utils.retry import retry_operation


import logging

RAW_FOLDER = "/home/ayush/MyDataHub/etl/data/raw"
PROCESSED_FOLDER = "/home/ayush/MyDataHub/etl/data/processed"
FAILED_FOLDER = "/home/ayush/MyDataHub/etl/data/failed"
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

    successful_files = []
    failed_files = []

    for file_path in json_files:

        logger.info("Processing file: %s", file_path)

        try:

            # Extract
            data = extract_daily_data(file_path)
            logger.info("Extract completed")

            # Validate
            if not validate_daily_data(data):

                logger.error("Validation failed")

                failed_files.append(
                    os.path.basename(file_path)
                )

                move_file(
                    file_path,
                    FAILED_FOLDER
                )

                continue

            logger.info("Validation passed")

            # Transform
            transformed_data = transform_daily_data(data)
            logger.info("Transformation completed")

            # Load
            # Load with retry

            def load_operation():

                load_daily_data(
                    transformed_data,
                    USER_ID
                )


            retry_operation(
                load_operation,
                max_attempts=3,
                delay=2
            )

            logger.info("Load completed")


            # Move successful file
            move_file(
                file_path,
                PROCESSED_FOLDER
            )

            successful_files.append(
                os.path.basename(file_path)
            )

            logger.info(
                "File processed successfully: %s",
                file_path
            )

        except Exception as error:

            logger.exception(
                "File processing failed: %s",
                file_path
            )

            failed_files.append(
                os.path.basename(file_path)
            )

            move_file(
                file_path,
                FAILED_FOLDER
            )
    logger.info(
        "Batch completed | Successful: %s | Failed: %s",
        len(successful_files),
        failed_files
    )

if __name__ == "__main__":
    run_pipeline()