# SOL AI — Gemini API Setup & Activation Guide

This guide explains how to configure and activate the **Google Gemini LLM Interpreter** (`GeminiLLMInterpreter`) in SOL AI for live contextual interpretations.

---

## 1. Obtain a Gemini API Key

1. Go to **Google AI Studio**: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account.
3. Click **Create API Key** and copy your API key string.

---

## 2. Environment Configuration

1. In the project root (`SOL_AI/`), copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and configure the following variables:
   ```env
   # Set provider to gemini for production live API calls
   SOL_LLM_PROVIDER=gemini

   # Configure Gemini model (default: gemini-2.5-flash)
   SOL_GEMINI_MODEL=gemini-2.5-flash

   # Paste your actual Google AI Studio API key below
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```

> [!CAUTION]
> **Security Warning**: Never commit `.env` or your `GEMINI_API_KEY` to Git!  
> `.env` is listed in `.gitignore`.

---

## 3. Running CLI Demo with Gemini

You can test Gemini interpretations directly from the CLI:

```bash
# Explicitly pass --provider gemini
python scripts/interpret_query.py "மரங்களில்" --provider gemini

# Or run with debug mode to inspect the EvidencePack sent to Gemini
python scripts/interpret_query.py "மரங்களில்" --provider gemini --debug
```

---

## 4. Running the REST API Server with Gemini

Start the REST API server with `.env` loaded or environment variables exported:

```bash
# Powershell
$env:SOL_LLM_PROVIDER="gemini"
$env:GEMINI_API_KEY="your_api_key_here"
python backend/api/server.py --port 8000
```

Send a test request via cURL:
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "மரங்களில்"}'
```

---

## 5. How to Switch Back to Offline Mock Mode

To switch back to offline, deterministic mock execution without needing an API key:

```env
SOL_LLM_PROVIDER=mock
```
Or via CLI:
```bash
python scripts/interpret_query.py "மரங்களில்" --provider mock
```
---
