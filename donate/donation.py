from .donee import Donee
from collections import Counter, defaultdict
from random import choices
from tabulate import tabulate


def create_donations(donees: list[Donee], total_donation: int, split: int,
                     decimal_currency: bool = False) -> dict[Donee, int]:
    """Generate a set of donations from `total_donation` split `split` ways."""
    # When using a decimal currency allow splitting donations into hundredths
    if decimal_currency:
        total_donation *= 100

    # Ensure the donation splits into whole parts
    if total_donation % split != 0:
        raise ValueError(
            f"The donation split {split} does not equally divide the total"
            f"donation amount {total_donation}."
            )

    individual_donation = total_donation // split

    # Choose donees to donate to, duplicates are possible
    split_donations = choices(
        donees,
        weights=weights(donees),
        k=split
        )

    # Count number of donations to each donee
    n_donations = Counter(split_donations)

    # Combine individual donations into total donation for each donee
    donations: dict[Donee, int] = {}
    for donee, occurances in n_donations.items():
        donations[donee] = individual_donation * occurances

    return donations


def split_decimal(amount: int) -> tuple[int, int]:
    """Split a decimal currency into who an hundredths."""
    whole = amount // 100
    hundreths = amount % 100
    return whole, hundreths


def weights(donees: list[Donee]) -> list[float]:
    """Get the weight of each donees."""
    return [donee.weight for donee in donees]


def normalised_weights(donees: list[Donee]) -> list[float]:
    """Calculate the normalised weight of each donee."""

    n_weights = weights(donees)
    total = sum(n_weights)
    n_weights = [weight / total for weight in n_weights]

    return n_weights


def _means(donees: list[Donee], total_donation: int) -> list[float]:
    weights = normalised_weights(donees)
    return [weight * total_donation for weight in weights]


def donee_means(donees: list[Donee],
                total_donation: int) -> list[tuple[str, float]]:
    """Calculate the mean donation received by each donee."""
    names = [donee.name for donee in donees]
    means = _means(donees, total_donation)
    return sorted(list(zip(names, means)), key=lambda elem: elem[1],
                  reverse=True)


def category_means(donees: list[Donee],
                   total_donation: int) -> list[tuple[str, float]]:
    """Calculate the mean donation received by each category of donee."""
    means = _means(donees, total_donation)

    category_means: defaultdict[str, float] = defaultdict(float)
    for donee, mean in zip(donees, means):
        category_means[donee.category] += mean

    return sorted(category_means.items(), key=lambda item: item[1],
                  reverse=True)


def means_summary(donees: list[Donee], total_donation: int,
                  currency_symbol: str) -> str:
    """Create tables summarising mean donations for donees and categories."""
    means = "\n".join([
        f"Mean donations from {currency_symbol}{total_donation}",
        "",
        tabulate(donee_means(donees, total_donation),
                 headers=["Donee", f"Mean donation / {currency_symbol}"]),
        "",
        tabulate(category_means(donees, total_donation),
                 headers=["Category", f"Mean donation / {currency_symbol}"])
    ])
    return means
