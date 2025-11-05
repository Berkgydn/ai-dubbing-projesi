from fastapi import FastAPI

# FastAPI uygulamasını "app" adıyla oluştur
# Bu, Dockerfile'daki 'main:app' komutunun aradığı "app" nesnesidir.
app = FastAPI()


# Ana sayfa ("/") için bir 'GET' isteği (endpoint) tanımla
# Birisi tarayıcıdan http://localhost:8000/ adresine girdiğinde,
# FastAPI bu fonksiyonu çalıştıracak.
@app.get("/")
def read_root():
    # Tarayıcıya bir JSON mesajı döndür
    return {"mesaj": "Tebrikler! FastAPI backend'iniz calisiyor!"}


# Başka bir test noktası (isteğe bağlı ama güzel bir pratik)
@app.get("/test")
def read_test():
    return {"deneme": "basarili", "proje_adi": "AI Dublaj Projesi"}