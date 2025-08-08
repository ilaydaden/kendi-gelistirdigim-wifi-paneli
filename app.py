from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'cok-gizli-bir-anahtar'  # Oturum yönetimi için

BASVURU_DOSYASI = 'basvurular.json'

def basvurulari_yukle():
    if not os.path.exists(BASVURU_DOSYASI):
        return []
    with open(BASVURU_DOSYASI, 'r') as f:
        return json.load(f)

def basvurulari_kaydet(basvurular):
    with open(BASVURU_DOSYASI, 'w') as f:
        json.dump(basvurular, f)

@app.route('/')
def form():
    return render_template('panel.html')

@app.route('/bildir', methods=['POST'])
def bildir():
    ad = request.form.get('ad')
    soyad = request.form.get('soyad')
    tc = request.form.get('tc')
    tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    yeni_basvuru = {
        'ad': ad,
        'soyad': soyad,
        'tc': tc,
        'tarih': tarih,
        'durum': 'beklemede'
    }

    basvurular = basvurulari_yukle()
    basvurular.append(yeni_basvuru)
    basvurulari_kaydet(basvurular)

    return redirect(url_for('form'))

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        sifre = request.form.get('sifre')
        if sifre == 'admin123':  # Şifreni buraya yaz
            session['admin_giris'] = True
            return redirect(url_for('admin_panel'))
        else:
            return render_template('admin_giris.html', hata="Şifre yanlış!")
    return render_template('admin_giris.html')

@app.route('/admin')
def admin_panel():
    if not session.get('admin_giris'):
        return redirect(url_for('admin_login'))
    basvurular = basvurulari_yukle()
    return render_template('admin.html', basvurular=basvurular)

@app.route('/onayla/<int:index>')
def onayla(index):
    if not session.get('admin_giris'):
        return redirect(url_for('admin_login'))
    basvurular = basvurulari_yukle()
    if 0 <= index < len(basvurular):
        basvurular[index]['durum'] = 'onaylandı'
        basvurulari_kaydet(basvurular)
    return redirect(url_for('admin_panel'))

@app.route('/reddet/<int:index>')
def reddet(index):
    if not session.get('admin_giris'):
        return redirect(url_for('admin_login'))
    basvurular = basvurulari_yukle()
    if 0 <= index < len(basvurular):
        basvurular[index]['durum'] = 'reddedildi'
        basvurulari_kaydet(basvurular)
    return redirect(url_for('admin_panel'))

@app.route('/istatistik')
def istatistik():
    basvurular = basvurulari_yukle()
    onaylanan = sum(1 for b in basvurular if b['durum'] == 'onaylandı')
    reddedilen = sum(1 for b in basvurular if b['durum'] == 'reddedildi')
    beklemede = sum(1 for b in basvurular if b['durum'] == 'beklemede')
    return jsonify({'onaylanan': onaylanan, 'reddedilen': reddedilen, 'beklemede': beklemede})

@app.route('/cikis')
def cikis():
    session.pop('admin_giris', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)
0

