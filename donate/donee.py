"""Donee object."""
from collections import namedtuple

Donee = namedtuple("Donee", ["name", "weight", "category", "donation_url"])
Donee.__doc__ += ": A Donee."
Donee.name.__doc__ = "The name of the donee."
Donee.weight.__doc__ = (
    "The relative weight of donations recieved by the donee."
    )
Donee.category.__doc__ = "The category of the donee."
Donee.donation_url.__doc__ = "The url of the donee's donation page."
