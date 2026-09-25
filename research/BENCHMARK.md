# சொல் AI — Benchmark

## 1. Purpose

The சொல் AI benchmark is a curated evaluation set used to measure
lexical coverage, morphological analysis, literary retrieval, and
contextual interpretation across the resources used by சொல் AI.

The benchmark is intentionally separate from the resource audit:

- Resource Audit → what each resource contains
- Benchmark → how well the resources perform on representative Tamil words

---

## 2. Benchmark Categories

| Category | Target |
|---|---:|
| Common words | 30 |
| Literary words | 15 |
| Polysemous words | 15 |
| Inflected words | 20 |
| Archaic / rare words | 10 |
| Modern / technical words | 10 |
| **Total** | **100** |

---

## 3. Lexical Coverage Benchmark

### 3.1 Common (30)

| ID | Word | Category | Notes |
|---|---|---|---|
| L001 | வீடு | Common | Everyday noun |
| L002 | நீர் | Common | Common noun |
| L003 | மரம் | Common | Common noun |
| L004 | மனிதன் | Common | Human/person |
| L005 | பெண் | Common | Common noun |
| L006 | குழந்தை | Common | Common noun |
| L007 | நாள் | Common | Time noun |
| L008 | கல் | Common | Common noun |
| L009 | மண் | Common | Common noun |
| L010 | கண் | Common | Body-part noun |
| L011 | கை | Common | Body-part noun |
| L012 | தலை | Common | Body-part noun |
| L013 | வழி | Common | Common noun |
| L014 | உணவு | Common | Common noun |
| L015 | பள்ளி | Common | Modern/common noun |
| L016 | புத்தகம் | Common | Common noun |
| L017 | நண்பன் | Common | Person/social noun |
| L018 | நாடு | Common | Place/nation noun |
| L019 | ஊர் | Common | Place noun |
| L020 | கடல் | Common | Natural feature |
| L021 | மலை | Common | Natural feature |
| L022 | வீதி | Common | Place/road noun |
| L023 | மழை | Common | Weather/nature noun |
| L024 | சூரியன் | Common | Celestial noun |
| L025 | நிலா | Common | Celestial/nature noun |
| L026 | காற்று | Common | Nature noun |
| L027 | பூ | Common | Plant/nature noun |
| L028 | நதி | Common | Natural feature |
| L029 | வயல் | Common | Agricultural noun |
| L030 | கதவு | Common | Household noun |

### 3.2 Literary (15)

Deliberately more literary/cultural vocabulary.

| ID | Word | Category | Notes |
|---|---|---|---|
| L031 | யாழ் | Literary | Classical musical instrument |
| L032 | திணை | Literary | Classical literary classification |
| L033 | குறிஞ்சி | Literary | Sangam landscape/category |
| L034 | முல்லை | Literary | Sangam landscape/category |
| L035 | மருதம் | Literary | Sangam landscape/category |
| L036 | நெய்தல் | Literary | Sangam landscape/category |
| L037 | பாலை | Literary | Sangam landscape/category |
| L038 | அகத்திணை | Literary | Classical literary concept |
| L039 | புறத்திணை | Literary | Classical literary concept |
| L040 | தோழி | Literary | Important Sangam literary/social role |
| L041 | அன்பு | Literary | Literary/emotional vocabulary |
| L042 | அருள் | Literary | Literary/religious vocabulary |
| L043 | வீரம் | Literary | Heroic/literary vocabulary |
| L044 | புகழ் | Literary | Literary/cultural vocabulary |
| L045 | செல்வம் | Literary | Classical/cultural vocabulary |

### 3.3 Polysemous (15)

Particularly important because contextual meaning is one of சொல் AI's core goals.

| ID | Word | Category | Notes |
|---|---|---|---|
| L046 | அகம் | Polysemous | Interior, mind, home/world of inner life etc. |
| L047 | அடி | Polysemous | Foot, blow, poetic/metrical unit, base etc. |
| L048 | ஆறு | Polysemous | Six, river, way/method etc. |
| L049 | பால் | Polysemous | Milk, side/direction, toward etc. |
| L050 | கால் | Polysemous | Leg/foot, quarter, fraction/time-related usages |
| L051 | மாலை | Polysemous | Evening, garland |
| L052 | பொருள் | Polysemous | Thing, meaning, wealth/subject matter |
| L053 | வாய் | Polysemous | Mouth, opening, entrance/outlet etc. |
| L054 | கரை | Polysemous | Shore/bank, boundary/limit |
| L055 | கோல் | Polysemous | Stick/staff, symbolic/functional usages |
| L056 | அணி | Polysemous | Ornament, group, arrangement/feature |
| L057 | கடி | Polysemous | Bite, sharpness, tax/levy-related usages |
| L058 | பார் | Polysemous | See/look, world/earth, contextual usages |
| L059 | படி | Polysemous | Step, manner, level, read/study-related usages |
| L060 | தாள் | Polysemous | Leaf/page, sheet, foot/sole in literary usage |

For a word like `அகம்`, சொல் AI should not merely dump every dictionary
definition. It should eventually be able to say: "In this particular
literary context, the evidence suggests this sense."

### 3.4 Inflected (20)

These are the forms pushed through ThamizhiMorph.

| ID | Surface form | Category | Expected lemma | Expected features |
|---|---|---|---|---|
| L061 | வந்தார்கள் | Inflected | வா | Past + 3rd person plural/honorific |
| L062 | சென்றுகொண்டிருந்தான் | Inflected | செல் | Past + progressive/complex + 3rd person singular masculine |
| L063 | மரங்களில் | Inflected | மரம் | Plural + locative |
| L064 | மனதினால் | Inflected | மனம் | Instrumental/case-marked |
| L065 | பாடுகின்றனர் | Inflected | பாடு | Present/progressive + 3rd person plural |
| L066 | மரத்தை | Inflected | மரம் | Accusative |
| L067 | வீட்டில் | Inflected | வீடு | Locative |
| L068 | மாணவர்களுக்கு | Inflected | மாணவர் | Plural + dative |
| L069 | பெண்களால் | Inflected | பெண் | Plural + instrumental |
| L070 | புத்தகங்களின் | Inflected | புத்தகம் | Plural + genitive |
| L071 | குழந்தைகளுடன் | Inflected | குழந்தை | Plural + comitative |
| L072 | நாடுகளில் | Inflected | நாடு | Plural + locative |
| L073 | அவனை | Inflected | அவன் | Accusative |
| L074 | அவர்களிடம் | Inflected | அவர் | Plural/honorific + locative/dative |
| L075 | சென்றேன் | Inflected | செல் | Past + 1st person singular |
| L076 | படித்துக்கொண்டிருக்கிறாள் | Inflected | படி | Progressive/complex + 3rd person singular feminine |
| L077 | வீடுகளுக்குள் | Inflected | வீடு | Plural + inside/dative construction |
| L078 | மரங்களிலிருந்து | Inflected | மரம் | Plural + ablative |
| L079 | செய்வார்கள் | Inflected | செய் | Future + 3rd person plural/honorific |
| L080 | பாடியவர் | Inflected | பாடு | Past participial form + human nominalization |

For this category, expected grammatical labels are not required to match
Foma's labels exactly. Foma output will be normalized later.

### 3.5 Archaic / Rare (10)

| ID | Word | Category | Notes |
|---|---|---|---|
| L081 | அணங்கு | Archaic / rare | Classical/religious-literary vocabulary |
| L082 | மடல் | Archaic / rare | Classical literary practice/concept |
| L083 | விறலி | Archaic / rare | Classical literary/social term |
| L084 | வேந்தன் | Archaic / rare | Classical term for king/ruler |
| L085 | பரத்தை | Archaic / rare | Classical literary/social vocabulary |
| L086 | மறவர் | Archaic / rare | Classical warrior/social term |
| L087 | வள்ளல் | Archaic / rare | Classical term for generous patron |
| L088 | செவ்வி | Archaic / rare | Rare/classical vocabulary |
| L089 | தொல் | Archaic / rare | Archaic/literary term meaning ancient/old |
| L090 | பாணர் | Archaic / rare | Classical poet/musician social term |

### 3.6 Modern / Technical (10)

| ID | Word | Category | Notes |
|---|---|---|---|
| L091 | கணினி | Modern / technical | Computing |
| L092 | மென்பொருள் | Modern / technical | Software |
| L093 | தரவுத்தளம் | Modern / technical | Database |
| L094 | இணையம் | Modern / technical | Internet |
| L095 | செயற்கை நுண்ணறிவு | Modern / technical | Artificial intelligence |
| L096 | வலைத்தளம் | Modern / technical | Website |
| L097 | நிரலாக்கம் | Modern / technical | Programming |
| L098 | தகவல்தொடர்பு | Modern / technical | Communication/technology |
| L099 | மின்வணிகம் | Modern / technical | E-commerce |
| L100 | தானியக்கம் | Modern / technical | Automation |

---

## 4. Resource Coverage Results

| Resource | Overall | Common | Literary | Polysemous | Inflected | Archaic | Modern |
|---|---:|---:|---:|---:|---:|---:|---:|
| Thani Thamizh Akarathi | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Tamil WordNet | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| ThamizhiMorph | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Sentamizh | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Project Madurai | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Combined | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

---

## 5. Morphological Benchmark

The 20 inflected cases (L061–L080) are included in the 110 lexical cases.

| ID | Lexical ID | Surface Form | Expected Lemma | Expected Features | Result |
|---|---|---|---|---|---|
| M001 | L101 | வந்தார்கள் | வா | past + 3rd person plural/honorific | TBD |
| M002 | L102 | சென்றுகொண்டிருந்தான் | செல் | past + progressive/complex + 3sg masculine | TBD |
| M003 | L103 | மரங்களில் | மரம் | plural + locative | TBD |
| M004 | L104 | மனதினால் | மனம் | instrumental/case-marked | TBD |
| M005 | L105 | பாடுகின்றனர் | பாடு | present/progressive + 3rd person plural | TBD |

Grammatical labels will be normalized against ThamizhiMorph (Foma)
output before scoring.

---

## 6. Literary Retrieval Benchmark

For selected literary words, சொல் AI should attempt to retrieve:

- Word / surface form
- Lemma
- Literary passage
- Work
- Author
- Collection
- Chapter / section where available
- Verse
- Line where available
- Period
- Genre
- Source dataset
- Source URL where available

---

## 7. Evaluation Metrics

### Lexical Coverage

Percentage of benchmark words found in each resource.

### Morphological Accuracy

Percentage of morphological test forms for which the expected lemma and
grammatical features are correctly recovered.

### Literary Retrieval

Percentage of literary test words for which at least one valid literary
occurrence is retrieved with usable provenance.

### Combined Evidence Coverage

Percentage of benchmark cases for which சொல் AI can provide evidence from
at least two independent resource layers.

---

## 8. Evaluation Results

To be completed after ingestion and implementation.

Numbers are not calculated until the ingestion layer exists, so that the
same benchmark can be run automatically against every resource.

---

## 9. Notes

The benchmark contains 110 lexical cases for the hackathon implementation.
A larger benchmark may be created later for more rigorous evaluation.

Next phase: design the unified சொல் AI data model, then build ingestion.