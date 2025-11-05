# --- Adım 1: Temel İmaj (Hangi Fırını Kullanacağız?) ---
# Python'un resmi 3.10 "slim" (hafif) versiyonunu temel alarak başla.
# "Benim makinemde biter" sorununu bu satır çözer. Herkesin fırını aynı olur.
FROM python:3.10-slim

# --- Adım 2: Çalışma Ortamı (Nerede Çalışacağız?) ---
# Kutucuğun içinde /app adında bir klasör oluştur ve tüm komutları orada çalıştır.
WORKDIR /app

# --- Adım 3: Malzemeleri Kopyalama (Malzemeler Fırına) ---
# Önce SADECE malzeme listemizi (requirements.txt) kutucuğun içine kopyala.
# Neden tüm kodu değil? Docker'ın "önbellekleme" özelliği için.
# Eğer kod değişir ama malzeme listesi değişmezse, Docker 4. adımı atlar ve inşa süresi 1-2 dakika kısalır.
COPY requirements.txt .

# --- Adım 4: Malzemeleri Kurma (Malzemeler Hazırlanıyor) ---
# Malzeme listesini kullanarak tüm Python kütüphanelerini kutucuğun içine kur.
RUN pip install --no-cache-dir -r requirements.txt

# --- Adım 5: Kodu Kopyalama (Yemek Fırına) ---
# Artık tüm kodumuzu (backend klasörümüzdeki her şeyi) kutucuğun içine, /app klasörüne kopyala.
COPY . .

# --- Adım 6: Başlatma Komutu (Fırını Çalıştır) ---
# Kutucuk (konteyner) ayağa kalktığında HANGİ komutu çalıştıracağını söyle.
# "uvicorn" sunucusunu başlat. Sunucu "main.py" dosyasındaki "app" adındaki FastAPI uygulamamızı çalıştırsın.
# "host 0.0.0.0" -> Kutucuğun içindeki *tüm* IP'lerden gelen isteklere cevap ver (Docker için şarttır).
# "port 8000" -> 8000 portunu dinle (docker-compose.yml'de eşleştirdiğimiz port).
# "reload" -> Koddaki değişikliği izle (volumes sayesinde kod değişince) ve sunucuyu yeniden başlat (canlı yenileme).
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]