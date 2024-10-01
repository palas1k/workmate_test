from adaptix import Retort
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.errors import DatabaseError
from src.infra.postgres.tables import BaseDBModel


class BasePostgresGateway:
    def __init__(self, retort: Retort, session: AsyncSession, table: type[BaseDBModel]) -> None:
        self.retort = retort
        self.session = session
        self.table = table

    async def delete_by_id(self, entity_id: int | str) -> int | str:
        stmt = delete(self.table).where(self.table.id == int(entity_id))

        try:
            result = await self.session.execute(stmt)
            if result.rowcount != 1:
                raise f"{str(DatabaseError)} {self.table} not found!"
            return entity_id
        except DatabaseError as e:
            raise e