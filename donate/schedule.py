from abc import ABC, abstractmethod
from datetime import datetime


class Schedule(ABC):
    """Schedule base class."""

    @abstractmethod
    def due_donations(self, last_donation):
        """
        Calculate how many donations are due based on the date of the last
        donation.

        :arg last_donation: Time of the last donation.
        :rtype last_donation: :class:`datetime.datetime`
        """
        pass


class AdHoc(Schedule):
    """Add hoc schedule. Donate whenever you want to."""

    def due_donations(self, last_donation):
        return 1


class Monthly(Schedule):
    """Monthly schedule. One donation per calendar month."""

    def due_donations(self, last_donation):
        date = datetime.today()

        elapsed_months = (
            (date.year - last_donation.year)*12
            + (date.month - last_donation.month)
            )

        return elapsed_months
