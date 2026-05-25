from sqlalchemy.orm import Session

from app.database.db import get_db
from app.dtos.usuario.UsuarioResponseDto import UsuarioResponseDto
from app.dtos.usuario.UsuarioCreatedDto import UsuarioCreatedDto
from app.service.FuncionarioUsuarioService import cadastrarCliente, listarCliente, listarClientes
from fastapi import APIRouter, Depends, status

router = APIRouter()

# acesso apenas do funcionario
@router.get("/clientes", response_model=list[UsuarioResponseDto], status_code=status.HTTP_200_OK)
async def listar_cliente(db: Session = Depends(get_db)):
    return listarClientes(db)

@router.get("/clientes/{id}", response_model=UsuarioResponseDto, status_code=status.HTTP_200_OK)
async def obter_cliente(id: int, db: Session = Depends(get_db)):
    return listarCliente(id, db)

@router.post("/clientes", response_model=UsuarioResponseDto, status_code=status.HTTP_201_CREATED)
async def cadastrar_cliente(request: UsuarioCreatedDto, db: Session = Depends(get_db)):
    cliente = cadastrarCliente(request, db)
    return UsuarioResponseDto.model_validate(cliente)

@router.put("/clientes/{id}", status_code=status.HTTP_200_OK)
async def atualizar_cliente(id: int):
    return ...

@router.delete("/clientes/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_cliente(id: int):
    return ...
