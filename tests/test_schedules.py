from datetime import datetime
from dateutil.relativedelta import relativedelta
import donate.schedule
from donate.schedule import (Schedule, AdHoc, Monthly, _last_donation_path,
                             get_last_donation, update_last_donation)
import pytest


def test_schedule():
    with pytest.raises(TypeError) as e:
        Schedule()

    exception_message = (
        "Can't instantiate abstract class Schedule with abstract method"
        )
    assert exception_message in str(e.value)
    assert "due_donations" in str(e.value)


@pytest.mark.parametrize("Schedule", [AdHoc, Monthly])
def test_no_last_donation(Schedule):
    schedule = Schedule()
    assert schedule.due_donations(None) == 1


def test_adhoc():
    s = AdHoc()
    last_donation = datetime.now()

    for i in range(2):
        assert s.due_donations(last_donation) == 1


@pytest.mark.parametrize(
    "years,months,expected",
    [(0, 0, 0),
     (0, 2, 2),
     (0, 5, 5),
     (1, 0, 12),
     (1, 8, 20)]
    )
def test_monthly(years, months, expected):
    s = Monthly()
    last_donation = datetime.now() - relativedelta(years=years, months=months)

    assert s.due_donations(last_donation) == expected


def test_last_donation_path():
    last_donation_path = _last_donation_path()
    path_string = str(last_donation_path.absolute())

    assert path_string.split("/")[-1] == "last_donation"
    assert path_string.split("/")[-2] == "donate"


@pytest.fixture
def mock_last_donation_path(tmp_path):
    def _last_donation_path():
        return tmp_path / "last_donation"
    return _last_donation_path


def test_get_empty_last_donation(monkeypatch, mock_last_donation_path):
    monkeypatch.setattr(donate.schedule, "_last_donation_path",
                        mock_last_donation_path)

    last_donation = get_last_donation()
    assert last_donation is None


def test_get_last_donation(monkeypatch, mock_last_donation_path):
    monkeypatch.setattr(donate.schedule, "_last_donation_path",
                        mock_last_donation_path)

    expected_last_donation = datetime(1990, 11, 9)
    with open(mock_last_donation_path(), "w") as last_donation_file:
        last_donation_file.write(expected_last_donation.isoformat() + "\n")

    last_donation = get_last_donation()
    assert last_donation == expected_last_donation


def test_update_last_donation(monkeypatch, mock_last_donation_path):
    expected_last_donation = datetime(1990, 11, 9)

    class MockDatetime(datetime):
        @staticmethod
        def today():
            return expected_last_donation

    monkeypatch.setattr(donate.schedule, "_last_donation_path",
                        mock_last_donation_path)
    monkeypatch.setattr(donate.schedule, "datetime", MockDatetime)

    update_last_donation()

    last_donation = get_last_donation()
    assert last_donation == expected_last_donation
