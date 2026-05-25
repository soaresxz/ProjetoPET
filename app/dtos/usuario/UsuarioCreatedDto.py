from pydantic import BaseModel, ConfigDict, EmailStr

class UsuarioCreatedDto(BaseModel, EmailStr):
    nome: str
    email: EmailStr
    senha: str
    telefone: str

    model_config = ConfigDict(from_attributes=True)