from pydantic import BaseModel, EmailStr

class UsuarioResponseDto(BaseModel, EmailStr):
    id: int
    nome: str
    email: EmailStr
    telefone: str