from donate.__main__ import create_parser, format_donations
import pytest
import re


@pytest.fixture()
def parser():
    return create_parser()


def test_parser(parser):
    args = parser.parse_args([
        "-c", "hello",
        "-a",
        "-d",
        "-s",
        "-m", "100"
    ])

    assert args.config == "hello"
    assert args.ad_hoc
    assert args.dry_run
    assert args.stats
    assert args.means == 100


def test_parser2(parser):
    args = parser.parse_args([])

    assert args.config is None
    assert args.ad_hoc is False
    assert args.dry_run is False
    assert args.stats is False
    assert args.means is None


def test_format_donations(donations):
    donation_text = format_donations(donations, "$", False)

    assert re.search(r"^Favourite distro\s+\$100\s+distro.com", donation_text,
                     re.MULTILINE)
    assert re.search(r"^Favourite software\s+\$50\s+software.com",
                     donation_text,
                     re.MULTILINE)
    assert re.search(r"^Podcast 1\s+\$10\s+podcast1.com", donation_text,
                     re.MULTILINE)


def test_format_donations2(donations):
    donation_text = format_donations(donations, "£", True)

    assert re.search(r"^Favourite distro\s+\£1.00\s+distro.com", donation_text,
                     re.MULTILINE)
    assert re.search(r"^Favourite software\s+\£0.50\s+software.com",
                     donation_text,
                     re.MULTILINE)
    assert re.search(r"^Podcast 1\s+\£0.10\s+podcast1.com", donation_text,
                     re.MULTILINE)
