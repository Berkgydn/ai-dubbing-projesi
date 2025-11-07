import React from 'react'
import ReactDOM from 'react-dom/client'

// Harita araçları
import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom"; 

// Sayfalarımızı ithal et
import App from './App.jsx' 
import Login from './pages/login.jsx';       // <-- YENİ İTHALAT
import Register from './pages/Register.jsx'; // <-- YENİ İTHALAT

import './index.css' 

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>

        {/* Ana adres (Hala App.jsx'i gösteriyor) */}
        <Route path="/" element={<App />} />

        {/* YENİ ADRESLERİMİZ (Adım 2.11) */}

        {/* path="/login" -> Kullanıcı localhost:3000/login adresine gelirse... */}
        {/* element={<Login />} -> ...ekrana 'Login.jsx' bileşenini yükle. */}
        <Route path="/login" element={<Login />} />

        {/* path="/register" -> Kullanıcı localhost:3000/register adresine gelirse... */}
        {/* element={<Register />} -> ...ekrana 'Register.jsx' bileşenini yükle. */}
        <Route path="/register" element={<Register />} />

      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
)