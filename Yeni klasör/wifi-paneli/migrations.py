from app import app, db
from models import Basvuru, Admin, SistemLog, WiFikonfigurasyon
from werkzeug.security import generate_password_hash
from datetime import datetime
import json
import os

def migrate_from_json():
    """JSON dosyasından veritabanına veri aktarımı"""
    json_file = 'basvurular.json'
    
    if not os.path.exists(json_file):
        print("JSON dosyası bulunamadı!")
        return
    
    with open(json_file, 'r', encoding='utf-8') as f:
        basvurular_data = json.load(f)
    
    migrated_count = 0
    for basvuru_data in basvurular_data:
        # TC kimlik numarası kontrolü
        existing = Basvuru.query.filter_by(tc=basvuru_data.get('tc', '')).first()
        if existing:
            print(f"TC {basvuru_data.get('tc')} zaten mevcut, atlanıyor...")
            continue
        
        # Tarih formatını düzelt
        try:
            tarih = datetime.strptime(basvuru_data.get('tarih', ''), "%Y-%m-%d %H:%M:%S")
        except:
            tarih = datetime.utcnow()
        
        # Yeni başvuru oluştur
        basvuru = Basvuru(
            ad=basvuru_data.get('ad', ''),
            soyad=basvuru_data.get('soyad', ''),
            tc=basvuru_data.get('tc', ''),
            email=basvuru_data.get('email', ''),
            telefon=basvuru_data.get('telefon', ''),
            durum=basvuru_data.get('durum', 'beklemede'),
            olusturma_tarihi=tarih
        )
        
        db.session.add(basvuru)
        migrated_count += 1
    
    db.session.commit()
    print(f"{migrated_count} başvuru başarıyla aktarıldı!")

def create_default_admin():
    """Varsayılan admin kullanıcısı oluşturur"""
    if Admin.query.first():
        print("Admin kullanıcısı zaten mevcut!")
        return
    
    admin = Admin(
        kullanici_adi='admin',
        email='admin@wifi-paneli.com',
        ad='Sistem',
        soyad='Yöneticisi',
        rol='super_admin',
        aktif=True
    )
    admin.set_password('admin123')
    
    db.session.add(admin)
    db.session.commit()
    print("Varsayılan admin kullanıcısı oluşturuldu!")
    print("Kullanıcı adı: admin")
    print("Şifre: admin123")

def create_default_wifi_config():
    """Varsayılan Wi-Fi konfigürasyonu oluşturur"""
    if WiFikonfigurasyon.query.first():
        print("Wi-Fi konfigürasyonu zaten mevcut!")
        return
    
    wifi_config = WiFikonfigurasyon(
        ssid='Misafir-WiFi',
        sifre='misafir123',
        erisim_suresi=24,
        maksimum_cihaz=1,
        aktif=True
    )
    
    db.session.add(wifi_config)
    db.session.commit()
    print("Varsayılan Wi-Fi konfigürasyonu oluşturuldu!")

if __name__ == '__main__':
    with app.app_context():
        print("Veritabanı tabloları oluşturuluyor...")
        db.create_all()
        
        print("Varsayılan admin kullanıcısı oluşturuluyor...")
        create_default_admin()
        
        print("Varsayılan Wi-Fi konfigürasyonu oluşturuluyor...")
        create_default_wifi_config()
        
        print("JSON dosyasından veri aktarımı yapılıyor...")
        migrate_from_json()
        
        print("Migration tamamlandı!")

