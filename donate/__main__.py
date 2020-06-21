from .configuration import parse_config
from .maths import single_donation
import argparse


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

    # Get individual donations
    individual_donations = single_donation(donees, total_donation, split,
                                           decimal_currency)
    for donee, amount in individual_donations.items():
        if decimal_currency:
            whole = amount // 100
            hundreths = amount % 100
            amount = f"{whole}.{hundreths:02d}"
        print(f"{donee.name} -- {currency_symbol}{amount} -->"
              f" {donee.donation_url}")


if __name__ == "__main__":
    main()
