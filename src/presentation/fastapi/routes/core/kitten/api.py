from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.application.schema.KittenTable import KittenTableSchema, UpdateKittenTableSchema
from src.infra.postgres.gateways.kittens import KittensGateway

ROUTER = APIRouter(route_class=DishkaRoute)


@ROUTER.get("")
async def get_kittens(kittens_gateway: FromDishka[KittensGateway]) -> list[KittenTableSchema]:
    return await kittens_gateway.get_kittens()


@ROUTER.get("/{kitten_id}", response_model=KittenTableSchema, status_code=status.HTTP_200_OK)
async def get_kitten(kittens_gateway: FromDishka[KittensGateway],
                     session: FromDishka[AsyncSession],
                     kitten_id: int) -> KittenTableSchema:
    async with session.begin():
        return await kittens_gateway.get_kitten_by_id(kitten_id)


@ROUTER.get("/by_breed/{breed}", response_model=list[KittenTableSchema], status_code=status.HTTP_200_OK)
async def get_kitten_by_breed(kittens_gateway: FromDishka[KittensGateway],
                              breed: str) -> list[KittenTableSchema]:
    return await kittens_gateway.get_kitten_by_breed(breed)


@ROUTER.post("")
async def create_kitten(kittens_gateway: FromDishka[KittensGateway],
                        session: FromDishka[AsyncSession],
                        breed_id: PositiveInt,
                        color: str,
                        age: int,
                        description: str) -> KittenTableSchema:
    async with session.begin():
        return await kittens_gateway.create_kitten(breed_id, color, age, description)


@ROUTER.patch("/{kitten_id}", response_model=KittenTableSchema, status_code=status.HTTP_200_OK)
async def update_kitten(kittens_gateway: FromDishka[KittensGateway],
                        session: FromDishka[AsyncSession],
                        kitten_id: int,
                        data: UpdateKittenTableSchema) -> KittenTableSchema:
    async with session.begin():
        return await kittens_gateway.update_kitten(kitten_id, data)


@ROUTER.delete("/{kitten_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_kitten(kittens_gateway: FromDishka[KittensGateway],
                        session: FromDishka[AsyncSession],
                        kitten_id: int):
    async with session.begin():
        return await kittens_gateway.delete_by_id(kitten_id)
