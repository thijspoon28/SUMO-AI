"""Basho endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.basho.schemas.basho import BashoSchema
from app.basho.services.basho import BashoService
from core.fastapi.dependencies.database import get_db
from core.fastapi.dependencies.permission import (
    PermissionDependency,
    AllowAll,
)
from core.versioning import version


basho_v1_router = APIRouter()


@basho_v1_router.get(
    "",
    response_model=list[BashoSchema],
    dependencies=[Depends(PermissionDependency(AllowAll))],
)
@version(1)
async def get_bashos(session: Session = Depends(get_db)):
    return await BashoService(session).get_bashos()


@basho_v1_router.get(
    "/{basho_id}",
    response_model=BashoSchema,
    dependencies=[Depends(PermissionDependency(AllowAll))],
)
@version(1)
async def get_basho(basho_id: str, session: Session = Depends(get_db)):
    return await BashoService(session).get_basho(basho_id)
