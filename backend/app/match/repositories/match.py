from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session
from app.match.dependencies.filter import MatchFilterParams
from app.match.dependencies.sorting import MatchSortingParams, SortField
from core.db.models import Match
from core.fastapi.dependencies.pagination import PaginationParams
from core.repositories.base import BaseRepository


class MatchRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Match, session)

    def get_by_ids(
        self,
        basho_id: str,
        day: str,
        east_id: int,
        west_id: int,
    ) -> Match | None:
        query = select(Match).where(
            Match.basho_id == basho_id,
            Match.day == day,
            Match.east_id == east_id,
            Match.basho_id == west_id,
        )
        query = self.query_options(query)
        result = self.session.execute(query)
        return result.scalars().first()

    def get_filtered(
        self,
        sorting: MatchSortingParams,
        filters: MatchFilterParams,
        pagination: PaginationParams,
    ) -> list[Match]:
        query = select(Match)

        if filters.basho_id:
            query = query.where(Match.basho_id == filters.basho_id)
        if filters.day:
            query = query.where(Match.day == filters.day)
        if filters.east_id:
            query = query.where(Match.east_id == filters.east_id)
        if filters.west_id:
            query = query.where(Match.west_id == filters.west_id)
        if filters.contains_ids:
            query = query.where(
                or_(
                    Match.east_id.in_(filters.contains_ids),
                    Match.west_id.in_(filters.contains_ids),
                )
            )
        if filters.contains_shikona:
            query = query.where(
                or_(
                    Match.east_shikona.in_(filters.contains_shikona),
                    Match.west_shikona.in_(filters.contains_shikona),
                )
            )
        if filters.contains_division:
            query = query.where(Match.division.in_(filters.contains_division))
        if filters.contains_rank:
            query = query.where(
                or_(
                    Match.east_rank.in_(filters.contains_rank),
                    Match.west_rank.in_(filters.contains_rank),
                )
            )
        
        sort_mapping = {
            SortField.basho_id: Match.basho_id,            
            SortField.day: Match.day,        
            SortField.match_no: Match.match_no,        
            SortField.east_id: Match.east_id,        
            SortField.west_id: Match.west_id,            
        }

        sort_column = sort_mapping.get(sorting.sort_field, Match.basho_id)
        query = query.order_by(sort_column.asc() if sorting.ascending else sort_column.desc())

        total_query = select(func.count()).select_from(query.subquery())
        total_result = self.session.execute(total_query)
        total_count = total_result.scalar()
        
        query = query.offset(pagination.skip).limit(pagination.limit)

        query = self.query_options(query)
        result = self.session.execute(query)
        return result.scalars().all(), total_count
