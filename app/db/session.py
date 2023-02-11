from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

if settings.PROJECT_ENVIRONMENT == "production":
    if settings.SQLALCHEMY_DATABASE_URI is None:
        raise Exception("settings.SQLALCHEMY_DATABASE_URI is None")
    engine = create_engine(
        "{}?sslmode=require".format(settings.SQLALCHEMY_DATABASE_URI),
        pool_pre_ping=True,
    )
else:
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
