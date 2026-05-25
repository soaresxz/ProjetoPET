from fastapi import APIRouter, status

router = APIRouter()

@router.post("/login", status_code=status.HTTP_200_OK)
async def login_usuario():
    return ...
