"""
AppFab - Configuration
"""

import streamlit as st
from typing import Dict, Any, Optional

def get_secret(key: str, default: Any = None) -> Any:
    """Streamlit secrets'ten değer al"""
    try:
        return st.secrets[key]
    except:
        return default

# =============================================================================
# APP CONFIGURATION
# =============================================================================

APP_CONFIG = {
    "name": "AppFab",
    "tagline": "AI ile App Üretin",
    "version": "1.0.0",
    "mode": "local"  # local | firebase
}

# =============================================================================
# OPENAI
# =============================================================================

OPENAI_API_KEY = get_secret("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-3.5-turbo"

# =============================================================================
# CREDITS
# =============================================================================

CREDIT_CONFIG = {
    "welcome_credits": 10,
    "cost_per_generation": 1,
    "pro_plan_price": 199,  # TL
    "credit_pack_price": 49,  # TL
    "credit_pack_amount": 50
}

# =============================================================================
# THEMES
# =============================================================================

THEME = {
    "primary": "#6366F1",
    "secondary": "#8B5CF6",
    "accent": "#22D3EE",
    "background": "#0F172A",
    "surface": "#1E293B",
    "text": "#F8FAFC",
    "text_muted": "#94A3B8",
    "success": "#10B981",
    "warning": "#F59E0B",
    "error": "#EF4444"
}

# =============================================================================
# FEATURES
# =============================================================================

FEATURES = {
    "allow_public_apps": True,
    "allow_app_likes": True,
    "enable_analytics": False,
    "enable_sharing": True
}
