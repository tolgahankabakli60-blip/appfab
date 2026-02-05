"""
AppFab - Authentication Module
Local Authentication (PC'de kayıt)
"""

import streamlit as st
from database import LocalAuth, LocalDatabase

def init_session_state():
    """Session state'i başlat"""
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'signup_success' not in st.session_state:
        st.session_state.signup_success = False
    if 'generated_app' not in st.session_state:
        st.session_state.generated_app = None
    if 'generated_code' not in st.session_state:
        st.session_state.generated_code = None
    if 'last_prompt' not in st.session_state:
        st.session_state.last_prompt = ""
    if 'credits_updated' not in st.session_state:
        st.session_state.credits_updated = False

def sign_up(email: str, password: str, username: str = ""):
    """Yeni kullanıcı kaydı"""
    if not username:
        username = email.split("@")[0]
    
    success, message, user_data = LocalAuth.create_user(email, password, username)
    
    if success:
        st.session_state.user = user_data
        st.session_state.page = 'dashboard'
        st.session_state.signup_success = True
        st.success(message)
        st.rerun()
    else:
        st.error(message)
    return success

def log_in(email: str, password: str):
    """Kullanıcı girişi"""
    success, message, user_data = LocalAuth.login(email, password)
    
    if success:
        st.session_state.user = user_data
        st.session_state.page = 'dashboard'
        st.success(message)
        st.rerun()
    else:
        st.error(message)
    return success

def log_out():
    """Çıkış yap"""
    st.session_state.user = None
    st.session_state.page = 'home'
    st.session_state.generated_app = None
    st.session_state.generated_code = None
    st.rerun()

def get_current_user():
    """Mevcut kullanıcıyı döndür"""
    return st.session_state.get('user')

def get_user_id():
    """Kullanıcı ID'sini al"""
    user = get_current_user()
    if user:
        return user.get('localId')
    return None

def get_user_email():
    """Kullanıcı e-posta adresini al"""
    user = get_current_user()
    if user:
        return user.get('email')
    return None

def is_logged_in():
    """Kullanıcı giriş yapmış mı?"""
    return get_current_user() is not None

def get_user_profile():
    """Kullanıcı profilini al"""
    user_id = get_user_id()
    if user_id:
        return LocalDatabase.get_user_profile(user_id)
    return None

def check_user_credit():
    """Kullanıcı kredisini kontrol et"""
    user_id = get_user_id()
    if user_id:
        return LocalDatabase.check_credit(user_id)
    return {"has_credit": False, "credits": 0, "is_pro": False}

def require_login():
    """Giriş gerektir - popup göster"""
    if not is_logged_in():
        st.warning("⚠️ Lütfen önce giriş yapın!")
        st.session_state.page = 'login'
        st.rerun()
        return False
    return True

def show_login_modal():
    """Login modal penceresi"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E293B 0%, #334155 100%); 
                border: 1px solid #6366F1; border-radius: 16px; padding: 30px; 
                text-align: center; margin: 20px 0;">
        <h3 style="color: #F8FAFC; margin-bottom: 10px;">🔐 Giriş Yapın</h3>
        <p style="color: #94A3B8;">App oluşturmak için giriş yapmanız gerekiyor.</p>
        <div style="margin-top: 20px;">
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Giriş Yap", use_container_width=True, type="primary"):
            st.session_state.page = 'login'
            st.rerun()
    with col2:
        if st.button("Kayıt Ol", use_container_width=True):
            st.session_state.page = 'register'
            st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def show_credit_warning():
    """Kredi uyarısı göster"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); 
                border: 1px solid #F59E0B; border-radius: 16px; padding: 25px; 
                text-align: center; margin: 20px 0;">
        <h3 style="color: #92400E; margin-bottom: 10px;">💳 Yetersiz Kredi</h3>
        <p style="color: #B45309; font-size: 1.1em;">
            App oluşturmak için krediye ihtiyacınız var.<br>
            <strong>Pro</strong> planla sınırsız üretim yapın!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("⬆️ Yükseltme Yapın", use_container_width=True, type="primary"):
        st.session_state.page = 'pricing'
        st.rerun()
