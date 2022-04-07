from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.body import Body
from app.schemas.body import BodyCreate, BodyUpdate


class CRUDBody(CRUDBase[Body, BodyCreate, BodyUpdate]):
    def create(self, db: Session, body: BodyCreate) -> Body:
        body_data = jsonable_encoder(body)
        db_obj = Body(**body_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


body = CRUDBody(Body)
