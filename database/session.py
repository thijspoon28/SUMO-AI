import os
from sqlalchemy import create_engine, select
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from database.models import Base, Rikishi



def get_engine():
    return create_engine("sqlite:///sumo.db", echo=False)


def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()


def init_db(delete: bool = False):
    if delete:
        os.remove("sumo.db")
        Base.metadata.create_all(get_engine())
        return
        
    session = get_session()
    q = select(Rikishi)

    try:
        session.execute(q)

    except sqlalchemy.exc.OperationalError:
        Base.metadata.create_all(get_engine())
