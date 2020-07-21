from collections import Counter
import donate
from donate.ledger import _get_ledger


class TestGetLedger:
    def test_no_ledger(self, monkeypatch, tmp_path):
        def mock_save_data_path(resource):
            return tmp_path / resource

        monkeypatch.setattr(donate.ledger.BaseDirectory, "save_data_path",
                            mock_save_data_path)

        ledger, ledger_path = _get_ledger()

        assert ledger == {"total": Counter(), "number": Counter()}
        print(ledger_path)
        print(tmp_path)
        assert str(ledger_path).endswith("donate/ledger.json")
