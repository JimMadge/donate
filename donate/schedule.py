from datetime import datetime


class Schedule(object):
    """Schedule base class."""

    def due_donations(self, last_donation):
        """
        Calculate how many donations are due based on the date of the last
        donation.
        """
        raise NotImplementedError


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
