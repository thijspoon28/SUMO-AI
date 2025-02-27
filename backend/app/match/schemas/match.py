from pydantic import ConfigDict, BaseModel


class CreateMatchSchema(BaseModel):
    basho_id: str
    division: str
    day: int
    match_no: int
    east_id: int
    east_shikona: str
    east_rank: str
    west_id: int
    west_shikona: str
    west_rank: str
    kimarite: str
    winner_id: int
    winner_en: str
    winner_jp: str | None = None


class MatchSchema(BaseModel):
    basho_id: str
    division: str
    day: int
    match_no: int
    east_id: int
    east_shikona: str
    east_rank: str
    west_id: int
    west_shikona: str
    west_rank: str
    kimarite: str
    winner_id: int
    winner_en: str
    winner_jp: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UpdateMatchSchema(BaseModel):
    basho_id: str
    division: str
    day: int
    match_no: int
    east_id: int
    east_shikona: str
    east_rank: str
    west_id: int
    west_shikona: str
    west_rank: str
    kimarite: str
    winner_id: int
    winner_en: str
    winner_jp: str | None = None
