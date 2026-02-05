"""
KodUret - AI Kod Olusturucu
"""

import streamlit as st
import requests
import sqlite3
import hashlib
import secrets
from datetime import datetime

st.set_page_config(page_title="KodUret", page_icon="⚡", layout="wide")

OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", "")

def get_db():
    conn = sqlite3.connect("appfab.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY, email TEXT UNIQUE, username TEXT,
        password_hash TEXT, credits INTEGER DEFAULT 10, is_pro INTEGER DEFAULT 0
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS apps (
        app_id TEXT PRIMARY KEY, user_id TEXT, name TEXT, description TEXT,
        prompt TEXT, code TEXT, is_public INTEGER DEFAULT 0, likes INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

init_db()

def create_user(email, password, username):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    if c.fetchone():
        return False, "Email kayitli"
    user_id = f"user_{secrets.token_hex(8)}"
    pwd_hash = hashlib.sha256(password.encode()).hexdigest()
    c.execute("INSERT INTO users VALUES (?,?,?,?,10,0)", (user_id, email, username, pwd_hash))
    conn.commit()
    conn.close()
    return True, "Kayit basarili! 10 kredi hediye"

def login_user(email, password):
    conn = get_db()
    c = conn.cursor()
    pwd_hash = hashlib.sha256(password.encode()).hexdigest()
    c.execute("SELECT * FROM users WHERE email=? AND password_hash=?", (email, pwd_hash))
    user = c.fetchone()
    conn.close()
    return (True, dict(user)) if user else (False, None)

def get_user(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = c.fetchone()
    conn.close()
    return dict(user) if user else None

def deduct_credit(user_id):
    user = get_user(user_id)
    if user["is_pro"] or user["credits"] > 0:
        if not user["is_pro"]:
            conn = get_db()
            c = conn.cursor()
            c.execute("UPDATE users SET credits = credits - 1 WHERE user_id=?", (user_id,))
            conn.commit()
            conn.close()
        return True
    return False

def save_app(user_id, name, description, prompt, code, is_public):
    conn = get_db()
    c = conn.cursor()
    app_id = f"app_{int(datetime.now().timestamp())}"
    c.execute("INSERT INTO apps VALUES (?,?,?,?,?,?,?,0,?)", 
              (app_id, user_id, name, description, prompt, code, int(is_public), datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return app_id

def get_user_apps(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM apps WHERE user_id=? ORDER BY created_at DESC", (user_id,))
    apps = [dict(row) for row in c.fetchall()]
    conn.close()
    return apps

def generate_app(prompt):
    if not OPENAI_API_KEY:
        return None, "API Key eksik"
    try:
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "Sen Streamlit uzmanisin. SADECE calisan Python kodu uret. st.set_page_config ile basla. Modern UI. SADECE kod, aciklama yok."},
                {"role": "user", "content": f"Streamlit app olustur: {prompt}"}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        code = response.json()["choices"][0]["message"]["content"]
        
        if code.startswith("```python"): code = code[9:]
        elif code.startswith("```"): code = code[3:]
        if code.endswith("```"): code = code[:-3]
        return code.strip(), None
    except Exception as e:
        return None, str(e)

if "user" not in st.session_state: st.session_state.user = None
if "page" not in st.session_state: st.session_state.page = "home"
if "generated_code" not in st.session_state: st.session_state.generated_code = None

st.title("⚡ KodUret")
st.caption("Yapay zeka ile aninda kod olustur")

with st.sidebar:
    st.header("Menu")
    if st.session_state.user:
        user = get_user(st.session_state.user["user_id"])
        st.write(f"👤 {user['username']}")
        st.write(f"💎 {user['credits']} Kredi")
        if st.button("Ana Sayfa", use_container_width=True): st.session_state.page = "home"; st.rerun()
        if st.button("Kod Uret", use_container_width=True): st.session_state.page = "create"; st.rerun()
        if st.button("Kodlarim", use_container_width=True): st.session_state.page = "myapps"; st.rerun()
        if st.button("Cikis", use_container_width=True): st.session_state.user = None; st.rerun()
    else:
        if st.button("Ana Sayfa", use_container_width=True): st.session_state.page = "home"; st.rerun()
        if st.button("Giris / Kayit", use_container_width=True): st.session_state.page = "auth"; st.rerun()

if st.session_state.page == "home":
    st.header("Hos Geldiniz")
    st.write("Tek cumleyle hesap makinesi, BMI hesaplayici olusturun.")
    
    if not st.session_state.user:
        if st.button("Baslamak icin Giris Yap", type="primary"):
            st.session_state.page = "auth"
            st.rerun()

elif st.session_state.page == "auth":
    st.header("Giris / Kayit")
    tab1, tab2 = st.tabs(["Giris Yap", "Kayit Ol"])
    
    with tab1:
        with st.form("login"):
            email = st.text_input("Email")
            password = st.text_input("Sifre", type="password")
            if st.form_submit_button("Giris Yap", use_container_width=True):
                ok, user = login_user(email, password)
                if ok:
                    st.session_state.user = user
                    st.success("Giris basarili!")
                    st.rerun()
                else:
                    st.error("Hatali giris")
    
    with tab2:
        with st.form("register"):
            username = st.text_input("Kullanici Adi")
            email = st.text_input("Email")
            password = st.text_input("Sifre", type="password")
            if st.form_submit_button("Kayit Ol", use_container_width=True):
                ok, msg = create_user(email, password, username)
                if ok: st.success(msg)
                else: st.error(msg)

elif st.session_state.page == "create":
    if not st.session_state.user:
        st.error("Lutfen giris yapin")
        st.stop()
    
    st.header("Yeni Kod Uret")
    user = get_user(st.session_state.user["user_id"])
    st.write(f"Krediniz: {user['credits']}")
    
    prompt = st.text_area("Ne yapmak istiyorsunuz?", placeholder="Orn: Basit hesap makinesi yap. Toplama, cikarma, carpma, bolme olsun.", height=100)
    col1, col2 = st.columns(2)
    app_name = col1.text_input("App Adi", "Benim App'im")
    is_public = col2.checkbox("Herkes Acik")
    
    if st.button("KOD URET", type="primary", use_container_width=True):
        if prompt:
            if deduct_credit(st.session_state.user["user_id"]):
                with st.spinner("AI dusunuyor..."):
                    code, error = generate_app(prompt)
                
                if error:
                    st.error(error)
                else:
                    save_app(st.session_state.user["user_id"], app_name, prompt[:100], prompt, code, is_public)
                    st.session_state.generated_code = code
                    st.success("Kod olusturuldu!")
            else:
                st.error("Krediniz bitti!")
        else:
            st.error("Lutfen aciklama yazin")
    
    if st.session_state.generated_code:
        st.divider()
        st.subheader("Olusturulan Kod")
        st.code(st.session_state.generated_code, language="python")
        st.download_button("Indir (.py)", st.session_state.generated_code, file_name="app.py")
        
        st.divider()
        st.subheader("Kodu Calistir")
        
        # CHECKBOX versiyonu - buton degil!
        if st.checkbox("Calistirmayi goster", key="run_checkbox"):
            st.info("Asagida kod calisiyor:")
            
            try:
                code_to_run = st.session_state.generated_code
                lines = code_to_run.split('\n')
                filtered_lines = [line for line in lines if 'set_page_config' not in line]
                clean_code = '\n'.join(filtered_lines)
                
                with st.container():
                    exec(clean_code)
            except Exception as e:
                st.error(f"Calistirma hatasi: {e}")

elif st.session_state.page == "myapps":
    if not st.session_state.user:
        st.error("Lutfen giris yapin")
        st.stop()
    
    st.header("Kodlarim")
    apps = get_user_apps(st.session_state.user["user_id"])
    
    if not apps:
        st.info("Henuz kod yok.")
    else:
        for i, app in enumerate(apps):
            with st.expander(f"{'Acik' if app['is_public'] else 'Gizli'} - {app['name']}"):
                st.write(f"Tarih: {app['created_at']}")
                st.code(app['code'], language="python")
                st.download_button("Indir", app['code'], file_name=f"{app['name']}.py", key=f"dl_{i}")
