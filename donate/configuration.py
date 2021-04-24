from .donee import Donee
from .schedule import schedule_map
from typing import Optional, Any, KeysView
from pydantic import BaseModel, Field, validator
from yaml import load


class Weights(BaseModel):
    weights: dict[str, float] = {}

    @validator("weights", each_item=True)
    def ensure_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Weights must be positive")
        return v

    def __getitem__(self, key: str) -> float:
        return self.weights[key]

    def keys(self) -> KeysView[str]:
        return self.weights.keys()


class Configuration(BaseModel):
    total_donation: int = Field(gt=0)
    split: int = Field(gt=0)

    currency_symbol: str = Field("£", min_length=1, max_length=1)
    decimal_currency: bool = False

    schedule: str = "ad hoc"

    donees: Optional[list[Donee]] = None

    @validator("schedule")
    def schedule_exists(cls, v: str) -> str:
        if v not in schedule_map.keys():
            raise ValueError(f"Schedule '{v}' is not valid")
        return v


def parse_config(config: str) -> Configuration:
    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import Loader  # type: ignore

    config_dict = load(config, Loader)
    return parse_config_dict(config_dict)


def parse_config_dict(config: dict[str, Any]) -> Configuration:
    weights = Weights(weights=config["weights"])

    # Convert named weights to their numerical value
    for donee in config["donees"]:
        if isinstance(donee["weight"], str):
            weight_string = donee["weight"]
            assert weight_string in weights.keys()
            donee["weight"] = weights[weight_string]

    configuration = Configuration(**config)

    return configuration
