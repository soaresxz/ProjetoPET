from app.database.models.PetModel import Pet
from sqlalchemy.orm import Session

def listarPets(db: Session):
    return db.query(Pet).all()