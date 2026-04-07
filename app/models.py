from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Location(Base):
    __tablename__ = "locations"

    id        = Column(Integer, primary_key=True, index=True)
    pet_id    = Column(String, index=True, nullable=False)
    lat       = Column(Float, nullable=False)
    lng       = Column(Float, nullable=False)
    speed     = Column(Float, default=0.0)
    step      = Column(Integer, default=0)
    received_at = Column(DateTime(timezone=True), server_default=func.now())