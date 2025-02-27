from typing import Generic, TypeVar
from pydantic import BaseModel

from core.external_api.schemas import (
    BashoBanzuke,
    BashoData,
    BashoTorikumi,
    Kimarite,
    Match,
    Measurement,
    Rank,
    Rikishi,
    RikishiMatch,
    RikishiStats,
    RikishiVersus,
    Shikona,
)


T = TypeVar("T", bound=BaseModel)


class BaseResponse(BaseModel, Generic[T]):
    limit: int
    skip: int
    total: int | None = None
    # sortField: str
    # sortOrder: str
    has_result: bool
    record: T | None = None
    records: list[T] | None = []

    @property
    def length(cls):
        """Custom prop to easily get result length"""
        return len(cls.records) if cls.records is not None else 0


class KimariteMatchesResponse(BaseResponse):
    record: None = None
    records: list[Match] | None = []


class RikishisResponse(BaseResponse):
    record: None = None
    records: list[Rikishi] | None = []


class RikishiResponse(BaseResponse):
    record: Rikishi | None = None
    records: None = None


class RikishiMatchesResponse(BaseResponse):
    record: None = None
    records: list[RikishiMatch] | None = []


class RikishiStatsResponse(BaseResponse):
    record: RikishiStats | None = None
    records: None = None


class RikishiVersusResponse(BaseResponse):
    record: RikishiVersus | None = None
    records: None = None


class BashoResponse(BaseResponse):
    record: BashoData | None = None
    records: None = None


class BashoBanzukeResponse(BaseResponse):
    record: BashoBanzuke | None = None
    records: None = None


class BashoTorikumiResponse(BaseResponse):
    record: BashoTorikumi | None = None
    records: None = None


class KimariteResponse(BaseResponse):
    record: None = None
    records: list[Kimarite] | None = []


class MeasurementResponse(BaseResponse):
    record: None = None
    records: list[Measurement] | None = []


class RankResponse(BaseResponse):
    record: None = None
    records: list[Rank] | None = []


class ShikonaResponse(BaseResponse):
    record: None = None
    records: list[Shikona] | None = []
