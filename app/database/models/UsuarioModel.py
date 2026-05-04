from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime 
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuario"

    ìd: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] 
    email: Mapped[str] = mapped_column(unique=True)
    senha: Mapped[str]
    telefone: Mapped[str] = mapped_column(unique=True)
    tipo: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    update_at: Mapped[datetime] = mapped_column(server_default=func.now())