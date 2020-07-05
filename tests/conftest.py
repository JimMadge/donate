"""Test configuration."""
import pytest
from donate.donee import Donee, Type, Weight


@pytest.fixture(scope="session")
def donees():
    """Create Example donees for testing."""
    return [Donee(*args) for args in [
        ("Favourite distro", Weight.CRITICAL, Type.DISTRIBUTION, "distro.com"),
        ("Favourite software", Weight.LARGE, Type.SOFTWARE, "software.com"),
        ("Useful software", Weight.MEDIUM, Type.SOFTWARE, "software.com"),
        ("Podcast 1", Weight.MEDIUM, Type.PODCAST, "podcast1.com"),
        ("Podcast 2", Weight.MEDIUM, Type.PODCAST, "podcast2.com"),
        ("Podcast 3", Weight.MEDIUM, Type.PODCAST, "podcast3.com"),
        ("Podcast 4", Weight.MEDIUM, Type.PODCAST, "podcast4.com"),
        ("Charity", Weight.MEDIUM, Type.ORGANISATION, "charity.com"),
        ("Token support", Weight.SMALL, Type.SOFTWARE, "softare.com")
        ]
        ]
