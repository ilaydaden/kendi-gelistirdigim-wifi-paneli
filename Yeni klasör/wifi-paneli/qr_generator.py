import qrcode
import os
from io import BytesIO
import base64

def generate_qr_code(data, size=10):
    """QR kod oluşturur"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Resmi base64'e çevir
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"

def generate_wifi_qr_code(ssid, password, security="WPA"):
    """Wi-Fi QR kodu oluşturur"""
    wifi_data = f"WIFI:S:{ssid};T:{security};P:{password};;"
    return generate_qr_code(wifi_data)

def generate_form_qr_code(base_url):
    """Form sayfası QR kodu oluşturur"""
    return generate_qr_code(base_url)


