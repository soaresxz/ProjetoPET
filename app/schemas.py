from datetime import datetime
from pydantic import BaseModel


class LocationIn(BaseModel):
    """Payload recebido via MQTT (parsed do JSON)."""
    pet_id: str
    lat: float
    lng: float
    speed: float = 0.0
    step: int = 0


class LocationOut(BaseModel):
    """Resposta da API com dados de localização."""
    id: int
    pet_id: str
    lat: float
    lng: float
    speed: float
    step: int
    received_at: datetime

    model_config = {"from_attributes": True}


class PetSummary(BaseModel):
    """Resumo de um pet: última localização + total de registros."""
    pet_id: str
    latest: LocationOut
    total_records: int