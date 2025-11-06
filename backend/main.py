# FastAPI'nin kendisini ithal et
from fastapi import FastAPI

# --- YENİ EKLENEN KISIM (Adım 2.2) ---

# Bizim "Mimar" dosyamızdan (models.py) planlarımızı (User sınıfı) ithal et
# (Doğrudan kullanmasak bile, 'Base'in onu tanıması için burada olmalı)
import models

# Bizim "Tesisatçı" dosyamızdan (database.py)
# 1. Ana Şablonu (Base)
# 2. Ana Motoru (engine)
# ithal et.
from database import Base, engine

# --- İNŞAAT EMRİ (Adım 2.2) ---
#
# Bu, Proje Yöneticisinin verdiği sihirli komuttur:
# "Ey Mimar'ın 'Ana Şablonu' (Base), sana bağlı olan TÜM planlara (models.py'deki User gibi)
# bak, ve Tesisatçı'nın 'Motoru'nu (engine) kullanarak o planları
# veritabanında GERÇEK TABLOLAR olarak İNŞA ET."
#
# FastAPI başladığı an bu kod çalışır ve (eğer yoksa) 'users' tablomuzu oluşturur.
Base.metadata.create_all(bind=engine)

# --- ESKİ KODUMUZ (Hala Çalışıyor) ---

# FastAPI uygulamasını "app" adıyla oluştur
app = FastAPI()


# Ana sayfa ("/") için bir 'GET' isteği (endpoint) tanımla
@app.get("/")
def read_root():
    # Mesajı güncelleyelim ki bir şeylerin değiştiğini anlayalım
    return {"mesaj": "Asama 2: Backend calisiyor VE veritabani raflari (tablolari) insa edildi!"}


# Başka bir test noktası
@app.get("/test")
def read_test():
    return {"deneme": "basarili", "proje_adi": "AI Dublaj Projesi"}