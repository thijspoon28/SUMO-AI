from fastapi import Query


class MatchFilterParams:
    basho_id: str | None
    day: int | None
    east_id: int | None
    west_id: int | None
    contains_ids: list[int] | None
    contains_shikona: list[str] | None
    contains_division: list[str] | None
    contains_rank: list[str] | None

    def __init__(
        self,
        basho_id: str | None = Query(None, alias="basho_id"),
        day: int | None = Query(None, alias="day"),
        east_id: int | None = Query(None, alias="east_id"),
        west_id: int | None = Query(None, alias="west_id"),
        contains_ids: list[int] | None = Query(None, alias="contains_ids"),
        contains_shikona: list[str] | None = Query(None, alias="contains_shikona"),
        contains_division: list[str] | None = Query(None, alias="contains_division"),
        contains_rank: list[str] | None = Query(None, alias="contains_rank"),
    ):
        self.basho_id = basho_id
        self.day = day
        self.east_id = east_id
        self.west_id = west_id
        self.contains_ids = contains_ids
        self.contains_shikona = contains_shikona
        self.contains_division = contains_division
        self.contains_rank = contains_rank


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
