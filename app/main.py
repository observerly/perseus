import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import ORJSONResponse, RedirectResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.coder import PickleCoder
from redis import asyncio as aioredis
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

app.router.redirect_slashes = True

ALLOWED_HOSTS = ["*"]

if settings.CLOUDRUN_SERVICE_URL:
    ALLOWED_HOSTS.append(settings.CLOUDRUN_SERVICE_URL)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=ALLOWED_HOSTS,
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
    response = RedirectResponse(url="{0}".format(settings.API_V1_STR), status_code=302)
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


@app.middleware("http")
async def add_helmet_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Strict-Transport-Security"] = "max-age=5184000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Download-Options"] = "noopen"
    response.headers["X-DNS-Prefetch-Control"] = "off"
    response.headers["X-Frame-Options"] = "Deny"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response


@app.on_event("startup")
async def startup():
    if settings.REDIS_DSN:
        redis = aioredis.from_url(
            settings.REDIS_DSN, encoding="utf8", decode_responses=True
        )
        FastAPICache.init(
            RedisBackend(redis),
            prefix="perseus-cache",
            expire=31556952,
            coder=PickleCoder,
        )
