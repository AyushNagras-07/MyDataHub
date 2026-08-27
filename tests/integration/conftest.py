import os

import psycopg2
import pytest
from dotenv import load_dotenv


@pytest.fixture
def db_connection():

    load_dotenv(".env.test", override=True)

    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    yield connection

    connection.rollback()
    connection.close()