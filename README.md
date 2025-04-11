# Şirket Yönetim Sistemi

Flask ile oluşturulmuş, şirket çalışanlarını, departmanları, izinleri ve projeleri yönetmek için tasarlanmış bir web uygulaması.

## Özellikler

- **Kullanıcı Giriş ve Yetkilendirme**
  - Rol bazlı erişim kontrolü (Admin, Yönetici, Personel)
  - Kullanıcı kaydı ve giriş sistemi
  - Şifre sıfırlama

- **Çalışan Yönetimi**
  - Çalışan ekleme, listeleme, düzenleme ve silme işlemleri
  - TC Kimlik No, iletişim bilgileri ve adres kayıtları
  - Departman ve pozisyon atama

- **Departman ve Pozisyon Yönetimi**
  - Departman ekleme ve düzenleme
  - Pozisyonları departmanlara bağlama

- **İzin Yönetimi**
  - Personel için izin talep formu
  - Yöneticilerin izin onaylama/reddetme paneli
  - Çeşitli izin türleri (Yıllık izin, Hastalık izni, vb.)

- **Proje ve Görev Yönetimi**
  - Proje oluşturma, düzenleme
  - Projelere çalışan atama
  - Görev listesi ve tamamlanma oranları

- **Raporlama ve İstatistik**
  - Toplam çalışan, departman, aktif izin sayıları
  - Tamamlanma oranları ve istatistikler

## Kurulum

### Gereksinimler
- Python 3.8+
- Flask ve ilgili paketler
- Veritabanı (SQLite geliştirme, PostgreSQL/MySQL üretim)

### Adımlar

1. Repo'yu klonlayın:
   ```
   git clone https://github.com/kullanici-adi/sirket-yonetim-sistemi.git
   cd sirket-yonetim-sistemi
   ```

2. Sanal ortam oluşturun ve aktive edin:
   ```
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. Gerekli paketleri yükleyin:
   ```
   pip install -r requirements.txt
   ```

4. Veritabanını oluşturun:
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

5. Admin kullanıcısı oluşturun:
   ```
   flask create-admin
   ```

6. Uygulamayı çalıştırın:
   ```
   flask run
   ```

## Konfigürasyon

Ortam değişkenleri ile yapılandırılabilir:

- `FLASK_APP`: Başlangıç dosyası (run.py)
- `FLASK_ENV`: Geliştirme ortamı (development, production)
- `SECRET_KEY`: Güvenlik anahtarı
- `DATABASE_URL`: Veritabanı bağlantı URL'si

## Geliştirme

Yeni özellikler eklemek veya hataları düzeltmek için:

1. Yeni bir branch oluşturun: `git checkout -b yeni-ozellik`
2. Değişikliklerinizi yapın ve commit edin: `git commit -am 'Yeni özellik eklendi'`
3. Branch'i push edin: `git push origin yeni-ozellik`
4. Pull request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın. 