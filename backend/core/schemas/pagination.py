from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class Pagination(BaseModel, Generic[T]):
    total: int
    skip: int
    limit: int
    records: list[T]
