from secrets import token_urlsafe
from typing import Any, Dict, List, Literal, Optional, Union
from urllib.parse import urlparse

from pydantic import AnyHttpUrl, AnyUrl, BaseSettings, EmailStr, HttpUrl, validator


class MySQLDsn(AnyUrl):
    allowed_schemes = [
        "mysql",
        "mysql+mysqlconnector",
        "mysql+aiomysql",
        "mysql+asyncmy",
        "mysql+mysqldb",
        "mysql+pymysql",
        "mysql+cymysql",
        "mysql+pyodbc",
    ]
    default_port = 3306


class Settings(BaseSettings):
    # API version 1 base URL, e.g., "https://perseus.observerly.com/api/v1"
    API_V1_STR: str = "/api/v1"

    API_VERSION: str = "v1.0.0@latest (2022-06-24)"

    SECRET_KEY: str = token_urlsafe(64)

    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl

    PROJECT_NAME: str

    PROJECT_ENVIRONMENT: str = "development"

    HTTPS_REDIRECT: bool = False

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:3000", \
    # "http://localhost:8080", "https://api.observerly.com"], \
    # "https://perseus.observerly.com]"':
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl | Literal["*"]] = ["*"]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str = "db"
    MYSQL_PORT: str = "3306"
    MYSQL_DATABASE: str
    MYSQL_INSTANCE_CONNECTION_NAME: str
    MYSQL_PRIVATE_IP: Optional[bool] = False

    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return MySQLDsn.build(
            scheme="mysql+pymysql",
            user=values.get("MYSQL_USER"),
            password=values.get("MYSQL_PASSWORD"),
            host=values.get("MYSQL_HOST"),
            port=values.get("MYSQL_PORT"),
            path=f"/{values.get('MYSQL_DATABASE') or ''}",
        )

    USE_CLOUD_SQL: Optional[bool] = False

    CLOUDRUN_SERVICE_URL: Optional[str] = None

    @validator("CLOUDRUN_SERVICE_URL", pre=True)
    def assemble_cloudrun_service_url(cls, v: Optional[str]) -> Optional[str]:
        if isinstance(v, str):
            return urlparse(v).netloc
        return None

    REDIS_DSN: Optional[str] = None

    @validator("REDIS_DSN", pre=True)
    def assemble_redis_dsn(cls, v: str, values: Dict[str, Any]) -> str:
        if isinstance(v, str):
            return v
        return "redis://redis"

    SENTRY_DSN: Optional[HttpUrl]

    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
        if len(v) == 0:
            return None
        return v

    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
