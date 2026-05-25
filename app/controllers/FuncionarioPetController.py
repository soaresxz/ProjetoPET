from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.service.FuncionarioPetService import listarPets

router = APIRouter()

# acesso apenas do funcionario
@router.get("/pets", status_code=status.HTTP_200_OK)
async def listar_pets(db: Session = Depends(get_db)):
    return listarPets(db)

@router.get("/pets/{id}", status_code=status.HTTP_200_OK)
async def obter_pet(id: int):
    return ...

@router.post("/pets", status_code=status.HTTP_201_CREATED)
async def cadastrar_pet():
    return ...

@router.put("/pets/{id}", status_code=status.HTTP_200_OK)
async def atualizar_pet(id: int):
    return ...

@router.delete("/pets/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_pet(id: int):
    return ...