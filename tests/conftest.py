"""Test configuration."""
import pytest
from donate.donee import Donee


@pytest.fixture(scope="session")
def donees():
    """Create Example donees for testing."""
    return [Donee(*args) for args in [
        ("Favourite distro", 1.0, "distribution", "distro.com"),
        ("Favourite software", 0.5, "software", "software.com"),
        ("Useful software", 0.25, "software", "software.com"),
        ("Podcast 1", 0.25, "podcast", "podcast1.com"),
        ("Podcast 2", 0.25, "podcast", "podcast2.com"),
        ("Podcast 3", 0.25, "podcast", "podcast3.com"),
        ("Podcast 4", 0.25, "podcast", "podcast4.com"),
        ("Charity", 0.25, "organisation", "charity.com"),
        ("Token support", 0.1, "software", "softare.com")
    ]]
