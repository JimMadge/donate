"""Test log functions."""
from datetime import date
import donate
from donate.ledger import _log_path, update_log
import pytest


def test_log_path():
    log_path = _log_path()
    path_string = str(log_path.absolute())

    assert path_string.split("/")[-1] == "donation_log.csv"
    assert path_string.split("/")[-2] == "donate"


@pytest.fixture
def mock_log_path(tmp_path):
    def _log_path():
        return tmp_path / "donation_log.csv"
    return _log_path


@pytest.fixture
def mock_date():
    class MyDate(object):
        @staticmethod
        def today():
            return date(1990, 9, 11)

    return MyDate()


def test_update_log(monkeypatch, mock_log_path, mock_date, donations):
    monkeypatch.setattr(donate.ledger, "_log_path", mock_log_path)
    monkeypatch.setattr(donate.ledger, "date", mock_date)

    update_log(donations, "£", False)

    with open(mock_log_path(), "r") as csvfile:
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
    monkeypatch.setattr(donate.ledger, "_log_path", mock_log_path)
    monkeypatch.setattr(donate.ledger, "date", mock_date)

    update_log(donations, "$", True)

    with open(mock_log_path(), "r") as csvfile:
        log_lines = csvfile.readlines()

    assert "1990-09-11" in log_lines[0]
    assert "Favourite distro" in log_lines[0]
    assert "$,1.0" in log_lines[0]
    assert "1990-09-11" in log_lines[1]
    assert "Favourite software" in log_lines[1]
    assert "$,0.5" in log_lines[1]
    assert "1990-09-11" in log_lines[2]
    assert "Podcast 1" in log_lines[2]
    assert "$,0.1" in log_lines[2]
