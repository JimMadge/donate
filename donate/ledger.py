from collections import Counter
import json
from pathlib import Path
from tabulate import tabulate
from xdg import BaseDirectory


def _get_ledger():
    # Open existing ledger, or create a new one
    data_path = Path(BaseDirectory.save_data_path("donate"))
    ledger_path = data_path / "ledger.json"
    try:
        with open(ledger_path, "r") as ledger_file:
            ledger = json.load(ledger_file)
            ledger["total"] = Counter(ledger["total"])
            ledger["number"] = Counter(ledger["number"])
    except FileNotFoundError:
        ledger = {"total": Counter(), "number": Counter()}

    return ledger, ledger_path


def update_ledger(donations, decimal_currency):
    ledger, ledger_path = _get_ledger()
    total = ledger["total"]
    number = ledger["number"]

    for donee, amount in donations.items():
        name = donee.name
        if decimal_currency:
            amount /= 100
        total[name] += amount
        number[name] += 1

    with open(ledger_path, "w") as ledger_file:
        json.dump(ledger, ledger_file, indent=2)


def print_ledger_stats(currency_symbol, decimal_currency):
    ledger, ledger_path = _get_ledger()
    total = ledger["total"]
    number = ledger["number"]

    print(tabulate(
        list(total.items()),
        headers=["Donee", f"Total / {currency_symbol}"]
        ))

    print("\n")
    print(tabulate(
        list(number.items()),
        headers=["Donee", "Number of donations"]
        ))
