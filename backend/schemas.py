#schemas.py dosyasının tek görevi, 
#backend'imize (API) gelen ve backend'imizden giden verilerin şeklini (kalıbını) tanımlamaktır.



# Pydantic, FastAPI'nin "Veri Zarfı" modellemesi için
# kullandığı ana kütüphanedir.
from pydantic import BaseModel

# --- Kullanıcı Zarfları ---

# Zarf 1: Kullanıcı Oluşturma (Frontend -> Backend)
# Frontend bize bir kullanıcıyı kaydetmek için NE göndermeli?
class UserCreate(BaseModel):
    email: str
    password: str
#Özetle: UserCreate zarfı, /register API'mize 
#"Bana sadece email ve password ver, ikisi de metin olsun" diye kural koyar. 
#Başka bir şey (örn: id) gönderilirse kabul etmez.


# Zarf 2: Kullanıcıyı Geri Döndürme (Backend -> Frontend)
# Biz bir kullanıcıyı (veya kaydettikten sonra) Frontend'e NE göndermeliyiz?
# ASLA 'hashed_password'ı göndermemeliyiz.
# BU, BİZİM FRONTEND'E GÜVENLE GÖNDERECEĞİMİZ VERİNİN ŞEKLİDİR.
class User(BaseModel):
    id: int
    email: str
    is_active: bool

    # Bu sihirli ayar, Pydantic'e der ki:
    # "Sen bir 'Mimar Planı'ndan ('models.User') veri alsan bile
    # (ki o bir Python sınıfıdır, JSON değil), onu 
    # bu 'Veri Zarfı'na ('User') dönüştürmeyi akıl et."
    # (Eskiden orm_mode=True idi, şimdi from_attributes=True)
    # Bu 'User' zarfı için özel bir "Yapılandırma" (Config) sınıfı tanımla.
    class Config:
        # Bu, Pydantic'e (Zarf Kütüphanesi) "Tercüman" (SQLAlchemy)
        # ile konuşmayı öğreten ayardır.
        # Anlamı: "Sana veri 'models.User' gibi bir 'Mimar Planı'ndan (nesneden)
        # gelse bile, sen o nesnenin 'id', 'email' gibi ÖZELLİKLERİNİ (attributes)
        # okuyup bu 'User' zarfına dönüştürmeyi akıl et."
        from_attributes = True