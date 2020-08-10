"""Mathematical and statistical operations."""
from collections import Counter
from random import choices


def weights(donees):
    """Get weights from donees."""
    return [donee.weight for donee in donees]


def normalised_weights(donees):
    """Calculate the normalised weights of each donee."""

    n_weights = weights(donees)
    total = sum(n_weights)
    n_weights = [weight / total for weight in n_weights]

    return n_weights


def single_donation(donees, total_donation, split, decimal_currency=False):
    """
    Generate a single donation.

    :arg donees: List of donees.
    :type donees: list(:class:`Donee`)
    :arg int total_donation: Total donation amount.
    :arg int split: Number of donees to split the total donation between.
    :arg bool decimal_currency: If `True` allow splitting individual donations
        into hundredths. Default: `False`.

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

    selected = choices(
        donees,
        weights=weights(donees),
        k=split
        )

    individual_donations = Counter()
    for donee in selected:
        individual_donations[donee] += individual_donation

    return individual_donations


def _means(donees, total_donation):
    weights = normalised_weights(donees)
    return [weight * total_donation for weight in weights]


def donee_means(donees, total_donation):
    """
    Calculate the mean donation received by each donee.

    :arg donees: List of donees.
    :type donees: list(:class:`Donee`)
    :arg int total_donation: Total donation amount.
    """
    names = [donee.name for donee in donees]
    means = _means(donees, total_donation)
    return list(zip(names, means))


def category_means(donees, total_donation):
    """
    Calculate the mean donation received by each category of donee.

    :arg donees: List of donees.
    :type donees: list(:class:`Donee`)
    :arg int total_donation: Total donation amount.
    """
    means = _means(donees, total_donation)

    category_means = Counter()
    for donee, mean in zip(donees, means):
        category_means[donee.category] += mean
    return category_means
