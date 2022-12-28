from logging import Logger

from sqlalchemy.orm import Session

from app import crud
from app.utils import ROOT_DIR


def flush_bodies(db: Session, logger: Logger) -> None:
    """
    This function call flushes the Body model
    """
    logger.info("ROOT_DIR: {}".format(ROOT_DIR))

    crud.body.delete_multi(db)
