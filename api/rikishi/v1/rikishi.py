"""Rikishi endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.rikishi.schemas.rikishi import FullRikishiSchema, RikishiSchema
from app.rikishi.services.rikishi import RikishiService
from core.fastapi.dependencies.database import get_db
from core.fastapi.dependencies.pagination import PaginationParams, get_pagination_params
from core.fastapi.dependencies.permission import (
    PermissionDependency,
    AllowAll,
)
from core.schemas.pagination import Pagination
from core.versioning import version


rikishi_v1_router = APIRouter()


@rikishi_v1_router.get(
    "",
    response_model=Pagination[RikishiSchema],
    dependencies=[Depends(PermissionDependency(AllowAll))],
)
@version(1)
async def get_rikishis(
    pagination: PaginationParams = Depends(get_pagination_params),
    session: Session = Depends(get_db),
):
    return await RikishiService(session).get_rikishis(pagination)


@rikishi_v1_router.get(
    "/{rikishi_id}",
    response_model=FullRikishiSchema,
    dependencies=[Depends(PermissionDependency(AllowAll))],
)
@version(1)
async def get_rikishi(rikishi_id: str, session: Session = Depends(get_db)):
    return await RikishiService(session).get_rikishi(rikishi_id)
