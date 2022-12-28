import logging

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.flush.bodies import flush_bodies

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def flush(db: Session) -> None:
    db = SessionLocal()
    # Flush the bodies table:
    flush_bodies(db, logger)


def main() -> None:
    db = SessionLocal()
    logger.info("Flushing Existing API Data Started")
    flush(db)
    logger.info("Flushing Existing API Data Success")


if __name__ == "__main__":
    main()
