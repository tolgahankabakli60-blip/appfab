# ⚡ AppFab - AI App Generator

**Prompt yaz → App oluştur → Anında kullan**

Yapay zeka destekli Streamlit uygulaması oluşturucu. Kod bilgisi gerektirmez.

---

## 🚀 Canlı Demo

**[appfab.streamlit.app](https://appfab.streamlit.app)** _(örnek link)_

---

## ✨ Özellikler

- 🎯 **Prompt → App**: Tek cümleyle çalışan uygulamalar
- 🤖 **AI Destekli**: GPT-4 ile akıllı kod üretimi
- 💾 **Kalıcı Kayıt**: SQLite veritabanı (veriler kaybolmaz)
- 🎨 **Modern UI**: Karanlık tema, glassmorphism tasarım
- 💎 **Kredi Sistemi**: 10 kredi hediye, Pro ile sınırsız
- 🌐 **Web Tabanlı**: Kurulum yok, tarayıcıdan kullan

---

## 🚀 Hemen Kullan (Ücretsiz)

### 1. Streamlit Cloud'da Aç (1 Dakika)

```bash
# 1. GitHub'da repo oluştur ve dosyaları yükle
git init
git add .
git commit -m "AppFab deploy"
git remote add origin https://github.com/KULLANICI/appfab.git
git push -u origin main
```

```bash
# 2. Streamlit Cloud'a git
# https://share.streamlit.io/deploy

# 3. GitHub repo'yu seç
# 4. Deploy butonuna tıkla
```

### 2. Secrets Ekle (ZORUNLU)

Streamlit Cloud → App → **⋮** → **Settings** → **Secrets**:

```toml
OPENAI_API_KEY = "sk-proj-API-KEY-BURAYA"
```

> 🔑 Kendi OpenAI API key'inizi [platform.openai.com](https://platform.openai.com)'dan alın.

---

## 💻 Yerelde Çalıştırma

```bash
# 1. İndir
git clone https://github.com/kullanici/appfab.git
cd appfab

# 2. Bağımlılıkları kur
pip install -r requirements.txt

# 3. API Key ekle (.streamlit/secrets.toml oluştur)
echo 'OPENAI_API_KEY = "sk-proj-..."' > .streamlit/secrets.toml

# 4. Çalıştır
streamlit run app.py
```

---

## 🎯 Kullanım

1. **Kayıt Ol** → 10 kredi hediye
2. **Prompt Yaz** → "Hesap makinesi yap", "BMI hesaplayıcı yap"
3. **App Üret** → AI kodu oluştursun
4. **Kaydet** → Galeride paylaş veya indir

---

## 📁 Proje Yapısı

```
appfab/
├── app.py              # Ana uygulama
├── database.py         # SQLite veritabanı
├── auth.py             # Giriş/Kayıt
├── app_generator.py    # AI kod üretimi
├── config.py           # Ayarlar
├── requirements.txt    # Bağımlılıklar
└── README.md          # Bu dosya
```

---

## 🛠️ Teknolojiler

- **Streamlit** - Web arayüzü
- **SQLite** - Veritabanı
- **OpenAI GPT-4** - Kod üretimi
- **Python 3.8+** - Backend

---

## ⚠️ Önemli Notlar

- **API Key**: OpenAI key'inizi güvenli tutun, GitHub'a push etmeyin
- **Veriler**: SQLite kullanıldığı için veriler kalıcı
- **Limitsiz**: Pro plan ile sınırsız app üretimi

---

## 📝 Lisans

MIT License - Özgürce kullan, değiştir, paylaş.

---

**Hazır mısın?** 🚀 [Hemen Dene](https://appfab.streamlit.app)
