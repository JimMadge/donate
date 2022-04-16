"""Test log functions."""
from datetime import date
import donate
from donate.ledger import Ledger
import pytest


def test_xdg_ledger_path():
    path = Ledger.xdg_ledger_path()
    path_string = str(path.absolute())

    assert path_string.split("/")[-1] == "ledger.db"
    assert path_string.split("/")[-2] == "donate"


@pytest.fixture
def mock_date():
    class MyDate(object):
        @staticmethod
        def today():
            return date(1990, 9, 11)

    return MyDate()


def test_update_log(monkeypatch, mock_date, donations):
    monkeypatch.setattr(donate.ledger, "date", mock_date)

    # Create ledger in memory
    ledger = Ledger(ledger_path=":memory:")

    # Add trial donations to ledger
    ledger.add(donations, "£", True)

    # Get all rows from ledger
    with ledger.con as con:
        rows = con.execute("select * from ledger").fetchall()

    # Check ledger entries match match trial donations
    # The first column is a unique id and is discarded
    assert rows[0][1:] == (date(1990, 9, 11), 'Favourite distro', '£', True,
                           100)
    assert rows[1][1:] == (date(1990, 9, 11), 'Favourite software', '£', True,
                           50)
    assert rows[2][1:] == (date(1990, 9, 11), 'Podcast 1', '£', True,
                           10)
    assert len(rows) == 3
