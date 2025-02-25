from sqlalchemy.orm import Session
from core.db.models import Match
from core.repositories.base import Baserepositories


class MatchRepository(Baserepositories):
    def __init__(self, session: Session):
        super().__init__(Match, session)
