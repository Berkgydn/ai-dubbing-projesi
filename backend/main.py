# === 1. GEREKLİ TÜM ARAÇLARI İTHAL ETME ===

# FastAPI'nin ana araçları
from fastapi import FastAPI, Depends, HTTPException, status

# SQLAlchemy'nin "Konuşma" (Session) aracı için
from sqlalchemy.orm import Session

# Bizim 'Süper-Takımımız' (Tüm yardımcılarımız)
import models, schemas, crud, security

# Bizim "Tesisatçı" dosyalarımız (Motor ve Konuşma Fabrikası)
from database import Base, engine, SessionLocal


# ... (diğer import'ların yanına)
from fastapi.middleware.cors import CORSMiddleware

# --- İNŞAAT EMRİ (Bu hala çok önemli) ---
# FastAPI başladığı an, Mimarın (models) planlarına bakarak
# Tesisatçının (engine) rafları (tabloları) inşa etmesini sağlar.
models.Base.metadata.create_all(bind=engine)

# FastAPI uygulamasını "app" adıyla oluştur
# FastAPI uygulamasını "app" adıyla oluştur
app = FastAPI()

# --- YENİ EKLENEN CORS TABELASI (Adım 2.12 Düzeltmesi) ---
#
# Bu, "B Apartmanı"nın (Backend) girişine astığımız "Tabela"dır.

# "origins" (İzin Verilen Kaynaklar/Apartmanlar)
# Sadece 'http://localhost:3000' (bizim Frontend'imiz) adresinden
# gelen isteklere izin ver.
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # 'origins' listemizdeki sitelere izin ver
    allow_credentials=True, # Çerezlere (ileride gerekirse) izin ver
    allow_methods=["*"],    # TÜM metotlara (* = GET, POST, OPTIONS, vb.) izin ver
    allow_headers=["*"],    # TÜM başlıklara (*) izin ver
)
# --- YENİ EKLENEN KISIM BİTTİ ---


# === 2. VERİTABANI "GİRİŞ İZNİ" YARDIMCISI ===
# (Geri kalan kodunuz ('get_db', '@app.get("/")' vb.) 
#  olduğu gibi kalacak)


# === 2. VERİTABANI "GİRİŞ İZNİ" YARDIMCISI ===

# Bu, "Tesisatçı"yı (database.py) kullanan sihirli bir yardımcıdır.
# Bir API isteği geldiğinde (Depends), "Konuşma Fabrikası"ndan (SessionLocal)
# 1 adet "Giriş İzni" (db session) alır.
# API'deki işini (örn: crud.create_user) yapar.
# Ve işi bittiğinde o "İzni" (db.close()) güvenle kapatır.
# Bizim artık her API'de 'db.close()' yazmamıza gerek kalmaz.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# === 3. ANA API ADRESLERİ (ENDPOINTS) ===

# --- "Merhaba Dünya" (Test için hala duruyor) ---
@app.get("/")
def read_root():
    return {"mesaj": "Asama 2: Backend calisiyor, /register API'si hazir!, /login modülü de eklendi!!"}


# --- ADIM 2.6: YENİ /register API'si ---

# Bu, 'main.py'nin (Proje Yöneticisi) 'Süper-Takımı' yönettiği yerdir.

# "/users/register" adresine bir "POST" (yeni veri yaratma) isteği gelirse
# bu fonksiyonu çalıştır.
# 'response_model=schemas.User': "İşin başarıyla biterse, 
#   cevabı 'User' (Giden Zarf) formatında (yani şifresiz!) döndür."
@app.post("/users/register", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate,         # İstekten 'UserCreate' (Gelen Zarf) al
    db: Session = Depends(get_db)     # Veritabanı "Giriş İzni" al (yukarıdaki yardımcıdan)
):

    # 1. YÖNETİCİ, DEPO GÖREVLİSİNE EMİR VERİYOR (Kontrol):
    # "Ey 'crud' (Depo Görevlisi)! Bu 'email' depoda var mı diye bak."
    db_user = crud.get_user_by_email(db, email=user.email)

    # 2. YÖNETİCİ, İŞLEM KARARI VERİYOR:
    if db_user:
        # "Eğer varsa, 'Hata 400' (Kötü İstek) fırlat ve işlemi durdur."
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Bu e-posta adresi zaten kayitli"
        )

    # 3. YÖNETİCİ, GÜVENLİK GÖREVLİSİNE EMİR VERİYOR (Şifreleme):
    # "Ey 'security' (Güvenlik Görevlisi)! 'Gelen Zarf'taki 'password'ü al 
    # ve 'şifrele' (hash'le)."
    hashed_password = security.get_password_hash(user.password)

    # 4. YÖNETİCİ, DEPO GÖREVLİSİNE EMİR VERİYOR (Kayıt):
    # "Ey 'crud'! 'Gelen Zarf'ı (user) ve 'şifrelenmiş parolayı' al,
    # depoya gidip bu kullanıcıyı 'oluştur' (create_user)."
    new_user = crud.create_user(db=db, user=user, hashed_password=hashed_password)

    # 5. YÖNETİCİ, CEVABI DÖNDÜRÜYOR:
    # (FastAPI, 'new_user'ı alır ve 'response_model' (schemas.User)
    # sayesinde şifresini otomatik olarak ayıklayıp frontend'e yollar).
    return new_user


# --- ADIM 2.8: YENİ /login API'si ---

# "Pasaport" (Token) almak için standart adres genellikle "/token" olur,
# ama biz daha net olması için "/users/login" kullanalım.
# 'response_model=schemas.Token': "İşin başarıyla biterse, 
#   cevabı 'Token' (Pasaport Zarfı) formatında döndür."
@app.post("/users/login", response_model=schemas.Token)
def login_for_access_token(
    # DİKKAT: Giriş için de 'Gelen Zarf' olarak 'UserCreate'i kullanıyoruz.
    # Çünkü o da 'email' ve 'password' içeriyor. Yeniden zarf çizmeye gerek yok.
    user_in: schemas.UserCreate, 
    db: Session = Depends(get_db)
):

    # 1. YÖNETİCİ, DEPO GÖREVLİSİNE EMİR VERİR (Bul):
    # "Ey 'crud'! Bu 'email' depoda var mı diye bak."
    db_user = crud.get_user_by_email(db, email=user_in.email)

    # 2. YÖNETİCİ, KONTROL EDER (Kullanıcı var mı?):
    if not db_user:
        # "Eğer 'email' HİÇ yoksa, 'Hata 401' (Yetkin Yok) fırlat."
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email veya sifre yanlis",
            headers={"WWW-Authenticate": "Bearer"}, # Bu, tarayıcıya "resmi" bir hata olduğunu söyler
        )

    # 3. YÖNETİCİ, GÜVENLİK GÖREVLİSİNE EMİR VERİR (Doğrula):
    # "Ey 'security'! Frontend'den gelen 'düz şifre' (user_in.password) ile
    # depodan gelen 'şifrelenmiş şifre' (db_user.hashed_password) eşleşiyor mu KONTROL ET."
    if not security.verify_password(user_in.password, db_user.hashed_password):
        # "Eğer eşleşmiyorsa, yine 'Hata 401' fırlat."
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email veya sifre yanlis",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 4. YÖNETİCİ, GÜVENLİK GÖREVLİSİNE EMİR VERİR (Pasaport Üret):
    # "Tebrikler, tüm kontrolleri geçtin.
    # Ey 'security'! Bu kullanıcı için ('sub' = subject = konu)
    # BİR PASAPORT (access_token) ÜRET."
    access_token = security.create_access_token(
        data={"sub": db_user.email}
    )

    # 5. YÖNETİCİ, PASAPORTU "ZARF"A KOYUP YOLLAR:
    # (FastAPI bunu 'response_model=schemas.Token' sayesinde
    # otomatik olarak 'access_token' ve 'token_type' JSON'una dönürür).
    return {"access_token": access_token, "token_type": "bearer"}