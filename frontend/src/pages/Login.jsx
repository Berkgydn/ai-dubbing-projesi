import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Login() {
  // 1. "Hafıza" alanlarını oluştur
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  // 'message' hafızası (Hata mesajlarını göstermek için)
  const [message, setMessage] = useState('');

  const navigate = useNavigate();

  // 2. "Gönder" Butonuna Tıklandığında Çalışacak Fonksiyon
  const handleSubmit = async (event) => {
    event.preventDefault(); // Formun sayfayı yenilemesini engelle

    try {
      // 3. "Posta Servisi"ni (axios) kullanarak Backend'e (API) VERİ GÖNDER
      // Nereye? 'http://localhost:8000/users/login' adresine
      // Ne? { email: ..., password: ... } verisini (Backend'imiz bu zarfı bekliyordu)
      const response = await axios.post('http://localhost:8000/users/login', {
        email: email,
        password: password
      });

      // 4. BAŞARILI OLURSA (Backend'den "Pasaport" - Token - gelirse):

      // Gelen "Pasaportu" (response.data.access_token) al
      const token = response.data.access_token;

      // "Pasaportu" tarayıcının 'localStorage' (kalıcı hafıza) bölümüne kaydet.
      // Bu, kullanıcı sayfayı yenilese veya kapatsa bile "giriş yapmış" kalmasını sağlar.
      localStorage.setItem('userToken', token);

      // Kullanıcıya bilgi ver
      setMessage('Giriş başarılı! Ana sayfaya yönlendiriliyorsunuz...');

      // 2 saniye bekle, sonra kullanıcıyı "/" (Ana Sayfa) adresine "yönlendir"
      setTimeout(() => {
        navigate('/');
      }, 2000);

    } catch (error) {
      // 5. BAŞARISIZ OLURSA (Backend'den Hata 401 - "Email veya sifre yanlis" - gelirse):
      setMessage(error.response.data.detail || 'Bir hata oluştu.');
    }
  };

  // 6. Ekrana Çizilecek Olan HTML (JSX) Formu
  return (
    <div>
      <h1>Giriş Yap</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Şifre:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Giriş Yap</button>
      </form>

      {message && <p>{message}</p>}
    </div>
  );
}

export default Login;