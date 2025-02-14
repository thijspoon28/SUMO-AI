from datetime import datetime
from typing import Optional, List, Dict

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

def get_engine():
    return create_engine("sqlite:///sumo.db", echo=True)

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

# SQLAlchemy Models

class MeasurementDB(Base):
    __tablename__ = "measurements"
    id = Column(String, primary_key=True)
    basho_id = Column(String, nullable=False)
    rikishi_id = Column(Integer, ForeignKey("rikishi.id"), nullable=False)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)

class RankDB(Base):
    __tablename__ = "ranks"
    id = Column(String, primary_key=True)
    basho_id = Column(String, nullable=False)
    rikishi_id = Column(Integer, ForeignKey("rikishi.id"), nullable=False)
    rank_value = Column(Integer, nullable=False)
    rank = Column(String, nullable=False)

class ShikonaDB(Base):
    __tablename__ = "shikonas"
    id = Column(String, primary_key=True)
    basho_id = Column(String, nullable=False)
    rikishi_id = Column(Integer, ForeignKey("rikishi.id"), nullable=False)
    shikona_en = Column(String, nullable=False)
    shikona_jp = Column(String, nullable=True)

class RikishiDB(Base):
    __tablename__ = "rikishi"
    id = Column(Integer, primary_key=True)
    sumodb_id = Column(Integer, nullable=True)
    nsk_id = Column(Integer, nullable=False)
    shikona_en = Column(String, nullable=False)
    shikona_jp = Column(String, nullable=True)
    current_rank = Column(String, nullable=False)
    heya = Column(String, nullable=True)
    birth_date = Column(DateTime, nullable=True)
    shusshin = Column(String, nullable=True)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    debut = Column(String, nullable=False)
    intai = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True)
    
    measurement_history = relationship("MeasurementDB", backref="rikishi")
    rank_history = relationship("RankDB", backref="rikishi")
    shikona_history = relationship("ShikonaDB", backref="rikishi")

# Function to convert Pydantic models to DB models

def create_rikishi(rikishi_data):
    return RikishiDB(
        id=rikishi_data.id,
        sumodb_id=rikishi_data.sumodbId,
        nsk_id=rikishi_data.nskId,
        shikona_en=rikishi_data.shikonaEn,
        shikona_jp=rikishi_data.shikonaJp,
        current_rank=rikishi_data.currentRank,
        heya=rikishi_data.heya,
        birth_date=rikishi_data.birthDate,
        shusshin=rikishi_data.shusshin,
        height=rikishi_data.height,
        weight=rikishi_data.weight,
        debut=rikishi_data.debut,
        intai=rikishi_data.intai,
        updated_at=rikishi_data.updatedAt,
        created_at=rikishi_data.createdAt
    )

def create_measurement(measurement_data):
    return MeasurementDB(
        id=measurement_data.id,
        basho_id=measurement_data.bashoId,
        rikishi_id=measurement_data.rikishiId,
        height=measurement_data.height,
        weight=measurement_data.weight
    )

def create_rank(rank_data):
    return RankDB(
        id=rank_data.id,
        basho_id=rank_data.bashoId,
        rikishi_id=rank_data.rikishiId,
        rank_value=rank_data.rankValue,
        rank=rank_data.rank
    )

def create_shikona(shikona_data):
    return ShikonaDB(
        id=shikona_data.id,
        basho_id=shikona_data.bashoId,
        rikishi_id=shikona_data.rikishiId,
        shikona_en=shikona_data.shikonaEn,
        shikona_jp=shikona_data.shikonaJp
    )

if __name__ == "__main__":
    engine = get_engine()
    Base.metadata.create_all(engine)
