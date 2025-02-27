from fastapi import Query
from enum import Enum
from pydantic import BaseModel


class SortField(str, Enum):
    id = "id"
    date = "date"
    start_date = "start_date"
    end_date = "end_date"


class BashoSortingParams(BaseModel):
    sort_field: SortField
    ascending: bool


def get_basho_sorting_params(
        sort_field: SortField = Query(SortField.id, alias="sort_field"),
        ascending: bool = Query(False, alias="ascending"),
    ):
    return BashoSortingParams(
        sort_field=sort_field,
        ascending=ascending
    )
