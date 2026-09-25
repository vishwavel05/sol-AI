# சொல் AI — Browser Extension (Manifest V3)

The **சொல் AI Browser Extension** allows users to encounter Tamil text on any webpage, select any Tamil word or phrase, and receive contextual etymological, morphological, dictionary, and Sangam literary evidence analysis directly inside a floating side panel.

---

## 🌟 Key Features

1. **Right-Click Context Menu**: Select any Tamil text on any webpage, right-click, and choose **"Explain with சொல் AI"**.
2. **Floating Scoped Side Panel**: Displays structured analysis directly on the page inside a Shadow DOM container without altering or breaking host page layout/styles.
3. **Manual Popup Lookup**: Click the extension icon in your browser toolbar to type or paste any Tamil word/phrase manually.
4. **Evidence Transparency**: Displays primary resource provenance (`ThamizhiMorph`, `Tamil WordNet`, `Thani Thamizh Akarathi`, `Sentamizh`, `Tamil Wiktionary`).
5. **Morphology & Literary Context**: Distinguishes **Core FST** vs **Guesser** analyses and renders selected classical Sangam verses with modern Tamil glosses.
6. **Configurable API Endpoint**: Easily set custom backend URLs (`http://localhost:8000`).

---

## 🛡️ Security Architecture

> [!IMPORTANT]
> **Zero Gemini Key Exposure**: The browser extension **NEVER** stores, communicates with, or receives the Gemini API key.  
> All LLM credentials and resource databases remain strictly server-side on the சொல் AI Python backend (`backend/api/server.py`). The extension communicates solely with the சொல் AI API server.

```
Host Webpage (Content Script)
    ↕ Chrome Extension Messaging
Background Service Worker (service-worker.js)
    ↕ HTTP POST /api/query
சொல் AI API Server (localhost:8000)
    ↕ Server-side LLM & Resource Adapters
Google Gemini / Mock Interpreter
```

---

## 🚀 Installation & Setup

### Step 1: Start சொல் AI API Server
Ensure the சொல் AI Python backend is running locally:
```bash
python backend/api/server.py --port 8000
```
Verify health:
```bash
curl http://localhost:8000/api/health
# Response: {"status": "ok"}
```

### Step 2: Load Extension in Chrome / Edge
1. Open Chrome or Edge and navigate to `chrome://extensions` (or `edge://extensions`).
2. Enable **Developer mode** toggle in the top-right corner.
3. Click **Load unpacked**.
4. Select the directory: `SOL_AI/extension`.

---

## 🧪 Testing the Extension

1. Open `extension/test-page.html` directly in your browser.
2. Highlight a Tamil word or phrase (e.g. **மரங்களில்**, **யாழ்**, **அகதி**, **வந்தார்கள்**).
3. Right-click and choose **"Explain with சொல் AI"**.
4. A floating side panel will appear on the page showing:
   - Root Lemma & Lexical Meaning
   - Morphological POS & Model (`noun.fst` [CORE])
   - Selected Classical Literary Contexts (*Kuruntokai*, *Manimekalai*, *Natrinai*)
   - Source Provenance & Uncertainty notes

---

## ⚙️ Configuration & Settings

To change the backend API server URL:
1. Click the **சொல் AI** extension icon in your toolbar.
2. Click the **Settings Gear (⚙)** in the popup header.
3. Enter your API URL (e.g. `http://localhost:8000` or custom server URL).
4. Click **Save**.

---

## 🔒 Permissions Surface

The extension uses the minimal required Manifest V3 permission surface:
- `contextMenus`: Creates "Explain with சொல் AI" right-click menu item.
- `storage`: Persists `SOL_API_BASE_URL` locally via `chrome.storage.local`.
- `activeTab`: Accesses active tab DOM for context menu target extraction.
- `host_permissions`: Accesses localhost API endpoints (`http://localhost:8000/*`).

---

## 🛠️ Troubleshooting

- **Panel shows "சொல் AI could not be reached"**: Ensure `python backend/api/server.py --port 8000` is running locally and `http://localhost:8000/api/health` returns status `ok`.
- **Extension fails to reload changes**: Go to `chrome://extensions` and click the reload icon on the சொல் AI extension card.
