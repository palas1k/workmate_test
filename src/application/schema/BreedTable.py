from dataclasses import dataclass


@dataclass(slots=True)
class BreedTableSchema:
    name: str | None
