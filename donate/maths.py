"""Mathematical and statistical operations."""
import numpy as np


def share(donees):
    """Calculate the share of each donee."""
    shares = np.empty(len(donees))

    for i, donee in enumerate(donees):
        shares[i] = donee.weight.value
    shares /= shares.sum()

    return shares
