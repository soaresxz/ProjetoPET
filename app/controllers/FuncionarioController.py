from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.dtos.funcionario.FuncionarioResponseDto import FuncionarioResponseDto
from app.dtos.funcionario.FuncionarioCreatedDto import FuncionarioCreatedDto
from app.service.FuncionarioService import login

router = APIRouter()

@router.post("/login", response_model=FuncionarioResponseDto, status_code=status.HTTP_200_OK)
async def login_usuario(request: FuncionarioCreatedDto, db: Session = Depends(get_db)):
    funcionario = login(request, db)
    return FuncionarioResponseDto.model_validate(funcionario)
