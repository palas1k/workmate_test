from typing import Any

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.infra.postgres.utils import integer_id


class BaseDBModel(DeclarativeBase):
    __tablename__: Any
    __table_args__ = {'schema': 'base_schema'}


class Breed(BaseDBModel):
    __tablename__ = 'breeds'
    __table_args__ = {'schema': 'breeds_schema'},
    id: Mapped[integer_id]
    name: Mapped[str] = mapped_column(nullable=False)


class Kitten(BaseDBModel):
    __tablename__ = 'kittens'
    __table_args__ = {'schema': 'kittens_schema'},
    id: Mapped[integer_id]
    breed_id: Mapped[int] = mapped_column(ForeignKey('breeds_schema.breeds.id'))
    color: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
