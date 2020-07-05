from .configuration import parse_config
from .ledger import update_ledger
from .maths import single_donation
from .schedule import AdHoc
import argparse
from datetime import datetime
from xdg import BaseDirectory


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
        help="Specify a path to a non-default configuration file."
        )
    parser.add_argument(
        "-d", "--dry-run",
        action="store_true",
        help=(
            "Generate sample donations but don't commit them to the donations"
            " ledger or update the last donation time."
            )
        )

    # Get command line argumnets
    args = parser.parse_args()

    # Get XDG configuration path
    # This function has side effects; it ensures that the path exists
    config_path = BaseDirectory.save_config_path("donate")

    # Locate configuration file
    if args.config:
        config_file_path = args.config
    else:
        config_file_path = config_path + "/config.yml"

    # Parse configuration file
    with open(config_file_path, "r") as config_file:
        config = parse_config(config_file)
    donees = config["donees"]
    total_donation = config["total_donation"]
    split = config["split"]
    currency_symbol = config["currency_symbol"]
    decimal_currency = config["decimal_currency"]
    schedule = config["schedule"]

    # Read last donation
    last_donation_file_path = config_path + "/last_donation"
    try:
        with open(last_donation_file_path) as last_donation_file:
            last_donation = datetime.fromisoformat(
                    last_donation_file.read().strip()
                    )
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

    # Write record of donation date and update ledger
    if not args.dry_run:
        with open(last_donation_file_path, "w") as last_donation_file:
            last_donation_file.write(datetime.today().isoformat()+"\n")

        update_ledger(individual_donations, decimal_currency)


if __name__ == "__main__":
    main()
