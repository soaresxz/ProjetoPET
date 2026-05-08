from pydantic import BaseModel

class LocalizacaoDto(BaseModel):
    latitude: float
    longitude: float
    obs: str