"""Configuration parsing."""
from .donee import Donee, Type
from .schedule import AdHoc, Monthly
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

_schedule_map = {
    "ad hoc": AdHoc,
    "monthly": Monthly
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

    # Ensure decimal currency is a boolean value if present
    try:
        if type(config["decimal_currency"]) is not bool:
            raise ConfigurationError("'decimal_currency' must be a boolean")
    except KeyError:
        config["decimal_currency"] = False

    # Set currency if one is not declared symbol
    if "currency_symbol" not in keys:
        config["currency_symbol"] = "£"

    # Set schedule
    if "schedule" not in keys:
        config["schedule"] = AdHoc()
    else:
        if config["schedule"] not in _schedule_map.keys():
            raise ConfigurationError(
                f"Schedule must be one of '{', '.join(_schedule_map.keys())}'"
                )

        config["schedule"] = _schedule_map[config["schedule"]]()

    # Ensure donees is a list
    if type(config["donees"]) is not list:
        raise ConfigurationError("Donees must be a list")

    # Ensure weights are numbers if declared
    if "weights" in keys:
        weight_dict = config["weights"]
        for name, value in weight_dict.items():
            if type(value) not in [int, float]:
                raise ConfigurationError(
                    f"Weight '{name}' value '{value}' is not a real number."
                    )
            elif value < 0:
                raise ConfigurationError(
                    f"Weight '{name}' value '{value}' is negative."
                    )
    else:
        weight_dict = None

    # Process donees
    donees = []
    for donee_dict in config["donees"]:
        donees.append(_parse_donee(donee_dict, weight_dict))
    config["donees"] = donees

    return config


def _parse_donee(donee_dict, weight_dict):
    # Process weight argument
    weight = donee_dict["weight"]
    if (weight_type := type(weight)) is str:
        # If weight is a string, ensure weight keywords have been declared
        if weight_dict is None:
            raise ConfigurationError(
                f"The weight of donee '{donee_dict['name']}' is a string, but"
                " no weights have been defined."
                )

        try:
            weight = weight_dict[weight]
        except KeyError:
            raise ConfigurationError(
                f"Weight '{weight}' of donee '{donee_dict['name']}' not"
                " defined"
                )
    elif weight_type is int:
        weight = float(weight)
    elif weight_type is float:
        weight = weight

    return Donee(
        name=donee_dict["name"],
        weight=weight,
        donee_type=_type_map[donee_dict["type"].lower()],
        donation_url=donee_dict["url"]
        )


class ConfigurationError(Exception):
    def __init__(self, message):
        super().__init__(message)
