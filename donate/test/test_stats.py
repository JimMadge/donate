from ..stats import share
import numpy as np
import pytest


@pytest.fixture(scope="session")
def example_shares(donees):
    return share(donees)


def test_share_total(example_shares):
    assert np.isclose(example_shares.sum(), 1.0)


@pytest.mark.parametrize("number,share", [
    (0, 0.3225806),
    (5, 0.0806452),
    (7, 0.0806452),
    (8, 0.0322581)
    ])
def test_share(example_shares, number, share):
    assert np.isclose(example_shares[number], share)
