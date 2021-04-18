from collections import Counter
import json
from pathlib import Path
from tabulate import tabulate
from xdg import BaseDirectory  # type: ignore


def _ledger_path():
    data_path = Path(BaseDirectory.save_data_path("donate"))
    return data_path / "ledger.json"


def _get_ledger():
    """Return the existing ledger or create an empty ledger."""
    try:
        with open(_ledger_path(), "r") as ledger_file:
            ledger = json.load(ledger_file)
            ledger["total"] = Counter(ledger["total"])
            ledger["number"] = Counter(ledger["number"])
    except FileNotFoundError:
        ledger = {"total": Counter(), "number": Counter()}

    return ledger


def update_ledger(donations, decimal_currency):
    ledger = _get_ledger()
    total = ledger["total"]
    number = ledger["number"]

    for donee, amount in donations.items():
        name = donee.name
        if decimal_currency:
            amount /= 100
        total[name] += amount
        number[name] += 1

    with open(_ledger_path(), "w") as ledger_file:
        json.dump(ledger, ledger_file, indent=2)


def ledger_stats(currency_symbol):
    ledger = _get_ledger()
    total = ledger["total"]
    number = ledger["number"]

    stats = "\n".join([
        tabulate(list(total.items()),
                 headers=["Donee", f"Total / {currency_symbol}"]),
        "",
        tabulate(list(number.items()),
                 headers=["Donee", "Number of donations"])
    ])
    return stats
