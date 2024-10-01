import logging
from dataclasses import asdict

from adaptix import Retort
from fastapi.logger import logger
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.errors import DatabaseError, NotFoundError
from src.application.schema.KittenTable import KittenTableSchema, UpdateKittenTableSchema
from src.infra.postgres.gateways.base import BasePostgresGateway
from src.infra.postgres.tables import Kitten, Breed

class KittensGateway(BasePostgresGateway):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            retort=Retort(),
            session=session,
            table=Kitten,
        )

    async def get_kittens(self) -> list[KittenTableSchema]:
        stmt = (
            select(Kitten)
            .with_only_columns(Kitten.breed_id,
                               Kitten.age,
                               Kitten.color,
                               Kitten.description)
        )

        result = (await self.session.execute(stmt)).mappings().fetchall()

        return self.retort.load(result, list[KittenTableSchema]) if len(result) > 0 else []

    async def get_kitten_by_breed(self, breed_name: str) -> list[KittenTableSchema]:
        stmt = (
            select(Kitten)
            .join(Breed).filter(Breed.name == breed_name)
            .with_only_columns(Kitten.breed_id,
                               Kitten.age,
                               Kitten.color,
                               Kitten.description)
        )

        result = (await self.session.execute(stmt)).mappings().fetchall()

        return self.retort.load(result, list[KittenTableSchema]) if len(result) > 0 else []

    async def get_kitten_by_id(self, kitten_id: int) -> KittenTableSchema:
        stmt = (
            select(Kitten)
            .where(Kitten.id == kitten_id)
            .with_only_columns(Kitten.breed_id,
                               Kitten.age,
                               Kitten.color,
                               Kitten.description)
        )
        try:
            result = (await self.session.execute(stmt)).mappings().first()
            if result is None:
                raise NotFoundError('kitten')
            return self.retort.load(result, KittenTableSchema)
        except DatabaseError as e:
            raise DatabaseError(str(e))

    async def create_kitten(self, breed_id: int, color: str, age: int, description: str) -> KittenTableSchema:
        stmt = (
            insert(Kitten)
            .values(breed_id=breed_id,
                    color=color,
                    age=age,
                    description=description)
            .returning(Kitten.breed_id,
                       Kitten.color,
                       Kitten.age,
                       Kitten.description)

        )

        try:
            result = (await self.session.execute(stmt)).mappings().first()
            return self.retort.load(result, KittenTableSchema)
        except DatabaseError as e:
            raise DatabaseError(str(e))

    async def update_kitten(self, kitten_id: int, data: UpdateKittenTableSchema) -> KittenTableSchema:
        dict_data = asdict(data, dict_factory=lambda x: {k: v for (k, v) in x if v is not None})
        stmt = (
            update(Kitten)
            .values(dict_data)
            .where(Kitten.id == kitten_id)
            .returning(Kitten.breed_id,
                       Kitten.color,
                       Kitten.age,
                       Kitten.description)
        )

        try:
            result = (await self.session.execute(stmt)).mappings().first()
            if result is None:
                raise NotFoundError('kitten')
            return self.retort.load(result, KittenTableSchema)
        except DatabaseError as e:
            raise DatabaseError(str(e))
