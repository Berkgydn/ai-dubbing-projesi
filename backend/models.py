# --- Gerekli Kütüphaneleri İthal Etme ---

# "sqlalchemy" kütüphanesinden, planımızı "çizmek" için gereken
# "inşaat malzemelerini" (Etiket/Sütun tiplerini) ithal et.
from sqlalchemy import Column, Integer, String, Boolean 

# Bizim kendi 'database.py' dosyamızdan ('.' aynı klasör demektir)
# az önce oluşturduğumuz o sihirli 'Base' (Ana Şablon Kağıdı) sınıfını ithal et.
from database import Base 

# --- Planın Çizilmesi ---

# 'User' (Kullanıcı) adında yeni bir Python sınıfı (plan) oluştur.
# Bu sınıfın, o sihirli 'Base' şablonunu "miras aldığını" (Base) ile belirt.
# (Böylece SQLAlchemy bunun bir "raf planı" olduğunu anlar).
class User(Base):
    
    # SQLAlchemy için sihirli bir değişken:
    # "Bu 'User' planı, veritabanında *gerçek* bir raf (tablo) olarak
    # inşa edildiğinde, ona lütfen 'users' adını ver."
    __tablename__ = "users" 

    # --- Rafın Etiketleri (Sütunlar) ---

    # 'id' adında bir "Etiket" (Column) oluştur.
    # Tipi: 'Integer' (Tamsayı: 1, 2, 3...)
    # 'primary_key=True': Bu, rafın 'Ana Anahtarı'dır (Benzersiz Kimlik Kartı). 
    #                     Boş olamaz, asla tekrar edemez.
    # 'index=True': Bu sütunda çok arama yapılır, bu yüzden aramayı hızlandır (fihrist oluştur).
    id = Column(Integer, primary_key=True, index=True) 

    # 'email' adında bir "Etiket" (Column) oluştur.
    # Tipi: 'String' (Metin: 'test@mail.com' gibi)
    # 'unique=True': BU ÇOK ÖNEMLİ BİR KURALDIR. Veritabanına der ki:
    #                "Bu rafa ASLA aynı 'email' değerine sahip ikinci bir kayıt ekleyemezsin."
    # 'index=True': E-postaya göre de çok arama yapılır, bunu da hızlandır.
    email = Column(String, unique=True, index=True) 

    # 'hashed_password' adında bir "Etiket" (Column) oluştur.
    # Tipi: 'String' (Metin).
    # Buraya kullanıcının '1234' şifresini değil, o şifrenin
    # 'e$2b$12...' gibi "karıştırılmış" (hash'lenmiş) halini saklayacağız.
    hashed_password = Column(String) 

    # 'is_active' adında bir "Etiket" (Column) oluştur.
    # Tipi: 'Boolean' (Evet/Hayır - True/False)
    # 'default=True': Eğer bu kullanıcıyı oluştururken bu alanı boş bırakırsak,
    #                 Veritabanı *varsayılan olarak* bu alanı 'True' (Aktif) yapsın.
    is_active = Column(Boolean, default=True)