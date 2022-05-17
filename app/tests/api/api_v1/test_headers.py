import pytest
from httpx import AsyncClient

from app.core.config import settings


@pytest.mark.asyncio
async def test_all_returns_http_x_headers_correctly(client: AsyncClient) -> None:
    page = 1

    response = await client.get(
        f"{settings.API_V1_STR}/bodies/{page}",
        headers={"Host": "perseus.docker.localhost"},
    )

    assert response.headers["x-perseus-api-version"] == str(settings.API_VERSION)
    assert response.status_code == 200
