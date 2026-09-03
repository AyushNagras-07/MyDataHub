import time
import logging


logger = logging.getLogger(__name__)


def retry_operation(operation, max_attempts=3, delay=2):

    for attempt in range(1, max_attempts + 1):

        try:

            return operation()

        except Exception as error:

            logger.warning(
                "Attempt %s/%s failed: %s",
                attempt,
                max_attempts,
                error
            )

            if attempt < max_attempts:

                wait_time = delay * (2 ** (attempt - 1))

                logger.info(
                    "Retrying in %s seconds...",
                    wait_time
                )

                time.sleep(wait_time)

            else:

                logger.error(
                    "All %s attempts failed",
                    max_attempts
                )

                raise