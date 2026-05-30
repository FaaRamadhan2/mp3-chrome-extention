import os
import sys
import yt_dlp
from urllib.parse import urlparse
from pathlib import Path

# =========================
# PATH SETUP
# =========================
base_dir = Path(__file__).resolve().parent
cookies_file = base_dir / "cookies" / "youtube.com_cookies.txt"


# =========================
# INPUT URL HANDLING
# =========================
def collect_urls():
    # CLI args
    if len(sys.argv) > 1:
        return [arg.strip() for arg in sys.argv[1:] if arg.strip()]

    # stdin
    if not sys.stdin.isatty():
        data = sys.stdin.read().strip()
        if data:
            return [line.strip() for line in data.splitlines() if line.strip()]

    # fallback file
    links_file = base_dir / "links yt.txt"

    if links_file.exists():
        with open(links_file, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    return []


# =========================
# SAFE FILENAME
# =========================
def safe_filename(name):
    illegal = r'\\/:*?"<>|'

    for ch in illegal:
        name = name.replace(ch, "")

    name = name.replace("｜", "")
    name = name.replace("–", "-")
    name = name.replace("—", "-")
    name = " ".join(name.split()).strip()

    if not name:
        return "Unknown Title"

    return name


# =========================
# FALLBACK TITLE
# =========================
def fallback_title(url):
    try:
        path = urlparse(url).path
        part = path.strip("/").split("/")

        if part and part[-1]:
            return part[-1].replace("-", " ").replace("_", " ")

    except Exception:
        pass

    return "Unknown Title"


# =========================
# FILE DETECTION
# =========================
def get_mp3_path(title):
    return base_dir / f"{title}.mp3"


def file_already_exists(title):
    mp3_path = get_mp3_path(title)
    return mp3_path.exists() and mp3_path.is_file() and mp3_path.stat().st_size > 0


# =========================
# URL COLLECTION
# =========================
urls = collect_urls()

if not urls:
    print("❌ Tidak ada URL.")
    sys.exit(1)

print("🎵✨ YouTube MP3 Downloader ✨🎵\n")


# =========================
# META CONFIG
# =========================
meta_opts = {
    "quiet": True,
    "ignoreerrors": True,
    "remote_components": ["ejs:github"],
}

if cookies_file.exists():
    meta_opts["cookiefile"] = str(cookies_file)


# =========================
# TITLE PROBE + QUEUE
# =========================
song_list = []

for url in urls:
    title = fallback_title(url)

    try:
        with yt_dlp.YoutubeDL(meta_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            if info and info.get("title"):
                title = info["title"]

    except Exception:
        pass

    title = safe_filename(title)
    save_path = get_mp3_path(title)

    print(f"🎧 {title}")
    print(f"   URL  : {url}")
    print(f"   Save : {save_path}")

    if file_already_exists(title):
        print("   ⏭ SKIP: file already exists\n")
        continue

    print("   ✅ QUEUED\n")

    song_list.append({
        "url": url,
        "title": title,
    })


# =========================
# EMPTY QUEUE GUARD
# =========================
if not song_list:
    print("✅ Semua file sudah ada. Tidak ada yang perlu didownload.")
    print("📂 Output:", base_dir)
    sys.exit(0)


# =========================
# BASE YT-DLP CONFIG
# =========================
base_ydl_opts = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "ignoreerrors": True,
    "remote_components": ["ejs:github"],
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
}

if cookies_file.exists():
    base_ydl_opts["cookiefile"] = str(cookies_file)


# =========================
# DOWNLOAD
# =========================
print("⬇ Downloading MP3...\n")

for i, song in enumerate(song_list, 1):
    title = song["title"]
    url = song["url"]

    print(f"▶ [{i}/{len(song_list)}] {title}")

    if file_already_exists(title):
        print("   ⏭ SKIP: file already exists before download\n")
        continue

    output_template = str(base_dir / f"{title}.%(ext)s")

    ydl_opts = dict(base_ydl_opts)
    ydl_opts["outtmpl"] = output_template

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if file_already_exists(title):
            print("   ✅ Done\n")
        else:
            print("   ⚠ Download finished, but MP3 file was not detected")
            print(f"   Expected: {get_mp3_path(title)}\n")

    except Exception as e:
        print(f"   ❌ Error: {e}\n")


print("🏁 DONE")
print("📂 Output:", base_dir)
