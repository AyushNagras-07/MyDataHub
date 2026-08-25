from etl.extract.daily_input import extract_daily_data
from etl.validation.daily_validation import validate_daily_data
from etl.transform.daily_transform import transform_daily_data
from etl.load.postgres_loader import load_daily_data
from etl.config.logging_config import setup_logging

import logging


FILE_PATH = "/home/ayush/MyDataHub/etl/data/raw/2026-08-13.json"
USER_ID = 1


setup_logging()

logger = logging.getLogger(__name__)


def run_pipeline():

    logger.info("Starting MyDataHub ETL")

    try:

        # Extract
        data = extract_daily_data(FILE_PATH)
        logger.info("Extract completed")

        # Validate
        if not validate_daily_data(data):
            logger.error("Validation failed")
            return

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
            "MyDataHub ETL completed successfully"
        )

    except Exception as error:
        logger.exception("MyDataHub ETL failed: %s", error)


if __name__ == "__main__":
    run_pipeline()