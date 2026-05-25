from pydantic import BaseModel, ConfigDict, EmailStr

class UsuarioResponseDto(BaseModel, EmailStr):
    id: int
    nome: str
    email: EmailStr
    telefone: str

    model_config = ConfigDict(from_attributes=True)