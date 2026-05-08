from fastapi import APIRouter, status

router = APIRouter()

@router.post("/login", status_code=status.HTTP_200_OK)
async def login_usuario():
    return ...

@router.get("/pets", status_code=status.HTTP_200_OK)
async def listar_pets_usuario():
    return ...

@router.get("/pets/{id}", status_code=status.HTTP_200_OK)
async def obter_pet_usuario(id: int):
    return ...

@router.put("/pets/{id}", status_code=status.HTTP_200_OK)
async def atualizar_pet_usuario(id: int):
    return ...