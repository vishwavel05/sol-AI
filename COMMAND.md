# சொல் AI — Command Reference & Operating Manual

This document summarizes all standard execution, testing, build, and development commands for the சொல் AI project.

---

## 1. Backend Server & API

Start the சொல் AI REST API server:

```bash
# From workspace root:
python backend/api/server.py --port 8000
```

Verify backend health:

```bash
curl http://localhost:8000/api/health
```

Query API with mock or Gemini LLM provider:

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query":"மரங்களில்","provider":"mock"}'
```

---

## 2. Backend Unit & Integration Tests

Run the full Python test suite (55 tests across retrieval, FST parsing, evidence aggregation, context selection, and LLM interpretation):

```bash
pytest tests/ -v
```

Run specific test modules:

```bash
pytest tests/test_retrieval_engine.py -v
pytest tests/test_api_server.py -v
```

---

## 3. Frontend Web Application (Next.js)

Navigate to frontend directory:

```bash
cd frontend
```

Install dependencies (if needed):

```bash
npm install
```

Run local development server (runs on http://localhost:3000):

```bash
npm run dev
```

Build production bundle:

```bash
npm run build
```

Start production server:

```bash
npm start
```

---

## 4. Chrome Extension

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable **Developer mode** (top-right toggle).
3. Click **Load unpacked** and select the `SOL_AI/extension` directory.
4. Highlight any Tamil word on any webpage to trigger the extension popup.

---

## 5. Benchmarking & Auditing Scripts

Run the 60-case deterministic benchmark:

```bash
python scripts/run_unified_benchmark.py
```

Run resource profiling:

```bash
python scripts/profile_resource.py
```
