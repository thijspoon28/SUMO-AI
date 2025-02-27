from fastapi import Query
from pydantic import BaseModel


class MatchFilterParams(BaseModel):
    basho_id: str | None
    day: int | None
    east_id: int | None
    west_id: int | None
    contains_ids: list[int] | None
    contains_shikona: list[str] | None
    contains_division: list[str] | None
    contains_rank: list[str] | None


def get_match_filter_params(
    basho_id: str | None = Query(None, alias="basho_id"),
    day: int | None = Query(None, alias="day"),
    east_id: int | None = Query(None, alias="east_id"),
    west_id: int | None = Query(None, alias="west_id"),
    contains_ids: list[int] | None = Query(None, alias="contains_ids"),
    contains_shikona: list[str] | None = Query(None, alias="contains_shikona"),
    contains_division: list[str] | None = Query(None, alias="contains_division"),
    contains_rank: list[str] | None = Query(None, alias="contains_rank"),
):
    return MatchFilterParams(
        basho_id=basho_id,
        day=day,
        east_id=east_id,
        west_id=west_id,
        contains_ids=contains_ids,
        contains_shikona=contains_shikona,
        contains_division=contains_division,
        contains_rank=contains_rank,
    )
