from datetime import datetime
from pydantic import ConfigDict, BaseModel

from app.match.schemas.match import MatchSchema
from app.rikishi.schemas.basho import RikishiBashoSchema
from app.rikishi.schemas.history import MeasurementSchema, RankSchema, ShikonaSchema


class CreateRikishiSchema(BaseModel):
    id: str
    date: str
    start_date: datetime
    end_date: datetime
    # rikishis: list
    # matches: list


class RikishiSchema(BaseModel):
    sumodb_id: int | None = None
    nsk_id: int
    shikona_en: str
    shikona_jp: str | None = None
    current_rank: str
    heya: str | None = None
    birth_date: datetime | None = None
    shusshin: str | None = None
    height: float
    weight: float
    debut: str
    intai: datetime | None = None
    updated_at: datetime | None = None
    created_at: datetime | None = None

    absence_by_division: dict[str, int]
    basho_count: int
    basho_count_by_division: dict[str, int]
    loss_by_division: dict[str, int]
    sansho: dict[str, int]
    total_absences: int
    total_by_division: dict[str, int]
    total_losses: int
    total_matches: int
    total_wins: int
    wins_by_division: dict[str, int]
    yusho_count: int
    yusho_count_by_division: dict[str, int]

    model_config = ConfigDict(from_attributes=True)


class FullRikishiSchema(BaseModel):
    sumodb_id: int | None = None
    nsk_id: int
    shikona_en: str
    shikona_jp: str | None = None
    current_rank: str
    heya: str | None = None
    birth_date: datetime | None = None
    shusshin: str | None = None
    height: float
    weight: float
    debut: str
    intai: datetime | None = None
    updated_at: datetime | None = None
    created_at: datetime | None = None

    absence_by_division: dict[str, int]
    basho_count: int
    basho_count_by_division: dict[str, int]
    loss_by_division: dict[str, int]
    sansho: dict[str, int]
    total_absences: int
    total_by_division: dict[str, int]
    total_losses: int
    total_matches: int
    total_wins: int
    wins_by_division: dict[str, int]
    yusho_count: int
    yusho_count_by_division: dict[str, int]

    measurement_history: list[MeasurementSchema]
    rank_history: list[RankSchema]
    shikona_history: list[ShikonaSchema]
    bashos: list[RikishiBashoSchema]
    east_matches: list[MatchSchema]
    west_matches: list[MatchSchema]

    model_config = ConfigDict(from_attributes=True)


class UpdateRikishiSchema(BaseModel):
    id: str
    date: str
    start_date: datetime
    end_date: datetime
