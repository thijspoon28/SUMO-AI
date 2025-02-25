from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload
from core.db.models import Basho
from core.fastapi.dependencies.pagination import PaginationParams
from core.repositories.base import BaseRepository


class BashoRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Basho, session)

    def get_by_id(self, basho_id: str) -> Basho:
        query = select(Basho).where(Basho.id == basho_id)
        query = query.options(
            joinedload(Basho.matches),
        )

        result = self.session.execute(query)
        return result.scalars().first()

    def get_filtered(
        self,
        pagination: PaginationParams,
    ) -> tuple[list[Basho], int]:
        query = select(Basho)
        
        total_query = select(func.count()).select_from(query.subquery())
        total_result = self.session.execute(total_query)
        total_count = total_result.scalar()

        query = query.offset(pagination.skip).limit(pagination.limit)

        query = self.query_options(query)
        result = self.session.execute(query)
        return result.scalars().all(), total_count

