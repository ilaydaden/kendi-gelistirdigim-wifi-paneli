from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
import re

class BasvuruForm(FlaskForm):
    """Wi-Fi başvuru formu"""
    ad = StringField('Ad', validators=[
        DataRequired(message='Ad alanı zorunludur'),
        Length(min=2, max=50, message='Ad 2-50 karakter arasında olmalıdır')
    ])
    
    soyad = StringField('Soyad', validators=[
        DataRequired(message='Soyad alanı zorunludur'),
        Length(min=2, max=50, message='Soyad 2-50 karakter arasında olmalıdır')
    ])
    
    tc = StringField('TC Kimlik Numarası', validators=[
        DataRequired(message='TC Kimlik Numarası zorunludur'),
        Length(min=11, max=11, message='TC Kimlik Numarası 11 haneli olmalıdır')
    ])
    
    email = StringField('E-posta Adresi', validators=[
        Email(message='Geçerli bir e-posta adresi giriniz'),
        Length(max=120, message='E-posta adresi çok uzun')
    ])
    
    telefon = StringField('Telefon Numarası', validators=[
        Length(max=15, message='Telefon numarası çok uzun')
    ])
    
    kvkk_onay = BooleanField('KVKK ve Kullanım Şartlarını kabul ediyorum', validators=[
        DataRequired(message='KVKK onayı zorunludur')
    ])
    
    submit = SubmitField('Başvuru Gönder')
    
    def validate_tc(self, field):
        """TC kimlik numarası validasyonu"""
        if not field.data.isdigit():
            raise ValidationError('TC Kimlik Numarası sadece rakam içermelidir')
        
        # TC kimlik numarası algoritma kontrolü
        tc = field.data
        if len(tc) != 11 or tc[0] == '0':
            raise ValidationError('Geçersiz TC Kimlik Numarası')
        
        # Basit algoritma kontrolü
        odd_sum = sum(int(tc[i]) for i in range(0, 9, 2))
        even_sum = sum(int(tc[i]) for i in range(1, 8, 2))
        
        if (odd_sum * 7 - even_sum) % 10 != int(tc[9]):
            raise ValidationError('Geçersiz TC Kimlik Numarası')
        
        if sum(int(tc[i]) for i in range(10)) % 10 != int(tc[10]):
            raise ValidationError('Geçersiz TC Kimlik Numarası')
    
    def validate_telefon(self, field):
        """Telefon numarası validasyonu"""
        if field.data:
            # Sadece rakamları al
            phone = re.sub(r'\D', '', field.data)
            if len(phone) < 10 or len(phone) > 11:
                raise ValidationError('Geçerli bir telefon numarası giriniz')

class AdminLoginForm(FlaskForm):
    """Admin giriş formu"""
    kullanici_adi = StringField('Kullanıcı Adı', validators=[
        DataRequired(message='Kullanıcı adı zorunludur')
    ])
    
    password = PasswordField('Şifre', validators=[
        DataRequired(message='Şifre zorunludur')
    ])
    
    remember_me = BooleanField('Beni Hatırla')
    submit = SubmitField('Giriş Yap')

class AdminCreateForm(FlaskForm):
    """Admin oluşturma formu"""
    kullanici_adi = StringField('Kullanıcı Adı', validators=[
        DataRequired(message='Kullanıcı adı zorunludur'),
        Length(min=3, max=80, message='Kullanıcı adı 3-80 karakter arasında olmalıdır')
    ])
    
    email = StringField('E-posta', validators=[
        DataRequired(message='E-posta zorunludur'),
        Email(message='Geçerli bir e-posta adresi giriniz')
    ])
    
    ad = StringField('Ad', validators=[
        DataRequired(message='Ad zorunludur'),
        Length(min=2, max=50, message='Ad 2-50 karakter arasında olmalıdır')
    ])
    
    soyad = StringField('Soyad', validators=[
        DataRequired(message='Soyad zorunludur'),
        Length(min=2, max=50, message='Soyad 2-50 karakter arasında olmalıdır')
    ])
    
    password = PasswordField('Şifre', validators=[
        DataRequired(message='Şifre zorunludur'),
        Length(min=6, message='Şifre en az 6 karakter olmalıdır')
    ])
    
    password_confirm = PasswordField('Şifre Tekrar', validators=[
        DataRequired(message='Şifre tekrarı zorunludur'),
        EqualTo('password', message='Şifreler eşleşmiyor')
    ])
    
    rol = SelectField('Rol', choices=[
        ('admin', 'Admin'),
        ('super_admin', 'Süper Admin')
    ], validators=[DataRequired()])
    
    submit = SubmitField('Admin Oluştur')

class BasvuruOnayForm(FlaskForm):
    """Başvuru onay/red formu"""
    durum = SelectField('Durum', choices=[
        ('onaylandı', 'Onayla'),
        ('reddedildi', 'Reddet')
    ], validators=[DataRequired()])
    
    aciklama = TextAreaField('Açıklama (Opsiyonel)', validators=[
        Length(max=500, message='Açıklama çok uzun')
    ])
    
    submit = SubmitField('İşlemi Tamamla')

