import logging

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.seed.messier import seed_messier
from app.seed.stars import seed_stars

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def seed(db: Session) -> None:
    # Seed Messier Objects:
    seed_messier(db, logger)
    # Seed Stars:
    seed_stars(db, logger)


def main() -> None:
    db = SessionLocal()
    logger.info("Populating Initial API Data Started")
    seed(db)
    logger.info("Populating Initial API Data Success")


if __name__ == "__main__":
    main()
