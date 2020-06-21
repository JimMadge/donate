"""Configuration parsing."""
from .donee import Donee, Type, Weight
from yaml import load

_required_keys = ["total_donation", "split", "donees"]

_type_map = {
    "software": Type.SOFTWARE,
    "distribution": Type.DISTRIBUTION,
    "service": Type.SERVICE,
    "podcast": Type.PODCAST,
    "organisation": Type.ORGANISATION,
    "charity": Type.CHARITY,
    "other": Type.OTHER
    }

_weight_map = {
    "critical": Weight.CRITICAL,
    "large": Weight.LARGE,
    "medium": Weight.MEDIUM,
    "small": Weight.SMALL
    }


def parse_config(config_yaml):
    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import Loader

    config = load(config_yaml, Loader)

    keys = config.keys()

    # Check required keys
    for key in _required_keys:
        if key not in keys:
            raise ConfigurationError(f"Required key '{key}' not declared")

    # Ensure donees is a list
    if type(config["donees"]) is not list:
        raise ConfigurationError("Donees must be a list")

    # Ensure decimal currency is a boolean value if present
    try:
        if type(config["decimal_currency"]) is not bool:
            raise ConfigurationError("'decimal_currency' must be a boolean")
    except KeyError:
        config["decimal_currency"] = False

    # Set currency if one is not declared symbol
    if "currency_symbol" not in keys:
        config["currency_symbol"] = "£"

    # Process donees
    donees = []
    for donee_dict in config["donees"]:
        donees.append(_parse_donee(donee_dict))
    config["donees"] = donees

    return config


def _parse_donee(donee_dict):
    return Donee(
        name=donee_dict["name"],
        weight=_weight_map[donee_dict["weight"].lower()],
        donee_type=_type_map[donee_dict["type"].lower()],
        donation_url=donee_dict["url"]
        )


class ConfigurationError(Exception):
    def __init__(self, message):
        super().__init__(message)
