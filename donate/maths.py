"""Mathematical and statistical operations."""
from collections import Counter
from random import choices


def share(donees):
    """Calculate the share of each donee."""
    shares = [donee.weight.value for donee in donees]
    total = sum(shares)
    shares = [share / total for share in shares]

    return shares


def single_donation(donees, total_donation, split, decimal_currency=False):
    """
    Generate a single donation.

    :arg donees: List of donees.
    :type donees: list(:class:`Donee`)
    :arg int total_donation: Total donation amount.
    :arg int split: Number of donees to split the total donation between.
    :arg bool decimal_currency: If `True` allow spliting individual donations
        into hundreths. Default: `False`.

    :returns: Dictionary of each donee and their donation amount.
    :rtype: :class:`collections.Counter`
    """
    # When using a decimal currency allow spliting donations into hundreths
    if decimal_currency:
        total_donation *= 100

    # Ensure the donation splits into whole parts
    if total_donation % split != 0:
        raise ValueError(
            f"The donation split {split} does not equally divide the total"
            f"donation amount {total_donation}."
            )

    individual_donation = total_donation // split

    selected = choices(donees, weights=share(donees), k=split)

    individual_donations = Counter()
    for donee in selected:
        individual_donations[donee] += individual_donation

    return individual_donations
