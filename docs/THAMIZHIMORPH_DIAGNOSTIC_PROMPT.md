# SOL AI — ThamizhiMorph Diagnostic Investigation

We have completed the first ThamizhiMorph vertical slice.

## Current benchmark

- 10 morphology cases
- 8/10 lemma matches
- 1/10 morphology matches
- 2 failed lemma cases:
  - சென்றுகொண்டிருந்தான் → expected செல், actual சென்றுகொண்டிரு
  - மனதினால் → expected மனம், actual மனதி
- பாடுகின்றனர் → expected பாடு and reported as passed, but it used `noun-guess.fst`, so this needs investigation.

**DO NOT implement arbitrary root-stripping rules yet.**

Before building any additional resource adapters, investigate the actual ThamizhiMorph/Foma behavior.

---

## TASK

### 1. Inspect the complete raw Foma output for:

- வந்தார்கள்
- சென்றுகொண்டிருந்தான்
- மரங்களில்
- மனதினால்
- பாடுகின்றனர்

### 2. Inspect the exact Evidence objects produced by the adapter for those five words.

### 3. Determine:

- every analysis returned by Foma
- which FST model produced each analysis
- whether multiple models were attempted
- whether the adapter is incorrectly selecting one analysis
- whether the lemma extraction/parser is responsible for the incorrect lemma
- whether the expected lemma actually appears somewhere in the raw Foma output

### 4. For: சென்றுகொண்டிருந்தான்

Determine whether Foma actually provides enough information to derive:

```text
செல்
```

or whether the current FST only analyzes the complex verbal form as:

```text
சென்றுகொண்டிரு
```

Do NOT assume that stripping "கொண்டிரு" is linguistically valid.

### 5. For: மனதினால்

Determine whether:

```text
மனதி
```

is genuinely the FST root/stem or whether the adapter parser incorrectly extracted it from a richer analysis.

### 6. For: பாடுகின்றனர்

Determine why `noun-guess.fst` produced the accepted lemma.

This is especially important because a verb being accepted through a noun guesser indicates that our model routing may need improvement.

### 7. Check whether the adapter should:

- try multiple appropriate FST models
- preserve multiple analyses
- rank analyses
- distinguish direct lexical analyses from guesser analyses

Do not implement ranking unless there is evidence that it is necessary.

### 8. Add a diagnostic script, for example:

`scripts/debug_thamizhimorph.py`

It should accept one or more Tamil words and print:

- Surface
- FST model
- Raw Foma output
- Parsed lemma
- POS
- Morphology

### 9. Add/modify tests for the five diagnostic cases.

### 10. Re-run the benchmark after any legitimate parser/adapter fixes.

---

## IMPORTANT

Do NOT:

- add special-case rules for these individual words
- hardcode "சென்றுகொண்டிருந்தான் → செல்"
- hardcode "மனதினால் → மனம்"
- invent linguistic rules
- modify the raw ThamizhiMorph resource
- build the other resource adapters yet
- build RAG/LLM/UI

The objective is to understand the failure mode first.

---

## FINAL REPORT

Give me:

1. Raw Foma analyses for the five diagnostic words
2. What caused each failure
3. Whether the adapter/parser or FST is responsible
4. Any legitimate general normalization rule discovered
5. Updated benchmark results
6. Whether ThamizhiMorph is now sufficiently stable to proceed to the next resource adapter

Do not claim a fix unless the actual Foma output and tests support it.
