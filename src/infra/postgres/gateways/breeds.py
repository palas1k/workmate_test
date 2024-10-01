import logging

from adaptix import Retort
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.schema.BreedTable import BreedTableSchema
from src.infra.postgres.gateways.base import BasePostgresGateway
from src.infra.postgres.tables import Breed

logger = logging.getLogger(__name__)


class BreedsGateway(BasePostgresGateway):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            retort=Retort(),
            session=session,
            table=Breed,
        )

    async def get_breeds(self) -> list[BreedTableSchema]:
        stmt = (
            select(Breed)
            .with_only_columns(Breed.name)
        )

        result = (await self.session.execute(stmt)).mappings().fetchall()
        return self.retort.load(result, list[BreedTableSchema]) if len(result) > 0 else []

    async def create_breed(self, breed_name: str) -> BreedTableSchema:
        stmt = (
            insert(Breed)
            .values(name=breed_name)
            .returning(Breed.name)
        )
        result = (await self.session.execute(stmt)).mappings().first()
        return self.retort.load(result, BreedTableSchema)
