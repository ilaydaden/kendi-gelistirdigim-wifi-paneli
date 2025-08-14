from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class Basvuru(db.Model):
    """Wi-Fi başvuru modeli"""
    __tablename__ = 'basvurular'
    
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(50), nullable=False)
    soyad = db.Column(db.String(50), nullable=False)
    tc = db.Column(db.String(11), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=True)
    telefon = db.Column(db.String(15), nullable=True)
    ip_adresi = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    durum = db.Column(db.String(20), default='beklemede')  # beklemede, onaylandı, reddedildi
    onay_tarihi = db.Column(db.DateTime, nullable=True)
    onaylayan_admin = db.Column(db.Integer, db.ForeignKey('adminler.id'), nullable=True)
    aciklama = db.Column(db.Text, nullable=True)
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    guncelleme_tarihi = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    onaylayan_admin_relation = db.relationship('Admin', backref='onayladigi_basvurular')
    
    def __repr__(self):
        return f'<Basvuru {self.ad} {self.soyad}>'
    
    def to_dict(self):
        """Modeli dictionary'e çevirir"""
        return {
            'id': self.id,
            'ad': self.ad,
            'soyad': self.soyad,
            'tc': self.tc,
            'email': self.email,
            'telefon': self.telefon,
            'durum': self.durum,
            'tarih': self.olusturma_tarihi.strftime("%Y-%m-%d %H:%M:%S"),
            'onay_tarihi': self.onay_tarihi.strftime("%Y-%m-%d %H:%M:%S") if self.onay_tarihi else None,
            'aciklama': self.aciklama
        }

class Admin(UserMixin, db.Model):
    """Admin kullanıcı modeli"""
    __tablename__ = 'adminler'
    
    id = db.Column(db.Integer, primary_key=True)
    kullanici_adi = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    ad = db.Column(db.String(50), nullable=False)
    soyad = db.Column(db.String(50), nullable=False)
    rol = db.Column(db.String(20), default='admin')  # admin, super_admin
    aktif = db.Column(db.Boolean, default=True)
    son_giris = db.Column(db.DateTime, nullable=True)
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """Şifreyi hash'ler"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Şifreyi kontrol eder"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Admin {self.kullanici_adi}>'

class SistemLog(db.Model):
    """Sistem log modeli"""
    __tablename__ = 'sistem_loglari'
    
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('adminler.id'), nullable=True)
    islem_tipi = db.Column(db.String(50), nullable=False)  # login, logout, basvuru_onayla, basvuru_reddet
    islem_detayi = db.Column(db.Text, nullable=True)
    ip_adresi = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    tarih = db.Column(db.DateTime, default=datetime.utcnow)
    
    # İlişkiler
    admin = db.relationship('Admin', backref='loglar')
    
    def __repr__(self):
        return f'<SistemLog {self.islem_tipi} - {self.tarih}>'

class WiFikonfigurasyon(db.Model):
    """Wi-Fi konfigürasyon modeli"""
    __tablename__ = 'wifi_konfigurasyon'
    
    id = db.Column(db.Integer, primary_key=True)
    ssid = db.Column(db.String(50), nullable=False)
    sifre = db.Column(db.String(100), nullable=False)
    erisim_suresi = db.Column(db.Integer, default=24)  # saat cinsinden
    maksimum_cihaz = db.Column(db.Integer, default=1)
    aktif = db.Column(db.Boolean, default=True)
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    guncelleme_tarihi = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<WiFikonfigurasyon {self.ssid}>'

