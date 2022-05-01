from .donee import Donee
from .schedule import schedule_map
from typing import Any, KeysView, Optional, Type, TypeVar
from pathlib import Path
from pydantic import BaseModel, Field, validator
from yaml import load
from xdg import BaseDirectory  # type: ignore


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


T = TypeVar("T", bound="Configuration")


class Configuration(BaseModel):
    total_donation: int = Field(gt=0)
    split: int = Field(gt=0)

    currency_symbol: str = Field("£", min_length=1, max_length=1)
    decimal_currency: bool = False

    schedule: str = "ad hoc"

    donees: list[Donee]

    @validator("schedule")
    def schedule_exists(cls, v: str) -> str:
        if v not in schedule_map.keys():
            raise ValueError(f"Schedule '{v}' is not valid")
        return v

    @staticmethod
    def xdg_config_path() -> Path:
        if directory := BaseDirectory.load_first_config("donate"):
            return Path(directory) / "config.yaml"
        else:
            raise FileNotFoundError("No configuration found")

    @classmethod
    def from_file(cls: Type[T], config_path: Optional[Path]) -> T:
        if not config_path:
            config_path = cls.xdg_config_path()

        with open(config_path, "r") as config_file:
            config = config_file.read()

        return cls.from_str(config)

    @classmethod
    def from_str(cls: Type[T], config: str) -> T:
        try:
            from yaml import CLoader as Loader
        except ImportError:
            from yaml import Loader  # type: ignore

        return cls.from_dict(load(config, Loader))

    @classmethod
    def from_dict(cls: Type[T], config: dict[str, Any]) -> T:
        weights = Weights(weights=config["weights"])

        # Convert named weights to their numerical value
        for donee in config["donees"]:
            if isinstance(donee["weight"], str):
                weight_string = donee["weight"]

                # Ensure weight has been declared
                if weight_string not in weights.keys():
                    raise ValueError(
                        f"Weight '{weight_string}' of donee '{donee['name']}'"
                        " not defined"
                    )

                donee["weight"] = weights[weight_string]

        return cls(**config)
