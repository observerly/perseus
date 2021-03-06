import pytest
from httpx import AsyncClient

from app.core.config import settings


@pytest.mark.asyncio
async def test_list_bodies_returns_http_ok_status(client: AsyncClient) -> None:
    page = 1

    response = await client.get(
        f"{settings.API_V1_STR}/bodies/{page}",
        headers={"Host": "perseus.docker.localhost"},
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_list_bodies_without_any_query_params(client: AsyncClient) -> None:
    page = 1

    response = await client.get(
        f"{settings.API_V1_STR}/bodies/{page}",
        headers={"Host": "perseus.docker.localhost"},
    )

    assert response.status_code == 200

    body = response.json()

    assert body["count"] == 3767
    assert "/api/v1/bodies/2?limit=20" in body["next_page"]
    assert body["previous_page"] is None
    assert len(body["results"]) == 20


@pytest.mark.asyncio
async def test_list_bodies_with_default_radial_search(client: AsyncClient) -> None:
    page = 1

    response = await client.get(
        f"{settings.API_V1_STR}/bodies/{page}?ra=2.294522&dec=59.14978",
        headers={"Host": "perseus.docker.localhost"},
    )

    assert response.status_code == 200

    body = response.json()

    assert body["count"] == 11
    assert body["next_page"] is None
    assert body["previous_page"] is None

    assert body["results"][0]["name"] == "α Cassiopeiae"
    assert body["results"][1]["name"] == "β Cassiopeiae"
    assert body["results"][2]["name"] == "ζ Cassiopeiae"


@pytest.mark.asyncio
async def test_list_bodies_with_the_name_betelgeuse(client: AsyncClient) -> None:
    page = 1

    response = await client.get(
        f"{settings.API_V1_STR}/bodies/{page}?name=betelgeuse",
        headers={"Host": "perseus.docker.localhost"},
    )

    assert response.status_code == 200

    body = response.json()

    assert body["count"] == 1
    assert body["next_page"] is None
    assert body["previous_page"] is None

    assert body["results"][0]["name"] == "α Orionis"
    assert body["results"][0]["iau"] == "Betelgeuse"


@pytest.mark.asyncio
async def test_list_bodies_with_specific_radial_search(client: AsyncClient) -> None:
    page = 1

    response = await client.get(
        f"{settings.API_V1_STR}/bodies/{page}?ra=2.294522&dec=59.14978&radius=1.0",
        headers={"Host": "perseus.docker.localhost"},
    )

    assert response.status_code == 200

    body = response.json()

    assert body["count"] == 1
    assert body["next_page"] is None
    assert body["previous_page"] is None
    assert body["results"][0]["name"] == "β Cassiopeiae"


@pytest.mark.asyncio
async def test_list_bodies_with_slightly_less_specific_radial_search(
    client: AsyncClient,
) -> None:
    page = 1

    response = await client.get(
        f"{settings.API_V1_STR}/bodies/{page}?ra=2.294522&dec=59.14978&radius=10.0",
        headers={"Host": "perseus.docker.localhost"},
    )

    assert response.status_code == 200

    body = response.json()

    assert body["count"] == 11
    assert body["next_page"] is None
    assert body["previous_page"] is None

    assert body["results"][0]["name"] == "α Cassiopeiae"
    assert body["results"][1]["name"] == "β Cassiopeiae"
    assert body["results"][2]["name"] == "ζ Cassiopeiae"


@pytest.mark.asyncio
async def test_list_bodies_with_too_specific_radial_search(client: AsyncClient) -> None:
    page = 1

    response = await client.get(
        f"{settings.API_V1_STR}/bodies/{page}?ra=180&dec=45&radius=0.1",
        headers={"Host": "perseus.docker.localhost"},
    )

    assert response.status_code == 200

    body = response.json()

    assert body["count"] == 0
    assert body["next_page"] is None
    assert body["previous_page"] is None
    assert len(body["results"]) == 0


@pytest.mark.asyncio
async def test_list_bodies_within_the_constellation_orion(client: AsyncClient) -> None:
    page = 1

    response = await client.get(
        f"{settings.API_V1_STR}/bodies/{page}?constellation=orion",
        headers={"Host": "perseus.docker.localhost"},
    )

    assert response.status_code == 200

    body = response.json()

    assert body["count"] == 85
    assert (
        "https://perseus.docker.localhost/api/v1/bodies/2?limit=20&constellation=orion"
        in body["next_page"]
    )
    assert body["previous_page"] is None
    assert len(body["results"]) == 20

    assert body["results"][1]["name"] == "α Orionis"
    assert body["results"][0]["name"] == "β Orionis"
    assert body["results"][2]["name"] == "γ Orionis"
    assert body["results"][6]["name"] == "δ Orionis"
    assert body["results"][3]["name"] == "ε Orionis"
    assert body["results"][4]["name"] == "ζ Orionis"
    assert body["results"][7]["name"] == "ι Orionis"
    assert body["results"][5]["name"] == "κ Orionis"
    assert body["results"][8]["name"] == "π³ Orionis"
    assert body["results"][9]["name"] == "η Orionis"


@pytest.mark.asyncio
async def test_list_bodies_above_local_observers_horizon(client: AsyncClient) -> None:
    page = 1

    response = await client.get(
        f"{settings.API_V1_STR}/bodies/{page}?latitude=19.8968&longitude=155.8912&datetime=2021-05-14T00:00:00.000Z",  # noqa: E501
        headers={"Host": "perseus.docker.localhost"},
    )

    assert response.status_code == 200

    body = response.json()

    assert body["count"] == 1493
    assert (
        "/api/v1/bodies/2?limit=20&latitude=19.8968&longitude=155.8912&datetime=2021-05-14T00%3A00%3A00.000Z"  # noqa: E501,
        in body["next_page"]
    )
    assert body["previous_page"] is None
    assert len(body["results"]) == 20


@pytest.mark.asyncio
async def test_list_bodies_above_local_observers_horizon_between_interval_for_20210514(
    client: AsyncClient,
) -> None:
    page = 1

    response = await client.get(
        f"{settings.API_V1_STR}/bodies/{page}?latitude=19.8968&longitude=-155.8912&start=2021-05-14T18:46:50.000-10:00&end=2021-05-15T05:49:30.000-10:00",  # noqa: E501
        headers={"Host": "perseus.docker.localhost"},
    )

    assert response.status_code == 200

    body = response.json()

    assert body["count"] == 2739
    assert (
        "/api/v1/bodies/2?limit=20&latitude=19.8968&longitude=-155.8912&start=2021-05-14T18%3A46%3A50.000-10%3A00&end=2021-05-15T05%3A49%3A30.000-10%3A00"  # noqa: E501,
        in body["next_page"]
    )
    assert body["previous_page"] is None
    assert len(body["results"]) == 20


@pytest.mark.asyncio
async def test_list_bodies_above_local_observers_horizon_between_interval_for_20220101(
    client: AsyncClient,
) -> None:
    page = 1

    response = await client.get(
        f"{settings.API_V1_STR}/bodies/{page}?latitude=19.8968&longitude=-155.8912&start=2022-01-01T17:58:56.000-10:00&end=2022-01-02T06:52:13.000-10:00",  # noqa: E501
        headers={"Host": "perseus.docker.localhost"},
    )

    assert response.status_code == 200

    body = response.json()

    assert body["count"] == 2717
    assert (
        "/api/v1/bodies/2?limit=20&latitude=19.8968&longitude=-155.8912&start=2022-01-01T17%3A58%3A56.000-10%3A00&end=2022-01-02T06%3A52%3A13.000-10%3A00"  # noqa: E501,
        in body["next_page"]
    )
    assert body["previous_page"] is None
    assert len(body["results"]) == 20
