"""
Subscriber MQTT — roda em thread separada dentro do FastAPI.

Assina: pets/+/location
Ao receber mensagem: faz parse do JSON e salva no SQLite.
"""

import json
import logging
import threading

import paho.mqtt.client as mqtt
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Location
from app.schemas import LocationIn

logger = logging.getLogger(__name__)

BROKER   = "broker.hivemq.com"
PORT     = 1883
TOPIC    = "pets/+/location"  # '+' = wildcard de um nível (qualquer pet_id)
CLIENT_ID = "fastapi_pet_tracker_sub"


def _on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        logger.info(f"[MQTT] Conectado ao broker '{BROKER}'")
        client.subscribe(TOPIC)
        logger.info(f"[MQTT] Inscrito em '{TOPIC}'")
    else:
        logger.error(f"[MQTT] Falha na conexão. Código: {rc}")


def _on_message(client, userdata, msg):
    """Chamado a cada mensagem recebida. Faz parse e persiste."""
    try:
        payload = json.loads(msg.payload.decode())
        location_in = LocationIn(**payload)

        db: Session = SessionLocal()
        try:
            record = Location(
                pet_id = location_in.pet_id,
                lat    = location_in.lat,
                lng    = location_in.lng,
                speed  = location_in.speed,
                step   = location_in.step,
            )
            db.add(record)
            db.commit()
            logger.info(
                f"[MQTT] Salvo → pet={location_in.pet_id} "
                f"lat={location_in.lat:.6f} lng={location_in.lng:.6f}"
            )
        finally:
            db.close()

    except json.JSONDecodeError:
        logger.warning(f"[MQTT] Payload inválido: {msg.payload}")
    except Exception as e:
        logger.error(f"[MQTT] Erro ao processar mensagem: {e}")


def _on_disconnect(client, userdata, rc, properties=None):
    if rc != 0:
        logger.warning(f"[MQTT] Desconectado inesperadamente (rc={rc}). Reconectando...")


def start_mqtt_subscriber() -> threading.Thread:
    """
    Cria o cliente MQTT e inicia o loop em background.
    Retorna a thread para que o FastAPI possa monitorá-la.
    """
    client = mqtt.Client(
        client_id=CLIENT_ID,
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    )
    client.on_connect    = _on_connect
    client.on_message    = _on_message
    client.on_disconnect = _on_disconnect

    client.connect(BROKER, PORT, keepalive=60)

    thread = threading.Thread(
        target=client.loop_forever,
        daemon=True,  # morre junto com o processo principal
        name="mqtt-subscriber",
    )
    thread.start()
    logger.info("[MQTT] Thread do subscriber iniciada.")
    return thread