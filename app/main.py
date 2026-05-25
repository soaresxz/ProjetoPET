from fastapi import FastAPI

from app.database.db import Base, engine
from app.database.models.FuncionarioModel import Funcionario
from app.database.models.UsuarioModel import Usuario
from app.database.models.PetModel import Pet
from app.database.models.LocalizacaoModel import Localizacao 
from app.controllers import FuncionarioPetController, FuncionarioUsuarioController, UsuarioController


app = FastAPI()

# linkando rotas ao FastAPI
app.include_router(FuncionarioUsuarioController.router, prefix="/admin", tags=["admin"])
app.include_router(FuncionarioPetController.router, prefix="/admin", tags=["admin"])
app.include_router(UsuarioController.router, prefix="/usuario", tags=["usuario"])

# criacao do models no banco de dados
Base.metadata.create_all(bind=engine)