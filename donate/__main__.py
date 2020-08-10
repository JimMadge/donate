from .configuration import parse_config
from .ledger import update_ledger, ledger_stats
from .maths import single_donation, donee_means, category_means
from .schedule import AdHoc
import argparse
from datetime import datetime
from tabulate import tabulate
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
        "-a", "--ad-hoc",
        action="store_true",
        help=(
            "Make an ad hoc donation, i.e. ignore your donation schedule and"
            " last donation date. Useful in combination with '--dry-run' for"
            " testing."
            )
        )
    parser.add_argument(
        "-d", "--dry-run",
        action="store_true",
        help=(
            "Generate sample donations but don't commit them to the donations"
            " ledger or update the last donation time."
            )
        )
    parser.add_argument(
        "-s", "--stats",
        action="store_true",
        help="Print some statistics about previous donations."
        )
    parser.add_argument(
        "-m", "--means",
        action="store",
        type=int,
        help=(
            "Print the mean donation recieved by each donee and donee category"
            " from a total donation of MEANS"
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

    # If the stats option has been declared, print statistics and exit
    if args.stats:
        print(ledger_stats(currency_symbol))
        return

    # If the means option has been declared, print means and exit
    if args.means:
        print_means(donees, args.means, currency_symbol)
        return

    # Read last donation
    if args.ad_hoc:
        last_donation = None
    else:
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
        if not args.ad_hoc:
            with open(last_donation_file_path, "w") as last_donation_file:
                last_donation_file.write(datetime.today().isoformat()+"\n")

        update_ledger(individual_donations, decimal_currency)


def print_means(donees, total_donation, currency_symbol):
    print(f"Mean donations from {currency_symbol}{total_donation}")
    print(tabulate(
        donee_means(donees, total_donation),
        headers=["Donee", "Mean donation"]
        ))
    print("\n")
    print(tabulate(
        category_means(donees, total_donation).items(),
        headers=["Category", "Mean donation"]
        ))


if __name__ == "__main__":
    main()
