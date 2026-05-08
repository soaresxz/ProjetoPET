from pydantic import BaseModel
from app.database.enums import SexoPet

class PetCreatedDto(BaseModel):
    nome_pet: str
    especie: str
    raca: str
    sexo: SexoPet
    idade: int
    peso: float
    tamanho: float