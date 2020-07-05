"""Test configuration."""
import pytest
from donate.donee import Donee, Type, Weight


@pytest.fixture(scope="session")
def donees():
    """Create Example donees for testing."""
    return [Donee(*args) for args in [
        ("Favourite distro", Weight.CRITICAL.value, Type.DISTRIBUTION,
         "distro.com"),
        ("Favourite software", Weight.LARGE.value, Type.SOFTWARE,
         "software.com"),
        ("Useful software", Weight.MEDIUM.value, Type.SOFTWARE,
         "software.com"),
        ("Podcast 1", Weight.MEDIUM.value, Type.PODCAST, "podcast1.com"),
        ("Podcast 2", Weight.MEDIUM.value, Type.PODCAST, "podcast2.com"),
        ("Podcast 3", Weight.MEDIUM.value, Type.PODCAST, "podcast3.com"),
        ("Podcast 4", Weight.MEDIUM.value, Type.PODCAST, "podcast4.com"),
        ("Charity", Weight.MEDIUM.value, Type.ORGANISATION, "charity.com"),
        ("Token support", Weight.SMALL.value, Type.SOFTWARE, "softare.com")
        ]
        ]
