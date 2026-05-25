from app.database.models.PetModel import Pet
from sqlalchemy.orm import Session

from app.dtos.pet import PetCreatedDto

def listarPets(db: Session):
    return db.query(Pet).all()

def cadastrarPet(pet: PetCreatedDto, db: Session):

    novo_pet = Pet(
        usuario_id=pet.usuario_id,
        nome_pet=pet.nome_pet,
        especie=pet.especie,
        raca=pet.raca,
        sexo=pet.sexo,
        idade=pet.idade,
        peso=pet.peso,
        tamanho=pet.tamanho,
        qr_code=pet.qr_code
    )

    db.add(novo_pet)
    db.commit()
    db.refresh(novo_pet)
    return novo_pet