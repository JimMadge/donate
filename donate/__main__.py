from .configuration import parse_config
from .maths import single_donation
from .schedule import AdHoc
import argparse
from datetime import datetime

_last_donation_file = "last_donation"


def main():
    parser = argparse.ArgumentParser(
        description=("Generate donations to projects according to a"
                     " distribution you control")
        )

    # Declare command line arguments
    parser.add_argument(
        "-c", "--config",
        action="store",
        type=str,
        default="config.yml",
        help="Path to the configuration YAML file, default: './config.yml'"
        )
    parser.add_argument(
        "-d", "--dry-run",
        action="store_true",
        help=(
            "Generate sample donations but don't commit them to the donations"
            " record"
            )
        )

    # Get command line argumnets
    args = parser.parse_args()

    # Read configuration file
    with open(args.config, "r") as config_file:
        config = parse_config(config_file)
    donees = config["donees"]
    total_donation = config["total_donation"]
    split = config["split"]
    currency_symbol = config["currency_symbol"]
    decimal_currency = config["decimal_currency"]
    schedule = config["schedule"]

    # Read last donation
    try:
        with open(_last_donation_file) as date_file:
            last_donation = datetime.fromisoformat(date_file.read().strip())
    except FileNotFoundError:
        last_donation = None

    # Determine number of donations due
    if last_donation:
        due_donations = schedule.due_donations(last_donation)
    else:
        due_donations = 1

    if not isinstance(schedule, AdHoc):
        if due_donations == 0:
            print("No donations due")
            return
        else:
            print(f"{due_donations} donations due")

    # Get individual donations
    individual_donations = single_donation(
        donees,
        total_donation * due_donations,
        split * due_donations,
        decimal_currency
        )
    for donee, amount in individual_donations.items():
        if decimal_currency:
            whole = amount // 100
            hundreths = amount % 100
            amount = f"{whole}.{hundreths:02d}"
        print(f"{donee.name} -- {currency_symbol}{amount} -->"
              f" {donee.donation_url}")

    # Write record of donation date
    if not args.dry_run:
        with open(_last_donation_file, "w") as date_file:
            date_file.write(datetime.today().isoformat())


if __name__ == "__main__":
    main()
