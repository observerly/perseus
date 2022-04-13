from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings


def test_list_bodies_returns_http_ok_status(client: TestClient, db: Session) -> None:
    page = 1

    response = client.get(
        f"{settings.API_V1_STR}/bodies/{page}",
    )

    assert response.status_code == 200


def test_list_bodies_without_any_query_params(client: TestClient, db: Session) -> None:
    page = 1

    response = client.get(
        f"{settings.API_V1_STR}/bodies/{page}",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["count"] == 406
    assert "/api/v1/bodies/2?limit=20" in body["next_page"]
    assert body["previous_page"] is None
    assert len(body["results"]) == 20


def test_list_bodies_with_default_radial_search(
    client: TestClient, db: Session
) -> None:
    page = 1

    response = client.get(
        f"{settings.API_V1_STR}/bodies/{page}?ra=2.294522&dec=59.14978",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["count"] == 3
    assert body["next_page"] is None
    assert body["previous_page"] is None

    assert body["results"][0]["name"] == "β Cassiopeiae"
    assert body["results"][1]["name"] == "ζ Cassiopeiae"
    assert body["results"][2]["name"] == "α Cassiopeiae"


def test_list_bodies_with_specific_radial_search(
    client: TestClient, db: Session
) -> None:
    page = 1

    response = client.get(
        f"{settings.API_V1_STR}/bodies/{page}?ra=2.294522&dec=59.14978&radius=1.0",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["count"] == 1
    assert body["next_page"] is None
    assert body["previous_page"] is None
    assert body["results"][0]["name"] == "β Cassiopeiae"


def test_list_bodies_with_slightly_less_specific_radial_search(
    client: TestClient, db: Session
) -> None:
    page = 1

    response = client.get(
        f"{settings.API_V1_STR}/bodies/{page}?ra=2.294522&dec=59.14978&radius=10.0",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["count"] == 3
    assert body["next_page"] is None
    assert body["previous_page"] is None

    assert body["results"][0]["name"] == "β Cassiopeiae"
    assert body["results"][1]["name"] == "ζ Cassiopeiae"
    assert body["results"][2]["name"] == "α Cassiopeiae"


def test_list_bodies_with_too_specific_radial_search(
    client: TestClient, db: Session
) -> None:
    page = 1

    response = client.get(
        f"{settings.API_V1_STR}/bodies/{page}?ra=180&dec=45&radius=0.1",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["count"] == 0
    assert body["next_page"] is None
    assert body["previous_page"] is None
    assert len(body["results"]) == 0


def test_list_bodies_within_the_constellation_orion(
    client: TestClient, db: Session
) -> None:
    page = 1

    response = client.get(
        f"{settings.API_V1_STR}/bodies/{page}?constellation=orion",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["count"] == 10
    assert body["next_page"] is None
    assert body["previous_page"] is None
    assert len(body["results"]) == 10

    assert body["results"][0]["name"] == "π³ Orionis"
    assert body["results"][1]["name"] == "β Orionis"
    assert body["results"][2]["name"] == "γ Orionis"
    assert body["results"][3]["name"] == "δ Orionis"
    assert body["results"][4]["name"] == "λ Orionis"
    assert body["results"][5]["name"] == "ι Orionis"
    assert body["results"][6]["name"] == "ε Orionis"
    assert body["results"][7]["name"] == "ζ Orionis"
    assert body["results"][8]["name"] == "κ Orionis"
    assert body["results"][9]["name"] == "α Orionis"
