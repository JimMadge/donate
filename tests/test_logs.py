"""Test log functions."""
from datetime import date
import donate
from donate.logs import update_log
import pytest


@pytest.fixture
def mock_log_path(tmp_path):
    return tmp_path / "donation_log.csv"


@pytest.fixture
def mock_date():
    class MyDate(object):
        @staticmethod
        def today():
            return date(1990, 9, 11)

    return MyDate()


def test_update_log(monkeypatch, mock_log_path, mock_date, donations):
    monkeypatch.setattr(donate.logs, "_log_path", mock_log_path)
    monkeypatch.setattr(donate.logs, "date", mock_date)

    update_log(donations, "£", False)

    with open(mock_log_path, "r") as csvfile:
        log_lines = csvfile.readlines()

    assert "1990-09-11" in log_lines[0]
    assert "Favourite distro" in log_lines[0]
    assert "£,100" in log_lines[0]
    assert "1990-09-11" in log_lines[1]
    assert "Favourite software" in log_lines[1]
    assert "£,50" in log_lines[1]
    assert "1990-09-11" in log_lines[2]
    assert "Podcast 1" in log_lines[2]
    assert "£,10" in log_lines[2]


def test_update_log_decimal(monkeypatch, mock_log_path, mock_date, donations):
    monkeypatch.setattr(donate.logs, "_log_path", mock_log_path)
    monkeypatch.setattr(donate.logs, "date", mock_date)

    update_log(donations, "$", True)

    with open(mock_log_path, "r") as csvfile:
        log_lines = csvfile.readlines()

    print(log_lines)
    assert "1990-09-11" in log_lines[0]
    assert "Favourite distro" in log_lines[0]
    assert "$,1.0" in log_lines[0]
    assert "1990-09-11" in log_lines[1]
    assert "Favourite software" in log_lines[1]
    assert "$,0.5" in log_lines[1]
    assert "1990-09-11" in log_lines[2]
    assert "Podcast 1" in log_lines[2]
    assert "$,0.1" in log_lines[2]
