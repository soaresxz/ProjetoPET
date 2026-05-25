from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.dtos.pet.PetCreatedDto import PetCreatedDto
from app.dtos.pet.PetResponseDto import PetResponseDto
from app.service.FuncionarioPetService import atualizarPet, cadastrarPet, listarPet, listarPets

router = APIRouter()

# acesso apenas do funcionario
@router.get("/pets", response_model=list[PetResponseDto], status_code=status.HTTP_200_OK)
async def listar_pets(db: Session = Depends(get_db)):
    return listarPets(db)

@router.get("/pets/{id}", response_model=PetResponseDto, status_code=status.HTTP_200_OK)
async def obter_pet(id: int, db: Session = Depends(get_db)):
    return listarPet(id, db)

@router.post("/pets", response_model=PetResponseDto, status_code=status.HTTP_201_CREATED)
async def cadastrar_pet(request: PetCreatedDto, db: Session = Depends(get_db)):
    pets = cadastrarPet(request, db)
    return PetResponseDto.model_validate(pets)

@router.put("/pets/{id}", response_model=PetResponseDto, status_code=status.HTTP_200_OK)
async def atualizar_pet(id: int, request: PetCreatedDto, db: Session = Depends(get_db)):
    pet = atualizarPet(id, request, db)
    return PetResponseDto.model_validate(pet)

@router.delete("/pets/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_pet(id: int):
    return ...