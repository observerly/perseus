import logging

from sqlalchemy.orm import Session

from app.db.session import SessionLocal

# from app.dump.messier import dump_messier
from app.dump.stars import dump_stars

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def dump(db: Session) -> None:
    # Dump Messier Objects:
    # dump_messier(db, logger)
    # Dump Stars:
    dump_stars(db, logger)


def main() -> None:
    db = SessionLocal()
    logger.info("Populating Initial API Data Started")
    dump(db)
    logger.info("Populating Initial API Data Success")


if __name__ == "__main__":
    main()
