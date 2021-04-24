"""Test configuration."""
import pytest
from donate.donee import Donee


@pytest.fixture(scope="session")
def donees():
    """Create example donees for testing."""
    return [Donee(**args) for args in [
        {"name": "Favourite software", "weight": 0.5, "category": "software",
         "url": "software.com"},
        {"name": "Useful software", "weight": 0.25, "category": "software",
         "url": "software.com"},
        {"name": "Favourite distro", "weight": 1.0, "category": "distribution",
         "url": "distro.com"},
        {"name": "Podcast 1", "weight": 0.25, "category": "podcast",
         "url": "podcast1.com"},
        {"name": "Podcast 2", "weight": 0.25, "category": "podcast",
         "url": "podcast2.com"},
        {"name": "Podcast 3", "weight": 0.25, "category": "podcast",
         "url": "podcast3.com"},
        {"name": "Token support", "weight": 0.1, "category": "software",
         "url": "sofware.com"},
        {"name": "Podcast 4", "weight": 0.25, "category": "podcast",
         "url": "podcast4.com"},
        {"name": "Charity", "weight": 0.25, "category": "organisation",
         "url": "charity.com"}
    ]]


@pytest.fixture(scope="session")
def donations(donees):
    """Create an example set of donations."""

    return {
        donees[2]: 100,
        donees[0]: 50,
        donees[3]: 10
    }
