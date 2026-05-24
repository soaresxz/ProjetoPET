from sqlalchemy import ForeignKey, Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base
from typing import Optional


class Localizacao(Base):
    __tablename__ = "localizacoes"

    id: Mapped[int] = mapped_column(primary_key=True)
    pet_id: Mapped[int] = mapped_column(ForeignKey("pets.id"))
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    obs: Mapped[Optional[str]]
    data_hora: Mapped[datetime] = mapped_column(server_default=func.now())


    pet = relationship("Pet", back_populates="localizacoes")