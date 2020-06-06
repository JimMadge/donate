"""Mathematical and statistical operations."""
from collections import Counter
import numpy as np
from numpy.random import choice


def share(donees):
    """Calculate the share of each donee."""
    shares = np.empty(len(donees))

    for i, donee in enumerate(donees):
        shares[i] = donee.weight.value
    shares /= shares.sum()

    return shares


def single_donation(donees, total_donation, split):
    """
    Generate a single donation.

    :arg donees: List of donees.
    :type donees: list(:class:`Donee`)
    :arg int total_donation: Total donation amount.
    :arg int split: Number of donees to split the total donation between.

    :returns: Dictionary of each donee and their donation amount.
    :rtype: :class:`collections.Counter`
    """
    if total_donation % split != 0:
        raise ValueError(
            f"The donation split {split} does not equally divide the total"
            f"donation amount {total_donation}."
            )

    individual_donation = total_donation // split

    choices = [
        donees[i] for i in choice(len(donees), split, p=share(donees))
        ]

    selected_donees = Counter()
    for donee in choices:
        selected_donees[donee] += individual_donation

    return selected_donees
