from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.config import ApiConfig
from src.presentation.fastapi.setup import setup_routes


def setup_fastapi(config:ApiConfig) -> FastAPI:
    app = FastAPI(title=config.project_name, debu=config.debug)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.allow_origins,
        allow_credentials=config.allow_credentials,
        allow_methods=config.allow_methods,
        allow_headers=config.allow_headers,
        expose_headers=['Content-Range'],
    )
    setup_routes(app)

    return app
