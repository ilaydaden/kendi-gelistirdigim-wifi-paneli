# Wi-Fi Misafir Ağı Başvuru Sistemi

Modern ve kullanıcı dostu bir Wi-Fi misafir ağı başvuru sistemi. Flask ve Python ile geliştirilmiştir.

## 🌟 Özellikler

### Form Sayfası
- **Modern ve Responsive Tasarım**: Bootstrap 5 ve özel CSS ile
- **Çok Adımlı Form**: 2 adımda tamamlanan kullanıcı dostu form
- **Gelişmiş Validasyon**: Client-side ve server-side form validasyonu
- **Animasyonlar**: Smooth geçişler ve hover efektleri
- **Mobil Uyumlu**: Tüm cihazlarda mükemmel görünüm

### Form Alanları
- Ad ve Soyad
- TC Kimlik Numarası (11 haneli validasyon)
- E-posta Adresi
- Telefon Numarası
- KVKK ve Kullanım Şartları Onayı

### Admin Paneli
- **Modern Dashboard**: İstatistik kartları ve grafikler
- **Detaylı Başvuru Listesi**: Tüm form bilgilerini görüntüleme
- **Onay/Red Sistemi**: Tek tıkla başvuru yönetimi
- **Gerçek Zamanlı İstatistikler**: Chart.js ile görsel grafikler
- **Responsive Tablo**: Mobilde de kullanışlı

### Güvenlik
- **Session Yönetimi**: Güvenli admin girişi
- **Form Validasyonu**: Hem client hem server tarafında
- **XSS Koruması**: Input sanitization
- **CSRF Koruması**: Form güvenliği

## 🚀 Kurulum

### Gereksinimler
- Python 3.7+
- Flask ve ek paketler

### Adımlar

1. **Projeyi klonlayın:**
```bash
git clone https://github.com/ilaydaden/wifi-paneli.git
cd wifi-paneli
```

2. **Sanal ortam oluşturun (önerilen):**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Gerekli paketleri yükleyin:**
```bash
pip install -r requirements.txt
```

4. **Veritabanını başlatın:**
```bash
python migrations.py
```

5. **Uygulamayı çalıştırın:**
```bash
python app.py
```

6. **Tarayıcıda açın:**
```
http://localhost:5000
```

### İlk Kurulum Notları

- İlk çalıştırmada otomatik olarak varsayılan admin kullanıcısı oluşturulur
- **Kullanıcı adı:** `admin`
- **Şifre:** `admin123`
- Eski JSON verileriniz otomatik olarak veritabanına aktarılır

## 📱 Kullanım

### Misafir Kullanıcılar
1. Ana sayfada Wi-Fi başvuru formunu doldurun
2. 2 adımlı form sürecini takip edin:
   - **Adım 1**: Kişisel bilgiler
   - **Adım 2**: Onay ve gönderim
3. Formu gönderin ve onay bekleyin

### Admin Kullanıcılar
1. `/admin_login` sayfasına gidin
2. Kullanıcı adı ve şifre ile giriş yapın (varsayılan: `ılayda` / `ılayda123`)
3. Başvuruları görüntüleyin ve onaylayın/reddedin
4. İstatistikleri takip edin
5. Sistem loglarını inceleyin (süper admin)

## 🎨 Tasarım Özellikleri

### Renk Paleti
- **Ana Renk**: #667eea (Mavi-Mor gradient)
- **İkincil Renk**: #764ba2 (Mor)
- **Başarı**: #28a745 (Yeşil)
- **Uyarı**: #ffc107 (Sarı)
- **Hata**: #dc3545 (Kırmızı)

### Animasyonlar
- **Slide In**: Sayfa yüklenirken
- **Fade In**: Form adımları arası geçiş
- **Hover Effects**: Butonlar ve kartlar
- **Loading States**: Form gönderimi sırasında

### Responsive Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## 🔧 Özelleştirme

### Admin Şifresini Değiştirme
`app.py` dosyasında şu satırı bulun ve değiştirin:
```python
if sifre == 'admin123':  # Şifreni buraya yaz
```

### Form Alanlarını Özelleştirme
`templates/panel.html` dosyasında form alanlarını ekleyebilir/çıkarabilirsiniz.

### Renkleri Değiştirme
CSS dosyalarında renk değişkenlerini güncelleyin.

## 📊 Veritabanı Yapısı

### Başvuru Tablosu
```sql
CREATE TABLE basvurular (
    id INTEGER PRIMARY KEY,
    ad VARCHAR(50) NOT NULL,
    soyad VARCHAR(50) NOT NULL,
    tc VARCHAR(11) NOT NULL UNIQUE,
    email VARCHAR(120),
    telefon VARCHAR(15),
    ip_adresi VARCHAR(45),
    user_agent TEXT,
    durum VARCHAR(20) DEFAULT 'beklemede',
    onay_tarihi DATETIME,
    onaylayan_admin INTEGER,
    aciklama TEXT,
    olusturma_tarihi DATETIME DEFAULT CURRENT_TIMESTAMP,
    guncelleme_tarihi DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Admin Tablosu
```sql
CREATE TABLE adminler (
    id INTEGER PRIMARY KEY,
    kullanici_adi VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    ad VARCHAR(50) NOT NULL,
    soyad VARCHAR(50) NOT NULL,
    rol VARCHAR(20) DEFAULT 'admin',
    aktif BOOLEAN DEFAULT TRUE,
    son_giris DATETIME,
    olusturma_tarihi DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Sistem Log Tablosu
```sql
CREATE TABLE sistem_loglari (
    id INTEGER PRIMARY KEY,
    admin_id INTEGER,
    islem_tipi VARCHAR(50) NOT NULL,
    islem_detayi TEXT,
    ip_adresi VARCHAR(45),
    user_agent TEXT,
    tarih DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🔒 Güvenlik Notları

1. **Production'da admin şifresini değiştirin**
2. **HTTPS kullanın**
3. **Rate limiting ekleyin**
4. **Log dosyaları tutun**
5. **Düzenli yedekleme yapın**
6. **Veritabanı bağlantısını güvenli hale getirin**
7. **Environment variables kullanın**
8. **SQL injection koruması aktif**
9. **CSRF token koruması aktif**
10. **Session güvenliği sağlanmış**

## 🐛 Sorun Giderme

### Yaygın Sorunlar

**Flask çalışmıyor:**
```bash
pip install --upgrade flask
```

**Port hatası:**
```python
app.run(debug=True, port=5001)  # Farklı port kullanın
```

**Encoding hatası:**
Dosyaların UTF-8 ile kaydedildiğinden emin olun.

## 📈 Yeni Özellikler (v2.0)

### ✅ Tamamlanan Özellikler
- [x] **Veritabanı entegrasyonu** (SQLite)
- [x] **Gelişmiş form validasyonu** (WTForms)
- [x] **Admin kullanıcı yönetimi** (Flask-Login)
- [x] **Sistem logları** (audit trail)
- [x] **Güvenli şifre hashleme** (Werkzeug)
- [x] **Sayfalama** (pagination)
- [x] **Arama ve filtreleme**
- [x] **CSRF koruması**
- [x] **Session yönetimi**

### 🚧 Gelecek Özellikler
- [ ] E-posta bildirimleri
- [ ] QR kod ile hızlı giriş
- [ ] REST API entegrasyonu
- [ ] Çoklu dil desteği
- [ ] Gelişmiş raporlama
- [ ] Otomatik Wi-Fi erişim yönetimi
- [ ] PostgreSQL desteği
- [ ] Docker containerization
- [ ] Redis caching
- [ ] WebSocket real-time bildirimler

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit yapın (`git commit -m 'Add some AmazingFeature'`)
4. Push yapın (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 👨‍💻 Geliştirici

**İlayda Den** - [GitHub](https://github.com/ilaydaden)

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!
