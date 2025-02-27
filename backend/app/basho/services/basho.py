from app.basho.dependencies.sorting import BashoSortingParams
from app.basho.schemas.basho import BashoSchema, CreateBashoSchema, UpdateBashoSchema
from app.basho.exceptions.basho import BashoNotFoundException
from app.basho.repositories.basho import BashoRepository
from core.fastapi.dependencies.pagination import PaginationParams
from core.schemas.pagination import Pagination


class BashoService:
    def __init__(self, session) -> None:
        self.repo = BashoRepository(session)

    async def create_basho(self, schema: CreateBashoSchema):
        raise NotImplementedError()

    async def delete_basho(self, basho_id: str) -> None:
        raise NotImplementedError()

    async def update_basho(self, basho_id: str, schema: UpdateBashoSchema):
        raise NotImplementedError()

    async def get_basho(self, basho_id: str) -> BashoSchema:
        basho = self.repo.get_by_id(basho_id)
        if not basho:
            raise BashoNotFoundException

        return basho

    async def get_bashos(
        self,
        sorting: BashoSortingParams,
        pagination: PaginationParams,
    ) -> Pagination[BashoSchema]:
        bashos, total = self.repo.get_filtered(sorting, pagination)

        response = Pagination[BashoSchema](
            total=total,
            skip=pagination.skip,
            limit=pagination.limit,
            records=bashos,
        )

        return response
