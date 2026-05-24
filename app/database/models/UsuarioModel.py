from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime 
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuario"

    ìd: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    senha: Mapped[str] = mapped_column(nullable=False)
    telefone: Mapped[str] = mapped_column(unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    update_at: Mapped[datetime] = mapped_column(server_default=func.now())

    pets = relationship("Pet", back_populates="usuario")