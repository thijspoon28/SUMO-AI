from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



def get_engine():
    return create_engine("sqlite:///sumo.db", echo=False)


def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()


if __name__ == "__main__":
    engine = get_engine()
    # Base.metadata.create_all(engine)
