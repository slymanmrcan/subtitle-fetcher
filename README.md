# YouTube Subtitle Downloader

YouTube videolarından alt yazıları çeken, temizleyen ve okunabilir formatta sunan Flask tabanlı web uygulaması.

## ✨ Özellikler

- 🎬 YouTube URL'si üzerinden otomatik alt yazı çekme
- 🧹 Zaman damgalarını ve gereksiz satırları temizleme
- 📝 Otomatik paragraf formatı
- 💾 Temizlenmiş alt yazıyı `.txt` olarak indirme
- 🎨 Modern ve responsive UI (Tailwind CSS)
- 🐳 Docker desteği

## 📋 Gereksinimler

- Python 3.11 veya üzeri
- pip (Python paket yöneticisi)
- Docker ve Docker Compose (opsiyonel)

## 🚀 Kurulum ve Çalıştırma

### Yöntem 1: Otomatik Kurulum (Önerilen)
```bash
bash setup_and_run.sh
```

Uygulama otomatik olarak başlatılacak ve `http://127.0.0.1:5001` adresinde çalışacaktır.

### Yöntem 2: Docker ile Çalıştırma
```bash
# Docker Compose ile (önerilen)
docker-compose up --build

# Veya sadece Docker kullanarak
docker build -t subtitle-app .
docker run -p 5001:5001 subtitle-app
```

Tarayıcınızdan `http://localhost:5001` adresine gidin.

### Yöntem 3: Manuel Kurulum
```bash
# Sanal ortam oluştur
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Uygulamayı çalıştır
python app.py
```

Tarayıcınızdan `http://127.0.0.1:5001` adresine gidin.

## 📁 Proje Yapısı

```
subtitle-check/
├── app.py                 # Ana Flask uygulaması
├── requirements.txt       # Python bağımlılıkları
├── Dockerfile            # Docker image tanımı
├── docker-compose.yml    # Docker Compose yapılandırması
├── .dockerignore         # Docker ignore kuralları
├── .gitignore           # Git ignore kuralları
├── setup_and_run.sh     # Otomatik kurulum scripti
├── templates/           # HTML şablonları
│   └── index.html
├── static/              # Statik dosyalar (CSS, JS)
└── temp_subs/          # Geçici alt yazı dosyaları (git'e dahil değil)
```

## 🔧 Teknik Detaylar

- **Backend:** Flask (Python)
- **Alt Yazı Motoru:** yt-dlp (Python API)
- **Frontend:** HTML5, Tailwind CSS
- **Container:** Docker & Docker Compose
- **Port:** 5001

## 🐛 Sorun Giderme

### Port zaten kullanımda hatası
Eğer 5001 portu kullanımdaysa, `docker-compose.yml` veya `app.py` dosyasındaki port numarasını değiştirebilirsiniz.

### Alt yazı bulunamadı hatası
- Videonun alt yazısı olduğundan emin olun
- YouTube URL'sinin doğru olduğunu kontrol edin
- Videonun erişilebilir olduğunu doğrulayın

### Docker ile ilgili sorunlar
```bash
# Container'ları temizle
docker-compose down

# Yeniden başlat
docker-compose up --build
```

## 📝 Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.
