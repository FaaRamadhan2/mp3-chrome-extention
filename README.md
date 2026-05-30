# MP3 Chrome Extension Downloader

Chrome Extension untuk mengirim URL tab aktif ke local Python server, lalu menjalankan downloader MP3 berbasis `yt-dlp`.

Struktur repo dipisah menjadi 2 bagian:

```txt
mp3-chrome-extention/
├─ ext/   # Chrome Extension files
└─ sc/    # Server + downloader script
```

Flow utama:

```txt
Chrome active tab
→ ext/popup.html button
→ ext/popup.js
→ ext/background.js
→ local server: http://127.0.0.1:8765/download
→ sc/server.py
→ sc/ytdl-a_crx.py <URL>
→ MP3 output
```

## Features

- Download MP3 dari URL tab aktif Chrome.
- UI popup ringan dan modern.
- Direct execute ke script Python downloader.
- Log downloader digabung ke terminal `server.py`.
- Tidak membuka CMD baru saat tombol download diklik.
- Output filename otomatis memakai title video.
- Local-only bridge via `127.0.0.1`.
- Support cookies optional.

## Tech Stack

- Chrome Extension Manifest V3
- JavaScript
- Python
- `yt-dlp`
- FFmpeg

## Project Structure

```txt
mp3-chrome-extention/
├─ ext/
│  ├─ manifest.json
│  ├─ background.js
│  ├─ popup.html
│  ├─ popup.css
│  └─ popup.js
│
├─ sc/
│  ├─ server.py
│  ├─ ytdl-a_crx.py
│  └─ cookies/
│     └─ youtube.com_cookies.txt
│
└─ README.md
```

## Folder Explanation

### `ext/`

Folder ini berisi semua file Chrome Extension.

```txt
ext/
├─ manifest.json
├─ background.js
├─ popup.html
├─ popup.css
└─ popup.js
```

Isi utama:

- `manifest.json` → konfigurasi Chrome Extension Manifest V3.
- `popup.html` → tampilan popup extension.
- `popup.css` → styling popup.
- `popup.js` → mengambil URL tab aktif dan mengirim command download.
- `background.js` → mengirim URL ke local server.

### `sc/`

Folder ini berisi semua file backend/local script.

```txt
sc/
├─ server.py
├─ ytdl-a_crx.py
└─ cookies/
   └─ youtube.com_cookies.txt
```

Isi utama:

- `server.py` → local HTTP server bridge.
- `ytdl-a_crx.py` → downloader utama berbasis `yt-dlp`.
- `cookies/` → optional cookies file.

## Requirements

Pastikan sudah terinstall:

- Python 3.10+
- Google Chrome / Chromium-based browser
- FFmpeg
- `yt-dlp`

Cek Python:

```bash
python --version
```

Cek FFmpeg:

```bash
ffmpeg -version
```

Install / update `yt-dlp`:

```bash
python -m pip install -U yt-dlp
```

Jika FFmpeg belum ada, install dulu dan pastikan command `ffmpeg` bisa dipanggil dari terminal.

## Installation

Clone repository:

```bash
git clone https://github.com/USERNAME/REPOSITORY_NAME.git
cd mp3-chrome-extention
```

Install dependency Python:

```bash
python -m pip install -U yt-dlp
```

## Run Local Server

Masuk ke folder `sc`:

```bash
cd sc
```

Jalankan server:

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
5. Pilih folder:

```txt
mp3-chrome-extention/ext
```

6. Extension siap digunakan.

> Jangan pilih root folder `mp3-chrome-extention`. Yang harus dipilih adalah folder `ext`.

## Usage

1. Jalankan local server dari folder `sc`:

```bash
cd sc
python server.py
```

2. Buka video/audio page di Chrome.
3. Klik icon extension.
4. Klik tombol **Download MP3**.
5. Progress download tampil di terminal `server.py`.
6. File `.mp3` tersimpan di folder `sc`.

Output default:

```txt
sc/<video-title>.mp3
```

## How It Works

### 1. Popup Extension

File:

```txt
ext/popup.html
ext/popup.js
```

`popup.js` mengambil URL tab aktif:

```js
chrome.tabs.query({ active: true, currentWindow: true }, ...)
```

Lalu mengirim message ke background script.

### 2. Background Service Worker

File:

```txt
ext/background.js
```

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

File:

```txt
sc/server.py
```

`server.py` menerima URL, lalu menjalankan:

```bash
python ytdl-a_crx.py "<URL>"
```

Downloader berjalan di terminal yang sama, sehingga tidak membuka CMD baru.

### 4. Downloader

File:

```txt
sc/ytdl-a_crx.py
```

Downloader menggunakan `yt-dlp` untuk:

- membaca metadata title,
- membuat nama file aman,
- download best audio,
- convert audio ke MP3,
- menyimpan output ke folder `sc`.

## Cookies Support

Downloader otomatis memakai cookies jika file ini ada:

```txt
sc/cookies/youtube.com_cookies.txt
```

Struktur:

```txt
mp3-chrome-extention/
└─ sc/
   └─ cookies/
      └─ youtube.com_cookies.txt
```

Jika file cookies tidak ada, downloader tetap jalan tanpa cookies.

## Troubleshooting

### Extension error: Cannot connect to local server

Penyebab:

```txt
sc/server.py belum dijalankan
```

Fix:

```bash
cd sc
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

Cek folder:

```txt
mp3-chrome-extention/sc
```

Output tersimpan di folder yang sama dengan `ytdl-a_crx.py`.

### FFmpeg error

Pastikan FFmpeg sudah masuk PATH.

Cek:

```bash
ffmpeg -version
```

### Chrome tidak bisa load extension

Pastikan file ini ada:

```txt
mp3-chrome-extention/ext/manifest.json
```

Pastikan saat **Load unpacked**, folder yang dipilih adalah:

```txt
mp3-chrome-extention/ext
```

Bukan:

```txt
mp3-chrome-extention
```

### Tombol download tidak bekerja di tab tertentu

Chrome tidak mengizinkan akses normal ke halaman internal seperti:

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

Default local server:

```txt
HOST = 127.0.0.1
PORT = 8765
```

Endpoint:

```txt
POST /download
```

Chrome Extension folder:

```txt
ext/
```

Script/backend folder:

```txt
sc/
```

Main downloader:

```txt
sc/ytdl-a_crx.py
```

Main output:

```txt
sc/%(title)s.%(ext)s
```

Final converted output:

```txt
sc/%(title)s.mp3
```

## Important Notes

Repository name currently uses:

```txt
mp3-chrome-extention
```

Note: the common English spelling is `extension`, but this README follows the current repo/folder name: `extention`.

## License

MIT License

## Disclaimer

Project ini dibuat untuk penggunaan pribadi dan edukasi. Pastikan penggunaan sesuai aturan platform dan hukum yang berlaku.
