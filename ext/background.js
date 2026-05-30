const SERVER_URL = "http://127.0.0.1:8765/download";

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (!msg || msg.action !== "DL") return false;

  const url = typeof msg.url === "string" ? msg.url.trim() : "";

  if (!url) {
    sendResponse({ ok: false, error: "URL kosong." });
    return false;
  }

  fetch(SERVER_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url })
  })
    .then(async (res) => {
      const text = await res.text();
      if (!res.ok) {
        throw new Error(text || `HTTP ${res.status}`);
      }
      sendResponse({ ok: true, message: text || "Downloader executed." });
    })
    .catch((err) => {
      sendResponse({
        ok: false,
        error: err && err.message ? err.message : "Gagal connect ke local server."
      });
    });

  return true;
});
