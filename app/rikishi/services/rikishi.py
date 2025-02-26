from app.rikishi.schemas.rikishi import RikishiSchema, CreateRikishiSchema, UpdateRikishiSchema
from app.rikishi.exceptions.rikishi import RikishiNotFoundException
from app.rikishi.repositories.rikishi import RikishiRepository
from core.fastapi.dependencies.pagination import PaginationParams
from core.schemas.pagination import Pagination


class RikishiService:
    def __init__(self, session) -> None:
        self.repo = RikishiRepository(session)

    async def create_rikishi(self, schema: CreateRikishiSchema):
        raise NotImplementedError()


    async def delete_rikishi(self, rikishi_id: int) -> None:
        raise NotImplementedError()


    async def update_rikishi(self, rikishi_id: int, schema: UpdateRikishiSchema):
        raise NotImplementedError()
    
    async def get_rikishi(self, rikishi_id: int) -> RikishiSchema:
        rikishi = self.repo.get_by_id(rikishi_id)
        if not rikishi:
            raise RikishiNotFoundException
        
        return rikishi
    
    async def get_rikishis(self, pagination: PaginationParams) -> Pagination[RikishiSchema]:
        rikishis, total = self.repo.get_filtered(pagination)

        print(rikishis[0])
        print(rikishis[0].bashos)

        response = Pagination[RikishiSchema](
            total=total,
            skip=pagination.skip,
            limit=pagination.limit,
            records=rikishis
        )

        return response
