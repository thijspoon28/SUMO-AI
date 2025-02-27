from pydantic import BaseModel, ConfigDict

from app.rikishi.schemas.rikishi import RikishiSchema


class RikishiBashoSchema(BaseModel):
    rikishi_id: int
    basho_id: str
    special_prize: str | None = None
    yusho: str | None = None
    rikishi: RikishiSchema
    
    model_config = ConfigDict(from_attributes=True)
