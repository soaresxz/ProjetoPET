from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime 
from app.database import Base

class Funcionario(Base):
    __tablename__ = "funcionarios"

    ìd: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    senha: Mapped[str] = mapped_column(nullable=False)