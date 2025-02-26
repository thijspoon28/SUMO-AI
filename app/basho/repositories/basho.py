from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload
from app.basho.dependencies.sorting import BashoSortingParams, SortField
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
        sorting: BashoSortingParams,
        pagination: PaginationParams,
    ) -> tuple[list[Basho], int]:
        query = select(Basho)
        
        sort_mapping = {
            SortField.id: Basho.id,
            SortField.date: Basho.date,
            SortField.start_date: Basho.start_date,
            SortField.end_date: Basho.end_date,
        }

        sort_column = sort_mapping.get(sorting.sort_field, Basho.id)
        query = query.order_by(sort_column.asc() if sorting.ascending else sort_column.desc())

        total_query = select(func.count()).select_from(query.subquery())
        total_result = self.session.execute(total_query)
        total_count = total_result.scalar()

        query = query.offset(pagination.skip).limit(pagination.limit)

        query = self.query_options(query)
        result = self.session.execute(query)
        return result.scalars().all(), total_count

