from pydantic import BaseModel


class FuncionarioCreatedDto(BaseModel):
    email: str
    senha: str
