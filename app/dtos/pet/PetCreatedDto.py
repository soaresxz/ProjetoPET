from pydantic import BaseModel
from app.database.enums.SexoPet import SexoPet

class PetCreatedDto(BaseModel):
    usuario_id: int
    nome_pet: str
    especie: str
    raca: str
    sexo: SexoPet
    idade: int
    peso: float
    tamanho: float
    qr_code: str

    