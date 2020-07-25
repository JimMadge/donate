from collections import Counter
import donate
from donate.ledger import _get_ledger
import json


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
