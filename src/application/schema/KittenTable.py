from dataclasses import dataclass


@dataclass(slots=True)
class KittenTableSchema:
    breed_id: int
    color: str
    age: int
    description: str


@dataclass(slots=True)
class UpdateKittenTableSchema:
    breed_id: int | None = None
    color: str | None = None
    age: int | None = None
    description: str | None = None
