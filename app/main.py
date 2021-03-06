import aioredis
import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import ORJSONResponse, RedirectResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings

API_DESCRIPTION = "\
Perseus Billion Stars API is observerly's Fast API \
of stars, galaxies and other astronomical bodies, \
adhering to the OpenAAS standard.\
"

API_NAME = "Perseus Billion Stars API by observerly"

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    default_response_class=ORJSONResponse,
)

app.router.redirect_slashes = False

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "perseus.docker.localhost",
        settings.SERVER_HOST,
        "observerly.com",
        "*.observerly.com",
        "0.0.0.0",
    ],
)

if settings.HTTPS_REDIRECT:
    app.add_middleware(HTTPSRedirectMiddleware)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if settings.PROJECT_ENVIRONMENT == "production":
    sentry_sdk.init(
        settings.SENTRY_DSN,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
    )
    app.add_middleware(SentryAsgiMiddleware)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def redirect_index():
    response = RedirectResponse(url="{0}".format(settings.API_V1_STR))
    return response


@app.get("{0}".format(settings.API_V1_STR))
async def api_v1_base():
    return {
        "description": API_DESCRIPTION,
        "endpoint": "{0}".format(settings.API_V1_STR),
        "name": API_NAME,
    }


@app.middleware("http")
async def add_custom_x_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Perseus-API-Version"] = str(settings.API_VERSION)
    return response


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://redis", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="perseus-cache")
