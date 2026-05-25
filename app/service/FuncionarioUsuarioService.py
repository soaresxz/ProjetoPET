from app.database.models.UsuarioModel import Usuario
from sqlalchemy.orm import Session

from app.dtos.usuario import UsuarioCreatedDto 

def listarClientes(db: Session):
    return db.query(Usuario).all()

def listarCliente(id: int, db: Session):
    return db.query(Usuario).filter(Usuario.id == id).first()

def cadastrarCliente(usuario: UsuarioCreatedDto, db: Session):

    novo_cliente = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=usuario.senha,
        telefone=usuario.telefone
    )

    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    return novo_cliente