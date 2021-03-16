import os

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_pg_engine():
    url = URL(
        drivername="postgresql+psycopg2",
        username=os.environ['PGUSER'],
        password=os.environ['PGPASSWORD'],
        host=os.environ['PGHOST'],
        port=5432,
        database=os.environ['PGDATABASE'],
    )
    # url = "sqlite:///./sql_app.db"
    return create_engine(url, pool_pre_ping=True)


engine = get_pg_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
