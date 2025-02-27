from app.match.dependencies.filter import MatchFilterParams
from app.match.dependencies.sorting import MatchSortingParams
from app.match.schemas.match import CreateMatchSchema, MatchSchema, UpdateMatchSchema
from app.match.exceptions.match import MatchNotFoundException
from app.match.repositories.match import MatchRepository
from core.fastapi.dependencies.pagination import PaginationParams
from core.schemas.pagination import Pagination


class MatchService:
    def __init__(self, session) -> None:
        self.repo = MatchRepository(session)

    async def create_match(self, schema: CreateMatchSchema):
        raise NotImplementedError()

    async def delete_match(self, match_id: int) -> None:
        raise NotImplementedError()

    async def update_match(self, match_id: int, schema: UpdateMatchSchema):
        raise NotImplementedError()

    async def get_match(
        self,
        basho_id: str,
        day: str,
        east_id: int,
        west_id: int,
    ):
        match = self.repo.get_by_ids(basho_id, day, east_id, west_id)
        if not match:
            raise MatchNotFoundException

        return match

    async def get_matches(
        self,
        sorting: MatchSortingParams,
        filters: MatchFilterParams,
        pagination: PaginationParams,
    ) -> Pagination[MatchSchema]:
        matches, total = self.repo.get_filtered(sorting, filters, pagination)

        response = Pagination[MatchSchema](
            total=total,
            skip=pagination.skip,
            limit=pagination.limit,
            records=matches
        )

        return response
