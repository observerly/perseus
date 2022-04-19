from typing import Any, Optional

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.api.api_v1.params.bodies import BodyQueryParams
from app.api.paginator import PaginatedResponse

router = APIRouter()


@router.get("/", name="bodies:list", response_model=PaginatedResponse[schemas.Body])
def list_bodies(
    req: Request,
    *,
    db: Session = Depends(deps.get_db),
    query: BodyQueryParams = Depends()
) -> Any:
    """
    returns the first page of list of bodies of any type based off of the
    search paramaters provided
    """
    page = 1

    start = (page - 1) * query.limit

    bodies = crud.body.get_multi(db, query_params=query, skip=start, limit=query.limit)

    count = bodies.count()

    return PaginatedResponse.paginate(
        request=req,
        name="bodies:list-paginated",
        items=bodies,
        count=count,
        current_page=page,
        limit=query.limit,
        query=query,
    )


@router.get(
    "/{page}",
    name="bodies:list-paginated",
    response_model=PaginatedResponse[schemas.Body],
)
def list_bodies_paginated(
    req: Request,
    *,
    db: Session = Depends(deps.get_db),
    page: Optional[int] = 1,
    query: BodyQueryParams = Depends()
) -> Any:
    """
    returns a paginated list of bodies of any type based off of the
    search paramaters provided
    """
    start = (page - 1) * query.limit

    bodies = crud.body.get_multi(db, query_params=query, skip=start, limit=query.limit)

    count = bodies.count()

    return PaginatedResponse.paginate(
        request=req,
        name="bodies:list-paginated",
        items=bodies,
        count=count,
        current_page=page,
        limit=query.limit,
        query=query,
    )
