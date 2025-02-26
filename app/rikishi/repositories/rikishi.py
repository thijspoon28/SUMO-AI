from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload
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
        pagination: PaginationParams,
    ) -> tuple[list[Rikishi], int]:
        query = select(Rikishi)
        
        total_query = select(func.count()).select_from(query.subquery())
        total_result = self.session.execute(total_query)
        total_count = total_result.scalar()

        query = query.offset(pagination.skip).limit(pagination.limit)

        query = self.query_options(query)
        result = self.session.execute(query)
        return result.scalars().all(), total_count

