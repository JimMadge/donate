from ..maths import share, single_donation
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


class TestSingleDonation:
    def test_single_split(self, donees):
        selected_donees = single_donation(donees, 20, 1)
        assert sum(selected_donees.values()) == 20
        assert len(selected_donees) == 1

    def test_multiple_split(self, donees):
        selected_donees = single_donation(donees, 20, 4)
        assert sum(selected_donees.values()) == 20
        assert len(selected_donees) <= 4
