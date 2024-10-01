import os
from dataclasses import dataclass, field

from adaptix import Retort
from dynaconf import Dynaconf
from sqlalchemy_utils import database_exists, create_database


@dataclass(slots=True)
class ApiConfig:
    host: str
    port: int
    debug: bool = True
    workers: int = 1
    cors_origin_regex: str = r'https://'
    allow_origins: list[str] = field(default_factory=list)
    allow_headers: list[str] = field(default_factory=list)
    allow_methods: list[str] = field(default_factory=list)
    allow_credentials: bool = True

    project_name: str = 'wmate'
    project_path: str = field(
        default_factory=lambda: os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..')
        )
    )

    default_pagination_limit: int = 10


@dataclass(slots=True)
class DatabaseConfig:
    host: str
    port: int
    username: str
    password: str
    database: str
    driver: str = 'postgresql+asyncpg'
    migrate: str = 'postgresql'

    @property
    def dsn(self) -> str:
        return f'{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'

    @property
    def migrate_dsn(self) -> str:
        url = f'{self.migrate}://{self.username}:{self.password}@localhost:{self.port}/{self.database}'
        if not database_exists(url):
            create_database(url)
        return url


@dataclass(slots=True)
class LoggingConfig:
    level: str
    human_readable_logs: bool = True


@dataclass(slots=True)
class Config:
    database: DatabaseConfig
    logging: LoggingConfig
    api: ApiConfig


def get_config() -> Config:
    dynaconf = Dynaconf(
        envvar_prefix='WMATE',
        settings_file=[os.getenv('CONFIG_PATH')],
        load_dotenv=True,
    )
    retort = Retort()

    return retort.load(dynaconf, Config)
