from typing import Optional

from fastapi import Query
from pydantic import BaseModel


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

    iau: Optional[str] = Query(
        default=None,
        title="The IAU's name of the body object to search",
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

    type: Optional[str] = Query(
        default=None,
        title="The type of the body object to search",
        deprecated=True,
    )

    latitude: Optional[float] = Query(
        default=None,
        title="The observer's latitude to perform body object search",
        deprecated=True,
    )

    longitude: Optional[float] = Query(
        default=None,
        title="The observer's latitude to perform body object search",
        deprecated=True,
    )

    datetime: Optional[str] = Query(
        default=None,
        title="The observer's local date / datetime  to perform body object search",
        deprecated=True,
    )

    start: Optional[str] = Query(
        default=None,
        title="The start date / datetime to perform body object search",
        deprecated=True,
    )

    end: Optional[str] = Query(
        default=None,
        title="The end date / datetime to perform body object search",
        deprecated=True,
    )

    catalogue: Optional[str] = Query(
        default=None,
        title="The catalogue of the body object to search",
        deprecated=True,
    )
