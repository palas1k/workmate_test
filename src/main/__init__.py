from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from fastapi import FastAPI

from src.config import Config, get_config
from src.main.di import DishkaProvider
from src.main.web import setup_fastapi

config: Config = get_config()


def app() -> FastAPI():
    container = make_async_container(DishkaProvider(config=config))
    fastapi = setup_fastapi(config.api)
    setup_dishka_fastapi(container, fastapi)

    return fastapi
