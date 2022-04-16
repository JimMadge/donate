from .donee import Donee
from collections import Counter
from datetime import date
from pathlib import Path
import sqlite3
from typing import Optional
from xdg import BaseDirectory  # type: ignore


class Ledger:
    def __init__(self, ledger_path: Optional[Path] = None):
        if ledger_path:
            self.path = ledger_path
        else:
            self.path = self.xdg_ledger_path()

        # Connect to database
        # PARSE_DECLTYPES gives support for type converters (like the built in
        # date converter)
        self.con = sqlite3.connect(
            self.path,
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        # Initialise database
        self.con.execute("create table if not exists ledger"
                         " (id integer primary key,"
                         " date date,"
                         " name text,"
                         " currency text,"
                         " decimal boolean,"
                         " amount int)")

    def add(self, donations: Counter[Donee], currency_symbol: str,
            decimal_currency: bool) -> None:
        """Add donation records to the ledger"""
        donation_date = date.today()

        rows = [
            (donation_date,
             donee.name,
             currency_symbol,
             decimal_currency,
             amount)
            for donee, amount in donations.items()
        ]

        with self.con:
            self.con.executemany(
                "insert into "
                "ledger (date, name, currency, decimal, amount) "
                "values (?, ?, ?, ?, ?)",
                rows
            )

    @staticmethod
    def xdg_ledger_path() -> Path:
        return Path(BaseDirectory.save_data_path("donate")) / "ledger.db"
