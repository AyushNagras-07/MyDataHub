from etl.load.pipeline_run_loader import (
    create_pipeline_run,
    complete_pipeline_run
)


def test_create_pipeline_run(db_connection):

    pipeline_run_id = create_pipeline_run()

    cursor = db_connection.cursor()

    cursor.execute(
        """
        SELECT
            status,
            started_at
        FROM pipeline_runs
        WHERE id = %s;
        """,
        (pipeline_run_id,)
    )

    result = cursor.fetchone()

    assert result is not None

    status, started_at = result

    assert status == "RUNNING"
    assert started_at is not None

    # Cleanup test pipeline run
    cursor.execute(
        """
        DELETE FROM pipeline_runs
        WHERE id = %s;
        """,
        (pipeline_run_id,)
    )

    db_connection.commit()

    cursor.close()


def test_complete_pipeline_run(db_connection):

    pipeline_run_id = create_pipeline_run()

    complete_pipeline_run(
        pipeline_run_id=pipeline_run_id,
        total_files=5,
        successful_files=4,
        failed_files=1,
        execution_time=2.5,
        status="PARTIAL_SUCCESS"
    )

    cursor = db_connection.cursor()

    cursor.execute(
        """
        SELECT
            completed_at,
            total_files,
            successful_files,
            failed_files,
            execution_time,
            status
        FROM pipeline_runs
        WHERE id = %s;
        """,
        (pipeline_run_id,)
    )

    result = cursor.fetchone()

    assert result is not None

    (
        completed_at,
        total_files,
        successful_files,
        failed_files,
        execution_time,
        status
    ) = result

    assert completed_at is not None
    assert total_files == 5
    assert successful_files == 4
    assert failed_files == 1
    assert float(execution_time) == 2.5
    assert status == "PARTIAL_SUCCESS"

    # Cleanup test pipeline run
    cursor.execute(
        """
        DELETE FROM pipeline_runs
        WHERE id = %s;
        """,
        (pipeline_run_id,)
    )

    db_connection.commit()

    cursor.close()