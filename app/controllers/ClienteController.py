from app.service.ClienteService import listar_clientes
from fastapi import APIRouter, status

router = APIRouter()

# acesso apenas do funcionario
@router.get("/clientes", status_code=status.HTTP_200_OK)
async def listar_cliente():
    return listar_clientes()

@router.get("/clientes/{id}", status_code=status.HTTP_200_OK)
async def obter_cliente(id: int):
    return ...

@router.post("/clientes", status_code=status.HTTP_201_CREATED)
async def cadastrar_cliente():
    return ...

@router.put("/clientes/{id}", status_code=status.HTTP_200_OK)
async def atualizar_cliente(id: int):
    return ...

@router.delete("/clientes/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_cliente(id: int):
    return ...
