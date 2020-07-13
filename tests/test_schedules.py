from datetime import datetime
from dateutil.relativedelta import relativedelta
from donate.schedule import Schedule, AdHoc, Monthly
import pytest


def test_schedule():
    with pytest.raises(TypeError) as e:
        Schedule()

    exception_message = (
        "Can't instantiate abstract class Schedule with abstract methods"
        " due_donations"
        )
    assert str(e.value) == exception_message


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
