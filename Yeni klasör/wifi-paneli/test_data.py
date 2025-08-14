from app import app, db
from models import Basvuru
from datetime import datetime, timedelta
import random

def create_test_data():
    """Test için örnek başvuru verileri oluşturur"""
    with app.app_context():
        # Mevcut başvuruları kontrol et
        if Basvuru.query.count() > 0:
            print("Zaten başvuru verileri mevcut!")
            return
        
        # Örnek isimler
        isimler = [
            ("Ahmet", "Yılmaz"),
            ("Ayşe", "Demir"),
            ("Mehmet", "Kaya"),
            ("Fatma", "Çelik"),
            ("Ali", "Özkan"),
            ("Zeynep", "Arslan"),
            ("Mustafa", "Doğan"),
            ("Elif", "Kılıç"),
            ("Hasan", "Şahin"),
            ("Meryem", "Koç")
        ]
        
        # Örnek e-posta domainleri
        domains = ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com"]
        
        # Durumlar
        durumlar = ["beklemede", "onaylandı", "reddedildi"]
        
        for i, (ad, soyad) in enumerate(isimler):
            # TC kimlik numarası oluştur (11 haneli)
            tc = f"1234567890{i:02d}"
            
            # E-posta oluştur
            email = f"{ad.lower()}.{soyad.lower()}@{random.choice(domains)}"
            
            # Telefon oluştur
            telefon = f"05{random.randint(30, 50)}{random.randint(1000000, 9999999)}"
            
            # Rastgele tarih (son 30 gün içinde)
            gun_farki = random.randint(0, 30)
            tarih = datetime.utcnow() - timedelta(days=gun_farki)
            
            # Rastgele durum
            durum = random.choice(durumlar)
            
            # Başvuru oluştur
            basvuru = Basvuru(
                ad=ad,
                soyad=soyad,
                tc=tc,
                email=email,
                telefon=telefon,
                durum=durum,
                olusturma_tarihi=tarih,
                ip_adresi=f"192.168.1.{random.randint(100, 200)}",
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            
            db.session.add(basvuru)
        
        db.session.commit()
        print("10 adet test başvurusu oluşturuldu!")

if __name__ == '__main__':
    create_test_data()


