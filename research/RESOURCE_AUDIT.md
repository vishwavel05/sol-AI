# சொல் AI — Resource Audit

> Phase 0: Audit Tamil lexical, morphological, and literary resources
> before integrating anything into the சொல் AI application.

---

# 1. Objective

The purpose of this audit is to evaluate available Tamil language
resources and determine:

- What each resource contains
- How large it actually is
- What format it uses
- What metadata it provides
- What linguistic information it contains
- How much usable data it provides
- How resources overlap
- What licensing restrictions apply
- How difficult each resource would be to integrate
- How each resource could contribute to சொல் AI

No resource will be integrated into the சொல் AI application until
its structure, contents, and licensing have been evaluated.

---

# 2. Resource Inventory

## 2.1 Core Resources

### Lexical

1. Thani Thamizh Akarathi / Kalanjiyam
2. Tamil WordNet

### Morphology

3. ThamizhiMorph

### Literature / Corpus

4. Sentamizh Corpus
5. Project Madurai

---

## 2.2 Secondary Resources

### Lexical

6. Tamil Virtual Academy
7. Tamil Wiktionary
8. University of Madras Tamil Lexicon
9. Other open Tamil dictionaries

### Linguistics

10. Tamil POS / tokenization resources
11. Other Tamil linguistic resources

### Literature

12. Other public-domain or appropriately licensed Tamil literary corpora

---

# 3. Evaluation Criteria

Every resource will be evaluated using the following criteria.

## 3.1 Identity

- What is the resource?
- Who created or maintains it?
- What is its intended purpose?
- Where is the official source?

## 3.2 Size

### Advertised

- Number of entries:
- Number of words:
- Number of texts:
- Number of records:
- Other advertised statistics:

### Measured

- Raw records:
- Valid records:
- Invalid/malformed records:
- Unique entries:
- Unique words:
- Unique lemmas:
- Entries with usable meanings:

## 3.3 Format

- File format:
- Encoding:
- Character normalization:
- Structure:
- Machine-readable:
- Human-readable:
- Repository/download method:

## 3.4 Metadata

List every useful field available.

Examples:

- Word
- Lemma
- Definition
- Meaning
- POS
- Synonym
- Antonym
- Root
- Author
- Work
- Chapter
- Verse
- Date
- Genre
- Source
- URL

## 3.5 Definitions

- Definition language:
- Tamil definitions:
- English definitions:
- Both:
- Other:

## 3.6 Semantic Information

- Multiple meanings:
- Synonyms:
- Antonyms:
- Related words:
- Hypernyms:
- Hyponyms:
- Semantic relations:
- Synsets:

## 3.7 Morphological Information

- Lemmas:
- Roots:
- Inflections:
- Morphological analysis:
- Morphological generation:
- POS:
- Grammatical features:

## 3.8 Literature / Context

Where applicable:

- Text:
- Passage:
- Sentence:
- Verse:
- Line:
- Work:
- Author:
- Period:
- Genre:
- Chapter:
- Section:
- Source:

## 3.9 Licensing

- License:
- Copyright holder:
- Commercial use:
- Modification:
- Redistribution:
- Attribution:
- Dataset-specific restrictions:
- Evidence/source:

## 3.10 சொல் AI Usage

- Can சொல் AI use this resource?
- Can we modify it?
- Can we redistribute derived data?
- Can it be used in a public demo?
- Can it be used commercially?
- Restrictions or concerns:

## 3.11 Integration Difficulty

Rating:

- Easy
- Medium
- Hard
- Unknown

Reason:

## 3.12 Example Record

Include at least one real record from the resource.

---

# 4. Resource Audits

---

# 4.1 Thani Thamizh Akarathi / Kalanjiyam

## What is it?

An open-source Tamil dictionary resource containing machine-readable
plain-text dictionary data and other linguistic resources.

The repository contains multiple resource types. The plain-text
dictionary structure is documented in `file_template.txt`.

## Advertised size

TBD — must be established from the repository/data files rather than
taken from an external advertised figure.

## Measured size

TBD — to be calculated from the raw resource.

## Format

At least one dictionary resource is represented as plain text.

The documented general structure is:

Dictionary name
→ word/type
→ one or more meanings

The inspected `Pav_Words.txt` uses a simpler delimiter-based structure:

WORD
==
MEANING(S)

Example:

அகதி
==
ஏதிலி

## Metadata

The inspected plain-text file does not appear to provide structured
metadata fields for each entry.

The information is primarily represented through text structure and
delimiters.

Further investigation is required across the other dictionary files.

## Definitions

The inspected file contains Tamil equivalents/meanings.

Some entries contain multiple comma-separated equivalents.

Example:

அஞ்சலி
==
கும்பீடு, இறுதி வணக்கம்

English → Tamil entries are also present later in the file.

## Multiple meanings

YES / OBSERVED

The same headword can occur more than once with different meanings or
contexts.

Examples observed include:

- வாக்கு
- வாதம்

This means deduplication cannot simply discard repeated headwords.

Repeated headwords may represent separate senses.

## Semantic relations

The inspected file does not explicitly expose structured semantic
relations such as synsets, hypernyms, or hyponyms.

Some entries provide equivalent/synonymous Tamil expressions.

Further investigation required.

## Morphology

No explicit morphological analysis or generation information was
identified in the inspected `Pav_Words.txt`.

Further investigation required across the repository.

## License

TBD — verify against the repository's license documentation.

## சொல் AI usage

Potentially useful as a lexical/equivalent resource.

Before integration, determine:

- exact licensing terms
- complete file inventory
- duplicate/sense structure
- encoding
- number of usable entries
- relationship between the different dictionary files

## Integration difficulty

TBD

A preliminary observation is that the plain-text structure appears
relatively straightforward to parse, but multiple dictionary formats
and repeated headwords will require careful normalization.

## Example record

### Example 1

அகதி
==
ஏதிலி

### Example 2

அஞ்சலி
==
கும்பீடு, இறுதி வணக்கம்

### Example 3

ஆகாரம்
==
உணவு, உண்டி

## Observations

1. The resource is not simply a flat CSV-style word list.
2. Multiple meanings/equivalents can exist.
3. Repeated headwords occur and must not automatically be treated as
   duplicate errors.
4. The inspected file contains both Tamil → Tamil and English → Tamil
   entries.
5. The repository's documented format and the inspected `Pav_Words.txt`
   format should both be investigated before designing the parser.
6. Raw files must remain unchanged; normalization will happen later.

## சொல் AI relevance

HIGH

The resource can potentially contribute lexical equivalents and
Tamil terminology, particularly for mapping commonly used or
non-Tamil-origin vocabulary to Tamil alternatives.

However, its actual coverage and relationship to the other dictionary
resources must be measured before assigning it a role in the final
சொல் AI architecture.

## Source

- Thani Thamizh Akarathi repository
- `file_template.txt`
- `Pav_Words.txt`

### Additional dictionary: Sanskrit to Tamil - Dictionary by Neelambigai Ammaiyar

The repository also contains a plain-text Sanskrit-to-Tamil dictionary
at:

`plain_text_dicts/Sanskrit to Tamil - Dictionary by Neelambigai Ammaiyar.txt`

## Observed structure

The file uses a primarily line-based structure:

`HEADWORD / VARIANT(S) - TAMIL MEANING(S)`

Examples include:

- அகங்காரம் - செருக்கு, இறுமாப்பு, முனைப்பு, யானெனல்
- அகிம்சை - இன்னா செய்யாமை, கொல்லாமை
- அக்கினி - நெருப்பு, தீ, அனல், எரி, தழல்

## Observed characteristics

- Multiple Tamil equivalents can occur for one headword.
- Multiple headword variants can occur within one record.
- Some entries explicitly identify the source language of a form.
- Some records contain several meanings.
- Repeated headwords occur.
- The file is plain text rather than a structured CSV/JSON database.
- No explicit POS field was observed in the inspected portion.
- No explicit structured morphological analysis was observed.

## Important distinction

This resource should be treated as a separate lexical source from
`Pav_Words.txt`.

It should not be merged with other dictionary resources until the
individual records have been parsed, normalized and evaluated.

## Measured size

- Total lines: TBD
- Candidate lexical records: TBD
- Unique headwords: TBD
- Unique normalized headwords: TBD
- Records containing multiple meanings: TBD
- Records containing variants: TBD

## License

Repository license grants reproduction, adaptation, distribution and public
performance subject to the stated Creative Commons conditions.

Important:
Individual embedded dictionaries/resources may have separate provenance or
licensing terms and must be checked before redistribution.

சொல் AI usage:
Potentially usable, including derived/processed data, provided attribution,
license preservation, and adaptation requirements are followed.

## சொல் AI relevance

Potentially useful for:

- Tamil equivalents of Sanskrit-derived vocabulary
- lexical coverage
- variant forms
- synonym/equivalent expansion
- identifying relationships between alternate lexical forms

However, its role should be determined after comparison with the other
lexical resources.

## Source

`Sanskrit to Tamil - Dictionary by Neelambigai Ammaiyar.txt`

---

# 4.2 Tamil WordNet

### Source
AU-KBC Research Centre, Chennai & Tamil University, Thanjavur.

Resource version: Tamil WordNet 1.0 (May 2007)

Downloaded archive:
`data/raw/tamil_wordnet/TamilWordNet.tgz`

Compressed archive size:
36,132,747 bytes (~34.5 MiB)

### What is it?

Tamil WordNet is a structured lexical-semantic resource implemented as a MySQL database and accompanied by an older Java Servlet-based web interface.

The archive contains a MySQL dump with four main tables:

- `twn`
- `sense`
- `morphtable`
- `frequency`

### Data structure

#### `twn` — Core lexical network

Fields:

- `nodeindex`
- `label`
- `gloss`
- `example`
- `relation`
- `feature`
- `english`
- `indexlength`
- `pos`

The `nodeindex` values form a hierarchical structure. For example:

`0,0,0,0,0,2`
→ `0,0,0,0,0,2,0`
→ `0,0,0,0,0,2,0,0`
→ `0,0,0,0,0,2,0,0,0`

This indicates that the resource represents lexical concepts in a hierarchical/graph-like organization.

Observed lexical entries include terms such as:

- `muuvulakam`
- `puumi`
- `ndilam`
- `tarai`
- `kaTal`
- `ndiir`
- `kuRinjci`
- `mullai`
- `marutam`
- `ndeytal`
- `paalai`

The `twn` table explicitly stores POS information such as `Noun` and `Adjective`.

### `sense` — Sense / hypernym information

Fields:

- `label`
- `pos`
- `hypercount`
- `hypernym`

This provides a separate representation of sense and hypernym information.

### `morphtable` — Morphological information

Fields:

- `inflated_word`
- `root_word`

This provides an observed mapping of an inflected/inflated word to its root word.

This is particularly relevant to சொல் AI because it provides a morphology signal that can later be compared against ThamizhiMorph.

### `frequency` — Word frequency

Fields:

- `word`
- `freq`

This provides frequency information for lexical items.

### Definitions / examples

The `twn` schema contains dedicated fields for:

- gloss
- example
- English equivalent

However, the records inspected during the initial audit contained many `NULL` values in these fields. Therefore, the presence of these fields is confirmed, but their actual coverage has not yet been measured.

### Encoding

The inspected lexical data uses a legacy Romanized Tamil representation rather than modern Unicode Tamil.

Examples:

- `iyaRkaikkappaaRpaTTavai`
- `muuvulakam`
- `puumi`
- `kuRinjci`
- `marutam`

The archive also contains Tamil font/encoding resources such as TAB fonts and `charmap.gif`.

Therefore, Unicode conversion/normalization will be required before directly integrating the resource into a modern சொல் AI pipeline.

### License

Tamil WordNet 1.0 states that:

- `tvudump.sql` is licensed under **Creative Commons Attribution-ShareAlike 2.5 (CC BY-SA 2.5)**.
- The remaining files are licensed under the **GNU General Public License (GPL)**.

Copyright is attributed to AU-KBC Research Centre, Chennai and Tamil University, Thanjavur.

The license distinction must be preserved when using or redistributing the database versus the accompanying software/application files.

### Initial சொல் AI relevance

Tamil WordNet is potentially a major lexical-semantic component for சொல் AI because it provides multiple complementary signals:

1. Lexical concepts
2. Hierarchical relationships
3. Sense information
4. Hypernym information
5. Morphological root mappings
6. Word frequency
7. POS information
8. Examples/gloss fields where populated
9. English equivalents where populated

### Integration considerations

The resource should not be integrated directly into the application in its original form.

A future ingestion pipeline should:

1. Extract the MySQL dump.
2. Parse the four tables.
3. Convert legacy Romanized Tamil into Unicode Tamil.
4. Normalize lexical forms.
5. Preserve the original WordNet identifiers and relation codes.
6. Preserve provenance and licensing metadata.
7. Convert the hierarchical structure into a modern graph/relational representation.
8. Evaluate the morphology table separately against ThamizhiMorph.
9. Measure actual coverage of glosses, examples, relations, senses and lexical items.

### Audit status

**Status: Audited — suitable for further evaluation and ingestion design.**

Exact usable lexical-entry count has not yet been measured and should not be inferred from the archive size or number of SQL records.
---

# 4.3 ThamizhiMorph

### Source

GitHub repository:

https://github.com/sarves/thamizhi-morph

ThamizhiMorph is an open-source Tamil morphological analyser and generator based on Finite-State Transducers (Foma).

### Repository structure

Important components identified:

- `Lexicons/`
- `Unique-word-list/`
- `FST-Models/`
- `Generated-Verbs/`
- `test-data/`
- `thamizhi-morph-parsing.py`

### Noun lexicons

The repository documents noun lexicons obtained from:

- Open-Tamil
- AU-KBC corpus
- Tamil Wiktionary

Documented source-list counts:

| Lexicon | Entries |
|---|---:|
| `Nouns-animals` | 71 |
| `Nouns-AUKBC` | 30,539 |
| `Nouns-birds` | 156 |
| `Nouns-flowers` | 99 |
| `Nouns-Open-Tamil-by Muthu Annamalai` | 85,254 |
| `Nouns-Propernouns` | 88,245 |
| `Nouns-trees` | 378 |

Total documented noun-source entries: **204,742**.

The repository explicitly warns that these lists are not necessarily clean and that words may not be in root form.

### Unique word inventories

Observed repository files:

- `Unique-nouns`: **26,006 entries**
- `Unique-verbs`: **19,249 entries**

These are plain word lists.

Inspection showed that the lists contain inflected and derived forms.

For example, the noun inventory contains forms such as:

- `அகம்`
- `அகத்தின்`
- `அகங்கள`
- `அகங்களைப்போல்`

The verb inventory contains many conjugated forms such as:

- `அகப்பட`
- `அகப்படும்`
- `அகப்பட்டான்`
- `அகப்பட்டிருந்தால்`
- `அகப்பட்டுக்கொண்டாள்`

Therefore, these files should **not** be treated as clean lemma inventories.

### FST models

The repository contains FST models for:

#### Nouns

- `noun.fst`
- `noun-guess.fst`

#### Verbs

- `verb-c3.fst`
- `verb-c4.fst`
- `verb-c62.fst`
- `verb-c11.fst`
- `verb-c12.fst`
- `verb-c-rest.fst`
- `verb-guess.fst`

The repository documentation states that the verb models are divided into classes because of orthographic-rule conflicts and should be iterated through. The guesser is intended as a fallback after the regular verb models.

Additional FST models exist for:

- adjectives
- adverbs
- pronouns
- particles

### Functional Foma testing

Foma was installed and the repository FST models were successfully loaded.

#### Test 1 — noun morphology

Input:

`மரங்களில்`

Model:

`noun.fst`

Observed output:

```text
மரம்+noun+pl+abl
மரம்+noun+pl+loc

---

# 4.4 Sentamizh Corpus

## What is it?

A multi-framework annotated Classical Tamil corpus containing literary verses from major Tamil works, with Tamil-native literary, interpretive, cultural, and provenance metadata.

## Advertised size

10,393 verses across 9 source texts, using a 32-field schema.

## Measured size

10,393 records, verified directly from the nine processed JSON files.

| Work | Records |
|---|---:|
| Akananuru | 400 |
| Divya Prabandham | 3,928 |
| Kuruntokai | 400 |
| Manimekalai | 493 |
| Natrinai | 396 |
| Purananuru | 388 |
| Silappatikaram | 10 |
| Thevaram | 4,043 |
| Thirumanthiram | 335 |
| **Total** | **10,393** |

## Format

Processed data is stored as UTF-8 JSON, with structured verse records.

The repository also contains schemas, documentation, annotation tooling, scripts, and source data.

## Metadata

Each record follows a 32-field schema:

- `verse_id`
- `source_text`
- `layer`
- `period`
- `verse_number`
- `classical_tamil`
- `modern_tamil`
- `english`
- `source_url`
- `difficulty`
- `thinai`
- `turai`
- `akam_or_puram`
- `karu`
- `uri`
- `ullurai`
- `speaker_role`
- `metre`
- `pann`
- `dhvani_layer`
- `rasa_primary`
- `rasa_secondary`
- `themes`
- `philosophical_concept`
- `cultural_context`
- `storytelling_seed_narrative`
- `storytelling_seed_emotional`
- `nayika_bheda`
- `visual_imagery`
- `emotional_valence`
- `annotator`
- `annotation_confidence`

The schema contains 32 fields, but they are not all populated in the current dataset.

## Text structure

The fundamental unit is a verse-level record.

Each record connects a Classical Tamil verse with its literary work, period/layer information, and available annotations.

Example identifiers include:

- `KURU-001`
- `NATR-001`
- `PURN-001`

## Linguistic annotations

The corpus contains literary, cultural, and interpretive annotations including:

- Thinai
- Turai
- Akam/Puram
- Speaker role
- Rasa
- Cultural context
- Pann
- Metre

Measured field population:

| Field | Populated |
|---|---:|
| `classical_tamil` | 10,393 / 10,393 |
| `cultural_context` | 10,393 / 10,393 |
| `speaker_role` | 9,990 / 10,393 |
| `rasa_primary` | 8,306 / 10,393 |
| `pann` | 4,009 / 10,393 |
| `thinai` | 1,196 / 10,393 |
| `akam_or_puram` | 1,584 / 10,393 |
| `turai` | 581 / 10,393 |
| `metre` | 388 / 10,393 |
| `english` | 795 / 10,393 |
| `source_url` | 1,184 / 10,393 |

Several other annotation fields are currently unpopulated.

## POS information

Not provided as a structured POS annotation field in the 32-field corpus schema.

## Morphology

No explicit morphological analysis is provided.

Sentamizh should therefore not be treated as the morphology engine for சொல் AI. ThamizhiMorph and Tamil WordNet's `morphtable` are more relevant for morphological processing.

## License

The repository uses the Apache License 2.0.

However, the corpus incorporates material originating from multiple upstream sources. Therefore, upstream provenance and licensing should be preserved when using individual source material rather than assuming the repository license automatically resolves every underlying source.

## சொல் AI usage

Highly relevant as a literary context and provenance layer.

Potential uses include:

- Finding literary occurrences of words
- Providing verse-level context
- Connecting words to specific works
- Period and literary-layer filtering
- Literary meaning exploration
- Cultural-context enrichment
- Supporting contextual meaning explanations
- Providing provenance for displayed literary examples

It should not be used as the sole lexical dictionary or morphological analyzer.

## Integration difficulty

Medium.

The processed JSON structure is straightforward to ingest.

The main integration considerations are:

1. Different fields have substantially different coverage.
2. The corpus is heavily weighted toward Bhakti literature.
3. Only 1,184 / 10,393 records have populated `source_url`.
4. Some upstream datasets have separate licensing considerations.
5. The corpus does not provide POS or morphological analysis.

## Example record

A representative record follows the 32-field structure:

```json
{
  "verse_id": "...",
  "source_text": "...",
  "layer": "...",
  "period": "...",
  "verse_number": "...",
  "classical_tamil": "...",
  "modern_tamil": "...",
  "english": "...",
  "source_url": "...",
  "difficulty": "...",
  "thinai": "...",
  "turai": "...",
  "akam_or_puram": "...",
  "karu": "...",
  "uri": "...",
  "ullurai": "...",
  "speaker_role": "...",
  "metre": "...",
  "pann": "...",
  "dhvani_layer": "...",
  "rasa_primary": "...",
  "rasa_secondary": "...",
  "themes": "...",
  "philosophical_concept": "...",
  "cultural_context": "...",
  "storytelling_seed_narrative": "...",
  "storytelling_seed_emotional": "...",
  "nayika_bheda": "...",
  "visual_imagery": "...",
  "emotional_valence": "...",
  "annotator": "...",
  "annotation_confidence": "..."
}

## Observations

1. The advertised 10,393 figure is accurate. The nine processed JSON files contain 10,393 records.

2. The 32-field schema should not be confused with 32 fully populated annotations.

3. Several fields currently have zero populated records, including:
   - `modern_tamil`
   - `karu`
   - `uri`
   - `ullurai`
   - `dhvani_layer`
   - `rasa_secondary`
   - `themes`
   - `philosophical_concept`
   - `storytelling_seed_narrative`
   - `storytelling_seed_emotional`
   - `nayika_bheda`
   - `visual_imagery`
   - `emotional_valence`

4. The corpus is heavily weighted toward Bhakti literature:
   - Bhakti: 7,971
   - Sangam: 1,584
   - Epic: 503
   - Spiritual: 335

5. Record-level source provenance is incomplete. Only 1,184 / 10,393 records have a populated `source_url`.

6. Kuruntokai, Natrinai, and Purananuru have complete source URL coverage:
   - Kuruntokai: 400 / 400
   - Natrinai: 396 / 396
   - Purananuru: 388 / 388

7. The six populated source URLs correspond to the three works above and their respective verse ranges.

## சொல் AI relevance

**High — primarily as the literary-context layer.**

Sentamizh can provide the part of சொல் AI that answers:

> "Where does this word appear in Tamil literature, and what is the surrounding literary context?"

It complements rather than replaces the other resources:

| Resource | Primary role in சொல் AI |
|---|---|
| Tamil WordNet | Lexical relations, senses, and morphology-related data |
| Thani Thamizh Akarathi | Dictionary meanings and lexical resources |
| ThamizhiMorph | Morphological analysis |
| Sentamizh | Literary context and annotations |
| Project Madurai | Broader literary corpus |

This combination can support a system that connects lexical meaning with actual literary usage.

## Source

Official repository: https://github.com/indic-corpora/sentamizh-corpus

---

# 4.5 Project Madurai

## What is it?

Project Madurai is an open, voluntary initiative that collects and publishes free electronic editions of Tamil literary works. It provides searchable digital texts of Tamil classics and other literary works through the web.

The project began in 1998 and initially released texts using TSCII encoding. Unicode releases began in the early 2000s, and the current collection provides many works in Unicode/UTF-8. :contentReference[oaicite:1]{index=1}

## Advertised size

The current Project Madurai Unicode catalogue contains approximately **1,090 catalogue entries**.

The catalogue is organized using:

- Work number
- Title
- Author
- Genre
- PDF
- Unicode HTML

Some work numbers contain multiple titles/parts, so the catalogue-entry count should not automatically be interpreted as the number of unique literary works. :contentReference[oaicite:2]{index=2}

## Measured size

Approximately **1,090 catalogue entries** were observed in the Unicode Tamil works catalogue.

A complete record-level corpus count was not performed because Project Madurai is a large collection of individual literary texts rather than a single structured dataset.

For சொல் AI, the useful unit will therefore be the individual text/work rather than the catalogue-entry count.

## Format

Project Madurai provides literary works in multiple formats, including:

- Unicode/UTF-8 HTML
- PDF
- EPUB
- Kindle formats for some works
- Older TSCII/legacy encoded material

For சொல் AI, **Unicode/UTF-8 HTML is the preferred format** because it can be directly parsed into searchable Tamil text without PDF/OCR extraction.

Project Madurai states that older works were converted from TSCII to Unicode/UTF-8, although some older formats may still exist on the website. :contentReference[oaicite:3]{index=3}

## Metadata

Metadata varies by individual work.

The catalogue provides:

- Work number
- Title
- Author
- Genre

Individual Unicode text pages may additionally provide:

- Author
- Work title
- Literary classification
- Thinai
- Turai
- Poetic form
- Verse/line numbering
- Acknowledgements
- E-text preparation information
- Proof-reading information
- Source/edition information
- Project Madurai attribution

For example, individual Sangam works can contain literary metadata such as thinai, turai, poetic form, and total number of lines. :contentReference[oaicite:4]{index=4}

## Text structure

Project Madurai is primarily a collection of **full literary texts**, rather than a standardized record-based linguistic corpus.

A typical Unicode HTML text contains:

1. Work title
2. Author information
3. Project/edition information
4. Acknowledgements
5. Literary metadata where available
6. The actual Tamil literary text
7. Verse/section/line numbering where applicable
8. Project Madurai attribution and distribution notice

The exact structure varies between works.

## Linguistic annotations

Project Madurai does not provide a standardized linguistic annotation layer across the entire collection.

Some individual works contain literary metadata such as:

- Thinai
- Turai
- Poetic form
- Verse numbers
- Section/chapter information

However, these should be treated as **work-specific metadata**, not as a corpus-wide annotation schema.

## POS information

No standardized POS annotation layer was identified.

Project Madurai should therefore not be treated as a POS-tagged corpus.

## Morphology

No standardized morphological analysis is provided.

Project Madurai primarily provides the original literary text. Morphological analysis should therefore be performed separately using resources such as ThamizhiMorph and Tamil WordNet's morphological data.

## License

Project Madurai describes itself as a voluntary project distributing its electronic texts freely.

Its distribution notice permits third-party distribution provided that the header page containing the Project Madurai logo and credit acknowledgements is kept intact, and it asks users to contact the project coordinators before online distribution. :contentReference[oaicite:5]{index=5}

The FAQ also explains that texts are selected for archiving when they are public-domain works or when the relevant author/rightsholder has given permission for electronic reproduction and free Internet distribution. :contentReference[oaicite:6]{index=6}

Therefore, சொல் AI should preserve the original Project Madurai attribution/header information and provenance when using these texts.

## சொல் AI usage

Highly relevant as a **large-scale literary text and occurrence-search layer**.

Potential uses include:

- Searching for occurrences of Tamil words
- Finding literary contexts
- Extracting surrounding passages
- Linking words to works
- Linking works to authors
- Filtering by genre
- Identifying verse/line numbers
- Expanding literary coverage beyond the smaller Sentamizh corpus
- Providing source provenance for literary examples

Project Madurai is particularly valuable because it provides access to complete literary texts rather than only pre-selected verses.

## Integration difficulty

**Medium to High.**

The individual Unicode HTML files are relatively accessible, but the collection is heterogeneous.

Main challenges include:

1. Different works have different HTML structures.
2. Metadata is not standardized across all texts.
3. Some older texts may use legacy encodings.
4. Verse/line numbering differs between works.
5. Some texts contain OCR-derived material requiring quality checking.
6. The catalogue contains multiple entries/parts under some work numbers.
7. A general parser will need work-specific normalization rules.

For the hackathon, we should therefore **not attempt to ingest all 1,090 entries**.

A small representative set should be selected first.

## Example record

A typical Project Madurai Unicode text contains metadata followed by the actual literary text.

Example structure:

```text
Title: பெரும்பாணாற்றுப்படை
Author: கடியலூர் உருத்திரங் கண்ணனார்

Genre:
பத்துப்பாட்டு

Metadata:
திணை :: பாடாண்திணை
துறை :: ஆற்றுப்படை
பாவகை :: ஆசிரியப்பா
மொத்த அடிகள் :: 500

Text:
அகலிரு விசும்பிற் பாயிருள் பருகிப்
...

## Observations

1. Project Madurai is significantly larger in scope than the current Sentamizh corpus.

2. It provides approximately 1,090 catalogue entries in the Unicode Tamil works list.

3. It is primarily a **literary text repository**, not a linguistic annotation resource.

4. Unicode/UTF-8 HTML is the most useful format for சொல் AI ingestion.

5. The collection contains both ancient/classical works and later Tamil literary material.

6. Metadata quality and structure vary between individual texts.

7. Individual texts can contain valuable literary metadata such as author, genre, thinai, turai, poetic form, and verse/line numbering.

8. Project Madurai's distribution notice requires preservation of its header/credit information when redistributing its files.

9. The project explicitly distinguishes public-domain material from works included with permission from authors/rightsholders.

10. A complete ingestion of the entire collection is unnecessary for the hackathon MVP.

## சொல் AI relevance

**Very High — as the broader literary corpus layer.**

Project Madurai complements Sentamizh:

| Resource | Primary role |
|---|---|
| Thani Thamizh Akarathi | Dictionary meanings and lexical resources |
| Tamil WordNet | Lexical relations and supporting morphological data |
| ThamizhiMorph | Morphological analysis |
| Sentamizh | Structured literary context and annotations |
| Project Madurai | Large-scale full literary text corpus |

The combination allows சொல் AI to move from:

```text
Word
↓
Dictionary meaning
↓
Morphological analysis
↓
Literary occurrence
↓
Full surrounding context
↓
Work / Author / Genre / Period
↓
AI-assisted contextual interpretation

## Source

Official Project Madurai website:

https://www.projectmadurai.org/

Unicode works catalogue:

https://www.projectmadurai.org/pmworks.html

---

# 5. Secondary Resource Audits

---

# 5.1 Tamil Virtual Academy

## What is it?

## Available resources

## Format

## Metadata

## License

## சொல் AI relevance

## Source

---

# 5.2 Tamil Wiktionary

## What is it?

## Advertised size

## Measured size

## Format

## Metadata

## Definitions

## Semantic relations

## Morphology

## License

## சொல் AI usage

## Integration difficulty

## Example record

## Observations

## சொல் AI relevance

## Source

---

# 5.3 University of Madras Tamil Lexicon

## What is it?

## Advertised size

## Measured size

## Format

## Metadata

## Definitions

## Multiple meanings

## Semantic relations

## Morphology

## License

## சொல் AI usage

## Integration difficulty

## Example record

## Observations

## சொல் AI relevance

## Source

---

# 5.4 Other Tamil Dictionaries

Resources investigated:

-

## Findings

## License considerations

## சொல் AI relevance

---

# 5.5 Tamil POS / Tokenization Resources

Resources investigated:

-

## Findings

## License considerations

## சொல் AI relevance

---

# 5.6 Other Tamil Literary Corpora

Resources investigated:

-

## Findings

## License considerations

## சொல் AI relevance

---

# 6. Cross-Resource Comparison

This section will be completed after individual audits.

| Resource | Layer | Raw Size | Usable Size | Meanings | Relations | Morphology | Literature | License | Difficulty |
|---|---|---:|---:|---|---|---|---|---|---|
| Thani Thamizh Akarathi | Lexical | TBD | TBD | TBD | TBD | TBD | — | TBD | TBD |
| Tamil WordNet | Lexical | TBD | TBD | TBD | TBD | TBD | — | TBD | TBD |
| ThamizhiMorph | Morphology | TBD | TBD | — | — | TBD | — | TBD | TBD |
| Sentamizh | Corpus | TBD | TBD | — | — | TBD | TBD | TBD | TBD |
| Project Madurai | Literature | TBD | TBD | — | — | TBD | TBD | TBD | TBD |
| Tamil Virtual Academy | Mixed | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Tamil Wiktionary | Lexical | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| University of Madras Lexicon | Lexical | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

---

# 7. Coverage Analysis

To be completed after the சொல் Benchmark is created.

| Resource | Overall Coverage | Common | Literary | Polysemous | Inflected | Archaic | Modern |
|---|---:|---:|---:|---:|---:|---:|---:|
| Thani Thamizh Akarathi | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Tamil WordNet | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| ThamizhiMorph | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Combined | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

---

# 8. Morphological Evaluation

Test categories:

- Simple words
- Inflected nouns
- Inflected verbs
- Case-marked nouns
- Tense-marked verbs
- Person/number/gender variations
- Compound forms
- Complex forms

Example test words:

- வந்தார்கள்
- சென்றுகொண்டிருந்தான்
- மரங்களில்
- மனதினால்
- பாடுகின்றனர்

Results will be recorded after ThamizhiMorph inspection.

---

# 9. Literature Provenance

For every literary occurrence eventually indexed by சொல் AI,
we should preserve provenance wherever available.

Expected fields:

```text
word
lemma
passage
work
author
collection
chapter
section
verse
line
period
genre
source URL
source dataset

# 10. Phase 0 Conclusion

## Core Resources Selected

| Resource | சொல் AI Role |
|---|---|
| Thani Thamizh Akarathi | Lexical meanings and Tamil equivalents |
| Tamil WordNet | Lexical-semantic relations and supporting morphology |
| ThamizhiMorph | Morphological analysis |
| Sentamizh | Structured literary context and annotations |
| Project Madurai | Large-scale literary text corpus |

## Decision

The initial சொல் AI implementation will use these five resources as the
primary evidence sources.

No additional resource will be integrated during Phase 0 unless a specific
implementation gap is discovered.

Further resources may be evaluated later if required by the implementation
or evaluation results.

## Phase 0 Status

**COMPLETE**

The resource audit is now frozen and implementation can begin.