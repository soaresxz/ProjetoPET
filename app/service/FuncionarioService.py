from sqlalchemy.orm import Session

from app.database.models.FuncionarioModel import Funcionario
from app.dtos.funcionario.FuncionarioCreatedDto import FuncionarioCreatedDto


def login(funcionario: FuncionarioCreatedDto, db: Session):
    funcionario = db.query(Funcionario).filter(Funcionario.email == funcionario.email,
                                               Funcionario.senha == funcionario.senha).first()

    return funcionario