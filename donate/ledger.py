from .donee import Donee
from collections import Counter
from csv import writer
from datetime import date
from pathlib import Path
from typing import Union
from xdg import BaseDirectory  # type: ignore


def _log_path() -> Path:
    data_path = Path(BaseDirectory.save_data_path("donate"))
    return data_path / "donation_log.csv"


def update_log(donations: Counter[Donee], currency_symbol: str,
               decimal_currency: bool) -> None:
    with open(_log_path(), "a", newline="") as csvfile:
        log_writer = writer(csvfile)

        donation_date = date.today().isoformat()

        for donee, amount in donations.items():
            log_amount: Union[int, float]
            if decimal_currency:
                log_amount = amount / 100
            else:
                log_amount = amount

            log_writer.writerow(
                [donation_date, donee.name, currency_symbol, log_amount]
            )
