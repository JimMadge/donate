from .configuration import Configuration
from .donee import Donee
from .ledger import Ledger
from .maths import split_decimal, single_donation, means_summary
from .schedule import (schedule_map, Schedule, AdHoc, get_last_donation,
                       update_last_donation)
from json import dumps as json_dumps
from pathlib import Path
from tabulate import tabulate
import typer
from typing import Optional
from yaml import dump as yaml_dump


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
    config = Configuration.from_file(config_path)

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
    ledger = Ledger()
    ledger.append(individual_donations, config.currency_symbol,
                  config.decimal_currency)


@app.command(
    help=("Print the mean donation received by each donee and donee category"
          " from a total donation of MEANS")
)
def means(
    total_donation: int = typer.Argument(..., help="total donation"),
    config_path: Optional[Path] = config_path_option
) -> None:
    config = Configuration.from_file(config_path)

    typer.echo(
        means_summary(config.donees, total_donation, config.currency_symbol)
    )
    typer.Exit()


@app.command(
    help=("Print the donation history from the donation ledger")
)
def ledger(
    json: bool = typer.Option(
        False,
        "--json",
        help="Print history in JSON format"
    ),
    yaml: bool = typer.Option(
        False,
        "--yaml",
        help="Print history in YAML format"
    )
) -> None:
    ledger = Ledger()

    entries = ledger[:]

    if json:
        typer.echo(
            json_dumps(entries, indent=4, ensure_ascii=False, default=str)
        )
    elif yaml:
        typer.echo(
            yaml_dump(entries, default_flow_style=False, allow_unicode=True,
                      canonical=False)
        )
    else:
        if isinstance(entries, list):
            typer.echo(tabulate(entries))
        elif isinstance(entries, tuple):
            typer.echo(tabulate([entries]))


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
