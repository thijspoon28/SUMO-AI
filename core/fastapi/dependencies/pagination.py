from core.config import config
from fastapi import Query
from typing import Optional


class PaginationParams:
    limit: int 
    skip: int
    
    def __init__(
        self,
        limit: int = Query(config.DEFAULT_LIMIT, alias="limit", ge=config.MIN_LIMIT, le=config.MAX_LIMIT),
        skip: int = Query(0, alias="skip", ge=0),
    ):
        self.limit = limit
        self.skip = skip


def get_pagination_params(
    limit: Optional[int] = Query(config.DEFAULT_LIMIT, ge=config.MIN_LIMIT, le=config.MAX_LIMIT),
    skip: Optional[int] = Query(0, ge=0),
):
    return PaginationParams(limit=limit, skip=skip)
