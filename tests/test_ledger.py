from collections import Counter
import donate
from donate.ledger import _ledger_path, _get_ledger, ledger_stats
import json
import pytest
import re


def test_ledger_path():
    ledger_path = _ledger_path()
    path_string = str(ledger_path.absolute())

    assert path_string.split("/")[-1] == "ledger.json"
    assert path_string.split("/")[-2] == "donate"


@pytest.fixture
def mock_ledger_path(tmp_path):
    def _ledger_path():
        return tmp_path / "ledger.json"
    return _ledger_path


def test_no_ledger(monkeypatch, mock_ledger_path):
    monkeypatch.setattr(donate.ledger, "_ledger_path", mock_ledger_path)

    ledger = _get_ledger()

    assert ledger == {"total": Counter(), "number": Counter()}


def test_ledger(monkeypatch, mock_ledger_path):
    ledger_dict = {
        "total": {"a": 50, "b": 30},
        "number": {"a": 5, "b": 2}
    }
    with open(mock_ledger_path(), "w") as ledger:
        json.dump(ledger_dict, ledger)

    monkeypatch.setattr(donate.ledger, "_ledger_path", mock_ledger_path)

    ledger = _get_ledger()

    assert ledger == {
        "total": Counter(ledger_dict["total"]),
        "number": Counter(ledger_dict["number"])}


def test_ledger_stats(monkeypatch):
    def mock_get_ledger():
        return {
            "total": {"a": 50, "b": 30},
            "number": {"a": 5, "b": 2}
        }

    monkeypatch.setattr(donate.ledger, "_get_ledger", mock_get_ledger)

    stats = ledger_stats("£")
    # Split the total donation and number of donation parts
    total_stats, number_stats = stats.rsplit("\n\n")

    assert re.match(r"^Donee\s+Total / £$", total_stats, re.MULTILINE)
    assert re.search(r"^a\s+50$", total_stats, re.MULTILINE)
    assert re.search(r"^b\s+30$", total_stats, re.MULTILINE)

    assert re.match(r"^Donee\s+Number of donations", number_stats,
                    re.MULTILINE)
    assert re.search(r"^a\s+5$", number_stats, re.MULTILINE)
    assert re.search(r"^b\s+2$", number_stats, re.MULTILINE)
