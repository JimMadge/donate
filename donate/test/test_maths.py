from ..maths import share, single_donation
import pytest


@pytest.fixture(scope="session")
def example_shares(donees):
    return share(donees)


def test_share_total(example_shares):
    assert example_shares.sum() == pytest.approx(1.0)


@pytest.mark.parametrize("number,share", [
    (0, 0.3225806),
    (5, 0.0806452),
    (7, 0.0806452),
    (8, 0.0322581)
    ])
def test_share(example_shares, number, share):
    assert example_shares[number] == pytest.approx(share, rel=1e-5)


class TestSingleDonation:
    def test_single_split(self, donees):
        individual_donations = single_donation(donees, 20, 1)
        assert sum(individual_donations.values()) == 20
        assert len(individual_donations) == 1

    def test_multiple_split(self, donees):
        individual_donations = single_donation(donees, 20, 4)
        assert sum(individual_donations.values()) == 20
        assert len(individual_donations) <= 4

    def test_non_divisable(self, donees):
        with pytest.raises(ValueError) as e:
            single_donation(donees, 10, 3)
        assert f"The donation split {3}" in str(e.value)
