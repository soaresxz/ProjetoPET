from sqlalchemy import ForeignKey, Mapped, mapped_column
from sqlalchemy.orm import relationship
from app.database import Base
from typing import Optional

class Pet(Base):
    __tablename__ = "pet"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome_pet: Mapped[str]
    especie: Mapped[str]
    raca: Mapped[str]
    sexo: Mapped[str]
    idade: Mapped[Optional[int]]
    peso: Mapped[Optional[float]]
    tamanho: Mapped[Optional[float]]
    qr_code: Mapped[str] = mapped_column(unique=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"))
    usuario = relationship("Usuario")