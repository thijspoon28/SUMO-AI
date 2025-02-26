from pydantic import BaseModel, ConfigDict


class MeasurementSchema(BaseModel):
    basho_id: str
    rikishi_id: int
    height: float
    weight: float

    model_config = ConfigDict(from_attributes=True)


class RankSchema(BaseModel):
    basho_id: str
    rikishi_id: int
    rank_value: int
    rank: str
    
    model_config = ConfigDict(from_attributes=True)


class ShikonaSchema(BaseModel):
    basho_id: str
    rikishi_id: int
    shikona_en: str
    shikona_jp: str | None = None
    
    model_config = ConfigDict(from_attributes=True)