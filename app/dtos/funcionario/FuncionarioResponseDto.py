from pydantic import BaseModel, ConfigDict


class FuncionarioResponseDto(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)
