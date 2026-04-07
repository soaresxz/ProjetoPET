"""
Pet Tracker — Backend FastAPI

Rotas disponíveis:
  GET  /                              → health check
  GET  /pets                          → lista todos os pets com última localização
  GET  /pets/{pet_id}/location        → última localização do pet
  GET  /pets/{pet_id}/history         → histórico de trajeto (paginado)
  DELETE /pets/{pet_id}/history       → apaga histórico de um pet
"""

import logging
import os
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Location
from app.mqtt_subscriber import start_mqtt_subscriber
from app.schemas import LocationOut, PetSummary

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Executado na inicialização e no encerramento da aplicação."""
    # Garante que a pasta /data existe (volume Docker)
    os.makedirs("data", exist_ok=True)

    # Cria tabelas no banco se não existirem
    Base.metadata.create_all(bind=engine)
    logger.info("Banco de dados inicializado.")

    # Inicia o subscriber MQTT em background
    start_mqtt_subscriber()

    yield  # aplicação rodando

    logger.info("Encerrando aplicação.")


app = FastAPI(
    title="Pet Tracker API",
    description="Rastreamento de pets via IoT + MQTT",
    version="1.0.0",
    lifespan=lifespan,
)


# ─── Health check ─────────────────────────────────────────────────────────────
@app.get("/", tags=["status"])
def health_check():
    return {"status": "online", "service": "pet-tracker"}


# ─── Lista todos os pets ──────────────────────────────────────────────────────
@app.get("/pets", response_model=list[PetSummary], tags=["pets"])
def list_pets(db: Session = Depends(get_db)):
    """Retorna todos os pets registrados com sua última localização."""

    # Subquery: maior id por pet_id (= registro mais recente)
    subq = (
        db.query(func.max(Location.id).label("max_id"))
        .group_by(Location.pet_id)
        .subquery()
    )
    latest_records = (
        db.query(Location)
        .join(subq, Location.id == subq.c.max_id)
        .all()
    )

    result = []
    for record in latest_records:
        total = db.query(func.count(Location.id)).filter(
            Location.pet_id == record.pet_id
        ).scalar()
        result.append(
            PetSummary(
                pet_id=record.pet_id,
                latest=LocationOut.model_validate(record),
                total_records=total,
            )
        )
    return result


# ─── Última localização de um pet ─────────────────────────────────────────────
@app.get("/pets/{pet_id}/location", response_model=LocationOut, tags=["pets"])
def get_latest_location(pet_id: str, db: Session = Depends(get_db)):
    """Retorna a localização mais recente do pet informado."""
    record = (
        db.query(Location)
        .filter(Location.pet_id == pet_id)
        .order_by(Location.id.desc())
        .first()
    )
    if not record:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhuma localização encontrada para o pet '{pet_id}'.",
        )
    return record


# ─── Histórico de trajeto ─────────────────────────────────────────────────────
@app.get("/pets/{pet_id}/history", response_model=list[LocationOut], tags=["pets"])
def get_location_history(
    pet_id: str,
    limit: int = Query(default=100, ge=1, le=1000, description="Máximo de registros"),
    offset: int = Query(default=0, ge=0, description="Pular N registros"),
    db: Session = Depends(get_db),
):
    """Retorna o histórico de localizações do pet (mais recente primeiro)."""
    records = (
        db.query(Location)
        .filter(Location.pet_id == pet_id)
        .order_by(Location.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    if not records:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhum histórico encontrado para o pet '{pet_id}'.",
        )
    return records


# ─── Apagar histórico de um pet ───────────────────────────────────────────────
@app.delete("/pets/{pet_id}/history", tags=["pets"])
def delete_history(pet_id: str, db: Session = Depends(get_db)):
    """Remove todo o histórico de localizações de um pet."""
    deleted = (
        db.query(Location)
        .filter(Location.pet_id == pet_id)
        .delete()
    )
    db.commit()
    return {"deleted_records": deleted, "pet_id": pet_id}