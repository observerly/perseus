from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.body import Body
from app.schemas.body import BodyCreate, BodyUpdate


class CRUDBody(CRUDBase[Body, BodyCreate, BodyUpdate]):
    def create(self, db: Session, body: BodyCreate) -> Body:
        db_obj = Body(
            name=body.name,
            iau=body.iau,
            ra=body.ra,
            dec=body.dec,
            constellation=body.constellation,
            type=body.type,
            m=body.m,
            M=body.M,
            d=body.d,
            hd=body.hd,
            hr=body.hr,
            hip=body.hip,
            bd=body.bd,
            flamsteed=body.flamsteed,
            simbad=body.simbad,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


body = CRUDBody(Body)
