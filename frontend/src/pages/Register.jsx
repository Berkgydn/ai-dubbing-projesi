// React'in 'useState' (hafıza) ve 'useNavigate' (yönlendirme)
// araçlarını ve 'axios' (Posta Servisi) kütüphanesini ithal et
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // Sayfa yönlendirme için

function Register() {
  // 1. "Hafıza" alanlarını oluştur
  // 'email' hafızası ve onu güncelleyecek 'setEmail' fonksiyonu
  const [email, setEmail] = useState('');
  // 'password' hafızası ve onu güncelleyecek 'setPassword' fonksiyonu
  const [password, setPassword] = useState('');

  // 'message' hafızası (Başarılı/Hata mesajlarını göstermek için)
  const [message, setMessage] = useState('');

  // Yönlendirme aracını çağır
  const navigate = useNavigate();

  // 2. "Gönder" Butonuna Tıklandığında Çalışacak Fonksiyon
  const handleSubmit = async (event) => {
    // Formun sayfayı yenilemesini (varsayılan HTML davranışı) engelle
    event.preventDefault();

    try {
      // 3. "Posta Servisi"ni (axios) kullanarak Backend'e (API) VERİ GÖNDER
      // Nereye? 'http://localhost:8000/users/register' adresine
      // Ne? { email: ..., password: ... } verisini (JSON olarak)
      const response = await axios.post('http://localhost:8000/users/register', {
        email: email,
        password: password
      });

      // 4. BAŞARILI OLURSA (Backend'den cevap gelirse):
      setMessage('Kayıt başarılı! Giriş sayfasına yönlendiriliyorsunuz...');

      // 2 saniye bekle, sonra kullanıcıyı "/login" sayfasına "yönlendir"
      setTimeout(() => {
        navigate('/login');
      }, 2000);

    } catch (error) {
      // 5. BAŞARISIZ OLURSA (Backend'den Hata 400 - "Email zaten kayıtlı" - gelirse):
      // Backend'den gelen 'detay' mesajını yakala ve 'message' hafızasına yaz
      setMessage(error.response.data.detail || 'Bir hata oluştu.');
    }
  };

  // 6. Ekrana Çizilecek Olan HTML (JSX) Formu
  return (
    <div>
      <h1>Kayıt Ol</h1>
      {/* 'onSubmit' -> Forma "gönder" emri geldiğinde 'handleSubmit' fonksiyonunu çalıştır */}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email} // Input'un değerini 'email' hafızasından al
            // Input'a bir şey yazıldığında 'email' hafızasını güncelle
            onChange={(e) => setEmail(e.target.value)}
            required // Bu alanın boş olmamasını sağla
          />
        </div>
        <div>
          <label>Şifre:</label>
          <input
            type="password"
            value={password} // Input'un değerini 'password' hafızasından al
            // Input'a bir şey yazıldığında 'password' hafızasını güncelle
            onChange={(e) => setPassword(e.target.value)}
            required // Bu alanın boş olmamasını sağla
          />
        </div>
        <button type="submit">Kayıt Ol</button>
      </form>

      {/* Başarı veya Hata mesajını göstermek için */}
      {message && <p>{message}</p>}
    </div>
  );
}

export default Register;