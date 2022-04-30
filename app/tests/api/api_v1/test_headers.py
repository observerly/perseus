from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings


def test_all_returns_http_x_headers_correctly(client: TestClient, db: Session) -> None:
    page = 1

    response = client.get(
        f"{settings.API_V1_STR}/bodies/{page}",
    )

    response.headers["X-Perseus-API-Version"] == str(settings.API_VERSION)

    assert response.status_code == 200
