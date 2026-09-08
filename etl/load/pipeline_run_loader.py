from datetime import datetime

from etl.load.postgres_loader import get_connection


def create_pipeline_run():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO pipeline_runs
            (
                started_at,
                status
            )
            VALUES (%s, %s)

            RETURNING id;
            """,
            (
                datetime.now(),
                "RUNNING"
            )
        )

        pipeline_run_id = cursor.fetchone()[0]

        connection.commit()

        return pipeline_run_id

    except Exception:

        connection.rollback()

        raise

    finally:

        cursor.close()
        connection.close()


def complete_pipeline_run(
    pipeline_run_id,
    total_files,
    successful_files,
    failed_files,
    execution_time,
    status
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE pipeline_runs
            SET
                completed_at = %s,
                total_files = %s,
                successful_files = %s,
                failed_files = %s,
                execution_time = %s,
                status = %s
            WHERE id = %s;
            """,
            (
                datetime.now(),
                total_files,
                successful_files,
                failed_files,
                execution_time,
                status,
                pipeline_run_id
            )
        )

        connection.commit()

    except Exception:

        connection.rollback()

        raise

    finally:

        cursor.close()
        connection.close()