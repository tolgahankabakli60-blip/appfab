"""
AppFab - App Generator
Streamlit app oluşturma ve kaydetme
"""

import streamlit as st
import requests
from config import OPENAI_API_KEY
from database import AppManager, LocalDatabase
from typing import Dict, Optional
import time

def generate_streamlit_app(prompt: str, name: str = "", description: str = "") -> Optional[Dict]:
    """
    OpenAI ile Streamlit app kodu oluştur
    """
    if not OPENAI_API_KEY or OPENAI_API_KEY == "sk-your-openai-api-key-here":
        demo_code = '''import streamlit as st
import pandas as pd
import numpy as np

# Page config
st.set_page_config(page_title="Demo App", layout="wide")

# Title
st.title("🚀 Demo App")
st.markdown("Bu bir Streamlit app örneğidir.")

# Sidebar
with st.sidebar:
    st.header("⚙️ Ayarlar")
    num_rows = st.slider("Satır sayısı", 5, 100, 20)
    
# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Örnek Veri")
    data = pd.DataFrame({
        'x': range(num_rows),
        'y': np.random.randn(num_rows).cumsum()
    })
    st.line_chart(data.set_index('x'))
    
with col2:
    st.subheader("📈 İstatistikler")
    st.metric("Ortalama", f"{data['y'].mean():.2f}")
    st.metric("Standart Sapma", f"{data['y'].std():.2f}")
    
    st.write("### Ham Veri")
    st.dataframe(data.head(10), use_container_width=True)

# Interactive element
st.subheader("🎯 Etkileşimli Bölüm")
user_input = st.text_input("Bir şey yazın:", placeholder="Merhaba...")
if user_input:
    st.success(f"Girdiğiniz: **{user_input}**")

# Info
col1, col2, col3 = st.columns(3)
with col1:
    st.info("💡 İpucu: Kenar çubuğundan ayarları değiştirin")
with col2:
    st.warning("⚠️ Bu bir demo uygulamadır")
with col3:
    st.success("✅ Streamlit ile güçlendirildi")
'''
        return {
            "success": True,
            "name": name or "Örnek App",
            "description": description or "Bu bir demo app örneğidir.",
            "code": demo_code,
            "app_id": None,
            "note": "Demo kodu (API key gerekli)"
        }
    
    try:
        # OpenAI API kullanımı - requests ile doğrudan çağrı
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": """Sen uzman bir Streamlit geliştiricisisin. 
Kullanıcının isteğine göre çalışan, modern ve profesyonel bir Streamlit uygulaması oluştur.

KURALLAR:
1. SADECE Python kodu üret - başka hiçbir şey yazma
2. st.set_page_config() ile başla
3. Modern UI: st.columns, st.metric, st.info/warning/success kullan
4. Etkileşimli öğeler ekle: button, slider, selectbox, text_input
5. Veri görselleştirme: st.line_chart, st.bar_chart, st.dataframe
6. Yanıtında SADECE kod bloğu olsun, açıklama olmasın
7. Kod çalışır ve hatasız olsun"""},
                {"role": "user", "content": f"Bir Streamlit app oluştur: {prompt}"}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        code = data["choices"][0]["message"]["content"]
        
        # Markdown kod bloğunu temizle
        if code.startswith("```python"):
            code = code[9:]
        elif code.startswith("```"):
            code = code[3:]
        if code.endswith("```"):
            code = code[:-3]
        code = code.strip()
        
        return {
            "success": True,
            "name": name or "AI Tarafından Oluşturuldu",
            "description": description or prompt[:100],
            "code": code,
            "app_id": None
        }
        
    except Exception as e:
        st.error(f"Üretim hatası: {str(e)}")
        import traceback
        st.error(traceback.format_exc())
        return None

def save_generated_app(user_id: str, prompt: str, generated_data: Dict, is_public: bool = False) -> Optional[str]:
    """
    Üretilen app'i veritabanına kaydet
    """
    try:
        app_id = AppManager.create_app(
            user_id=user_id,
            name=generated_data.get("name", "İsimsiz App"),
            description=generated_data.get("description", ""),
            prompt=prompt,
            code=generated_data.get("code", ""),
            is_public=is_public
        )
        return app_id
    except Exception as e:
        st.error(f"Kayıt hatası: {str(e)}")
        return None

def preview_app(code: str, unique_key: str):
    """
    App önizlemesi (kod gösterimi)
    """
    st.subheader("📝 Oluşturulan Kod")
    
    # Copy button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("📋 Kopyala", key=f"copy_{unique_key}"):
            st.code(code, language="python")
            st.success("Kod panoya kopyalandı!")
            
    with col2:
        if st.button("💾 İndir", key=f"download_{unique_key}"):
            st.download_button(
                label="📥 app.py İndir",
                data=code,
                file_name="app.py",
                mime="text/x-python",
                key=f"dl_{unique_key}"
            )
    
    st.code(code, language="python")

def run_app_preview(code: str):
    """
    App çalıştırma talimatları
    """
    st.markdown("""
    ### 🚀 App'i Çalıştırma
    
    **1. Yöntem: Doğrudan Çalıştırma**
    ```bash
    # app.py dosyası oluşturun
    streamlit run app.py
    ```
    
    **2. Yöntem: Mevcut Projeye Ekleme**
    ```python
    # Oluşturulan kodu mevcut projenize yapıştırın
    ```
    """)
