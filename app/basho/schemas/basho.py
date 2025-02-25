from datetime import datetime
from pydantic import ConfigDict, BaseModel

from app.match.schemas.match import MatchSchema


class CreateBashoSchema(BaseModel):
    id: str
    date: str
    start_date: datetime
    end_date: datetime
    # rikishis: list
    # matches: list


class BashoSchema(BaseModel):
    id: str
    date: str
    start_date: datetime
    end_date: datetime
    # rikishis: list
    matches: list[MatchSchema]

    model_config = ConfigDict(from_attributes=True)


class UpdateBashoSchema(BaseModel):
    id: str
    date: str
    start_date: datetime
    end_date: datetime
