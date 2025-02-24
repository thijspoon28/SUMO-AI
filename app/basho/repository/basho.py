from sqlalchemy.orm import Session
from core.db.models import Basho
from core.repository.base import BaseRepository


class BashoRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Basho, session)
