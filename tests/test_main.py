from donate.__main__ import create_parser
import pytest


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
