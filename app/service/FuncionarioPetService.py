from app.database.models.PetModel import Pet
from sqlalchemy.orm import Session

from app.dtos.pet import PetCreatedDto

def listarPets(db: Session):
    return db.query(Pet).all()

def listarPet(id: int, db: Session):
    return db.query(Pet).filter(Pet.id == id).first()

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

def atualizarPet(id: int, pet: PetCreatedDto, db: Session):
    pet_existente = db.query(Pet).filter(Pet.id == id).first()

    pet_existente.usuario_id = pet.usuario_id
    pet_existente.nome_pet = pet.nome_pet
    pet_existente.especie = pet.especie
    pet_existente.raca = pet.raca
    pet_existente.sexo = pet.sexo
    pet_existente.idade = pet.idade
    pet_existente.peso = pet.peso
    pet_existente.tamanho = pet.tamanho
    pet_existente.qr_code = pet.qr_code

    db.commit()
    db.refresh(pet_existente)

    return pet_existente

def deletarPet(id: int, db: Session):
    pet_existente = db.query(Pet).filter(Pet.id == id).first()
    db.delete(pet_existente)
    db.commit()

    return pet_existente
    
