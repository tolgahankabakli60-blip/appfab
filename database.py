"""
AppFab - Database Module
SQLite Database (Cloud uyumlu - kalıcı)
"""

import streamlit as st
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import sqlite3
import json
import hashlib
import secrets
import os

DB_FILE = "appfab.db"

def get_db_connection():
    """SQLite bağlantısı oluştur"""
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Veritabanı tablolarını oluştur"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Kullanıcılar tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            username TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            credits INTEGER DEFAULT 10,
            is_pro BOOLEAN DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # App'ler tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS apps (
            app_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            prompt TEXT,
            code TEXT NOT NULL,
            is_public BOOLEAN DEFAULT 0,
            likes INTEGER DEFAULT 0,
            views INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    # Beğeniler tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS likes (
            app_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            PRIMARY KEY (app_id, user_id),
            FOREIGN KEY (app_id) REFERENCES apps (app_id),
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    conn.commit()
    conn.close()

# DB'yi başlat
init_db()

# =============================================================================
# AUTH
# =============================================================================

class LocalAuth:
    """Local authentication (SQLite)"""
    
    @staticmethod
    def create_user(email: str, password: str, username: str) -> Tuple[bool, str, Optional[Dict]]:
        """Yeni kullanıcı oluştur"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Email kontrolü
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            return False, "Bu e-posta adresi zaten kayıtlı", None
        
        user_id = f"user_{secrets.token_hex(8)}"
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            cursor.execute('''
                INSERT INTO users (user_id, email, username, password_hash, credits)
                VALUES (?, ?, ?, ?, 10)
            ''', (user_id, email, username, password_hash))
            conn.commit()
            
            user_data = {
                "localId": user_id,
                "email": email,
                "username": username,
                "idToken": secrets.token_urlsafe(32)
            }
            conn.close()
            return True, "Kayıt başarılı!", user_data
            
        except Exception as e:
            conn.close()
            return False, f"Kayıt hatası: {str(e)}", None
    
    @staticmethod
    def login(email: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """Giriş yap"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute('''
            SELECT * FROM users 
            WHERE email = ? AND password_hash = ?
        ''', (email, password_hash))
        
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return False, "E-posta veya şifre hatalı", None
        
        return True, "Giriş başarılı!", {
            "localId": user["user_id"],
            "email": user["email"],
            "username": user["username"],
            "idToken": secrets.token_urlsafe(32)
        }

# =============================================================================
# DATABASE
# =============================================================================

class LocalDatabase:
    """SQLite database operations"""
    
    @staticmethod
    def get_user_profile(user_id: str) -> Optional[Dict]:
        """Kullanıcı profilini al"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                "user_id": user["user_id"],
                "email": user["email"],
                "username": user["username"],
                "credits": user["credits"],
                "is_pro": bool(user["is_pro"]),
                "created_at": user["created_at"]
            }
        return None
    
    @staticmethod
    def update_user_profile(user_id: str, data: Dict):
        """Kullanıcı profilini güncelle"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for key, value in data.items():
            if key in ['credits', 'is_pro']:
                cursor.execute(f"UPDATE users SET {key} = ? WHERE user_id = ?", 
                             (value, user_id))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def add_credits(user_id: str, amount: int):
        """Kredi ekle"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET credits = credits + ? WHERE user_id = ?
        ''', (amount, user_id))
        conn.commit()
        conn.close()
    
    @staticmethod
    def deduct_credit(user_id: str, amount: int = 1) -> bool:
        """Kredi düş"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Pro kullanıcı kontrolü
        cursor.execute("SELECT credits, is_pro FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return False
        
        if user["is_pro"]:
            conn.close()
            return True
        
        if user["credits"] < amount:
            conn.close()
            return False
        
        cursor.execute('''
            UPDATE users SET credits = credits - ? WHERE user_id = ?
        ''', (amount, user_id))
        conn.commit()
        conn.close()
        return True
    
    @staticmethod
    def check_credit(user_id: str) -> Dict[str, Any]:
        """Kredi durumunu kontrol et"""
        profile = LocalDatabase.get_user_profile(user_id)
        if not profile:
            return {"has_credit": False, "credits": 0, "is_pro": False}
        
        return {
            "has_credit": profile["is_pro"] or profile["credits"] > 0,
            "credits": profile["credits"],
            "is_pro": profile["is_pro"]
        }
    
    @staticmethod
    def create_app(user_id: str, name: str, description: str, prompt: str, 
                   code: str, is_public: bool = False) -> Optional[str]:
        """App oluştur"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        import time
        app_id = f"app_{int(time.time())}_{secrets.token_hex(4)}"
        
        cursor.execute('''
            INSERT INTO apps (app_id, user_id, name, description, prompt, code, is_public)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (app_id, user_id, name, description, prompt, code, is_public))
        
        conn.commit()
        conn.close()
        return app_id
    
    @staticmethod
    def get_app(app_id: str) -> Optional[Dict]:
        """App detaylarını al"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM apps WHERE app_id = ?", (app_id,))
        app = cursor.fetchone()
        conn.close()
        
        if app:
            return dict(app)
        return None
    
    @staticmethod
    def get_user_apps(user_id: str) -> List[Dict]:
        """Kullanıcının app'lerini listele"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM apps WHERE user_id = ? ORDER BY created_at DESC
        ''', (user_id,))
        apps = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return apps
    
    @staticmethod
    def get_public_apps() -> List[Dict]:
        """Public app'leri getir"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM apps WHERE is_public = 1 ORDER BY likes DESC, created_at DESC
        ''')
        apps = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return apps
    
    @staticmethod
    def search_apps(query: str) -> List[Dict]:
        """App ara"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM apps 
            WHERE is_public = 1 AND (name LIKE ? OR description LIKE ?)
            ORDER BY likes DESC
        ''', (f'%{query}%', f'%{query}%'))
        apps = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return apps
    
    @staticmethod
    def toggle_like(app_id: str, user_id: str) -> Tuple[bool, bool]:
        """Beğeni ekle/kaldır"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Kullanıcı daha önce beğenmiş mi?
        cursor.execute('''
            SELECT * FROM likes WHERE app_id = ? AND user_id = ?
        ''', (app_id, user_id))
        
        if cursor.fetchone():
            # Beğeniyi kaldır
            cursor.execute('''
                DELETE FROM likes WHERE app_id = ? AND user_id = ?
            ''', (app_id, user_id))
            cursor.execute('''
                UPDATE apps SET likes = likes - 1 WHERE app_id = ?
            ''', (app_id,))
            conn.commit()
            conn.close()
            return True, False  # Kaldırıldı
        else:
            # Beğeni ekle
            cursor.execute('''
                INSERT INTO likes (app_id, user_id) VALUES (?, ?)
            ''', (app_id, user_id))
            cursor.execute('''
                UPDATE apps SET likes = likes + 1 WHERE app_id = ?
            ''', (app_id,))
            conn.commit()
            conn.close()
            return True, True  # Eklendi
    
    @staticmethod
    def delete_app(app_id: str):
        """App sil"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM apps WHERE app_id = ?", (app_id,))
        cursor.execute("DELETE FROM likes WHERE app_id = ?", (app_id,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_stats() -> Dict[str, int]:
        """İstatistikleri al"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM apps")
        total_apps = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM apps WHERE is_public = 1")
        public_apps = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(likes) FROM apps")
        total_likes = cursor.fetchone()[0] or 0
        
        conn.close()
        return {
            "total_users": total_users,
            "total_apps": total_apps,
            "public_apps": public_apps,
            "total_likes": total_likes
        }

# =============================================================================
# WRAPPER CLASSES
# =============================================================================

class UserManager:
    """Kullanıcı yönetimi wrapper"""
    
    @staticmethod
    def create_user_profile(user_id: str, email: str, username: str):
        pass  # Auth'da oluşturuluyor
    
    @staticmethod
    def get_user_profile(user_id: str):
        return LocalDatabase.get_user_profile(user_id)
    
    @staticmethod
    def update_user_profile(user_id: str, data: Dict):
        LocalDatabase.update_user_profile(user_id, data)
    
    @staticmethod
    def add_credits(user_id: str, amount: int, reason: str = ""):
        LocalDatabase.add_credits(user_id, amount)
    
    @staticmethod
    def deduct_credit(user_id: str, amount: int = 1, reason: str = "") -> bool:
        return LocalDatabase.deduct_credit(user_id, amount)
    
    @staticmethod
    def check_credit(user_id: str) -> Dict[str, Any]:
        return LocalDatabase.check_credit(user_id)
    
    @staticmethod
    def activate_pro(user_id: str, months: int = 1):
        # Pro aktivasyonu
        LocalDatabase.update_user_profile(user_id, {"is_pro": True})

class AppManager:
    """App yönetimi wrapper"""
    
    @staticmethod
    def create_app(user_id: str, name: str, description: str, prompt: str, 
                   code: str, is_public: bool = False) -> Optional[str]:
        return LocalDatabase.create_app(user_id, name, description, prompt, code, is_public)
    
    @staticmethod
    def get_app(app_id: str):
        return LocalDatabase.get_app(app_id)
    
    @staticmethod
    def get_user_apps(user_id: str):
        return LocalDatabase.get_user_apps(user_id)
    
    @staticmethod
    def get_public_apps(limit: int = 50, order_by_likes: bool = True):
        return LocalDatabase.get_public_apps()[:limit]
    
    @staticmethod
    def search_apps(query: str, limit: int = 20):
        return LocalDatabase.search_apps(query)[:limit]
    
    @staticmethod
    def toggle_like(app_id: str, user_id: str):
        return LocalDatabase.toggle_like(app_id, user_id)
    
    @staticmethod
    def delete_app(app_id: str):
        LocalDatabase.delete_app(app_id)

class AnalyticsManager:
    """Analytics wrapper"""
    
    @staticmethod
    def get_dashboard_stats():
        return LocalDatabase.get_stats()

class FirebaseManager:
    def is_using_local(self):
        return True
    def get_db(self):
        return None

firebase_mgr = FirebaseManager()
