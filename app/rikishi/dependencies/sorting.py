from fastapi import Query
from enum import Enum
from pydantic import BaseModel


class SortField(str, Enum):
    id = "id"
    sumodb_id = "sumodb_id"
    nsk_id = "nsk_id"
    birth_date = "birth_date"
    height = "height"
    weight = "weight"
    debut = "debut"
    intai = "intai"
    basho_count = "basho_count"
    total_absences = "total_absences"
    total_losses = "total_losses"
    total_matches = "total_matches"
    total_wins = "total_wins"
    yusho_count = "yusho_count"


class RikishiSortingParams(BaseModel):
    sort_field: SortField
    ascending: bool


def get_rikishi_sorting_params(
        sort_field: SortField = Query(SortField.id, alias="sort_field"),
        ascending: bool = Query(False, alias="ascending"),
    ):
    return RikishiSortingParams(
        sort_field=sort_field,
        ascending=ascending
    )
