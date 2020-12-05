from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from xdg import BaseDirectory


class Schedule(ABC):
    """Schedule base class."""

    @abstractmethod
    def due_donations(self, last_donation):
        """
        Calculate how many donations are due based on the date of the last
        donation.

        If `last_donation` is `None` this method should return 1.

        :arg last_donation: Time of the last donation.
        :rtype last_donation: :class:`datetime.datetime` or NoneType
        """


class AdHoc(Schedule):
    """Add hoc schedule. Donate whenever you want to."""

    def due_donations(self, last_donation):
        return 1


class Monthly(Schedule):
    """Monthly schedule. One donation per calendar month."""

    def due_donations(self, last_donation):
        if last_donation is None:
            return 1

        date = datetime.today()

        elapsed_months = (
            (date.year - last_donation.year)*12
            + (date.month - last_donation.month)
            )

        return elapsed_months


def _last_donation_path():
    data_path = Path(BaseDirectory.save_data_path("donate"))
    return data_path / "last_donation"


def get_last_donation():
    """Get the time of the last donation."""
    last_donation_path = _last_donation_path()

    try:
        with open(last_donation_path) as last_donation_file:
            last_donation = datetime.fromisoformat(
                last_donation_file.read().strip()
            )
    except FileNotFoundError:
        last_donation = None

    return last_donation


def update_last_donation():
    """Write the current time to the last donation file."""
    last_donation_path = _last_donation_path()

    with open(last_donation_path, "w") as last_donation_file:
        last_donation_file.write(datetime.today().isoformat()+"\n")
