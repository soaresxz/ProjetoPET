from pydantic import BaseModel, ConfigDict
from app.database.enums.SexoPet import SexoPet

class PetResponseDto(BaseModel):
    id: int
    usuario_id: int
    nome_pet: str
    especie: str
    raca: str
    sexo: SexoPet
    idade: int
    peso: float
    tamanho: float
    qr_code: str

    model_config = ConfigDict(from_attributes=True)