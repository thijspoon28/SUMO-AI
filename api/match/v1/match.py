"""Match endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.match.dependencies.match import MatchFilterParams, get_match_filter_params
from app.match.schemas.match import MatchSchema
from app.match.services.match import MatchService
from core.fastapi.dependencies.database import get_db
from core.fastapi.dependencies.pagination import PaginationParams, get_pagination_params
from core.fastapi.dependencies.permission import (
    PermissionDependency,
    AllowAll,
)
from core.schemas.pagination import Pagination
from core.versioning import version


match_v1_router = APIRouter()


@match_v1_router.get(
    "",
    response_model=Pagination[MatchSchema],
    dependencies=[Depends(PermissionDependency(AllowAll))],
)
@version(1)
async def get_matches(
    filters: MatchFilterParams = Depends(get_match_filter_params),
    pagination: PaginationParams = Depends(get_pagination_params),
    session: Session = Depends(get_db),
):
    return await MatchService(session).get_matches(filters, pagination)


@match_v1_router.get(
    "/{match_id}",
    response_model=MatchSchema,
    dependencies=[Depends(PermissionDependency(AllowAll))],
)
@version(1)
async def get_match(match_id: str, session: Session = Depends(get_db)):
    return await MatchService(session).get_match(match_id)
