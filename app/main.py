"""
Pet QR Tracker — Backend FastAPI

Rotas:
  GET  /pet/{pet_id}           → página pública do QR (quem achou o pet vê isso)
  POST /scan/{pet_id}          → recebe localização de quem escaneou → envia SMS
  POST /admin/pets             → cadastra um pet
  GET  /admin/pets             → lista todos os pets
  GET  /admin/pets/{pet_id}/qr → gera e baixa o QR code PNG da coleira
  GET  /admin/pets/{pet_id}/scans → histórico de escaneamentos
  DELETE /admin/pets/{pet_id}  → remove pet
"""

import logging
import os
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from sqlalchemy.orm import Session

from app.service.qr_service import generate_qr_bytes
from app.service.sms import send_scan_sms

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s [%(levelname)s] %(message)s",
# )
# logger = logging.getLogger(__name__)


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     os.makedirs("data", exist_ok=True)
#     Base.metadata.create_all(bind=engine)
#     logger.info("Banco de dados inicializado.")
#     yield


app = FastAPI()


# # ─── Página pública: aberta por quem escaneia a coleira ──────────────────────
# @app.get("/pet/{pet_id}", response_class=HTMLResponse, tags=["público"])
# def pet_scan_page(pet_id: str, db: Session = Depends(get_db)):
#     """
#     Página que abre no celular de quem escaneia o QR da coleira.
#     Mostra dados do pet e botão para enviar localização ao dono.
#     """
#     pet = db.query(Pet).filter(Pet.pet_id == pet_id).first()
#     if not pet:
#         raise HTTPException(status_code=404, detail="Pet não encontrado.")

#     # Lê o template e substitui as variáveis manualmente (sem Jinja2)
#     template_path = os.path.join(os.path.dirname(__file__), "templates", "pet_scan.html")
#     with open(template_path, "r", encoding="utf-8") as f:
#         html = f.read()

#     html = html.replace("{{ pet_id }}",    pet.pet_id)
#     html = html.replace("{{ pet_name }}",  pet.pet_name)
#     html = html.replace("{{ owner_name }}", pet.owner_name)

#     return HTMLResponse(content=html)


# # ─── Recebe localização de quem escaneou e envia SMS ─────────────────────────
# @app.post("/scan/{pet_id}", response_model=ScanOut, tags=["público"])
# def receive_scan(pet_id: str, data: ScanIn, db: Session = Depends(get_db)):
#     """
#     Chamado pelo browser de quem achou o pet.
#     Salva a localização e envia SMS ao dono.
#     """
#     pet = db.query(Pet).filter(Pet.pet_id == pet_id).first()
#     if not pet:
#         raise HTTPException(status_code=404, detail="Pet não encontrado.")

#     # Salva o scan no banco
#     scan = Scan(pet_id=pet_id, lat=data.lat, lng=data.lng)
#     db.add(scan)
#     db.commit()
#     db.refresh(scan)

#     logger.info(
#         f"Scan registrado → pet={pet_id} lat={data.lat:.6f} lng={data.lng:.6f}"
#     )

#     # Envia SMS ao dono
#     sms_ok = send_scan_sms(
#         owner_phone=pet.owner_phone,
#         pet_name=pet.pet_name,
#         lat=data.lat,
#         lng=data.lng,
#     )

#     if not sms_ok:
#         logger.warning(f"SMS não enviado para o dono do pet {pet_id}")

#     return scan


# # ─── Admin: cadastrar pet ─────────────────────────────────────────────────────
# @app.post("/admin/pets", response_model=PetOut, status_code=201, tags=["admin"])
# def create_pet(data: PetCreate, db: Session = Depends(get_db)):
#     """Cadastra um novo pet no sistema."""
#     if db.query(Pet).filter(Pet.pet_id == data.pet_id).first():
#         raise HTTPException(
#             status_code=409,
#             detail=f"Pet com id '{data.pet_id}' já existe.",
#         )

#     pet = Pet(
#         pet_id=data.pet_id,
#         pet_name=data.pet_name,
#         owner_name=data.owner_name,
#         owner_phone=data.owner_phone,
#     )
#     db.add(pet)
#     db.commit()
#     db.refresh(pet)
#     logger.info(f"Pet cadastrado: {pet.pet_id} — {pet.pet_name}")
#     return pet


# # ─── Admin: listar pets ───────────────────────────────────────────────────────
# @app.get("/admin/pets", response_model=list[PetOut], tags=["admin"])
# def list_pets(db: Session = Depends(get_db)):
#     """Lista todos os pets cadastrados."""
#     return db.query(Pet).order_by(Pet.created_at.desc()).all()


# # ─── Admin: gerar QR code PNG ─────────────────────────────────────────────────
# @app.get("/admin/pets/{pet_id}/qr", tags=["admin"])
# def get_qr_code(pet_id: str, db: Session = Depends(get_db)):
#     """
#     Gera e retorna o QR code PNG da coleira do pet.
#     Baixe e imprima para colocar na coleira.
#     """
#     if not db.query(Pet).filter(Pet.pet_id == pet_id).first():
#         raise HTTPException(status_code=404, detail="Pet não encontrado.")

#     qr_bytes = generate_qr_bytes(pet_id)
#     return Response(
#         content=qr_bytes,
#         media_type="image/png",
#         headers={"Content-Disposition": f'attachment; filename="qr_{pet_id}.png"'},
#     )


# # ─── Admin: histórico de scans ────────────────────────────────────────────────
# @app.get("/admin/pets/{pet_id}/scans", response_model=list[ScanOut], tags=["admin"])
# def get_scans(pet_id: str, db: Session = Depends(get_db)):
#     """Retorna todos os escaneamentos registrados para um pet."""
#     if not db.query(Pet).filter(Pet.pet_id == pet_id).first():
#         raise HTTPException(status_code=404, detail="Pet não encontrado.")

#     return (
#         db.query(Scan)
#         .filter(Scan.pet_id == pet_id)
#         .order_by(Scan.scanned_at.desc())
#         .all()
#     )


# # ─── Admin: remover pet ───────────────────────────────────────────────────────
# @app.delete("/admin/pets/{pet_id}", tags=["admin"])
# def delete_pet(pet_id: str, db: Session = Depends(get_db)):
#     """Remove um pet e todo seu histórico de scans."""
#     pet = db.query(Pet).filter(Pet.pet_id == pet_id).first()
#     if not pet:
#         raise HTTPException(status_code=404, detail="Pet não encontrado.")

#     db.delete(pet)
#     db.commit()
#     return {"detail": f"Pet '{pet_id}' removido com sucesso."}


# # ─── Health check ─────────────────────────────────────────────────────────────
# @app.get("/", tags=["status"])
# def health_check():
#     return {"status": "online", "service": "pet-qr-tracker"}