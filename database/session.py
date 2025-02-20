import os
from sqlalchemy import create_engine, select
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from database.models import Base, Rikishi


DB = "sumo.db"
_main_db = "sumo.db"


def get_engine():
    if _main_db != DB:
        for _ in range(3):
            print(f"WARNING! WARNING! WARNING! USING DATABASE '{DB}' INSTEAD OF '{_main_db}'!!!")
    return create_engine(f"sqlite:///{DB}", echo=False)


def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()


def init_db(delete: bool = False):
    session = get_session()

    if delete:
        os.remove(DB)
        Base.metadata.create_all(session.get_bind())
        return
        
    q = select(Rikishi)

    try:
        session.execute(q)

    except sqlalchemy.exc.OperationalError:
        Base.metadata.create_all(session.get_bind())
