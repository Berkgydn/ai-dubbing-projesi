# --- Adım 1: Temel İmaj (Hangi Fırın/Motor?) ---
# Vite jeneratörünü 'node:22-alpine' ile kurduk, o yüzden 'fırınımız' da 'node:22-alpine' olmalı.
# Motorlarımızın uyumlu olması KRİTİKTİR.
FROM node:22-alpine

# --- Adım 2: Çalışma Ortamı ---
# Kutucuğun içinde /app adında bir klasör oluştur ve tüm komutları orada çalıştır.
WORKDIR /app

# --- Adım 3: Malzeme Listesini Kopyala (Önbellekleme için) ---
# Önce SADECE 'package.json' ve 'package-lock.json' (eğer oluştuysa) dosyalarını kopyala.
# Neden? Kod değişir ama 'Malzeme Listesi' değişmezse, Docker 4. adımı (npm install) atlar
# ve inşa 2 dakika daha hızlı biter.
COPY package.json package-lock.json* ./

# --- Adım 4: Malzemeleri Kur (İşte 'No' Dediğimiz O Adım!) ---
# 'npm install' komutunu kutucuğun içinde çalıştır.
# Bu, 'Malzeme Listesine' bakarak devasa 'node_modules' klasörünü kutucuğun İÇİNDE oluşturur.
RUN npm install

# --- Adım 5: Kodu Kopyala (Yemek Fırına) ---
# Geri kalan tüm kodumuzu (src, vite.config.js vb.) kutucuğun içine kopyala.
# ( volumes-portalımız bu dosyaları 'canlı' olarak güncelleyecek olsa da,
# 'ilk inşa' ve 'volumes' olmadan çalıştırma için bu adım şarttır.)
COPY . .

# --- Adım 6: Başlatma Komutu (Vite'e Özel SİHİRLİ KISIM) ---
# Bu, size bahsettiğim o "küçük teknik ayardır".
#
# "npm run dev" -> 'package.json' dosyasındaki "dev" komutunu çalıştır (o da 'vite' demektir).
# "--"          -> "Bundan sonra gelenler 'npm' için değil, doğrudan 'vite'in kendisi içindir" der.
# "--host"      -> "Sadece 'localhost'u değil, dışarıdan (yani bizim ana makinemizden - Dünya 1) 
#                  gelen bağlantıları da dinle" der.
#
# BU İKİ KÜÇÜK EKLEME, VITE'IN DOCKER'DA ÇALIŞMASI İÇİN HAYATİ ÖNEM TAŞIR.


# Bu yeni satırda "--port", "3000" ekledik
CMD ["npm", "run", "dev", "--", "--host", "--port", "3000"]