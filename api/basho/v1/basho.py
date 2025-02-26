"""Basho endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.basho.dependencies.sorting import BashoSortingParams, get_basho_sorting_params
from app.basho.schemas.basho import BashoSchema, FullBashoSchema
from app.basho.services.basho import BashoService
from core.fastapi.dependencies.database import get_db
from core.fastapi.dependencies.pagination import PaginationParams, get_pagination_params
from core.fastapi.dependencies.permission import (
    PermissionDependency,
    AllowAll,
)
from core.schemas.pagination import Pagination
from core.versioning import version


basho_v1_router = APIRouter()


@basho_v1_router.get(
    "",
    response_model=Pagination[BashoSchema],
    dependencies=[Depends(PermissionDependency(AllowAll))],
)
@version(1)
async def get_bashos(
    sorting: BashoSortingParams = Depends(get_basho_sorting_params),
    pagination: PaginationParams = Depends(get_pagination_params),
    session: Session = Depends(get_db),
):
    return await BashoService(session).get_bashos(sorting, pagination)


@basho_v1_router.get(
    "/{basho_id}",
    response_model=FullBashoSchema,
    dependencies=[Depends(PermissionDependency(AllowAll))],
)
@version(1)
async def get_basho(basho_id: str, session: Session = Depends(get_db)):
    return await BashoService(session).get_basho(basho_id)
