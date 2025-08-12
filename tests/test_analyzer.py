import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import pytest
from log_analyzer.app import process_files


def test_process_files_base():
    report = process_files(file_paths=["tests/test_data.log"], report_type="average", filter_date_str=None)
    stats_dict = {url: {"count": count, "avg_time": avg_time} for url, count, avg_time in report}

    assert len(stats_dict) == 2
    assert stats_dict["/api/users"]["count"] == 2
    assert stats_dict["/api/posts"]["count"] == 1


def test_date_filter():
    report = process_files(file_paths=["tests/test_data.log"], report_type="average", filter_date_str="2025-06-22")
    assert len(report) == 2

    user_stats = None
    for row in report:
        if row[0] == "/api/users":
            user_stats = row
            break

    assert user_stats is not None
    assert user_stats[1] == 2


def test_no_data_for_date_filter():
    report = process_files(file_paths=["tests/test_data.log"], report_type="average", filter_date_str="2025-01-01")
    assert len(report) == 0
    assert report == []


def test_file_not_found():
    report = process_files(file_paths=["tests/test_xyz.log"], report_type="average", filter_date_str=None)
    assert report == []


def test_invalid_date():
    report = process_files(file_paths=["tests/test_data.log"], report_type="average", filter_date_str="2135-01-01")
    assert report == []