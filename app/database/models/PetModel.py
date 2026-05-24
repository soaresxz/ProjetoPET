from sqlalchemy import ForeignKey, Mapped, mapped_column
from sqlalchemy.orm import relationship
from app.database import Base
from app.database.enums import SexoPet
from typing import Optional

class Pet(Base):
    __tablename__ = "pets"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"))
    nome_pet: Mapped[str] = mapped_column(nullable=False)
    especie: Mapped[str] = mapped_column(nullable=False)
    raca: Mapped[Optional[str]] 
    sexo: Mapped[SexoPet] = mapped_column(nullable=False)
    idade: Mapped[Optional[int]] = mapped_column(nullable=False)
    peso: Mapped[Optional[float]]
    tamanho: Mapped[Optional[float]]
    qr_code: Mapped[str] = mapped_column(unique=True, nullable=False)

    usuario = relationship("Usuario", back_populates="pets")
    localizacoes = relationship("Localizacao", back_populates="pet")