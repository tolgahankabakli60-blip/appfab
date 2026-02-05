"""
AppFab - Utility Functions
"""

import streamlit as st
import qrcode
import io
import base64
from typing import Optional

def show_success_message(message: str):
    """Başarı mesajı göster"""
    st.markdown(f"""
    <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); 
                border-radius: 10px; padding: 1rem; color: #34D399; margin-bottom: 1rem;">
        ✅ {message}
    </div>
    """, unsafe_allow_html=True)

def show_error_message(message: str):
    """Hata mesajı göster"""
    st.markdown(f"""
    <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); 
                border-radius: 10px; padding: 1rem; color: #F87171; margin-bottom: 1rem;">
        ❌ {message}
    </div>
    """, unsafe_allow_html=True)

def show_warning_message(message: str):
    """Uyarı mesajı göster"""
    st.markdown(f"""
    <div style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); 
                border-radius: 10px; padding: 1rem; color: #FBBF24; margin-bottom: 1rem;">
        ⚠️ {message}
    </div>
    """, unsafe_allow_html=True)

def show_info_message(message: str):
    """Bilgi mesajı göster"""
    st.markdown(f"""
    <div style="background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.3); 
                border-radius: 10px; padding: 1rem; color: #818CF8; margin-bottom: 1rem;">
        ℹ️ {message}
    </div>
    """, unsafe_allow_html=True)

def generate_qr_code(url: str) -> qrcode.image.base.Image:
    """QR kod oluştur"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")

def qr_to_base64(img: qrcode.image.base.Image) -> str:
    """QR kodu base64'e çevir"""
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode()

def format_datetime(dt_str: str) -> str:
    """Tarih formatı"""
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(dt_str)
        return dt.strftime("%d.%m.%Y %H:%M")
    except:
        return dt_str

def truncate_text(text: str, max_length: int = 100) -> str:
    """Metni kısalt"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def generate_unique_id(prefix: str = "id") -> str:
    """Benzersiz ID oluştur"""
    import uuid
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
