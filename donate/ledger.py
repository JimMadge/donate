from .donee import Donee
from .maths import split_decimal
from collections import Counter
import json
from pathlib import Path
from tabulate import tabulate
from typing import Union
from xdg import BaseDirectory  # type: ignore


def _ledger_path() -> Path:
    data_path = Path(BaseDirectory.save_data_path("donate"))
    return data_path / "ledger.json"


def _get_ledger() -> dict[str, Counter[str]]:
    """Return the existing ledger or create an empty ledger."""
    try:
        with open(_ledger_path(), "r") as ledger_file:
            ledger_dict = json.load(ledger_file)
            ledger: dict[str, Counter[str]] = dict(
                total=Counter(ledger_dict["total"]),
                number=Counter(ledger_dict["number"])
            )
    except FileNotFoundError:
        ledger = {"total": Counter(), "number": Counter()}

    return ledger


def update_ledger(donations: Counter[Donee]) -> None:
    ledger = _get_ledger()
    total = ledger["total"]
    number = ledger["number"]

    for donee, amount in donations.items():
        name = donee.name
        total[name] += amount
        number[name] += 1

    with open(_ledger_path(), "w") as ledger_file:
        json.dump(ledger, ledger_file, indent=2)


def ledger_stats(currency_symbol: str, decimal_currency: bool) -> str:
    ledger = _get_ledger()
    total = ledger["total"]
    number = ledger["number"]

    total_output: dict[str, Union[float, int]] = dict()
    if decimal_currency:
        for donee, amount in total.items():
            whole, hundreths = split_decimal(amount)
            total_output[donee] = whole + (hundreths/100)
    else:
        total_output = dict(total)

    stats = "\n".join([
        tabulate(list(total_output.items()),
                 headers=["Donee", f"Total / {currency_symbol}"],
                 floatfmt=".2f"),
        "",
        tabulate(list(number.items()),
                 headers=["Donee", "Number of donations"])
    ])
    return stats
