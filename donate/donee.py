from pydantic import BaseModel, Field


class Donee(BaseModel):
    """Donee definition."""
    name: str
    weight: float = Field(gt=0.)
    category: str = "other"
    url: str

    def __hash__(self):
        return hash(self.name)
