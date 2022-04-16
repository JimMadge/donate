from .configuration import parse_config, Configuration
from .donee import Donee
from .logs import update_log
from .maths import split_decimal, single_donation, means_summary
from .schedule import (schedule_map, Schedule, AdHoc, get_last_donation,
                       update_last_donation)
from pathlib import Path
from tabulate import tabulate
import typer
from typing import Optional
from xdg import BaseDirectory  # type: ignore


app = typer.Typer()


config_path_option = typer.Option(
    None, "--config", "-c",
    help="Specify a path to a non-default configuration file."
)


@app.command(help="Generate a set of donations.")
def generate(
    config_path: Optional[Path] = config_path_option,
    ad_hoc: bool = typer.Option(
        False, "--ad-hoc", "-a",
        help=(
            "Make an ad hoc donation, i.e. ignore your donation schedule and"
            " last donation date. Useful in combination with '--dry-run' for"
            " testing."
        )
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", "-d",
        help=(
            "Generate sample donations but don't commit them to the donations"
            " ledger or update the last donation time."
        )
    )
) -> None:
    config = get_config(check_config_path(config_path))

    # Create instance of schedule object
    if ad_hoc:
        schedule: Schedule = AdHoc()
    else:
        schedule = schedule_map[config.schedule]()

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
        config.donees,
        config.total_donation * due_donations,
        config.split * due_donations,
        config.decimal_currency
    )
    print(format_donations(individual_donations, config.currency_symbol,
                           config.decimal_currency))

    # Return before updating any files if this is a dry run
    if dry_run:
        typer.Exit()

    # Record donation date
    update_last_donation()

    # Append donations to log
    update_log(individual_donations, config.currency_symbol,
               config.decimal_currency)


@app.command(
    help=("Print the mean donation received by each donee and donee category"
          " from a total donation of MEANS")
)
def means(
    total_donation: int = typer.Argument(..., help="total donation"),
    config_path: Optional[Path] = config_path_option
) -> None:
    config = get_config(check_config_path(config_path))

    typer.echo(
        means_summary(config.donees, total_donation, config.currency_symbol)
    )
    typer.Exit()


def get_config(config_path: Path) -> Configuration:
    with open(config_path, "r") as config_text:
        config = parse_config(config_text.read())
    return config


def check_config_path(path: Optional[Path]) -> Path:
    if path is None:
        try:
            path = (
                BaseDirectory.load_first_config("donate") + "/config.yaml"
            )
        except TypeError:
            print("No configuration file specified and no file at "
                  f"{BaseDirectory.xdg_config_home + '/config.yaml'}")
            typer.Exit()
            exit()  # mypy doesn't know typer.Exit() will terminate

    return path


def format_donations(donations: dict[Donee, int], currency_symbol: str,
                     decimal_currency: bool) -> str:
    table: list[tuple[str, str, str]] = []
    for donee, amount in donations.items():
        if decimal_currency:
            whole, hundreths = split_decimal(amount)
            amount_str: str = f"{whole}.{hundreths:02d}"
        else:
            amount_str = f"{amount}"

        amount_str = f"{currency_symbol}{amount_str}"
        table.append((donee.name, amount_str, donee.url))

    return tabulate(
        sorted(
            table,
            key=lambda item: float(item[1][1:]),  # type: ignore
            reverse=True)
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
