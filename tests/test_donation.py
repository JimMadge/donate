import donate
from donate.donation import (weights, normalised_weights, create_donations,
                             _means, donee_means, category_means,
                             means_summary)
import pytest
import re


def test_weights(donees):
    donee_weights = weights(donees)
    for donee, weight in zip(donees, donee_weights):
        assert donee.weight == weight


@pytest.fixture(scope="session")
def example_normalised_weights(donees):
    return normalised_weights(donees)


def test_normalised_weights(example_normalised_weights):
    assert sum(example_normalised_weights) == pytest.approx(1.0)


@pytest.mark.parametrize("number,share", [
    (2, 0.3225806),
    (5, 0.0806452),
    (7, 0.0806452),
    (6, 0.0322581)
    ])
def test_share(example_normalised_weights, number, share):
    assert example_normalised_weights[number] == pytest.approx(share, rel=1e-5)


class TestSingleDonation:
    def test_single_split(self, donees):
        individual_donations = create_donations(donees, 20, 1)
        assert sum(individual_donations.values()) == 20
        assert len(individual_donations) == 1

    def test_single_split_decimal(self, donees):
        individual_donations = create_donations(donees, 20, 1, True)
        assert sum(individual_donations.values()) == 2000
        assert len(individual_donations) == 1

    def test_multiple_split(self, donees):
        individual_donations = create_donations(donees, 20, 4)
        assert sum(individual_donations.values()) == 20
        assert len(individual_donations) <= 4

    def test_multiple_split_decimal(self, donees):
        individual_donations = create_donations(donees, 20, 4, True)
        assert sum(individual_donations.values()) == 2000
        assert len(individual_donations) <= 4

    def test_non_divisable(self, donees):
        with pytest.raises(ValueError) as e:
            create_donations(donees, 10, 3)
        assert f"The donation split {3}" in str(e.value)

    def test_create_donations_output(self, donees, monkeypatch):
        # Create mock choices function which just returns 'k' of the first
        # element
        def mock_choices(population, weights, *, k=1):
            return [population[0]]*k
        monkeypatch.setattr(donate.donation, "choices", mock_choices)

        individual_donations = create_donations(donees, 20, 4)
        assert sum(individual_donations.values()) == 20
        assert len(individual_donations) == 1
        for donee in individual_donations:
            assert donee is donees[0]


expected_means = [16.129032258064516, 8.064516129032258, 32.25806451612903,
                  8.064516129032258, 8.064516129032258, 8.064516129032258,
                  3.225806451612903, 8.064516129032258, 8.064516129032258]


def test_means(donees):
    means = _means(donees, 100)
    assert means == expected_means


def test_donee_means(donees):
    means = donee_means(donees, 100)

    expected_donees = [
        "Favourite distro", "Favourite software", "Useful software",
        "Podcast 1", "Podcast 2", "Podcast 3", "Podcast 4", "Charity",
        "Token support"
    ]

    assert [elem[1] for elem in means] == sorted(expected_means, reverse=True)
    assert [elem[0] for elem in means] == expected_donees


def test_category_means(donees):
    means = category_means(donees, 100)

    assert len(means) == 4
    assert means[0] == ("distribution", 32.25806451612903)
    assert means[1] == ("podcast", 32.25806451612903)
    assert means[2] == ("software", 27.41935483870968)
    assert means[3] == ("organisation", 8.064516129032258)


def test_means_summary(donees):
    means = means_summary(donees, 100, "£")

    header, donee_means, category_means = means.rsplit("\n\n")

    assert re.search(r"^Mean donations from £100$", header, re.MULTILINE)

    assert re.search(r"^Donee\s+Mean donation / £$", donee_means, re.MULTILINE)
    assert re.search(r"^Favourite distro\s+32.2581$", donee_means,
                     re.MULTILINE)
    assert re.search(r"^Favourite software\s+16.129$", donee_means,
                     re.MULTILINE)

    assert re.search(r"^Category\s+Mean donation / £$", category_means,
                     re.MULTILINE)
    assert re.search(r"^distribution\s+32.2581$", category_means,
                     re.MULTILINE)
    assert re.search(r"^podcast\s+32.2581$", category_means,
                     re.MULTILINE)
