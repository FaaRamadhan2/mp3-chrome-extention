from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json
import subprocess
import sys

HOST = "127.0.0.1"
PORT = 8765
BASE_DIR = Path(__file__).resolve().parent
YTDLP_SCRIPT = BASE_DIR / "ytdl-a_crx.py"
PYTHON_EXE = sys.executable


def build_response(handler: BaseHTTPRequestHandler, status: int, body: str) -> None:
    data = body.encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "text/plain; charset=utf-8")
    handler.send_header("Content-Length", str(len(data)))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.end_headers()
    handler.wfile.write(data)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print("[server]", fmt % args, flush=True)

    def do_OPTIONS(self):
        build_response(self, 204, "")

    def do_POST(self):
        if self.path != "/download":
            build_response(self, 404, "Endpoint not found.")
            return

        if not YTDLP_SCRIPT.exists():
            build_response(self, 500, f"Downloader script not found: {YTDLP_SCRIPT}")
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(length).decode("utf-8")
            payload = json.loads(raw_body or "{}")
            url = str(payload.get("url", "")).strip()

            if not url:
                build_response(self, 400, "URL missing.")
                return

            if not (url.startswith("http://") or url.startswith("https://")):
                build_response(self, 400, "Only http/https URL is allowed.")
                return

            print("\n" + "=" * 70, flush=True)
            print(f"[download-request] {url}", flush=True)
            print("[exec] Running downloader in THIS server terminal...", flush=True)
            print("=" * 70, flush=True)

            # IMPORTANT:
            # No CREATE_NEW_CONSOLE here.
            # stdout/stderr/stdin inherit from server.py, so yt-dlp logs appear
            # in the same CMD/PowerShell window that runs this server.
            subprocess.Popen(
                [PYTHON_EXE, str(YTDLP_SCRIPT), url],
                cwd=str(BASE_DIR),
                stdin=None,
                stdout=None,
                stderr=None,
                shell=False,
                close_fds=False if sys.platform.startswith("win") else True,
            )

            build_response(self, 200, "Downloader executed in server terminal.")

        except Exception as exc:
            build_response(self, 500, str(exc))


def run():
    print(f"🚀 Direct MP3 Downloader Server running: http://{HOST}:{PORT}", flush=True)
    print(f"📄 Downloader script: {YTDLP_SCRIPT}", flush=True)
    print("📌 Logs downloader akan muncul di terminal ini, bukan CMD baru.", flush=True)
    print("Press CTRL+C to stop.\n", flush=True)
    HTTPServer((HOST, PORT), Handler).serve_forever()


if __name__ == "__main__":
    run()
