from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Pet(Base):
    __tablename__ = "pets"

    id           = Column(Integer, primary_key=True, index=True)
    pet_id       = Column(String, unique=True, index=True, nullable=False)  # ex: "pet_01"
    pet_name     = Column(String, nullable=False)
    owner_name   = Column(String, nullable=False)
    owner_phone  = Column(String, nullable=False)  # formato E.164: +5579999999999
    created_at   = Column(DateTime(timezone=True), server_default=func.now())

    scans = relationship("Scan", back_populates="pet", cascade="all, delete-orphan")


class Scan(Base):
    __tablename__ = "scans"

    id         = Column(Integer, primary_key=True, index=True)
    pet_id     = Column(String, ForeignKey("pets.pet_id"), nullable=False)
    lat        = Column(Float, nullable=False)
    lng        = Column(Float, nullable=False)
    scanned_at = Column(DateTime(timezone=True), server_default=func.now())

    pet = relationship("Pet", back_populates="scans")