import pymysql
from google.cloud.sql.connector import Connector, IPTypes
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


# Python Connector database connection function
def getconn() -> pymysql.connections.Connection:
    # if env var PRIVATE_IP is set to True, use private IP Cloud SQL connections
    ip_type = IPTypes.PRIVATE if settings.MYSQL_PRIVATE_IP is True else IPTypes.PUBLIC

    # Initialize the Connector object:
    with Connector(ip_type=ip_type) as connector:
        conn: pymysql.connections.Connection = connector.connect(
            settings.MYSQL_INSTANCE_CONNECTION_NAME,
            "pymysql",
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            db=settings.MYSQL_DATABASE,
        )
        return conn


SQL_ALCHEMY_DATABASE_URL = "mysql+pymysql://"

if settings.USE_CLOUD_SQL:
    if settings.MYSQL_INSTANCE_CONNECTION_NAME is None:
        raise ValueError("MYSQL_INSTANCE_CONNECTION_NAME is not set")
    if settings.MYSQL_USER is None:
        raise ValueError("MYSQL_USER is not set")
    if settings.MYSQL_PASSWORD is None:
        raise ValueError("MYSQL_PASSWORD is not set")
    if settings.MYSQL_DATABASE is None:
        raise ValueError("MYSQL_DATABASE is not set")
    engine = create_engine(SQL_ALCHEMY_DATABASE_URL, creator=getconn)
else:
    if settings.SQLALCHEMY_DATABASE_URI is None:
        raise ValueError("SQLALCHEMY_DATABASE_URI is not set")

    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
