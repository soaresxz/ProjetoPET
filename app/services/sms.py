"""
Serviço de notificação via SMS usando Twilio.

Variáveis de ambiente necessárias (.env):
  TWILIO_ACCOUNT_SID  — Account SID do painel Twilio
  TWILIO_AUTH_TOKEN   — Auth Token do painel Twilio
  TWILIO_FROM_NUMBER  — Número Twilio no formato E.164: +15551234567
  BASE_URL            — URL pública da aplicação: https://meusite.com
"""

import logging
import os

from twilio.rest import Client

logger = logging.getLogger(__name__)


def send_scan_sms(owner_phone: str, pet_name: str, lat: float, lng: float) -> bool:
    """
    Envia SMS ao dono informando que o QR foi escaneado e a localização de quem escaneou.
    Retorna True em caso de sucesso, False em caso de erro.
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token  = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_FROM_NUMBER")

    if not all([account_sid, auth_token, from_number]):
        logger.error("Variáveis Twilio não configuradas. Verifique o .env")
        return False

    logger.info(f"[SMS DEBUG] FROM={from_number!r}  TO={owner_phone!r}  SID={account_sid[:10]}...")

    maps_link = f"https://maps.google.com/?q={lat},{lng}"

    body = (
        f"🐾 Seu pet {pet_name} foi encontrado!\n"
        f"Alguém escaneou a coleira agora.\n"
        f"Localização de quem achou:\n{maps_link}"
    )

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=body,
            from_=from_number,
            to=owner_phone,
        )
        logger.info(f"SMS enviado para {owner_phone} | SID: {message.sid}")
        return True
    except Exception as e:
        logger.error(f"Erro ao enviar SMS: {e}")
        logger.error(f"[SMS DEBUG] Detalhes: FROM={from_number!r} TO={owner_phone!r}")
        return False