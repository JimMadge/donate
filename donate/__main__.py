from .configuration import parse_config
from .ledger import update_ledger, ledger_stats
from .logs import update_log
from .maths import single_donation, means_summary
from .schedule import AdHoc, get_last_donation, update_last_donation
import argparse
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
        config_file_path = config_path + "/config.yaml"

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
        print(means_summary(donees, args.means, currency_symbol))
        return

    # Determine number of donations due
    due_donations = schedule.due_donations(get_last_donation())

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

    # Return before updating any files if this is a dry run
    if args.dry_run:
        return

    # Record donation date
    update_last_donation()

    # Append donations to log
    update_log(individual_donations, currency_symbol, decimal_currency)

    # Update ledger
    update_ledger(individual_donations, decimal_currency)


if __name__ == "__main__":
    main()
