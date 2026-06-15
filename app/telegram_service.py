import os
import requests
import logging

logger = logging.getLogger(__name__)

def send_location_telegram(chat_id: str, pet_name: str, lat: float, lng: float) -> bool:
    token = os.getenv("TELEGRAM_TOKEN")

    if not token:
        logger.error("TELEGRAM_TOKEN não configurado")
        return False

    maps_link = f"https://maps.google.com/?q={lat},{lng}"

    message = (
        f"🐾 Seu pet {pet_name} foi encontrado!\n"
        f"Alguém escaneou a coleira agora.\n"
        f"Localização:\n{maps_link}"
    )

    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"

        requests.post(url, data={
            "chat_id": chat_id,
            "text": message
        })

        logger.info(f"Mensagem Telegram enviada para {chat_id}")
        return True

    except Exception as e:
        logger.error(f"Erro Telegram: {e}")
        return False