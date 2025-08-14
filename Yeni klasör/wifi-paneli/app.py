from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
import os
from datetime import datetime
from config import Config
from models import db, Basvuru, Admin, SistemLog
from forms import BasvuruForm, AdminLoginForm, BasvuruOnayForm
from qr_generator import generate_form_qr_code, generate_wifi_qr_code

app = Flask(__name__)
app.config.from_object(Config)

# Veritabanı ve login manager kurulumu
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'
login_manager.login_message = 'Bu sayfaya erişmek için giriş yapmalısınız.'

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

def log_islem(islem_tipi, islem_detayi=None):
    """Sistem log kaydı oluşturur"""
    log = SistemLog(
        admin_id=current_user.id if current_user.is_authenticated else None,
        islem_tipi=islem_tipi,
        islem_detayi=islem_detayi,
        ip_adresi=request.remote_addr,
        user_agent=request.headers.get('User-Agent')
    )
    db.session.add(log)
    db.session.commit()

@app.route('/')
def form():
    form = BasvuruForm()
    return render_template('panel.html', form=form)

@app.route('/bildir', methods=['POST'])
def bildir():
    form = BasvuruForm()
    if form.validate_on_submit():
        # TC kimlik numarası kontrolü
        mevcut_basvuru = Basvuru.query.filter_by(tc=form.tc.data).first()
        if mevcut_basvuru:
            flash('Bu TC kimlik numarası ile daha önce başvuru yapılmış.', 'error')
            return render_template('panel.html', form=form)
        
        # Yeni başvuru oluştur
        yeni_basvuru = Basvuru(
            ad=form.ad.data,
            soyad=form.soyad.data,
            tc=form.tc.data,
            email=form.email.data,
            telefon=form.telefon.data,
            ip_adresi=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        
        db.session.add(yeni_basvuru)
        db.session.commit()
        
        flash('Başvurunuz başarıyla alınmıştır. Onaylandıktan sonra size bilgi verilecektir.', 'success')
        return redirect(url_for('form'))
    
    # Form hataları varsa
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{getattr(form, field).label.text}: {error}', 'error')
    
    return render_template('panel.html', form=form)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_panel'))
    
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(kullanici_adi=form.kullanici_adi.data).first()
        if admin and admin.check_password(form.password.data) and admin.aktif:
            login_user(admin, remember=form.remember_me.data)
            admin.son_giris = datetime.utcnow()
            db.session.commit()
            
            log_islem('login', f'Admin girişi: {admin.kullanici_adi}')
            flash('Başarıyla giriş yaptınız!', 'success')
            return redirect(url_for('admin_panel'))
        else:
            flash('Geçersiz kullanıcı adı veya şifre!', 'error')
    
    return render_template('admin_giris.html', form=form)

@app.route('/admin')
@login_required
def admin_panel():
    # Filtreleme parametreleri
    durum = request.args.get('durum', '')
    arama = request.args.get('arama', '')
    sayfa = request.args.get('sayfa', 1, type=int)
    
    # Sorgu oluştur
    query = Basvuru.query
    
    if durum:
        query = query.filter(Basvuru.durum == durum)
    
    if arama:
        query = query.filter(
            db.or_(
                Basvuru.ad.contains(arama),
                Basvuru.soyad.contains(arama),
                Basvuru.tc.contains(arama),
                Basvuru.email.contains(arama)
            )
        )
    
    # Tüm başvuruları al (sayfalama olmadan)
    basvurular_list = query.order_by(Basvuru.olusturma_tarihi.desc()).all()
    
    # Template için uygun formata çevir
    basvurular = []
    for basvuru in basvurular_list:
        basvurular.append({
            'id': basvuru.id,
            'ad': basvuru.ad,
            'soyad': basvuru.soyad,
            'tc': basvuru.tc,
            'email': basvuru.email,
            'telefon': basvuru.telefon,
            'durum': basvuru.durum,
            'tarih': basvuru.olusturma_tarihi.strftime("%Y-%m-%d %H:%M:%S"),
            'onay_tarihi': basvuru.onay_tarihi.strftime("%Y-%m-%d %H:%M:%S") if basvuru.onay_tarihi else None,
            'aciklama': basvuru.aciklama
        })
    
    return render_template('admin.html', basvurular=basvurular, durum=durum, arama=arama)

@app.route('/basvuru/<int:basvuru_id>', methods=['GET', 'POST'])
@login_required
def basvuru_detay(basvuru_id):
    basvuru = Basvuru.query.get_or_404(basvuru_id)
    form = BasvuruOnayForm()
    
    if form.validate_on_submit():
        eski_durum = basvuru.durum
        basvuru.durum = form.durum.data
        basvuru.aciklama = form.aciklama.data
        basvuru.onay_tarihi = datetime.utcnow()
        basvuru.onaylayan_admin = current_user.id
        
        db.session.commit()
        
        log_islem(
            'basvuru_durum_degistir',
            f'Başvuru {basvuru_id}: {eski_durum} -> {basvuru.durum}'
        )
        
        flash(f'Başvuru {basvuru.durum}!', 'success')
        return redirect(url_for('admin_panel'))
    
    return render_template('basvuru_detay.html', basvuru=basvuru, form=form)

@app.route('/onayla/<int:basvuru_id>')
@login_required
def hizli_onayla(basvuru_id):
    basvuru = Basvuru.query.get_or_404(basvuru_id)
    basvuru.durum = 'onaylandı'
    basvuru.onay_tarihi = datetime.utcnow()
    basvuru.onaylayan_admin = current_user.id
    
    db.session.commit()
    
    log_islem('basvuru_onayla', f'Başvuru {basvuru_id} onaylandı')
    flash('Başvuru onaylandı!', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/reddet/<int:basvuru_id>')
@login_required
def hizli_reddet(basvuru_id):
    basvuru = Basvuru.query.get_or_404(basvuru_id)
    basvuru.durum = 'reddedildi'
    basvuru.onay_tarihi = datetime.utcnow()
    basvuru.onaylayan_admin = current_user.id
    
    db.session.commit()
    
    log_islem('basvuru_reddet', f'Başvuru {basvuru_id} reddedildi')
    flash('Başvuru reddedildi!', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/istatistik')
@login_required
def istatistik():
    # Toplam istatistikler
    toplam_basvuru = Basvuru.query.count()
    onaylanan = Basvuru.query.filter_by(durum='onaylandı').count()
    reddedilen = Basvuru.query.filter_by(durum='reddedildi').count()
    beklemede = Basvuru.query.filter_by(durum='beklemede').count()
    
    # Bugünkü istatistikler
    bugun = datetime.utcnow().date()
    bugun_basvuru = Basvuru.query.filter(
        db.func.date(Basvuru.olusturma_tarihi) == bugun
    ).count()
    
    # Son 7 günlük istatistikler
    from datetime import timedelta
    son_7_gun = datetime.utcnow() - timedelta(days=7)
    son_7_gun_basvuru = Basvuru.query.filter(
        Basvuru.olusturma_tarihi >= son_7_gun
    ).count()
    
    return jsonify({
        'toplam': toplam_basvuru,
        'onaylanan': onaylanan,
        'reddedilen': reddedilen,
        'beklemede': beklemede,
        'bugun': bugun_basvuru,
        'son_7_gun': son_7_gun_basvuru
    })

@app.route('/cikis')
@login_required
def cikis():
    log_islem('logout', f'Admin çıkışı: {current_user.kullanici_adi}')
    logout_user()
    flash('Başarıyla çıkış yaptınız!', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin_olustur', methods=['GET', 'POST'])
def admin_olustur():
    """İlk admin kullanıcısını oluşturur"""
    if Admin.query.first():
        flash('Admin kullanıcısı zaten mevcut!', 'error')
        return redirect(url_for('admin_login'))
    
    from forms import AdminCreateForm
    form = AdminCreateForm()
    
    if form.validate_on_submit():
        admin = Admin(
            kullanici_adi=form.kullanici_adi.data,
            email=form.email.data,
            ad=form.ad.data,
            soyad=form.soyad.data,
            rol=form.rol.data
        )
        admin.set_password(form.password.data)
        
        db.session.add(admin)
        db.session.commit()
        
        flash('Admin kullanıcısı başarıyla oluşturuldu!', 'success')
        return redirect(url_for('admin_login'))
    
    return render_template('admin_olustur.html', form=form)

@app.route('/logs')
@login_required
def sistem_loglari():
    """Sistem loglarını görüntüler"""
    if current_user.rol != 'super_admin':
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('admin_panel'))
    
    sayfa = request.args.get('sayfa', 1, type=int)
    loglar = SistemLog.query.order_by(SistemLog.tarih.desc()).paginate(
        page=sayfa, per_page=50, error_out=False
    )
    
    return render_template('logs.html', loglar=loglar)

@app.route('/qr')
def qr_page():
    """QR kod sayfası"""
    base_url = request.host_url.rstrip('/')
    form_qr = generate_form_qr_code(f"{base_url}/")
    
    # Wi-Fi bilgilerini veritabanından al
    from models import WiFikonfigurasyon
    wifi_config = WiFikonfigurasyon.query.first()
    
    if wifi_config:
        wifi_qr = generate_wifi_qr_code(wifi_config.ssid, wifi_config.sifre)
    else:
        wifi_qr = None
    
    return render_template('qr.html', form_qr=form_qr, wifi_qr=wifi_qr, wifi_config=wifi_config)

@app.route('/qr/form')
def qr_form():
    """Sadece form QR kodu"""
    base_url = request.host_url.rstrip('/')
    form_qr = generate_form_qr_code(f"{base_url}/")
    return render_template('qr_form.html', form_qr=form_qr)

@app.route('/qr/wifi')
def qr_wifi():
    """Sadece Wi-Fi QR kodu"""
    from models import WiFikonfigurasyon
    wifi_config = WiFikonfigurasyon.query.first()
    
    if wifi_config:
        wifi_qr = generate_wifi_qr_code(wifi_config.ssid, wifi_config.sifre)
        return render_template('qr_wifi.html', wifi_qr=wifi_qr, wifi_config=wifi_config)
    else:
        flash('Wi-Fi konfigürasyonu bulunamadı!', 'error')
        return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

