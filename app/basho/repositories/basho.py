from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from core.db.models import Basho
from core.repositories.base import Baserepositories


class BashoRepository(Baserepositories):
    def __init__(self, session: Session):
        super().__init__(Basho, session)

    def get_by_id(self, basho_id: str) -> Basho:
        query = select(Basho).where(Basho.id == basho_id)
        query = query.options(
            joinedload(Basho.matches),
        )

        result = self.session.execute(query)
        return result.scalars().first()
