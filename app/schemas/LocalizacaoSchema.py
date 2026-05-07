from pydantic import BaseModel

class LocalizacaoSchema(BaseModel):
    latitude: float
    longitude: float
    obs: str