from asyncio import get_event_loop
from typing import Generator

import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from app.db.session import SessionLocal
from app.main import app


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
async def client() -> Generator:
    async with AsyncClient(app=app, base_url="https://test") as client, LifespanManager(
        app
    ):
        yield client


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = get_event_loop()
    yield loop
    loop.close()
