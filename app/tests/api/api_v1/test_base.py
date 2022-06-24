import pytest
from httpx import AsyncClient

from app.core.config import settings
from app.main import API_DESCRIPTION


@pytest.mark.asyncio
async def test_base_index_route_returns_http_redirect_status(
    client: AsyncClient,
) -> None:
    response = await client.get(
        "/",
        headers={"Host": "perseus.docker.localhost"},
    )

    assert response.status_code in [301, 302, 307]


@pytest.mark.asyncio
async def test_base_api_v1_route_returns_http_ok_status(
    client: AsyncClient,
) -> None:
    response = await client.get(
        f"{settings.API_V1_STR}",
        headers={"Host": "perseus.docker.localhost"},
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_base_api_v1_route_returns_correct_json_body(
    client: AsyncClient,
) -> None:
    response = await client.get(
        f"{settings.API_V1_STR}",
        headers={"Host": "perseus.docker.localhost"},
    )

    assert response.status_code == 200

    body = response.json()

    assert body["description"] == API_DESCRIPTION
    assert body["endpoint"] == f"{settings.API_V1_STR}"
    assert body["name"] == "Perseus Billion Stars API by observerly"
