from donate.currency import Currency
import pytest


@pytest.fixture
def stirling():
    return Currency("£")


def test_symbol(stirling):
    assert stirling.symbol == "£"


def test_position(stirling):
    assert stirling.position == "before"


def test_ratio(stirling):
    assert stirling.ratio == 100


def test_decimal_separator(stirling):
    assert stirling.decimal_separator == "."


def test_minor_unit_width(stirling):
    assert stirling.minor_unit_width == 2


@pytest.mark.parametrize(
    "amount,expected",
    [(1, "£0.01"),
     (50, "£0.50"),
     (42, "£0.42"),
     (100, "£1.00"),
     (402, "£4.02"),
     (5342, "£53.42")]
)
def test_format(stirling, amount, expected):
    assert stirling.format(amount) == expected
