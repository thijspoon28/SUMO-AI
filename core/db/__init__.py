import os
import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

from core.config import config


engine = create_engine(config.DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_engine():
    return create_engine(config.DB_URL, echo=False)


def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()


def init_db(delete: bool = False):
    session = get_session()

    if delete:
        os.remove(config.DB_URL.split("/")[-1])
        Base.metadata.create_all(session.get_bind())
        return
        
    q = text("SELECT * FROM Rikishi")

    try:
        session.execute(q)

    except sqlalchemy.exc.OperationalError:
        Base.metadata.create_all(session.get_bind())
