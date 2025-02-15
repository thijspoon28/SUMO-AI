from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class Measurement(Base):
    __tablename__ = 'measurements'
    id = Column(String, primary_key=True)
    basho_id = Column(String, nullable=False)
    rikishi_id = Column(Integer, ForeignKey('rikishi.id'), nullable=False)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)


class Rank(Base):
    __tablename__ = 'ranks'
    id = Column(String, primary_key=True)
    basho_id = Column(String, nullable=False)
    rikishi_id = Column(Integer, ForeignKey('rikishi.id'), nullable=False)
    rank_value = Column(Integer, nullable=False)
    rank = Column(String, nullable=False)


class Shikona(Base):
    __tablename__ = 'shikonas'
    id = Column(String, primary_key=True)
    basho_id = Column(String, nullable=False)
    rikishi_id = Column(Integer, ForeignKey('rikishi.id'), nullable=False)
    shikona_en = Column(String, nullable=False)
    shikona_jp = Column(String, nullable=False)


class Match(Base):
    __tablename__ = 'matches'
    id = Column(String, primary_key=True)
    basho_id = Column(String, nullable=False)
    division = Column(String, nullable=False)
    day = Column(Integer, nullable=False)
    match_no = Column(Integer, nullable=False)
    east_id = Column(Integer, nullable=False)
    east_shikona = Column(String, nullable=False)
    east_rank = Column(String, nullable=False)
    west_id = Column(Integer, nullable=False)
    west_shikona = Column(String, nullable=False)
    west_rank = Column(String, nullable=False)
    kimarite = Column(String, nullable=False)
    winner_id = Column(Integer, nullable=False)
    winner_en = Column(String, nullable=False)
    winner_jp = Column(String, nullable=False)


class RikishiStats(Base):
    __tablename__ = 'rikishi_stats'
    id = Column(Integer, primary_key=True)
    absence_by_division = Column(JSON, nullable=False)
    basho = Column(Integer, nullable=False)
    basho_by_division = Column(JSON, nullable=False)
    loss_by_division = Column(JSON, nullable=False)
    sansho = Column(JSON, nullable=False)
    total_absences = Column(Integer, nullable=False)
    total_by_division = Column(JSON, nullable=False)
    total_losses = Column(Integer, nullable=False)
    total_matches = Column(Integer, nullable=False)
    total_wins = Column(Integer, nullable=False)
    wins_by_division = Column(JSON, nullable=False)
    yusho = Column(Integer, nullable=False)
    yusho_by_division = Column(JSON, nullable=False)


class Rikishi(Base):
    __tablename__ = 'rikishi'
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

    measurement_history = relationship("Measurement", backref="rikishi")
    rank_history = relationship("Rank", backref="rikishi")
    shikona_history = relationship("Shikona", backref="rikishi")
    stats = relationship("RikishiStats", backref="rikishi", uselist=False)


class Kimarite(Base):
    __tablename__ = 'kimarite'
    kimarite = Column(String, primary_key=True)
    count = Column(Integer, nullable=False)
    last_usage = Column(String, nullable=False)


class SpecialPrize(Base):
    __tablename__ = 'special_prizes'
    type = Column(String, primary_key=True)
    rikishi_id = Column(Integer, ForeignKey('rikishi.id'), nullable=False)
    shikona_en = Column(String, nullable=False)
    shikona_jp = Column(String, nullable=False)


class BashoData(Base):
    __tablename__ = 'basho_data'
    id = Column(String, primary_key=True)
    date = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    yusho = Column(JSON, nullable=True)
    special_prizes = Column(JSON, nullable=True)


class BashoBanzuke(Base):
    __tablename__ = 'basho_banzuke'
    basho_id = Column(String, primary_key=True)
    division = Column(String, nullable=False)
    east = Column(JSON, nullable=True)
    west = Column(JSON, nullable=True)
