"""Test configuration."""
import pytest
from donate.donee import Donee


@pytest.fixture(scope="session")
def donees():
    """Create example donees for testing."""
    return [Donee(*args) for args in [
        ("Favourite software", 0.5, "software", "software.com"),
        ("Useful software", 0.25, "software", "software.com"),
        ("Favourite distro", 1.0, "distribution", "distro.com"),
        ("Podcast 1", 0.25, "podcast", "podcast1.com"),
        ("Podcast 2", 0.25, "podcast", "podcast2.com"),
        ("Podcast 3", 0.25, "podcast", "podcast3.com"),
        ("Token support", 0.1, "software", "softare.com"),
        ("Podcast 4", 0.25, "podcast", "podcast4.com"),
        ("Charity", 0.25, "organisation", "charity.com")
    ]]


@pytest.fixture(scope="session")
def donations(donees):
    """Create an example set of donations."""

    return {
        donees[2]: 100,
        donees[0]: 50,
        donees[3]: 10
    }
