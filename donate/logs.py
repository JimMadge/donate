from csv import writer
from datetime import date
from pathlib import Path
from xdg import BaseDirectory


def update_log(donations, currency_symbol, decimal_currency):
    data_path = Path(BaseDirectory.save_data_path("donate"))
    log_path = data_path / "donation_log.csv"

    with open(log_path, "a", newline="") as csvfile:
        log_writer = writer(csvfile)

        donation_date = date.today().isoformat()

        for donee, amount in donations.items():
            if decimal_currency:
                amount /= 100

            log_writer.writerow(
                [donation_date, donee.name, currency_symbol, amount]
            )
