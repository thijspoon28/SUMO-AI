from fastapi import Query
from enum import Enum
from pydantic import BaseModel


class SortField(str, Enum):
    basho_id = "basho_id"
    day = "day"
    match_no = "match_no"
    east_id = "east_id"
    west_id = "west_id"


class MatchSortingParams(BaseModel):
    sort_field: SortField
    ascending: bool


def get_match_sorting_params(
        sort_field: SortField = Query(SortField.basho_id, alias="sort_field"),
        ascending: bool = Query(False, alias="ascending"),
    ):
    return MatchSortingParams(
        sort_field=sort_field,
        ascending=ascending
    )
