import datetime
from typing import List, Tuple, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import case, or_
from sqlalchemy.orm import Query, Session
from sqlalchemy.sql import func

from app.crud.base import CRUDBase
from app.db.base_class import Base
from app.models.body import Body
from app.schemas.body import BodyCreate, BodyUpdate

ModelType = TypeVar("ModelType", bound=Base)

QueryParams = TypeVar("QueryParams", bound=BaseModel)


class CRUDBody(CRUDBase[Body, BodyCreate, BodyUpdate]):
    def get_or_create(
        self, db: Session, body: BodyCreate, **kwargs
    ) -> Tuple[Body, bool]:
        db_obj = db.query(Body).filter_by(**kwargs).first()

        if db_obj:
            return db_obj, False

        return self.create(db, body), True

    def merge_or_create(
        self, db: Session, body: BodyCreate, **kwargs
    ) -> Tuple[Body, bool]:
        db_obj, created = self.get_or_create(db, body, **kwargs)

        if not created:
            # Update only the fields that are not None in the
            # body object, but are None in the db_obj:
            body_data = jsonable_encoder(body)

            for field in body_data:
                if body_data[field] is not None and getattr(db_obj, field) is None:
                    setattr(db_obj, field, body_data[field])

            db.add(db_obj)

        return db_obj, created

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

        query = self.perform_type_search_filter(query, query_params)

        query = self.perform_catalogue_search_filter(query, query_params)

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

        if latitude and latitude > 0:
            query = query.filter(
                self.model.dec > latitude - 90,
            )

        if latitude and latitude < 0:
            query = query.filter(
                self.model.dec > latitude - 90,
            )

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

        if not name:
            return query

        # If the name starts with "M", then we need to
        # filter by the Messier catalogue:
        if (
            name.lower().strip().startswith("m")
            and len(name) >= 2
            and name[1:].isdigit()
        ):
            return query.filter(
                self.model.messier.op("LIKE")("%{0}%".format(name[1:])),
            )

        # If the name starts with "NGC", then we need to
        # filter by the New General catalogue:
        if (
            name.lower().strip().startswith("ngc")
            and len(name) >= 4
            and name[3:].isdigit()
        ):
            return query.filter(
                self.model.ngc.op("LIKE")("%{0}%".format(name[3:])),
            )

        # If the name starts with "IC", then we need to
        # filter by the Index catalogue:
        if (
            name.lower().strip().startswith("ic")
            and len(name) >= 3
            and name[2:].isdigit()
        ):
            return query.filter(
                self.model.ic.op("LIKE")("%{0}%".format(name[2:])),
            )

        query = query.filter(
            or_(
                self.model.name.op("LIKE")("%{0}%".format(name)),
                self.model.iau.op("LIKE")("%{0}%".format(name)),
            )
        )

        return query

    def perform_constellation_search_filter(
        self, query: Query, query_params: QueryParams
    ) -> Query:
        # Constellation
        constellation = getattr(query_params, "constellation", None)

        if constellation:
            query = query.filter(
                or_(
                    self.model.constellation.op("LIKE")("%{0}%".format(constellation)),
                    self.model.constellation.op("%")("%{0}%".format(constellation)),
                )
            )

        return query

    def perform_type_search_filter(
        self, query: Query, query_params: QueryParams
    ) -> Query:
        # Type
        type = getattr(query_params, "type", None)

        if type:
            query = query.filter(
                self.model.type.op("LIKE")("{0}".format(type)),
            )

        return query

    def perform_catalogue_search_filter(
        self, query: Query, query_params: QueryParams
    ) -> Query:
        # Catalogue
        catalogue = getattr(query_params, "catalogue", None)

        # If no catalogue is specified, return all:
        if not catalogue or catalogue == "all":
            return query

        # Otherwise, filter by the given catalogue:

        # Messier:
        if catalogue.strip().lower() == "messier":
            query = query.filter(
                self.model.messier.isnot(None),
            )

        # New General Catalogue:
        if catalogue.strip().lower() == "ngc":
            query = query.filter(
                self.model.ngc.isnot(None),
            )

        # Index Catalogue:
        if catalogue.strip().lower() == "ic":
            query = query.filter(
                self.model.ic.isnot(None),
            )

        return query

    def perform_order_by_type(self, query: Query) -> Query:
        whens = {
            "Other": 4,
            "*": 3,
            "**": 3,
            "*Ass": 3,
            "OCl": 2,
            "GCl": 2,
            "G": 1,
            "Cl+N": 0,
            "PN": 0,
            "HII": 0,
            "DrkN": 0,
            "EmN": 0,
            "Neb": 0,
            "RfN": 0,
            "SNR": 0,
        }

        sort = case(value=Body.type, whens=whens).label("type")

        return query.order_by(sort)

    def get_multi(
        self, db: Session, *, query_params: QueryParams, skip: int = 0, limit: int = 100
    ) -> Tuple[List[ModelType], int]:
        query = db.query(self.model)
        # Filter w/Query Params:
        query = self.get_filter_query(query, query_params)

        query = self.perform_order_by_type(query)

        count = query.count()

        # Here we are ordering by apparent magnitude (mag) in ascending order because
        # negative magnitudes are actually "brighter" than positive magnitudes:
        return (
            query.order_by(func.coalesce(Body.m, 99999).asc())
            .offset(skip)
            .limit(limit)
            .all(),
            count,
        )

    def delete_multi(self, db: Session) -> None:
        db.query(self.model).delete()
        db.commit()


body = CRUDBody(Body)
