from typing import Any, Optional

from fastapi import APIRouter, Depends, Query, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.api.paginator import PaginatedResponse

router = APIRouter()


class BodyQueryParams(BaseModel):
    limit: Optional[int] = Query(
        default=20, title="The number of records to return per page", deprecated=True
    )

    ra: Optional[float] = Query(
        default=None, title="The right ascension to search", deprecated=True
    )

    dec: Optional[float] = Query(
        default=None, title="The declination to search", deprecated=True
    )

    radius: Optional[float] = Query(
        default=None,
        title="The search radius from the point { ra, dec }",
        deprecated=True,
    )

    name: Optional[str] = Query(
        default=None, title="The name of the body object to search", deprecated=True
    )

    constellation: Optional[str] = Query(
        default=None,
        title="The constellation of the body object to search",
        deprecated=True,
    )


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

    count = crud.body.get_count(db)

    bodies = crud.body.get_multi(db, query_params=query, skip=start, limit=query.limit)

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

    count = crud.body.get_count(db, query_params=query)

    bodies = crud.body.get_multi(db, query_params=query, skip=start, limit=query.limit)

    return PaginatedResponse.paginate(
        request=req,
        name="bodies:list-paginated",
        items=bodies,
        count=count,
        current_page=page,
        limit=query.limit,
        query=query,
    )
