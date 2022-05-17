import pytest
from httpx import AsyncClient

from app.core.config import settings
from app.main import app


@pytest.mark.anyio
async def test_all_returns_http_x_headers_correctly() -> None:
    page = 1

    async with AsyncClient(app=app, base_url="https://test") as client:
        response = await client.get(
            f"{settings.API_V1_STR}/bodies/{page}",
            headers={"Host": "perseus.docker.localhost"},
        )

        assert response.headers["x-perseus-api-version"] == str(settings.API_VERSION)
        assert response.status_code == 200
