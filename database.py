from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATEBASE = 'postgresql+psycopg2://root:root@postgres_container:5432/test_db'

engine = create_engine(URL_DATEBASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
