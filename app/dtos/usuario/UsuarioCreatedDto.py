from pydantic import BaseModel, EmailStr

class UsuarioCreatedDto(BaseModel, EmailStr):
    nome: str
    email: EmailStr
    senha: str
    telefone: str

    