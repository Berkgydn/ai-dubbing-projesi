# SQLAlchemy'nin "Konuşma" (Session) aracını ithal et.
# Bu, 'database.py'deki o "Giriş İzni Ofisi"nden (SessionLocal)
# izin almamızı sağlayacak.
from sqlalchemy.orm import Session

# Mimarın "Raf Planı"nı (models) ve "Veri Zarfı"nı (schemas) ithal et.
# Çünkü depo görevlisi, bu ikisini de bilmek zorundadır.
import models, schemas
# (Not: .database, .models gibi göreceli import yerine,
# __init__.py sayesinde 'doğrudan' import ediyoruz)

# --- DEPO GÖREVLİSİNİN FONKSİYONLARI ---

# Görev 1: E-postaya Göre Kullanıcı Bul
# (Bu, "Bu e-posta zaten kayıtlı mı?" diye kontrol etmek için ÇOK önemlidir)
def get_user_by_email(db: Session, email: str):
    # Der ki: "Ey 'db' (veritabanı konuşması)! Mimarın 'User' rafına (modeline) git.
    # O raftaki 'email' etiketi (sütunu), benim sana verdiğim 'email' ile
    # eşleşen İLK kaydı bul ve bana getir."
    return db.query(models.User).filter(models.User.email == email).first()

# Görev 2: ID'ye Göre Kullanıcı Bul (Şimdilik Gerekli Değil ama İyi Bir Pratik)
def get_user(db: Session, user_id: int):
    # Der ki: "Ey 'db'! 'User' rafına git. 'id' etiketi benim sana
    # verdiğim 'user_id' ile eşleşen İLK kaydı bul."
    return db.query(models.User).filter(models.User.id == user_id).first()

# Görev 3: Yeni Kullanıcı Oluştur (KAYIT İŞLEMİ BURADA OLUR)
# Bu, 'main.py'den "kayıt zarfı"nı (schemas.UserCreate) ve "şifrelenmiş şifreyi" alır.
def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):

    # 1. Mimarın "User" planını kullanarak (models.User) yeni bir "ürün" (kullanıcı) oluştur.
    db_user = models.User(
        email=user.email,             # Zarfın içindeki e-postayı al
        hashed_password=hashed_password # DİKKAT: 'main.py'den gelen "şifrelenmiş" parolayı al
    )

    # 2. O yeni "ürünü" (db_user) al ve depoya (db) "ekle" (add).
    # (Bu henüz depoya YAZMAZ, sadece "yazılacaklar listesine" ekler).
    db.add(db_user)

    # 3. "Şimdi tüm listeyi depoya kalıcı olarak YAZ" (commit).
    db.commit()

    # 4. Deponun bu yeni ürüne verdiği 'id'yi ve diğer bilgileri "yenile" (refresh).
    # (Bunu yapmazsak, db_user'ın 'id' alanı boş kalırdı).
    db.refresh(db_user)

    # 5. Bu yeni oluşturulmuş, tam teşekküllü "ürünü" (db_user) geri döndür.
    return db_user