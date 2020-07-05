"""Test configuration."""
import pytest
from donate.donee import Donee, Type


@pytest.fixture(scope="session")
def donees():
    """Create Example donees for testing."""
    return [Donee(*args) for args in [
        ("Favourite distro", 1.0, Type.DISTRIBUTION,
         "distro.com"),
        ("Favourite software", 0.5, Type.SOFTWARE,
         "software.com"),
        ("Useful software", 0.25, Type.SOFTWARE,
         "software.com"),
        ("Podcast 1", 0.25, Type.PODCAST, "podcast1.com"),
        ("Podcast 2", 0.25, Type.PODCAST, "podcast2.com"),
        ("Podcast 3", 0.25, Type.PODCAST, "podcast3.com"),
        ("Podcast 4", 0.25, Type.PODCAST, "podcast4.com"),
        ("Charity", 0.25, Type.ORGANISATION, "charity.com"),
        ("Token support", 0.1, Type.SOFTWARE, "softare.com")
        ]
        ]
