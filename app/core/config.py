from secrets import token_urlsafe
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, validator


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

    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return "sqlite:///./perseus.db.sqlite3"

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
