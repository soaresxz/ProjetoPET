from datetime import datetime
from pydantic import BaseModel, field_validator
import re


class PetCreate(BaseModel):
    pet_name:    str
    owner_name:  str
    owner_phone: str  
    owner_chat_id: str

    @field_validator("owner_phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not re.match(r"^\+\d{10,15}$", v):
            raise ValueError(
                "Telefone deve estar no formato E.164, ex: +5579999999999"
            )
        return v


class PetOut(BaseModel):
    pet_id:     str
    pet_name:   str
    owner_name: str
    owner_phone: str
    created_at: datetime

    model_config = {"from_attributes": True}


class PetPublic(BaseModel):
    """Dados expostos publicamente na página do QR code (sem telefone)."""
    pet_name:   str
    owner_name: str


class ScanIn(BaseModel):
    lat: float
    lng: float


class ScanOut(BaseModel):
    id:         int
    pet_id:     str
    lat:        float
    lng:        float
    scanned_at: datetime

    model_config = {"from_attributes": True}