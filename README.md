# சொல் AI — Scholarly Tamil Literary Knowledge & Etymological Intelligence System

> **A living interface to Tamil lexical knowledge and classical literary usage.**

சொல் AI is an open-access, evidence-grounded Tamil etymological, morphological, and literary research system. It integrates four foundational Tamil linguistic resources with a zero-hallucination artificial intelligence interpretation layer.

---

## 🌟 Approved 10 Frontend Screens

1. **Home / Landing (`/`)**: Tamil-first search header, product philosophy, sample query chips (`மரங்களில்`, `யாழ்`, `அகதி`).
2. **Word Explorer (`/search?q=மரங்களில்`)**: Surface form, core root lemma isolation (`மரம்`), morphology decomposition, lexical definitions, contextual interpretation, literary verses, and hit audit.
3. **Literary Context / Reading View (`/read`)**: Sangam verse reader in Noto Serif Tamil typography with query word highlighting, modern glosses, and verse metadata.
4. **Multiple Meanings — அகதி (`/search?q=அகதி`)**: Preserves separate entry definitions from purist lexicons without collapsing distinct senses.
5. **Evidence & Sources (`/sources`)**: Provenance drawer and detailed audit for ThamizhiMorph, Tamil WordNet, Thani Thamizh Akarathi, and Sentamizh Corpus.
6. **Unknown Word (`/search?q=போலிசொல்வார்த்தை123`)**: Responsible failure state ("சொல் AI could not find sufficient evidence") with base-form suggestions.
7. **Chrome Extension — Default Idle (`/extension-demo`)**: Compact search bar and text-selection listener in Chrome browser popup.
8. **Chrome Extension — Result Popup (`/extension-demo`)**: Selected word, root lemma, core morphology, dictionary definition, and Sangam verse snippet.
9. **Chrome Extension — Error/Edge States (`/extension-demo`)**: User-friendly offline, timeout, and unknown word notifications without raw stack traces.
10. **About / Resources (`/about`)**: Product architecture, evidence-first principles, AI as interpretation layer, and licensing acknowledgments.

---

## 🎨 Visual & Design Tokens

- **Deep Navy**: `#0B132B`
- **Muted Teal**: `#147D7A`
- **Antique Gold**: `#C9A227`
- **Warm Ivory**: `#F7F3EA`
- **Near Black**: `#161616`
- **Muted Gray**: `#6B7280`
- **Typography**: Noto Sans Tamil (UI), Noto Serif Tamil (Literary Passages), Inter (Latin/System).

---

## 🚀 Quick Start Guide

### 1. Download & Build the Lexical Databases
The raw Tamil datasets are extremely large and are excluded from this repository via `.gitignore` to comply with GitHub's storage limits.
Before starting the server for the first time, you must download the raw datasets into `data/raw/` and build the indexes.

Run the following commands in your terminal to fetch the open-source repositories:
```bash
# 1. Download ThamizhiMorph (Morphological Engine)
git clone https://github.com/sarves/thamizhi-morph data/raw/thamizhimorph

# 2. Download Thani Thamizh Akarathi (Dictionary)
git clone https://github.com/Kaviyarasan-N/Thani_Thamizh_Akarathi data/raw/thani_thamizh_akarathi

# 3. Download Sentamizh (Literary Corpus)
git clone https://github.com/e-thamil/sentamizh-corpus data/raw/sentamizh
```
*(Note: For WordNet and Wiktionary XML dumps, refer to `research/RESOURCE_AUDIT.md` for manual download links).*

Once downloaded, build the indexes by running the compilation scripts:
```bash
python scripts/build_akarathi_index.py
python scripts/build_sentamizh_index.py
python scripts/build_wiktionary_index.py
python scripts/build_wordnet_index.py
```

### 2. Configure Your LLM API Key
The AI interpretation layer requires an API key to function. By default, it uses the Google Gemini API.

1. Create a `.env` file in the root directory (you can copy `.env.example` if it exists).
2. Add your API key:
```env
# Primary LLM (Google Gemini)
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: If you prefer Groq as a fallback or primary
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Start the Backend API (Python)
```bash
python backend/api/server.py --port 8000
```

### 2. Start the Frontend Application (Next.js)
```bash
cd frontend
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🧪 Testing

Run Python backend tests:
```bash
pytest tests/ -v
```

Build Next.js production bundle:
```bash
cd frontend
npm run build
```

---

## 🏛️ Foundational Tamil Resources

1. **ThamizhiMorph**: Finite-State Transducer (FST) morphological parser for Tamil (`noun.fst` & `verb.fst`).
2. **Tamil WordNet**: Lexical-semantic network containing 50,497 synset nodes and 434,849 morphtable mappings.
3. **Thani Thamizh Akarathi**: Purist Tamil dictionary containing 11,540+ lexical entries.
4. **Sentamizh Corpus**: Sangam literary corpus containing 10,393 verse records across classical Tamil works.
5. **Tamil Wiktionary**: Open-source collaborative dictionary for modern and historical definitions.
