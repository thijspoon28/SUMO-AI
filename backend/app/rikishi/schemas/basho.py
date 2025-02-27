from pydantic import BaseModel, ConfigDict


class RikishiBashoSchema(BaseModel):
    rikishi_id: int
    basho_id: str
    special_prize: str | None = None
    yusho: str | None = None
    
    model_config = ConfigDict(from_attributes=True)
