# MP3 Direct Execute Chrome Extension

Chrome Extension sederhana untuk mengirim URL tab aktif ke local Python server, lalu langsung menjalankan downloader MP3 berbasis `yt-dlp`.

Flow utama:

```txt
Chrome active tab
→ popup button
→ background service worker
→ local server: http://127.0.0.1:8765/download
→ ytdl-a_crx.py <URL>
→ MP3 output
```

## Features

- Download MP3 dari URL tab aktif.
- UI popup modern dan ringan.
- Direct execute ke script Python downloader.
- Log downloader digabung ke terminal `server.py`.
- Tidak membuka CMD baru saat tombol download diklik.
- Output filename otomatis memakai title video.
- Local-only bridge via `127.0.0.1`.
- Support cookies optional melalui folder `cookies/`.

## Tech Stack

- Chrome Extension Manifest V3
- JavaScript
- Python
- `yt-dlp`
- FFmpeg

## Project Structure

```txt
mp3-direct-exec-extension/
├─ manifest.json
├─ background.js
├─ popup.html
├─ popup.css
├─ popup.js
├─ server.py
├─ ytdl-a_crx.py
├─ requirements.txt
├─ run_server.bat
└─ README.md
```

## Requirements

Pastikan sudah terinstall:

- Python 3.10+
- Google Chrome / Chromium-based browser
- FFmpeg
- yt-dlp dependency dari `requirements.txt`

Cek Python:

```bash
python --version
```

Cek FFmpeg:

```bash
ffmpeg -version
```

Jika FFmpeg belum ada, install dulu dan pastikan `ffmpeg` bisa dipanggil dari terminal.

## Installation

Clone repository:

```bash
git clone https://github.com/USERNAME/REPOSITORY_NAME.git
cd REPOSITORY_NAME
```

Install dependency:

```bash
python -m pip install -r requirements.txt
```

## Run Local Server

Windows:

```bat
run_server.bat
```

Atau manual:

```bash
python server.py
```

Jika berhasil, terminal akan menampilkan server berjalan di:

```txt
http://127.0.0.1:8765
```

## Load Extension to Chrome

1. Buka Chrome.
2. Masuk ke:

```txt
chrome://extensions
```

3. Aktifkan **Developer mode**.
4. Klik **Load unpacked**.
5. Pilih folder project ini.
6. Extension siap digunakan.

## Usage

1. Jalankan `server.py`.
2. Buka video/audio page di Chrome.
3. Klik icon extension.
4. Klik tombol **Download MP3**.
5. Progress download akan tampil di terminal `server.py`.
6. File `.mp3` akan tersimpan di folder project.

Output default:

```txt
<video-title>.mp3
```

## How It Works

### 1. Popup

`popup.html` menampilkan UI tombol download.

`popup.js` mengambil URL tab aktif:

```js
chrome.tabs.query({ active: true, currentWindow: true }, ...)
```

Lalu mengirim message ke background script.

### 2. Background Service Worker

`background.js` menerima message dari popup, lalu mengirim request ke local server:

```txt
POST http://127.0.0.1:8765/download
```

Body request:

```json
{
  "url": "https://example.com/video"
}
```

### 3. Local Python Server

`server.py` menerima URL, lalu menjalankan:

```bash
python ytdl-a_crx.py "<URL>"
```

Downloader berjalan di terminal yang sama, sehingga tidak membuka CMD baru.

### 4. Downloader

`ytdl-a_crx.py` menggunakan `yt-dlp` untuk:

- membaca metadata title,
- membuat nama file aman,
- download best audio,
- convert audio ke MP3,
- menyimpan output ke folder project.

## Cookies Support

Downloader akan otomatis memakai cookies jika file ini ada:

```txt
cookies/youtube.com_cookies.txt
```

Struktur folder:

```txt
mp3-direct-exec-extension/
├─ cookies/
│  └─ youtube.com_cookies.txt
```

Jika file cookies tidak ada, downloader tetap jalan tanpa cookies.

## Troubleshooting

### Extension error: Cannot connect to local server

Penyebab:

```txt
server.py belum dijalankan
```

Fix:

```bash
python server.py
```

### Download tidak mulai

Cek terminal `server.py`.

Kemungkinan penyebab:

- URL tidak valid.
- Website membutuhkan cookies.
- FFmpeg belum terinstall.
- `yt-dlp` outdated.
- Koneksi internet bermasalah.

Update `yt-dlp`:

```bash
python -m pip install -U yt-dlp
```

### MP3 tidak muncul

Cek folder project. Output tersimpan di folder yang sama dengan `ytdl-a_crx.py`.

### FFmpeg error

Pastikan FFmpeg sudah masuk PATH.

Cek:

```bash
ffmpeg -version
```

### Chrome tidak bisa load extension

Pastikan file ini ada:

```txt
manifest.json
```

Pastikan load folder project, bukan file ZIP.

### Tombol download tidak bekerja di tab tertentu

Chrome tidak mengizinkan akses normal ke beberapa halaman internal seperti:

```txt
chrome://extensions
chrome://settings
chrome://newtab
```

Gunakan pada tab website biasa dengan URL `http` atau `https`.

## Security Notes

Extension ini hanya mengirim URL tab aktif ke local server:

```txt
127.0.0.1:8765
```

Tidak ada upload data ke server eksternal dari extension.

Namun downloader menggunakan `yt-dlp`, sehingga koneksi download tetap mengikuti URL target yang diproses oleh `yt-dlp`.

## Development Notes

Default server:

```txt
HOST = 127.0.0.1
PORT = 8765
```

Endpoint:

```txt
POST /download
```

Main downloader:

```txt
ytdl-a_crx.py
```

Main output:

```txt
%(title)s.%(ext)s
```

Final converted output:

```txt
%(title)s.mp3
```

## License

MIT License

## Disclaimer

Project ini dibuat untuk penggunaan pribadi dan edukasi. Pastikan penggunaan sesuai aturan platform dan hukum yang berlaku.
