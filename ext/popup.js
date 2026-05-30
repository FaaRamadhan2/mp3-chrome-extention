const els = {
  btn: document.getElementById("downloadBtn"),
  status: document.getElementById("status"),
  urlBox: document.getElementById("urlBox"),
  tabStatus: document.getElementById("tabStatus")
};

let activeUrl = "";
let activeTitle = "";

function setStatus(message, type = "") {
  els.status.textContent = message;
  els.status.className = `status ${type}`.trim();
}

function setTabStatus(message, type = "") {
  els.tabStatus.textContent = message;
  els.tabStatus.className = `pill ${type}`.trim();
}

function isValidDownloadUrl(url) {
  return /^https?:\/\//i.test(url || "");
}

async function loadActiveTab() {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    activeUrl = tab?.url || "";
    activeTitle = tab?.title || "Untitled tab";

    if (!isValidDownloadUrl(activeUrl)) {
      els.urlBox.textContent = activeUrl || "No active tab URL detected.";
      setTabStatus("unsupported", "bad");
      setStatus("Buka tab video/halaman http atau https dulu.", "warn");
      els.btn.disabled = true;
      return;
    }

    els.urlBox.textContent = activeUrl;
    setTabStatus(activeTitle, "ok");
    setStatus("Ready. Klik tombol untuk execute downloader.", "");
    els.btn.disabled = false;
  } catch (err) {
    els.urlBox.textContent = "Failed to read active tab.";
    setTabStatus("error", "bad");
    setStatus(err?.message || "Gagal membaca tab aktif.", "bad");
    els.btn.disabled = true;
  }
}

els.btn.addEventListener("click", () => {
  if (!isValidDownloadUrl(activeUrl)) {
    setStatus("URL tab aktif tidak valid.", "bad");
    return;
  }

  els.btn.disabled = true;
  setStatus("Executing downloader...", "warn");

  chrome.runtime.sendMessage({ action: "DL", url: activeUrl }, (response) => {
    const runtimeError = chrome.runtime.lastError;

    if (runtimeError) {
      setStatus(runtimeError.message || "Runtime error.", "bad");
      els.btn.disabled = false;
      return;
    }

    if (!response || !response.ok) {
      setStatus(response?.error || "Server tidak merespons. Jalankan server.py dulu.", "bad");
      els.btn.disabled = false;
      return;
    }

    setStatus("Downloader executed. Cek terminal/server output.", "ok");
    els.btn.disabled = false;
  });
});

loadActiveTab();
