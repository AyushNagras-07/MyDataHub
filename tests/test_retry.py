from etl.utils.retry import retry_operation
import pytest
import psycopg2

def test_operation_succeeds_first_attempt():

    def operation():
        return "success"

    result = retry_operation(
        operation,
        max_attempts=3,
        delay=0,
        retry_exceptions=(Exception,)
    )

    assert result == "success"

def test_operation_succeeds_after_retry():

    attempts = {"count": 0}

    def operation():

        attempts["count"] += 1

        if attempts["count"] < 2:
            raise Exception("Temporary failure")

        return "success"

    result = retry_operation(
        operation,
        max_attempts=3,
        delay=0
    )

    assert result == "success"
    assert attempts["count"] == 2



def test_operation_fails_after_max_attempts():

    attempts = {"count": 0}

    def operation():

        attempts["count"] += 1

        raise Exception("Permanent failure")

    with pytest.raises(Exception):

        retry_operation(
            operation,
            max_attempts=3,
            delay=0
        )

    assert attempts["count"] == 3

def test_operation_retries_transient_error():

    attempts = {"count": 0}

    def operation():

        attempts["count"] += 1

        if attempts["count"] < 2:
            raise psycopg2.OperationalError("Temporary database failure")

        return "success"

    result = retry_operation(
        operation,
        max_attempts=3,
        delay=0,
        retry_exceptions=(psycopg2.OperationalError,)
    )

    assert result == "success"
    assert attempts["count"] == 2

def test_non_retryable_error_is_not_retried():

    attempts = {"count": 0}

    def operation():

        attempts["count"] += 1
        raise ValueError("Permanent failure")

    with pytest.raises(ValueError):

        retry_operation(
            operation,
            max_attempts=3,
            delay=0,
            retry_exceptions=(psycopg2.OperationalError,)
        )

    assert attempts["count"] == 1