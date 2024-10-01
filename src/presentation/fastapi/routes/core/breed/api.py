import logging

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.schema.BreedTable import BreedTableSchema
from src.infra.postgres.gateways.breeds import BreedsGateway

ROUTER = APIRouter(route_class=DishkaRoute)

logger = logging.getLogger(__name__)


@ROUTER.get("")
async def get_breeds(breeds_gateway: FromDishka[BreedsGateway]) -> list[BreedTableSchema]:
    return await breeds_gateway.get_breeds()


@ROUTER.post("")
async def create_breeds(breeds_gateway: FromDishka[BreedsGateway],
                        session: FromDishka[AsyncSession],
                        breed_name: str) -> BreedTableSchema:
    async with session.begin():
        return await breeds_gateway.create_breed(breed_name)
