import math

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False},
)


@event.listens_for(engine, "connect")
def create_math_functions_on_connect(dbapi_connection, connection_record):
    dbapi_connection.create_function("sin", 1, math.sin)
    dbapi_connection.create_function("cos", 1, math.cos)
    dbapi_connection.create_function("asin", 1, math.asin)
    dbapi_connection.create_function("radians", 1, math.radians)
    dbapi_connection.create_function("degrees", 1, math.degrees)
    dbapi_connection.create_function("sqrt", 1, math.sqrt)
    dbapi_connection.create_function("pow", 2, math.pow)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
