# Şifre "karıştırma" (hashing) ve "doğrulama" (verification) işleri için
# 'passlib' kütüphanesinden 'CryptContext' (Şifreleme Yöneticisi) aracını ithal et.
from passlib.context import CryptContext

# "Pasaport" (JWT Token) oluşturma, okuma ve doğrulama işleri için
# 'jose' kütüphanesinden 'jwt' ve 'JWTError' araçlarını ithal et.
from jose import JWTError, jwt

# Pydantic'ten 'datetime' (tarih/saat) tipini al (pasaportun son kullanma tarihi için).
from datetime import datetime, timedelta

# .env dosyasından sırları okumak için
import os

# --- ŞİFRELEME BÖLÜMÜ (Passlib) ---

# 1. Şifreleme Yöneticisini (CryptContext) Oluştur
# Python'a diyoruz ki: "Biz 'bcrypt' adlı modern ve güvenli
# şifreleme (hashing) algoritmasını kullanacağız."
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Görev 1: Şifreyi Doğrulama Fonksiyonu
# Bu fonksiyon, "düz şifre" (plaintext_password) ile "depodaki şifrelenmiş şifreyi" (hashed_password)
# alıp karşılaştırır ve "Evet" (True) veya "Hayır" (False) der.
def verify_password(plaintext_password, hashed_password):
    return pwd_context.verify(plaintext_password, hashed_password)

# Görev 2: Şifreyi Şifreleme (Hash'leme) Fonksiyonu
# Bu fonksiyon, "düz şifreyi" (password) alır ve onu
# 'bcrypt' algoritmasıyla karıştırıp (hash'leyip) geri döndürür.
def get_password_hash(password):
    return pwd_context.hash(password)


# --- PASAPORT BÖLÜMÜ (JWT) ---

# "Pasaportlarımızı" (JWT) imzalarken kullanacağımız 3 sırrı
# .env dosyamızdan okumamız gerekiyor.
# (BU SIRLARI BİR SONRAKİ ADIMDA .env DOSYAMIZA EKLEYECEĞİZ!)

# Sır 1: Gizli Anahtar (Pasaportu imzalayan mühür)
SECRET_KEY = os.getenv("SECRET_KEY", "varsayilan_gizli_anahtar_eger_env_de_yoksa")

# Sır 2: Algoritma (Hangi imza tekniği?)
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Sır 3: Geçerlilik Süresi (Pasaport kaç dakika geçerli?)
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


# Görev 3: "Pasaport" (JWT Token) Oluşturma Fonksiyonu
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    # Alınan veriyi (örn: {'sub': 'test@mail.com'}) kopyala
    to_encode = data.copy()

    # Eğer özel bir geçerlilik süresi verilmezse, 
    # .env'den okuduğumuz (örn: 30 dakika) süreyi kullan
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Pasaportun "Son Kullanma Tarihi"ni ('exp') ekle
    to_encode.update({"exp": expire})

    # 'jwt.encode' aracını kullanarak pasaportu "imzala":
    # Veri + Gizli Anahtar (Mühür) + Algoritma
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # Oluşan 'eyJhbGciOi...' gibi şifreli metni geri döndür.
    return encoded_jwt