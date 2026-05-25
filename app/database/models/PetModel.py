from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.db import Base
from app.database.enums.SexoPet import SexoPet
from typing import Optional

class Pet(Base):
    __tablename__ = "pets"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    nome_pet: Mapped[str] = mapped_column(nullable=False)
    especie: Mapped[str] = mapped_column(nullable=False)
    raca: Mapped[Optional[str]] 
    sexo: Mapped[SexoPet] = mapped_column(Enum(SexoPet), nullable=False)
    idade: Mapped[Optional[int]] = mapped_column(nullable=False)
    peso: Mapped[Optional[float]]
    tamanho: Mapped[Optional[float]]
    qr_code: Mapped[str] = mapped_column(unique=True, nullable=False)

    usuarios = relationship("Usuario", back_populates="pets")
    localizacoes = relationship("Localizacao", back_populates="pet")