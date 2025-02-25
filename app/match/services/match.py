from app.match.schemas.match import CreateMatchSchema, UpdateMatchSchema
from app.auth.services.utils import get_password_hash
from app.match.exceptions.match import DuplicateMatchnameException, MatchNotFoundException
from app.match.repositories.match import MatchRepository
from core.db.models import Match


class MatchService:
    def __init__(self, session) -> None:
        self.repo = MatchRepository(session)

    async def get_by_matchname(self, matchname):
        return self.repo.get_by_matchname(matchname)

    async def create_match(self, schema: CreateMatchSchema):
        match = self.repo.get_by_matchname(schema.matchname)

        if match:
            raise DuplicateMatchnameException

        hashed_pass = get_password_hash(schema.password)
        match = Match(matchname=schema.matchname, password=hashed_pass)
        return self.repo.create(match)

    async def delete_match(self, match_id: int) -> None:
        match = self.repo.get_by_id(match_id)
        if not match:
            raise MatchNotFoundException
        
        self.repo.delete(match)

    async def update_match(self, match_id: int, schema: UpdateMatchSchema):
        match = self.repo.get_by_id(match_id)
        if not match:
            raise MatchNotFoundException
        
        hashed_pass = get_password_hash(schema.password)
        params = {"matchname": schema.matchname, "password": hashed_pass}
        
        self.repo.update_by_id(match_id, params)
        return self.repo.get_by_id(match_id)
    
    async def get_match(self, match_id: int):
        match = self.repo.get_by_id(match_id)
        if not match:
            raise MatchNotFoundException
        
        return match
    
    async def get_matchs(self):
        return self.repo.get()
