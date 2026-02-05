"""
AppFab Pro - Premium SaaS Interface
Modern, Glassmorphism, Dark Theme
"""

import streamlit as st
import time
from typing import Optional, Dict, Any

# Konfigürasyon
from config import APP_CONFIG
from database import UserManager, AppManager, LocalDatabase
from auth import (
    init_session_state, sign_up, log_in, log_out,
    get_current_user, get_user_id, is_logged_in,
    get_user_profile, check_user_credit
)
from app_generator import generate_streamlit_app, save_generated_app, preview_app

# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="AppFab - AI App Generator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================================================
# SESSION STATE INIT
# =============================================================================

init_session_state()

# =============================================================================
# PREMIUM CSS - DARK GLASSMORPHISM THEME
# =============================================================================

def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    :root {
        --primary: #6366F1;
        --primary-dark: #4F46E5;
        --primary-light: #818CF8;
        --secondary: #8B5CF6;
        --accent: #22D3EE;
        --bg: #0F172A;
        --surface: #1E293B;
        --surface-light: #334155;
        --text: #F8FAFC;
        --text-muted: #94A3B8;
        --text-dim: #64748B;
        --success: #10B981;
        --warning: #F59E0B;
        --error: #EF4444;
    }
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        box-sizing: border-box;
    }
    
    /* Hide Streamlit UI */
    #MainMenu, footer, header, .stDeployButton, [data-testid="stToolbar"] {
        display: none !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #0F172A 100%);
        background-attachment: fixed;
    }
    
    /* ============================================
       NAVBAR - Glassmorphism
       ============================================ */
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 70px;
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 3rem;
    }
    
    .nav-logo {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 1.5rem;
        font-weight: 800;
        color: white;
        text-decoration: none;
        cursor: pointer;
    }
    
    .nav-logo-icon {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #6366F1, #8B5CF6);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    }
    
    .nav-links {
        display: flex;
        gap: 0.5rem;
    }
    
    .nav-link {
        padding: 0.625rem 1.25rem;
        border-radius: 8px;
        font-size: 0.875rem;
        font-weight: 500;
        color: #94A3B8;
        text-decoration: none;
        transition: all 0.2s;
        cursor: pointer;
        border: none;
        background: transparent;
    }
    
    .nav-link:hover {
        color: #F8FAFC;
        background: rgba(255, 255, 255, 0.05);
    }
    
    .nav-link.active {
        color: #F8FAFC;
        background: rgba(99, 102, 241, 0.2);
    }
    
    .nav-right {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .credit-badge {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: rgba(34, 211, 238, 0.1);
        border: 1px solid rgba(34, 211, 238, 0.3);
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        color: #22D3EE;
    }
    
    .btn-nav {
        padding: 0.625rem 1.5rem;
        background: linear-gradient(135deg, #6366F1, #8B5CF6);
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 0.875rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .btn-nav:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
    }
    
    /* ============================================
       HERO SECTION - Premium
       ============================================ */
    .hero {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 8rem 2rem 4rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero-bg {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(ellipse 80% 50% at 50% -20%, rgba(99, 102, 241, 0.3), transparent),
            radial-gradient(ellipse 60% 40% at 80% 50%, rgba(139, 92, 246, 0.2), transparent),
            radial-gradient(ellipse 40% 60% at 20% 80%, rgba(34, 211, 238, 0.15), transparent);
        animation: pulse 8s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.05); }
    }
    
    .hero-content {
        position: relative;
        z-index: 2;
        max-width: 900px;
    }
    
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        color: #818CF8;
        margin-bottom: 2rem;
    }
    
    .hero-title {
        font-size: clamp(2.5rem, 6vw, 4.5rem);
        font-weight: 800;
        line-height: 1.1;
        letter-spacing: -0.02em;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, #F8FAFC 0%, #818CF8 50%, #22D3EE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: #94A3B8;
        max-width: 600px;
        margin: 0 auto 2.5rem;
        line-height: 1.6;
    }
    
    .btn-hero {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 1rem 2rem;
        background: linear-gradient(135deg, #6366F1, #8B5CF6);
        color: white;
        border: none;
        border-radius: 12px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 0 40px rgba(99, 102, 241, 0.4);
        text-decoration: none;
    }
    
    .btn-hero:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 60px rgba(99, 102, 241, 0.6);
    }
    
    /* ============================================
       FEATURES
       ============================================ */
    .section {
        padding: 6rem 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .section-header {
        text-align: center;
        margin-bottom: 4rem;
    }
    
    .section-label {
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #818CF8;
        margin-bottom: 1rem;
    }
    
    .section-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 1rem;
    }
    
    .section-subtitle {
        font-size: 1.125rem;
        color: #94A3B8;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
    }
    
    .feature-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        border-color: rgba(99, 102, 241, 0.3);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }
    
    .feature-icon {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2));
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1.25rem;
    }
    
    .feature-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #F8FAFC;
        margin-bottom: 0.75rem;
    }
    
    .feature-desc {
        font-size: 0.9375rem;
        color: #94A3B8;
        line-height: 1.6;
    }
    
    /* ============================================
       CREATE PAGE
       ============================================ */
    .create-container {
        padding-top: 100px;
        min-height: 100vh;
        max-width: 1400px;
        margin: 0 auto;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    .create-header {
        margin-bottom: 2rem;
    }
    
    .create-title {
        font-size: 2rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.5rem;
    }
    
    .create-subtitle {
        font-size: 1rem;
        color: #94A3B8;
    }
    
    .glass-panel {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
    }
    
    /* ============================================
       AUTH PAGE
       ============================================ */
    .auth-container {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        padding-top: 100px;
    }
    
    .auth-box {
        width: 100%;
        max-width: 420px;
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2.5rem;
    }
    
    .auth-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .auth-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.5rem;
    }
    
    .auth-subtitle {
        font-size: 0.9375rem;
        color: #94A3B8;
    }
    
    /* ============================================
       STREAMLIT OVERRIDES
       ============================================ */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        padding: 0.875rem 1rem !important;
        font-size: 0.9375rem !important;
        color: #F8FAFC !important;
        transition: all 0.2s !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #64748B !important;
    }
    
    button[kind="primary"] {
        background: linear-gradient(135deg, #6366F1, #8B5CF6) !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.875rem 1.5rem !important;
        font-size: 0.9375rem !important;
        font-weight: 600 !important;
        color: white !important;
        transition: all 0.2s !important;
    }
    
    button[kind="primary"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4) !important;
    }
    
    button[kind="secondary"] {
        background: transparent !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #94A3B8 !important;
        border-radius: 10px !important;
    }
    
    /* Code block */
    pre {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }
    
    /* ============================================
       ALERTS
       ============================================ */
    .alert {
        padding: 1rem 1.25rem;
        border-radius: 10px;
        font-size: 0.875rem;
        font-weight: 500;
        margin-bottom: 1rem;
    }
    
    .alert-info {
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.2);
        color: #818CF8;
    }
    
    .alert-success {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.2);
        color: #34D399;
    }
    
    .alert-error {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.2);
        color: #F87171;
    }
    
    /* ============================================
       RESPONSIVE
       ============================================ */
    @media (max-width: 768px) {
        .navbar {
            padding: 0 1rem;
        }
        
        .nav-links {
            display: none;
        }
        
        .hero {
            padding: 6rem 1rem 3rem;
        }
        
        .section {
            padding: 4rem 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

inject_css()

# =============================================================================
# NAVBAR
# =============================================================================

def render_navbar():
    user = None
    credits = 0
    is_pro = False
    
    if is_logged_in():
        user = get_user_profile()
        if user:
            credits = user.get('credits', 0)
            is_pro = user.get('is_pro', False)
    
    # Navbar HTML
    nav_html = f'''
    <div class="navbar">
        <div class="nav-logo" onclick="window.location.reload()">
            <div class="nav-logo-icon">⚡</div>
            <span>AppFab</span>
        </div>
        <div class="nav-links">
    '''
    
    pages = [
        ('🏠 Ana Sayfa', 'home'),
        ('✨ App Üret', 'create'),
        ('🎨 Galeri', 'gallery'),
        ('💎 Fiyat', 'pricing'),
    ]
    
    for label, page in pages:
        active = 'active' if st.session_state.page == page else ''
        nav_html += f'<button class="nav-link {active}">{label}</button>'
    
    nav_html += '''
        </div>
        <div class="nav-right">
    '''
    
    st.markdown(nav_html, unsafe_allow_html=True)
    
    # Buttons (Streamlit)
    if is_logged_in() and user:
        if is_pro:
            st.markdown('<span class="credit-badge">⭐ PRO</span>', unsafe_allow_html=True)
        else:
            st.markdown(f'<span class="credit-badge">💎 {credits} Kredi</span>', unsafe_allow_html=True)
        
        if st.button("🚪 Çıkış", key="nav_logout"):
            log_out()
    else:
        if st.button("🔐 Giriş / Kayıt", key="nav_login"):
            st.session_state.page = 'login'
            st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# =============================================================================
# HERO PAGE
# =============================================================================

def render_hero():
    st.markdown("""
    <div class="hero">
        <div class="hero-bg"></div>
        <div class="hero-content">
            <div class="hero-badge">🚀 Yapay Zeka Destekli</div>
            <h1 class="hero-title">Yapay Zeka ile<br>Kod Yazın</h1>
            <p class="hero-subtitle">30 saniyede çalışan uygulamalar oluşturun. Kod bilgisi gerektirmez.</p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✨ Hemen Başla", key="hero_cta", use_container_width=True, type="primary"):
            st.session_state.page = 'create' if is_logged_in() else 'login'
            st.rerun()
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# FEATURES
# =============================================================================

def render_features():
    st.markdown("""
    <div class="section">
        <div class="section-header">
            <p class="section-label">Neden AppFab?</p>
            <h2 class="section-title">Uygulama Geliştirmeyi Kolaylaştırıyoruz</h2>
            <p class="section-subtitle">Yapay zeka gücüyle hayalinizdeki uygulamaları saniyeler içinde oluşturun</p>
        </div>
        <div class="features-grid">
    """, unsafe_allow_html=True)
    
    features = [
        ('⚡', 'Saniyeler İçinde', 'Tek bir cümleyle çalışan uygulamalar oluşturun'),
        ('🎨', 'Modern Tasarım', 'Otomatik şık ve profesyonel arayüz'),
        ('💾', 'PC\'de Kayıt', 'Tüm veriler bilgisayarınızda güvenle saklanır'),
    ]
    
    for icon, title, desc in features:
        st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <h3 class="feature-title">{title}</h3>
                <p class="feature-desc">{desc}</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# =============================================================================
# AUTH PAGE
# =============================================================================

def render_auth():
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    tab = st.radio("", ["🔐 Giriş Yap", "📝 Kayıt Ol"], horizontal=True, label_visibility="collapsed")
    
    st.markdown('<div class="auth-box">', unsafe_allow_html=True)
    
    if tab == "🔐 Giriş Yap":
        st.markdown("""
            <div class="auth-header">
                <h1 class="auth-title">Hoş Geldiniz</h1>
                <p class="auth-subtitle">Hesabınıza giriş yapın</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("📧 E-posta", placeholder="ornek@email.com")
            password = st.text_input("🔒 Şifre", type="password", placeholder="••••••")
            
            submitted = st.form_submit_button("🚀 Giriş Yap", use_container_width=True, type="primary")
            
            if submitted:
                if email and password:
                    log_in(email, password)
                else:
                    st.warning("Lütfen tüm alanları doldurun")
    
    else:
        st.markdown("""
            <div class="auth-header">
                <h1 class="auth-title">Hesap Oluştur</h1>
                <p class="auth-subtitle">10 kredi hediye ile hemen başlayın!</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("register_form"):
            username = st.text_input("👤 Kullanıcı Adı", placeholder="kullanici123")
            email = st.text_input("📧 E-posta", placeholder="ornek@email.com")
            password = st.text_input("🔒 Şifre", type="password", placeholder="••••••")
            password2 = st.text_input("🔒 Şifre Tekrar", type="password", placeholder="••••••")
            
            submitted = st.form_submit_button("🚀 Hesap Oluştur", use_container_width=True, type="primary")
            
            if submitted:
                if all([username, email, password, password2]):
                    if password != password2:
                        st.error("❌ Şifreler eşleşmiyor")
                    else:
                        sign_up(email, password, username)
                else:
                    st.warning("Lütfen tüm alanları doldurun")
    
    st.markdown('</div></div>', unsafe_allow_html=True)

# =============================================================================
# CREATE PAGE
# =============================================================================

def render_create():
    if not is_logged_in():
        st.session_state.page = 'login'
        st.rerun()
        return
    
    user_id = get_user_id()
    credit_status = check_user_credit()
    
    if not credit_status["has_credit"]:
        st.error("💳 Krediniz bitti! Pro plana yükseltin.")
        st.session_state.page = 'pricing'
        st.rerun()
        return
    
    st.markdown("""
    <div class="create-container">
        <div class="create-header">
            <h1 class="create-title">✨ Yeni App Üret</h1>
            <p class="create-subtitle">Hayalinizdeki uygulamayı tek bir cümleyle anlatın</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Kredi durumu
        if credit_status["is_pro"]:
            st.markdown('<div class="alert alert-success">⭐ Pro Plan Aktif - Sınırsız Üretim!</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="alert alert-info">💎 {credit_status["credits"]} Kredi kaldı</div>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
            
            prompt = st.text_area(
                "📝 Ne yapmak istiyorsunuz?",
                placeholder="Örn: KDV hesaplayıcı yap. KDV oranı %1, %10, %20 olsun. Net tutarı girip KDV'li fiyat hesaplasın...",
                height=150
            )
            
            with st.expander("⚙️ Gelişmiş Ayarlar"):
                app_name = st.text_input("App Adı (Opsiyonel)", placeholder="Benim App'im")
                api_key = st.text_input("OpenAI API Key (Opsiyonel)", type="password", 
                                       help="Kendi API key'inizi kullanmak isterseniz")
            
            if st.button("🚀 APP ÜRET", use_container_width=True, type="primary", disabled=not prompt):
                # Kredi düş (eğer API key yoksa)
                if not api_key:
                    success = UserManager.deduct_credit(user_id, 1, "app_generation")
                    if not success:
                        st.error("Kredi düşme hatası")
                        st.rerun()
                
                # Progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i in range(100):
                    time.sleep(0.02)
                    progress_bar.progress(i + 1)
                    if i < 30:
                        status_text.text("🤖 AI düşünüyor...")
                    elif i < 60:
                        status_text.text("💻 Kod yazılıyor...")
                    elif i < 90:
                        status_text.text("✨ Son dokunuşlar...")
                    else:
                        status_text.text("🎉 Hazır!")
                
                # Generate
                result = generate_streamlit_app(prompt, app_name or "AI App")
                progress_bar.empty()
                status_text.empty()
                
                if result and result.get("success"):
                    st.session_state.generated_app = result
                    st.session_state.last_prompt = prompt
                    st.success("✅ App başarıyla oluşturuldu!")
                    st.rerun()
                else:
                    st.error("❌ App oluşturulamadı. Tekrar deneyin.")
                    # Kredi iadesi
                    if not api_key:
                        UserManager.add_credits(user_id, 1, "refund")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-panel">
            <h4 style="color: #F8FAFC; margin-bottom: 1rem;">💡 Nasıl Yazmalıyım?</h4>
            <ul style="color: #94A3B8; line-height: 2; padding-left: 1.2rem;">
                <li><b>Ne yapacağını</b> açıkça yazın</li>
                <li><b>Giriş alanlarını</b> belirtin</li>
                <li><b>Hesaplama mantığını</b> anlatın</li>
                <li><b>Grafik/Tablo</b> isteyin</li>
            </ul>
            <hr style="border-color: rgba(255,255,255,0.1); margin: 1.5rem 0;">
            <h4 style="color: #F8FAFC; margin-bottom: 0.5rem;">🎯 Örnekler</h4>
            <p style="color: #64748B; font-size: 0.875rem; line-height: 1.6;">
                • BMI hesaplayıcı<br>
                • Yatırım getiri hesaplayıcı<br>
                • Todo list uygulaması<br>
                • Kurlar takipçisi
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Sonuç göster
    if st.session_state.get('generated_app'):
        app = st.session_state.generated_app
        
        st.divider()
        
        col_save, col_download = st.columns([1, 1])
        
        with col_save:
            with st.expander("💾 App'i Kaydet"):
                save_name = st.text_input("App Adı", value=app.get("name", "Benim App'im"))
                save_desc = st.text_area("Açıklama", value=app.get("description", ""))
                is_public = st.toggle("🌐 Herkese Açık", value=False)
                
                if st.button("💾 Kaydet", type="primary", use_container_width=True):
                    app_id = save_generated_app(
                        user_id=user_id,
                        prompt=st.session_state.get('last_prompt', ''),
                        generated_data={
                            "name": save_name,
                            "description": save_desc,
                            "code": app.get("code", "")
                        },
                        is_public=is_public
                    )
                    if app_id:
                        st.success(f"✅ Kaydedildi! ID: {app_id}")
        
        with col_download:
            with st.expander("📥 İndir / Kopyala"):
                st.download_button(
                    label="📥 app.py İndir",
                    data=app.get("code", ""),
                    file_name="app.py",
                    mime="text/x-python",
                    use_container_width=True
                )
        
        # Kod göster
        st.subheader("📝 Oluşturulan Kod")
        st.code(app.get("code", ""), language="python")

# =============================================================================
# GALLERY PAGE
# =============================================================================

def render_gallery():
    st.markdown("""
    <div class="section" style="padding-top: 100px;">
        <div class="section-header">
            <p class="section-label">🎨 Topluluk Galerisi</p>
            <h2 class="section-title">Kullanıcıların Harika Uygulamaları</h2>
        </div>
    """, unsafe_allow_html=True)
    
    search = st.text_input("🔍 App Ara", placeholder="App adı veya açıklaması...")
    
    apps = AppManager.search_apps(search) if search else AppManager.get_public_apps()
    
    if not apps:
        st.info("📝 Henüz public app paylaşılmamış. İlk siz paylaşın!")
        if st.button("✨ App Üret", type="primary"):
            st.session_state.page = 'create'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        return
    
    # Apps grid
    cols = st.columns(3)
    for idx, app in enumerate(apps):
        with cols[idx % 3]:
            st.markdown(f"""
                <div class="feature-card" style="margin-bottom: 1rem;">
                    <h3 class="feature-title">{app.get('name', 'İsimsiz')}</h3>
                    <p class="feature-desc">{app.get('description', '')[:100]}...</p>
                    <p style="color: #64748B; font-size: 0.875rem; margin-top: 1rem;">
                        👁️ {app.get('views', 0)} • ❤️ {app.get('likes', 0)}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            if is_logged_in() and st.button("❤️ Beğen", key=f"like_{app.get('app_id')}"):
                user_id = get_user_id()
                AppManager.toggle_like(app.get('app_id'), user_id)
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# =============================================================================
# PRICING PAGE
# =============================================================================

def render_pricing():
    st.markdown("""
    <div class="section" style="padding-top: 100px;">
        <div class="section-header">
            <p class="section-label">💎 Fiyatlandırma</p>
            <h2 class="section-title">Size Uygun Planı Seçin</h2>
            <p class="section-subtitle">İhtiyacınıza göre esnek seçenekler</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <h3 style="color: #94A3B8;">Ücretsiz</h3>
            <div style="font-size: 2.5rem; font-weight: 700; color: #F8FAFC; margin: 1rem 0;">₺0</div>
            <ul style="color: #94A3B8; text-align: left; line-height: 2;">
                <li>✅ 10 kredi (hoşgeldin)</li>
                <li>✅ Temel app üretimi</li>
                <li>✅ PC'de kayıt</li>
                <li>❌ Sınırlı kredi</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🆓 Devam Et", use_container_width=True, key="btn_free"):
            st.session_state.page = 'create'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="feature-card" style="text-align: center; border-color: #6366F1;">
            <h3 style="color: #818CF8;">⭐ Pro</h3>
            <div style="font-size: 2.5rem; font-weight: 700; color: #F8FAFC; margin: 1rem 0;">₺199<small style="font-size: 1rem; color: #64748B;">/ay</small></div>
            <ul style="color: #94A3B8; text-align: left; line-height: 2;">
                <li>✅ Sınırsız app üretimi</li>
                <li>✅ Öncelikli destek</li>
                <li>✅ Gelişmiş özellikler</li>
                <li>✅ Dışa aktarma</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⭐ Pro Ol", use_container_width=True, type="primary", key="btn_pro"):
            st.info("💳 Ödeme entegrasyonu yakında!")
    
    with col3:
        st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <h3 style="color: #94A3B8;">💎 Kredi Paketi</h3>
            <div style="font-size: 2.5rem; font-weight: 700; color: #F8FAFC; margin: 1rem 0;">₺49</div>
            <ul style="color: #94A3B8; text-align: left; line-height: 2;">
                <li>✅ 50 kredi</li>
                <li>✅ Geçerlilik: Sonsuz</li>
                <li>✅ Tüm özellikler</li>
                <li>✅ Tek seferlik</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("💎 Satın Al", use_container_width=True, key="btn_credits"):
            st.info("💳 Ödeme entegrasyonu yakında!")
    
    st.markdown("</div>", unsafe_allow_html=True)

# =============================================================================
# DASHBOARD PAGE
# =============================================================================

def render_dashboard():
    if not is_logged_in():
        st.session_state.page = 'login'
        st.rerun()
        return
    
    user_id = get_user_id()
    profile = get_user_profile()
    my_apps = AppManager.get_user_apps(user_id)
    
    st.markdown("""
    <div class="section" style="padding-top: 100px;">
        <div class="create-header">
            <h1 class="create-title">📊 Dashboard</h1>
            <p class="create-subtitle">Uygulamalarınızı yönetin</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💎 Kredi", profile.get('credits', 0))
    with col2:
        st.metric("📱 App Sayısı", len(my_apps))
    with col3:
        st.metric("❤️ Toplam Beğeni", sum(a.get('likes', 0) for a in my_apps))
    with col4:
        st.metric("👁️ Toplam Görüntülenme", sum(a.get('views', 0) for a in my_apps))
    
    st.divider()
    
    # My Apps
    st.subheader("📱 Benim App'lerim")
    
    if not my_apps:
        st.info("Henüz app oluşturmadınız.")
        if st.button("✨ İlk App'ini Oluştur", type="primary"):
            st.session_state.page = 'create'
            st.rerun()
    else:
        for app in my_apps:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    visibility = "🌐" if app.get('is_public') else "🔒"
                    st.write(f"**{visibility} {app.get('name', 'İsimsiz')}**")
                    st.caption(app.get('description', '')[:100])
                with col2:
                    st.caption(f"❤️ {app.get('likes', 0)} | 👁️ {app.get('views', 0)}")
                with col3:
                    if st.button("🗑️ Sil", key=f"del_{app.get('app_id')}"):
                        AppManager.delete_app(app.get('app_id'))
                        st.rerun()
                st.divider()
    
    st.markdown("</div>", unsafe_allow_html=True)

# =============================================================================
# MAIN
# =============================================================================

def main():
    render_navbar()
    
    if st.session_state.page == 'home':
        render_hero()
        render_features()
    elif st.session_state.page == 'login':
        render_auth()
    elif st.session_state.page == 'create':
        render_create()
    elif st.session_state.page == 'gallery':
        render_gallery()
    elif st.session_state.page == 'pricing':
        render_pricing()
    elif st.session_state.page == 'dashboard':
        render_dashboard()
    else:
        render_hero()
        render_features()

if __name__ == "__main__":
    main()
