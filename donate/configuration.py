"""Configuration parsing."""
from yaml import load

_required_keys = ["total_donation", "split", "donees"]


def parse_config(yaml_string):
    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import Loader

    config = load(yaml_string, Loader)

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
        pass

    return config


class ConfigurationError(Exception):
    def __init__(self, message):
        super().__init__(message)
