"""Donee object."""
from collections import namedtuple
from enum import Enum, auto

Donee = namedtuple("Donee", ["name", "weight", "donee_type", "donation_url"])
Donee.__doc__ += ": A Donee."
Donee.name.__doc__ = "The name of the donee."
Donee.weight.__doc__ = (
    "The relative weight of donations recieved by the donee."
    )
Donee.donee_type.__doc__ = "The category of the donee."
Donee.donation_url.__doc__ = "The url of the donee's donation page."


class Type(Enum):
    """Donee type enumeration."""

    SOFTWARE = auto
    DISTRIBUTION = auto
    SERVICE = auto
    PODCAST = auto
    ORGANISATION = auto
    CHARITY = auto
    OTHER = auto
