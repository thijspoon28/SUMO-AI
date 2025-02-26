from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload
from app.rikishi.dependencies.sorting import RikishiSortingParams, SortField
from core.db.models import Rikishi
from core.fastapi.dependencies.pagination import PaginationParams
from core.repositories.base import BaseRepository


class RikishiRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Rikishi, session)

    def get_by_id(self, rikishi_id: int) -> Rikishi:
        query = select(Rikishi).where(Rikishi.id == rikishi_id)
        query = query.options(
            joinedload(Rikishi.measurement_history),
            joinedload(Rikishi.rank_history),
            joinedload(Rikishi.shikona_history),
            joinedload(Rikishi.bashos),
            joinedload(Rikishi.east_matches),
            joinedload(Rikishi.west_matches),
        )

        result = self.session.execute(query)
        return result.scalars().first()

    def get_filtered(
        self,
        sorting: RikishiSortingParams,
        pagination: PaginationParams,
    ) -> tuple[list[Rikishi], int]:
        query = select(Rikishi)
        
        sort_mapping = {
            SortField.id: Rikishi.id,
            SortField.sumodb_id: Rikishi.sumodb_id,
            SortField.nsk_id: Rikishi.nsk_id,
            SortField.birth_date: Rikishi.birth_date,
            SortField.height: Rikishi.height,
            SortField.weight: Rikishi.weight,
            SortField.debut: Rikishi.debut,
            SortField.intai: Rikishi.intai,
            SortField.basho_count: Rikishi.basho_count,
            SortField.total_absences: Rikishi.total_absences,
            SortField.total_losses: Rikishi.total_losses,
            SortField.total_matches: Rikishi.total_matches,
            SortField.total_wins: Rikishi.total_wins,
            SortField.yusho_count: Rikishi.yusho_count,
        }

        sort_column = sort_mapping.get(sorting.sort_field, Rikishi.id)
        query = query.order_by(sort_column.asc() if sorting.ascending else sort_column.desc())
        
        total_query = select(func.count()).select_from(query.subquery())
        total_result = self.session.execute(total_query)
        total_count = total_result.scalar()

        query = query.offset(pagination.skip).limit(pagination.limit)

        query = self.query_options(query)
        result = self.session.execute(query)
        return result.scalars().all(), total_count

