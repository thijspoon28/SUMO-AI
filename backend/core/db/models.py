from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship, Mapped

from core.db.mixins import TimestampMixin
from core.db import Base


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id: Mapped[int] = Column(Integer, primary_key=True)
    username: Mapped[str] = Column(String, nullable=False)
    password: Mapped[str] = Column(String, nullable=False)
    is_admin: Mapped[bool] = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"User('{self.username}')"


class Measurement(Base):
    __tablename__ = "measurement"

    basho_id = Column(String, ForeignKey("basho.id"), primary_key=True)
    rikishi_id = Column(Integer, ForeignKey("rikishi.id"), primary_key=True)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)

    def __repr__(self) -> str:
        return f"Measurement(rikishi_id={self.rikishi_id}, basho_id={self.basho_id}, h/w={self.height}/{self.weight})"


class Rank(Base):  # type: ignore
    __tablename__ = "rank"

    basho_id = Column(String, ForeignKey("basho.id"), primary_key=True)
    rikishi_id = Column(Integer, ForeignKey("rikishi.id"), primary_key=True)
    rank_value = Column(Integer, nullable=False)
    rank = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f"Rank(rikishi_id={self.rikishi_id}, basho_id={self.basho_id}, r/v={self.rank}/{self.rank_value})"


class Shikona(Base):  # type: ignore
    __tablename__ = "shikona"

    basho_id = Column(String, ForeignKey("basho.id"), primary_key=True)
    rikishi_id = Column(Integer, ForeignKey("rikishi.id"), primary_key=True)
    shikona_en = Column(String, nullable=False)
    shikona_jp = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f"Shikona(rikishi_id={self.rikishi_id}, basho_id={self.basho_id}, en/jp={self.shikona_en}/{self.shikona_jp})"


class Match(Base):  # type: ignore
    __tablename__ = "match"

    basho_id = Column(String, ForeignKey("basho.id"), nullable=False, primary_key=True)
    division = Column(String, nullable=False)
    day = Column(Integer, primary_key=True)
    match_no = Column(Integer, nullable=False)
    east_id = Column(Integer, ForeignKey("rikishi.id"), primary_key=True)
    east_shikona = Column(String, nullable=False)
    east_rank = Column(String, nullable=False)
    west_id = Column(Integer, ForeignKey("rikishi.id"), primary_key=True)
    west_shikona = Column(String, nullable=False)
    west_rank = Column(String, nullable=False)
    kimarite = Column(String, nullable=False)
    winner_id = Column(Integer, nullable=False)
    winner_en = Column(String, nullable=False)
    winner_jp = Column(String, nullable=False)

    east_rikishi = relationship("Rikishi", foreign_keys=[east_id], back_populates="east_matches")
    west_rikishi = relationship("Rikishi", foreign_keys=[west_id], back_populates="west_matches")

    basho = relationship("Basho", back_populates="matches")

    def concat_id(self) -> str:
        return f"{self.basho_id}-{self.day}-{self.east_id}-{self.west_id}"

    def __repr__(self) -> str:
        return f"Match({self.concat_id()})"


class Rikishi(Base):  # type: ignore
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

    absence_by_division = Column(JSON, nullable=False)
    basho_count = Column(Integer, nullable=False)
    basho_count_by_division = Column(JSON, nullable=False)
    loss_by_division = Column(JSON, nullable=False)
    sansho = Column(JSON, nullable=False)
    total_absences = Column(Integer, nullable=False)
    total_by_division = Column(JSON, nullable=False)
    total_losses = Column(Integer, nullable=False)
    total_matches = Column(Integer, nullable=False)
    total_wins = Column(Integer, nullable=False)
    wins_by_division = Column(JSON, nullable=False)
    yusho_count = Column(Integer, nullable=False)
    yusho_count_by_division = Column(JSON, nullable=False)

    measurement_history: Mapped[list[Measurement]] = relationship(Measurement, backref="rikishi")
    rank_history: Mapped[list[Rank]] = relationship(Rank, backref="rikishi")
    shikona_history: Mapped[list[Shikona]] = relationship(Shikona, backref="rikishi")

    bashos: Mapped[list["RikishiBasho"]] = relationship(
        back_populates="rikishi", cascade="all, delete"
    )

    east_matches: Mapped[list[Match]] = relationship("Match", foreign_keys="[Match.east_id]", back_populates="east_rikishi")
    west_matches: Mapped[list[Match]] = relationship("Match", foreign_keys="[Match.west_id]", back_populates="west_rikishi")

    def matches(self) -> list[Match]:
        return self.east_matches + self.west_matches

    def __repr__(self) -> str:
        return f"Rikishi({self.id})"


class Basho(Base):  # type: ignore
    __tablename__ = "basho"

    id = Column(String, primary_key=True)
    date = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    rikishis: Mapped[list["RikishiBasho"]] = relationship(
        back_populates="basho", cascade="all, delete"
    )
    matches: Mapped[list[Match]] = relationship(Match, back_populates="basho")


class RikishiBasho(Base):  # type: ignore
    __tablename__ = "rikishi_basho"

    rikishi_id = Column(Integer, ForeignKey("rikishi.id"), primary_key=True)
    basho_id = Column(String, ForeignKey("basho.id"), primary_key=True)
    special_prize = Column(String, nullable=True)
    yusho = Column(String, nullable=True)

    rikishi: Mapped[Rikishi] = relationship(back_populates="bashos")
    basho: Mapped[Basho] = relationship(back_populates="rikishis")
