from .donee import Donee
from collections.abc import Sequence
from datetime import date
from pathlib import Path
import sqlite3
from typing import Any, Optional, Union, overload
from xdg import BaseDirectory  # type: ignore


def _convert_boolean(boolean: bytes) -> Any:
    return bool(boolean)


sqlite3.register_converter("boolean", _convert_boolean)

Entry = tuple[date, str, str, str, bool, int]


class Ledger(Sequence[Entry]):
    """A collection of donations backed by an sqlite database"""

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
                             " category text,"
                             " currency text,"
                             " decimal boolean,"
                             " amount int)")

    def __len__(self) -> int:
        """Count number of entries"""
        with self.con:
            length = self.con.execute("select count(*) from ledger")

        return int(length.fetchone()[0])

    @overload
    def __getitem__(self, index: int) -> Entry:
        ...

    @overload
    def __getitem__(self, index: slice) -> list[Entry]:
        ...

    def __getitem__(
        self, index: Union[int, slice]
    ) -> Union[Entry, list[Entry]]:
        """Get entries by index or a slice"""
        with self.con:
            entries = self.con.execute(
                "select "
                "date, name, category, currency, decimal, amount "
                "from ledger"
            ).fetchall()

        return entries[index]

    @staticmethod
    def xdg_ledger_path() -> Path:
        """Return XDG location of the ledger database"""
        return Path(BaseDirectory.save_data_path("donate")) / "ledger.db"

    def append(self, donations: dict[Donee, int], currency_symbol: str,
               decimal_currency: bool) -> None:
        """Add donation records to the ledger"""
        donation_date = date.today()

        rows = [
            (donation_date,
             donee.name,
             donee.category,
             currency_symbol,
             decimal_currency,
             amount)
            for donee, amount in donations.items()
        ]

        with self.con:
            self.con.executemany(
                "insert into "
                "ledger (date, name, category, currency, decimal, amount) "
                "values (?, ?, ?, ?, ?, ?)",
                rows
            )


DictEntry = dict[str, Union[date, str, str, str, bool, int]]


@overload
def dictify(entries: Entry) -> DictEntry:
    ...


@overload
def dictify(entries: list[Entry]) -> list[DictEntry]:
    ...


def dictify(entries: Entry | list[Entry]) -> DictEntry | list[DictEntry]:
    keys = ("date", "donee", "category", "currency", "decimal", "amount")
    match entries:
        case tuple():
            return dict(zip(keys, entries))
        case list():
            return [dict(zip(keys, entry)) for entry in entries]
