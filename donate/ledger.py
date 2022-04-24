from .donee import Donee
from collections import Counter
from datetime import date
from pathlib import Path
import sqlite3
from typing import Optional, Union
from xdg import BaseDirectory  # type: ignore


def _convert_boolean(boolean: int) -> bool:
    return bool(boolean)


sqlite3.register_converter("boolean", _convert_boolean)


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
        with self.con:
            self.con.execute("create table if not exists ledger"
                             " (id integer primary key,"
                             " date date,"
                             " name text,"
                             " currency text,"
                             " decimal boolean,"
                             " amount int)")

    @staticmethod
    def xdg_ledger_path() -> Path:
        return Path(BaseDirectory.save_data_path("donate")) / "ledger.db"

    def append(self, donations: Counter[Donee], currency_symbol: str,
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

    def __len__(self) -> int:
        """Count number of entries"""
        with self.con:
            length = self.con.execute("select count(*) from ledger")

        return int(length.fetchone()[0])

    def __getitem__(
        self, key: Union[int, slice]
    ) -> tuple[date, str, str, bool, int]:
        """Access entries by index or a slice"""
        with self.con:
            entries = self.con.execute(
                "select "
                "date, name, currency, decimal, amount "
                "from ledger"
            ).fetchall()

        return entries[key]
