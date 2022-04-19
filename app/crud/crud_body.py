from typing import List, Tuple, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
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
        # Search Bodies By ra, dec & radius:
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

        # Name:
        name = getattr(query_params, "name", None)

        if name:
            query = query.filter(self.model.name.op("%")(name))

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
