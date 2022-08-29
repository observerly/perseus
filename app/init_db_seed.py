import logging

from app.db.session import SessionLocal
from app.seed.messier import seed_messier
from app.seed.stars import seed_stars

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def seed() -> None:
    db = SessionLocal()
    seed_messier(db, logger)
    seed_stars(db, logger)


def main() -> None:
    logger.info("Populating Initial API Data Started")
    seed()
    logger.info("Populating Initial API Data Success")


if __name__ == "__main__":
    main()
