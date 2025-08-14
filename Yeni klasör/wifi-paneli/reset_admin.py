from app import app, db
from models import Admin
from werkzeug.security import generate_password_hash

def reset_admin_password():
    """Admin şifresini sıfırlar"""
    with app.app_context():
        # Mevcut admin kullanıcısını bul
        admin = Admin.query.filter_by(kullanici_adi='admin').first()
        
        if admin:
            # Şifreyi sıfırla
            admin.set_password('admin123')
            admin.aktif = True
            db.session.commit()
            print("Admin şifresi başarıyla sıfırlandı!")
            print("Kullanıcı adı: admin")
            print("Şifre: admin123")
        else:
            # Yeni admin kullanıcısı oluştur
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
            print("Yeni admin kullanıcısı oluşturuldu!")
            print("Kullanıcı adı: admin")
            print("Şifre: admin123")

if __name__ == '__main__':
    reset_admin_password()


