"""Test log functions."""
from datetime import date
import donate
from donate.ledger import Ledger, _convert_boolean
import pytest


def test_convert_boolen():
    assert _convert_boolean(1)
    assert not _convert_boolean(0)


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


@pytest.fixture
def example_ledger(monkeypatch, mock_date, donations):
    monkeypatch.setattr(donate.ledger, "date", mock_date)

    # Create ledger in memory
    ledger = Ledger(ledger_path=":memory:")

    # Add trial donations to ledger
    ledger.add(donations, "£", True)

    return ledger


def test_add(example_ledger):
    # Get all rows from ledger
    with example_ledger.con as con:
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


def test_len(example_ledger):
    assert len(example_ledger) == 3


def test_all_entries(example_ledger):
    entries = example_ledger[:]

    # Check entry types
    types = (date, str, str, bool, int)
    assert type(entries) == list
    assert type(entries[0]) == tuple
    for a, b in zip(entries[0], types):
        assert type(a) == b

    # Check entry values
    assert entries[0] == (date(1990, 9, 11), 'Favourite distro', '£', True,
                          100)
    assert entries[1] == (date(1990, 9, 11), 'Favourite software', '£', True,
                          50)
    assert entries[2] == (date(1990, 9, 11), 'Podcast 1', '£', True, 10)
    assert len(entries) == 3


def test_first_entry(example_ledger):
    entry = example_ledger[0]

    types = (date, str, str, bool, int)
    assert type(entry) == tuple
    for a, b in zip(entry, types):
        assert type(a) == b

    assert entry == (date(1990, 9, 11), 'Favourite distro', '£', True, 100)


def test_out_of_index(example_ledger):
    with pytest.raises(IndexError):
        example_ledger[10]


def test_invalid_key(example_ledger):
    with pytest.raises(TypeError):
        example_ledger["hello"]
