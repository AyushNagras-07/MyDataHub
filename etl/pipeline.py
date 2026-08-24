from etl.extract.daily_input import extract_daily_data
from etl.validation.daily_validation import validate_daily_data
from etl.transform.daily_transform import transform_daily_data
from etl.load.postgres_loader import load_daily_data


FILE_PATH = "/home/ayush/MyDataHub/etl/data/raw/2026-08-13.json"

USER_ID = 1


def run_pipeline():

    print("Starting MyDataHub ETL...")

    # Extract
    data = extract_daily_data(FILE_PATH)
    print("✓ Extract completed")

    # Validate
    if not validate_daily_data(data):
        print("✗ Validation failed")
        return

    print("✓ Validation passed")

    # Transform
    transformed_data = transform_daily_data(data)
    print("✓ Transformation completed")

    # Load
    load_daily_data(transformed_data, USER_ID)
    print("✓ Load completed")

    print("MyDataHub ETL completed successfully.")


if __name__ == "__main__":
    run_pipeline()