from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Type
from xdg import BaseDirectory  # type: ignore


class Schedule(ABC):
    """Schedule base class."""
    friendly_name = ""

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
    friendly_name = "ad hoc"

    def due_donations(self, last_donation):
        return 1


class Monthly(Schedule):
    """Monthly schedule. One donation per calendar month."""
    friendly_name = "monthly"

    def due_donations(self, last_donation):
        if last_donation is None:
            return 1

        date = datetime.today()

        elapsed_months = (
            (date.year - last_donation.year)*12
            + (date.month - last_donation.month)
            )

        return elapsed_months


# Raises and error with mypy
# schedule_map: dict[str, Type[Schedule]] = {
#     cls.friendly_name: cls for cls in Schedule.__subclasses__()
# }
schedule_map: dict[str, Type[Schedule]] = {
    "ad hoc": AdHoc,
    "monthly": Monthly
}


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
