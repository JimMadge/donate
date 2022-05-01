from typing import Optional


class Currency:
    def __init__(self, symbol: str, position: str = "before",
                 ratio: Optional[int] = 100,
                 decimal_separator: str = ".") -> None:

        if position not in ("before", "after"):
            raise ValueError("position must be one of 'before' or 'after'")

        if ratio not in (None, 10, 100, 1000):
            raise ValueError("decimal must be one of '10', '100', '1000'")

        self.symbol = symbol
        self.position = position
        self.ratio = ratio
        self.decimal_separator = decimal_separator

    def split(self, amount: int) -> tuple[int, int]:
        """Split amount (in minor units) into the largest number of major units
        and a remainder in minor units."""
        assert self.ratio

        major = amount // self.ratio
        minor = amount % self.ratio

        return major, minor

    @property
    def minor_unit_width(self):
        return {
            10: 1,
            100: 2,
            1000: 3,
        }[self.ratio]

    def format(self, amount: int) -> str:
        if self.ratio:
            major, minor = self.split(amount)
            width = self.minor_unit_width
            amount_str = f"{major}{self.decimal_separator}{minor:0{width}d}"
        else:
            amount_str = str(amount)

        if self.position == "before":
            amount_str = f"{self.symbol}{amount_str}"
        else:
            amount_str = f"{amount_str}{self.symbol}"

        return amount_str
