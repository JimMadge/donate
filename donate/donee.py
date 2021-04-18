from pydantic import BaseModel, Field


class Donee(BaseModel):
    name: str
    weight: float = Field(gt=0.)
    url: str
    category: str = "other"
