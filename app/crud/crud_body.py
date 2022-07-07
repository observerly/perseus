import datetime
from typing import List, Tuple, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Query, Session
from sqlalchemy.sql import func

from app.crud.base import CRUDBase
from app.db.base_class import Base
from app.models.body import Body
from app.schemas.body import BodyCreate, BodyUpdate

ModelType = TypeVar("ModelType", bound=Base)

QueryParams = TypeVar("QueryParams", bound=BaseModel)


class CRUDBody(CRUDBase[Body, BodyCreate, BodyUpdate]):
    def create(self, db: Session, body: BodyCreate) -> Body:
        body_data = jsonable_encoder(body)
        db_obj = Body(**body_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_filter_query(self, query: Query, query_params: QueryParams):
        query = self.perform_equatorial_radial_search_filter(query, query_params)

        query = self.perform_name_search_filter(query, query_params)

        query = self.perform_constellation_search_filter(query, query_params)

        query = self.perform_horizontal_altitude_search_filter(query, query_params)

        return query

    def perform_equatorial_radial_search_filter(
        self, query: Query, query_params: QueryParams
    ) -> Query:
        # Right Ascension & Declination (in degrees):
        ra = getattr(query_params, "ra", None)

        dec = getattr(query_params, "dec", None)

        # Radius should be quoted in degrees:
        radius = getattr(query_params, "radius", None) or 10

        # Performs a radial search for the given { ra, dec } point in the DB:
        if ra and dec and radius:
            query = query.filter(
                func.sqrt(
                    func.pow(self.model.ra - ra, 2) + func.pow(self.model.dec - dec, 2)
                )
                < radius
            )

        return query

    def perform_horizontal_altitude_search_filter(
        self, query: Query, query_params: QueryParams
    ) -> Query:
        # Date:
        d = getattr(query_params, "datetime", None)

        start = getattr(query_params, "start", None)

        end = getattr(query_params, "end", None)

        try:
            d = datetime.datetime.strptime(d, "%Y-%m-%dT%H:%M:%S.%f%z")
        except (ValueError, TypeError):
            d = None

        try:
            start = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%f%z")
            end = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S.%f%z")
        except (ValueError, TypeError):
            start = None
            end = None

        # Latitude & Longitude (in degrees):
        latitude = getattr(query_params, "latitude", None)

        longitude = getattr(query_params, "longitude", None)

        # Performs a search for the give body above a local altitude of 15 degrees
        # (above horizon) in the DB:
        if d and latitude and longitude:
            LST = self.model.get_LST(d, latitude, longitude)

            query = query.filter(self.model.altitude(LST, latitude) > 15)

        # Performs a search for the give body above a local altitude of 15 degrees
        # (above horizon) between the given start and end datetime interval in the DB:
        if start and end and latitude and longitude:
            LSTr = self.model.get_LST(start, latitude, longitude)

            LSTs = self.model.get_LST(end, latitude, longitude)

            query = query.filter(
                or_(
                    self.model.altitude(LSTr, latitude) > 15,
                    self.model.altitude(LSTs, latitude) > 15,
                )
            )

        return query

    def perform_name_search_filter(
        self, query: Query, query_params: QueryParams
    ) -> Query:
        # Name:
        name = getattr(query_params, "name", None)

        if name:
            query = query.filter(
                or_(self.model.name.op("%")(name), self.model.iau.op("%")(name))
            )

        return query

    def perform_constellation_search_filter(
        self, query: Query, query_params: QueryParams
    ) -> Query:
        # Constellation
        constellation = getattr(query_params, "constellation", None)

        if constellation:
            query = query.filter(self.model.constellation.op("%")(constellation))

        return query

    def get_multi(
        self, db: Session, *, query_params: QueryParams, skip: int = 0, limit: int = 100
    ) -> Tuple[List[ModelType], int]:
        query = db.query(self.model)
        # Filter w/Query Params:
        query = self.get_filter_query(query, query_params)

        count = query.count()

        return query.offset(skip).limit(limit).all(), count


body = CRUDBody(Body)
