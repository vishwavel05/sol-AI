# SOL AI — ThamizhiMorph Implementation Task

## PROJECT CONTEXT

SOL AI is a Tamil lexical + literary intelligence system.

The Phase 0 resource audit is COMPLETE and FROZEN.

Do NOT go hunting for additional datasets or resources unless the implementation encounters a concrete technical gap that cannot be solved with the five selected resources.

The five primary resources are:

1. Thani Thamizh Akarathi
   Role: lexical meanings, Tamil equivalents, related lexical forms

2. Tamil WordNet
   Role: lexical-semantic information and supporting morphology

3. ThamizhiMorph
   Role: morphological analysis

4. Sentamizh Corpus
   Role: structured Classical Tamil literary context and annotations

5. Project Madurai
   Role: broad literary text corpus

Relevant research files already exist:

```text
research/RESOURCE_AUDIT.md
research/BENCHMARK.md
```

READ BOTH FILES BEFORE IMPLEMENTING ANYTHING.

Do not assume their contents. Use the actual files as the source of truth.

---

## CURRENT IMPLEMENTATION GOAL

We are now moving from Phase 0 research into implementation.

For this task, build ONLY the foundational resource/evidence architecture and implement the first real resource adapter:

THAMIZHIMORPH.

Do NOT build the frontend.
Do NOT build the LLM/RAG layer.
Do NOT build the browser extension.
Do NOT integrate Gemini/OpenAI/etc.
Do NOT build authentication.
Do NOT redesign the project.
Do NOT search for additional datasets.

The goal is to prove that SOL AI can take a Tamil word, run morphological analysis through ThamizhiMorph/Foma, normalize the result into our internal evidence format, and evaluate the result against our benchmark.

---

## STEP 1 — INSPECT THE REPOSITORY

Before changing anything:

1. Inspect the complete current repository structure.
2. Read:
   - research/RESOURCE_AUDIT.md
   - research/BENCHMARK.md
   - data/raw/thamizhimorph/
3. Inspect the actual ThamizhiMorph repository structure and README.
4. Determine how Foma is currently expected to be invoked.
5. Determine which FST models are available.
6. Do not overwrite or modify anything under data/raw/.

If something already exists that performs part of the requested architecture, REUSE it rather than creating a duplicate.

---

## STEP 2 — CREATE THE BACKEND FOUNDATION

Create a minimal Python backend architecture under:

`backend/`

Suggested structure:

```text
backend/
├── __init__.py
├── schemas/
│   ├── __init__.py
│   └── evidence.py
└── resources/
    ├── __init__.py
    ├── base.py
    └── thamizhimorph.py
```

You may adjust the exact structure if the existing repository suggests a better organization, but keep the architecture simple.

Create a shared Evidence model.

Use a Python dataclass or an equivalent lightweight structure.

It should support at least:

- surface
- lemma
- source
- evidence_type
- meaning
- pos
- morphology
- passage
- work
- author
- period
- genre
- verse
- line
- relations
- source_url
- source_id
- metadata

Example conceptual model:

```python
@dataclass
class Evidence:
    surface: str
    lemma: Optional[str] = None
    source: str = ""
    evidence_type: str = ""
    meaning: Optional[str] = None
    pos: Optional[str] = None
    morphology: Optional[str] = None
    passage: Optional[str] = None
    work: Optional[str] = None
    author: Optional[str] = None
    period: Optional[str] = None
    genre: Optional[str] = None
    verse: Optional[str] = None
    line: Optional[str] = None
    relations: list = field(default_factory=list)
    source_url: Optional[str] = None
    source_id: Optional[str] = None
    metadata: dict = field(default_factory=dict)
```

Do not over-engineer this.

---

## STEP 3 — CREATE RESOURCE ADAPTER INTERFACE

Create a minimal common interface for resources.

For example:

```python
class ResourceAdapter(ABC):

    @abstractmethod
    def lookup(self, query: str) -> list[Evidence]:
        raise NotImplementedError
```

The purpose is that later we can plug in:

- Thani Thamizh Akarathi
- Tamil WordNet
- Sentamizh
- Project Madurai

without redesigning the entire backend.

Do NOT implement those four adapters yet.

Only create the reusable interface.

---

## STEP 4 — IMPLEMENT THAMIZHIMORPH ADAPTER

Implement:

`backend/resources/thamizhimorph.py`

The adapter must interact with the actual ThamizhiMorph/Foma installation available on this machine.

Use the actual repository paths discovered during inspection.

Do NOT hardcode assumptions about the current working directory.

The adapter should:

1. Accept a Tamil surface word.
2. Invoke the appropriate Foma FST.
3. Capture the raw Foma output.
4. Parse successful analyses.
5. Extract the lemma/root when possible.
6. Preserve the morphological analysis.
7. Preserve which FST/model generated the result.
8. Return normalized Evidence objects.
9. Handle unknown words safely.

IMPORTANT:

Do NOT discard ambiguous analyses.

If Foma produces multiple analyses, preserve ALL analyses.

Do NOT arbitrarily select one analysis unless the existing ThamizhiMorph tooling explicitly provides a justified disambiguation mechanism.

For example, if:

```text
வந்தார்கள்
```

produces multiple analyses, preserve them all.

Likewise:

```text
சென்றுகொண்டிருந்தான்
```

may produce multiple analyses.

The raw Foma output must remain accessible in the returned evidence metadata.

Suggested metadata:

```python
{
    "fst_model": "...",
    "raw_foma_output": "...",
    "normalization_status": "...",
}
```

---

## STEP 5 — NORMALIZATION

Create a lightweight normalization layer.

The raw ThamizhiMorph output may look something like:

```text
மரம்+noun+pl+loc
```

or:

```text
மரம்+noun+pl+abl
```

or a more complex verb analysis.

Do NOT invent linguistic interpretations that are not present in the FST output.

The normalized Evidence should contain:

- **surface:** the original input
- **lemma:** the root/lemma if it can be reliably extracted
- **source:** "ThamizhiMorph"
- **evidence_type:** "morphology"
- **pos:** if available
- **morphology:** the parsed morphological features
- **metadata:** raw Foma output + FST model + any other useful information

If the analysis cannot be confidently parsed, preserve the raw output rather than guessing.

For unknown/failure cases:

```text
lemma = None
```

and metadata should record the failure/unknown status.

---

## STEP 6 — USE THE EXISTING THAMIZHIMORPH MODELS

Inspect the actual FST models.

Likely relevant models include:

- noun.fst
- noun-guess.fst
- verb-c-rest.fst
- verb-c11.fst
- verb-c12.fst
- verb-c3.fst
- verb-c4.fst
- verb-c62.fst
- verb-guess.fst
- adj.fst
- adj-guess.fst
- adv.fst
- adverb-guesser.fst
- part.fst
- pronoun.fst

BUT DO NOT blindly use this list.

Use the actual models present in the repository.

Determine a reasonable routing strategy for the first implementation.

For example:

- noun input → noun FST
- verb input → appropriate verb FST(s)

If automatic POS/model routing cannot be reliably determined, implement a small configurable model list and preserve the model name in the result.

Do not create a complicated machine-learning classifier.

The first goal is reliable integration with Foma.

---

## STEP 7 — CREATE A SIMPLE CLI TEST

Create a simple way to test the adapter from the command line.

For example:

```bash
python -m backend.resources.thamizhimorph வந்தார்கள்
```

or an equivalent command.

It should print readable structured output.

Example conceptual output:

```text
Surface: வந்தார்கள்
Source: ThamizhiMorph

Analysis 1:
Lemma: வா
POS: verb
Morphology: ...
FST: verb-c-rest.fst

Raw:
...

Analysis 2:
...
```

If the word is unknown:

```text
Surface: XXXXX
Source: ThamizhiMorph
Status: UNKNOWN
```

Do not fabricate analyses.

---

## STEP 8 — CREATE THE BENCHMARK RUNNER

Create a reusable benchmark script under:

`scripts/`

For example:

`scripts/run_benchmark.py`

Read the actual benchmark definition from:

`research/BENCHMARK.md`

Do NOT recreate the benchmark from memory if the file already defines it.

The runner should be capable of executing the benchmark against the ThamizhiMorph adapter.

For the first implementation, focus specifically on the morphology-related benchmark cases.

The known morphology cases include examples such as:

- வந்தார்கள்
- சென்றுகொண்டிருந்தான்
- மரங்களில்
- மனதினால்
- பாடுகின்றனர்

But again, use the actual BENCHMARK.md as the source of truth.

For each test case, record:

- input
- expected lemma
- expected morphology
- actual analyses
- matched/not matched
- raw Foma output
- FST model used
- error/failure if any

Output machine-readable JSON to:

`data/evaluation/thamizhimorph_results.json`

Also print a concise summary in the terminal.

Example:

```text
ThamizhiMorph Benchmark
------------------------
Cases: 10
Successful: X
Failed: Y
Unknown: Z
Lemma accuracy: XX%
Morphology match: XX%
```

IMPORTANT:

Do NOT invent or manually fill benchmark results.

Run the actual benchmark.

---

## STEP 9 — PRESERVE RAW EVIDENCE

Never modify:

`data/raw/thamizhimorph/`

Never rewrite the original FSTs, lexicons, README, or source files.

The raw source remains immutable.

Any normalized/processed data must go into:

`data/processed/`

Any evaluation results must go into:

`data/evaluation/`

---

## STEP 10 — ADD TESTS

Create a small test suite if practical.

At minimum test:

1. A known noun
2. A known inflected noun
3. A known verb
4. A complex verb
5. An unknown/random token

The tests should verify that:

- the adapter returns Evidence
- surface is preserved
- source is ThamizhiMorph
- raw Foma output is preserved
- unknown words do not crash the system
- multiple analyses are preserved

Do not spend excessive time on exhaustive testing yet.

---

## STEP 11 — DOCUMENT THE IMPLEMENTATION

Create a concise document:

`docs/IMPLEMENTATION.md`

Document:

1. Current architecture
2. Evidence model
3. ResourceAdapter interface
4. ThamizhiMorph integration
5. Foma invocation method
6. FST models used
7. Output normalization
8. Unknown-word handling
9. Benchmark command
10. Benchmark result location
11. Known limitations

Keep it technical and concise.

Do not write marketing language.

---

## IMPORTANT ENGINEERING RULES

1. Inspect before modifying.
2. Reuse existing code if present.
3. Keep data/raw immutable.
4. Do not invent linguistic information.
5. Preserve raw evidence.
6. Preserve ambiguity.
7. Do not silently discard failed analyses.
8. Do not hardcode machine-specific absolute paths.
9. Use relative/project-root-aware paths or configuration.
10. Keep dependencies minimal.
11. Do not introduce a large framework unless necessary.
12. Do not build the UI.
13. Do not build RAG.
14. Do not integrate an LLM.
15. Do not add new datasets.
16. Do not modify RESOURCE_AUDIT.md unless a factual implementation correction is genuinely required.
17. Do not modify BENCHMARK.md merely to make tests easier.
18. Do not fabricate benchmark scores.
19. Do not optimize prematurely.
20. Favor a working vertical slice over architectural complexity.

---

## SUCCESS CRITERIA

This task is COMPLETE only when:

- [ ] Repository was inspected first
- [ ] RESOURCE_AUDIT.md was read
- [ ] BENCHMARK.md was read
- [ ] ThamizhiMorph source was inspected
- [ ] Evidence model exists
- [ ] ResourceAdapter interface exists
- [ ] ThamizhiMorph adapter exists
- [ ] Foma integration works
- [ ] Tamil input works
- [ ] Raw Foma output is preserved
- [ ] Multiple analyses are preserved
- [ ] Unknown input is handled safely
- [ ] CLI test works
- [ ] Benchmark runner exists
- [ ] Morphology benchmark was actually executed
- [ ] data/evaluation/thamizhimorph_results.json exists
- [ ] No raw resource files were modified
- [ ] Basic tests exist/pass
- [ ] docs/IMPLEMENTATION.md exists

---

## FINAL RESPONSE TO ME

When finished, DO NOT give me a huge explanation.

Report exactly:

1. Files created/modified
2. How to run the ThamizhiMorph adapter
3. How to run the benchmark
4. Actual benchmark results
5. Which morphology cases passed/failed
6. Any technical blockers
7. What you recommend implementing NEXT

If something cannot be implemented because of an environment/tooling issue, STOP and clearly report the exact blocker and the command/error.

Do not hide failures.

Do not claim something works unless you actually tested it.

MOST IMPORTANT:

The objective is to get a real, working SOL AI foundation today.

Do not spend time making the architecture beautiful.

Make the smallest clean implementation that works end-to-end and produces real evaluation evidence.
