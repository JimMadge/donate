"""Mathematical and statistical operations."""
from .donee import Donee
from collections import Counter, defaultdict
from random import choices
from tabulate import tabulate


def weights(donees: list[Donee]) -> list[float]:
    """Get weights from donees."""
    return [donee.weight for donee in donees]


def normalised_weights(donees: list[Donee]) -> list[float]:
    """Calculate the normalised weights of each donee."""

    n_weights = weights(donees)
    total = sum(n_weights)
    n_weights = [weight / total for weight in n_weights]

    return n_weights


def single_donation(donees: list[Donee], total_donation: int, split: int,
                    decimal_currency: bool = False) -> Counter[Donee]:
    """Generate a single donation."""
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

    individual_donations: Counter[Donee] = Counter()
    for donee in selected:
        individual_donations[donee] += individual_donation

    return individual_donations


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
                 headers=["Donee", "Mean donation"]),
        "",
        tabulate(category_means(donees, total_donation),
                 headers=["Category", "Mean donation"])
    ])
    return means
