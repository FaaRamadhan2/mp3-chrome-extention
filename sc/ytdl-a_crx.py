import os
import sys
import yt_dlp
from urllib.parse import urlparse
from pathlib import Path

# =========================
# PATH SETUP
# =========================
base_dir = Path(__file__).resolve().parent

output_template = str(base_dir / "%(title)s.%(ext)s")

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


urls = collect_urls()

if not urls:
    print("❌ Tidak ada URL.")
    sys.exit(1)

# =========================
# SERVER LOG MODE
# =========================
# Clear screen disabled so logs stay merged in server.py terminal.

print("🎵✨ YouTube MP3 Downloader ✨🎵\n")

# =========================
# SAFE FILENAME
# =========================
def safe_filename(name):

    illegal = r'\/:*?"<>|'

    for ch in illegal:
        name = name.replace(ch, "")

    return name.strip()


# =========================
# FALLBACK TITLE
# =========================
def fallback_title(url):

    try:
        path = urlparse(url).path
        part = path.strip("/").split("/")

        if part and part[-1]:
            return part[-1].replace("-", " ").replace("_", " ")

    except:
        pass

    return "Unknown Title"


# =========================
# TITLE PROBE
# =========================
song_list = []

meta_opts = {
    "quiet": True,
    "ignoreerrors": True,
    "remote_components": ["ejs:github"]
}

if cookies_file.exists():
    meta_opts["cookiefile"] = str(cookies_file)

for url in urls:

    title = fallback_title(url)

    try:

        with yt_dlp.YoutubeDL(meta_opts) as ydl:

            info = ydl.extract_info(url, download=False)

            if info and info.get("title"):
                title = info["title"]

    except:
        pass

    title = safe_filename(title)

    save_path = str(base_dir / (title + ".mp3"))

    print(f"🎧 {title}")
    print(f"   URL  : {url}")
    print(f"   Save : {save_path}\n")

    song_list.append({
        "url": url,
        "title": title
    })

# =========================
# YT-DLP CONFIG
# =========================
ydl_opts = {

    "format": "bestaudio/best",

    "outtmpl": output_template,

    "noplaylist": True,

    "ignoreerrors": True,

    "remote_components": ["ejs:github"],

    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192"
    }],

}

# cookies optional
if cookies_file.exists():
    ydl_opts["cookiefile"] = str(cookies_file)

# =========================
# DOWNLOAD
# =========================
print("⬇ Downloading MP3...\n")

with yt_dlp.YoutubeDL(ydl_opts) as ydl:

    for i, song in enumerate(song_list, 1):

        print(f"▶ [{i}/{len(song_list)}] {song['title']}")

        try:

            ydl.download([song["url"]])

            print("   ✅ Done\n")

        except Exception as e:

            print(f"   ❌ Error: {e}\n")


print("🏁 DONE")
print("📂 Output:", base_dir)