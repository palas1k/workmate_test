from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi import FastAPI

from src.presentation.fastapi.exception_handlers import setup_exception_handlers
from src.presentation.fastapi.routes.core.breed.api import ROUTER as BREED_ROUTER
from src.presentation.fastapi.routes.core.kitten.api import ROUTER as KITTEN_ROUTER


def setup_routes(app: FastAPI) -> None:
    """Установка всех роутеров."""
    router = APIRouter(prefix='/api', route_class=DishkaRoute)

    router.include_router(router=BREED_ROUTER, prefix='/breed', tags=['Breed'])
    router.include_router(router=KITTEN_ROUTER, prefix='/kitten', tags=['Kitten'])

    app.include_router(router)
    setup_exception_handlers(app)
