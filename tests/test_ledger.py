from collections import Counter
import donate
from donate.ledger import _get_ledger, ledger_stats
import json
import re


class TestGetLedger:
    def test_no_ledger(self, monkeypatch, tmp_path):
        def mock_save_data_path(resource):
            return tmp_path / resource

        monkeypatch.setattr(donate.ledger.BaseDirectory, "save_data_path",
                            mock_save_data_path)

        ledger, ledger_path = _get_ledger()

        assert ledger == {"total": Counter(), "number": Counter()}
        assert str(ledger_path).endswith("donate/ledger.json")

    def test_ledger(self, monkeypatch, tmp_path):
        def mock_save_data_path(resource):
            return tmp_path / resource

        ledger_dict = {
            "total": {"a": 50, "b": 30},
            "number": {"a": 5, "b": 2}
        }
        ledger_path = mock_save_data_path("donate")
        ledger_path.mkdir()
        with open(ledger_path / "ledger.json", "w") as ledger:
            json.dump(ledger_dict, ledger)

        monkeypatch.setattr(donate.ledger.BaseDirectory, "save_data_path",
                            mock_save_data_path)

        ledger, ledger_path = _get_ledger()

        assert ledger == {
            "total": Counter(ledger_dict["total"]),
            "number": Counter(ledger_dict["number"])}
        assert str(ledger_path).endswith("donate/ledger.json")


def test_ledger_stats(monkeypatch):
    def mock_get_ledger():
        return (
            {
                "total": {"a": 50, "b": 30},
                "number": {"a": 5, "b": 2}
            },
            None
        )

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
