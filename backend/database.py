# --- Gerekli Kütüphaneleri İthal Etme ---

# "os" (Operating System) modülü, .env dosyasındaki değişkenleri
# okumak gibi işletim sistemiyle ilgili işler için kullanılır.
import os 

# "dotenv" kütüphanesinden, .env dosyasını "yüklememizi" sağlayan
# 'load_dotenv' fonksiyonunu ithal et.
from dotenv import load_dotenv 

# "sqlalchemy" (Bizim Tercümanımız) kütüphanesinden 3 ana araç ithal et:
# 1. create_engine: Veritabanına giden "ana motoru" (boru hattını) inşa eder.
from sqlalchemy import create_engine 

# 2. declarative_base: "Ana Şablon Kağıdımızı" (Base) oluşturmamızı sağlar.
from sqlalchemy.ext.declarative import declarative_base 

# 3. sessionmaker: "Konuşma Fabrikamızı" (SessionLocal) oluşturur.
from sqlalchemy.orm import sessionmaker 

# --- Kurulum Adımları ---

# '.env' dosyasını bul ve içindeki tüm sırları (DATABASE_URL gibi)
# bu programın "ortam değişkenlerine" yükle.
load_dotenv() 

# Az önce yüklenen o "ortam değişkenleri" arasından, 
# tam olarak "DATABASE_URL" adındakini oku ve bir Python değişkenine ata.
# Bu bizim "Adres Mektubumuzdur".
DATABASE_URL = os.getenv("DATABASE_URL") 

# --- Araçların Oluşturulması ---

# "Motor Kurucu" (create_engine) aracını çağır.
# Ona "Adres Mektubu"nu (DATABASE_URL) ver.
# O da bu adresteki veritabanı (db servisi) ile konuşabilen
# ana "motoru" (engine) inşa etsin.
engine = create_engine(DATABASE_URL) 

# "Konuşma Fabrikası"nı (sessionmaker) çağır.
# Bu fabrikaya 'SessionLocal' adını veriyoruz.
# Bu fabrikadan çıkacak her "konuşma" (session) için şu 3 kuralı koy:
# 1. autocommit=False: Kaydetme işini (commit) otomatik yapma, ben sana 'kaydet' deyince yap.
# 2. autoflush=False: Verileri otomatik olarak veritabanına "yollama", ben deyince yolla.
# 3. bind=engine: Bu fabrikadan çıkan her "konuşma", az önce oluşturduğumuz 'engine' (motoru) kullansın.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

# "Ana Şablon Kağıdı Oluşturucu"yu (declarative_base) çağır.
# O da bize, üzerine tüm "raf planlarımızı" (modellerimizi) çizeceğimiz
# sihirli 'Base' (Ana Şablon) sınıfını oluştursun.
Base = declarative_base()