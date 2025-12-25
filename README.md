# YouTube Subtitle Downloader

Bu uygulama, YouTube videolarındaki alt yazıları çekmek, temizlemek ve okunabilir bir formatta sunmak için tasarlanmıştır.

## Özellikler

- YouTube URL'si üzerinden alt yazı çekme.
- Zaman damgalarını ve gereksiz satırları temizleme.
- Otomatik paragraf formatı.
- Temizlenmiş alt yazıyı `.txt` olarak indirme.
- Modern UI (Tailwind CSS).

## Kurulum ve Çalıştırma

### Yöntem 1: Otomatik Kurulum (Önerilen)
```bash
bash setup_and_run.sh
```

### Yöntem 2: Docker ile Çalıştırma
```bash
# Docker image oluştur ve çalıştır
docker-compose up --build

# Veya sadece Docker kullanarak
docker build -t subtitle-app .
docker run -p 5000:5000 subtitle-app
```

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

Tarayıcınızdan `http://127.0.0.1:5000` adresine gidin.

## Teknik Detaylar

- **Backend:** Flask
- **Alt Yazı Motoru:** yt-dlp (Python API)
- **Styling:** Tailwind CSS
