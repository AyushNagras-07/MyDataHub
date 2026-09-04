from unittest.mock import patch

from etl.pipeline import process_file


@patch("etl.pipeline.retry_operation")
@patch("etl.pipeline.transform_daily_data")
@patch("etl.pipeline.validate_daily_data")
@patch("etl.pipeline.extract_daily_data")
def test_process_file_success(
    mock_extract,
    mock_validate,
    mock_transform,
    mock_retry
):

    mock_extract.return_value = {
        "log_date": "2026-08-13"
    }

    mock_validate.return_value = True

    mock_transform.return_value = {
        "log_date": "2026-08-13"
    }

    result = process_file(
        "dummy_file.json"
    )

    assert result is True

from etl import pipeline


def test_run_pipeline_moves_successful_file(
    tmp_path,
    monkeypatch
):

    # Temporary folders
    raw_folder = tmp_path / "raw"
    processed_folder = tmp_path / "processed"
    failed_folder = tmp_path / "failed"

    raw_folder.mkdir()
    processed_folder.mkdir()
    failed_folder.mkdir()

    # Create test JSON file
    test_file = raw_folder / "test.json"

    test_file.write_text(
        '{"log_date": "2026-09-01"}'
    )

    # Replace pipeline folders with temporary folders
    monkeypatch.setattr(
        pipeline,
        "RAW_FOLDER",
        raw_folder
    )

    monkeypatch.setattr(
        pipeline,
        "PROCESSED_FOLDER",
        processed_folder
    )

    monkeypatch.setattr(
        pipeline,
        "FAILED_FOLDER",
        failed_folder
    )

    # Mock successful processing
    monkeypatch.setattr(
        pipeline,
        "process_file",
        lambda file_path: True
    )

    # Run pipeline
    pipeline.run_pipeline()

    # Assertions
    assert not test_file.exists()

    assert (
        processed_folder / "test.json"
    ).exists()

    assert not (
        failed_folder / "test.json"
    ).exists()

def test_run_pipeline_moves_failed_file(
    tmp_path,
    monkeypatch
):

    # Temporary folders
    raw_folder = tmp_path / "raw"
    processed_folder = tmp_path / "processed"
    failed_folder = tmp_path / "failed"

    raw_folder.mkdir()
    processed_folder.mkdir()
    failed_folder.mkdir()

    # Create test JSON file
    test_file = raw_folder / "test.json"

    test_file.write_text(
        '{"log_date": "2026-09-01"}'
    )

    # Replace pipeline folders
    monkeypatch.setattr(
        pipeline,
        "RAW_FOLDER",
        raw_folder
    )

    monkeypatch.setattr(
        pipeline,
        "PROCESSED_FOLDER",
        processed_folder
    )

    monkeypatch.setattr(
        pipeline,
        "FAILED_FOLDER",
        failed_folder
    )

    # Mock failed processing
    monkeypatch.setattr(
        pipeline,
        "process_file",
        lambda file_path: False
    )

    # Run pipeline
    pipeline.run_pipeline()

    # Assertions
    assert not test_file.exists()

    assert (
        failed_folder / "test.json"
    ).exists()

    assert not (
        processed_folder / "test.json"
    ).exists()

def test_run_pipeline_with_empty_raw_folder(
    tmp_path,
    monkeypatch
):

    raw_folder = tmp_path / "raw"
    processed_folder = tmp_path / "processed"
    failed_folder = tmp_path / "failed"

    raw_folder.mkdir()
    processed_folder.mkdir()
    failed_folder.mkdir()

    monkeypatch.setattr(
        pipeline,
        "RAW_FOLDER",
        raw_folder
    )

    monkeypatch.setattr(
        pipeline,
        "PROCESSED_FOLDER",
        processed_folder
    )

    monkeypatch.setattr(
        pipeline,
        "FAILED_FOLDER",
        failed_folder
    )

    pipeline.run_pipeline()

    assert list(processed_folder.iterdir()) == []
    assert list(failed_folder.iterdir()) == []