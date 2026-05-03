"""
Gera QR codes para a coleira do pet.
O QR aponta para: {BASE_URL}/pet/{pet_id}
"""

import io
import os

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer


def generate_qr_bytes(pet_id: str) -> bytes:
    """
    Gera o QR code do pet e retorna como bytes PNG.
    """
    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    url = f"{base_url}/pet/{pet_id}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Alta correção de erro
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
    )

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.read()