import json



def extract_daily_data(file_path):

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"Input file not found: {file_path}"
        ) from error

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON format in file: {file_path}"
        ) from error