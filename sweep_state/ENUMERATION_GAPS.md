# Enumeration gap diagnosis — 2026-08-14

20 reports present in `v10.csv` were never enumerated by the sweep. Each was traced to the
publication surface it lives on and compared against `cached_enumerations.json`. They are not
20 one-off misses — they are **seven classes of enumeration failure**, each of which will have
cost other reports that are *not* in v10 and therefore invisible.

## A. Whole site sections never paginated  (6 reports)

| Venue | Sections enumerated | Section MISSED | Reports lost |
|---|---|---|---|
| **UK AISI** | `/blog` (94), `/research` (58) | **`/work/*`** | `UKAISI-2024-05c` (fourth progress report) |
| **Holistic AI** | `/blog`, `/papers`, `/news`, `/learn`, `/newsletters`, `/press-release` | **`/red-teaming/*`** | `HOLISTIC-2025-02`, `-02b`, `-02c`, `-2025-03` (Grok-3, DeepSeek R1, Claude 3.7, ChatGPT 4.5 audits) |
| **US CAISI** | `nist.gov/news-events` (35), `/blogs`, `/aisi` (1) | **`nist.gov/caisi/*`** | `USCAISI-2025-11` |

US CAISI is the sharpest case: the org was **renamed** from US AISI to CAISI, and the enumeration
kept crawling the old `/aisi` path — which now holds 1 item — while the live `/caisi` section was
never touched.

## B. Second domain never added to the venue  (2 reports)

**CIP** enumerated `cip.org`, `blog.cip.org`, `globaldialogues.ai` — but **not `weval.org`**, the
product domain where the evaluation cards live. Lost: `CIP-2025-08-OPUS41`, `CIP-2025-08-GPT5`.

## C. Pagination stopped early  (1 report)

**Cisco**: `blogs.cisco.com/security` yielded 29 items but `blogs.cisco.com/ai` only 6 — the AI
blog was not paginated to the end. Lost: `CISCO-2025-11`.

## D. PDF assets linked from pages but not indexed  (2 reports)

`palisaderesearch.org/assets/reports/*.pdf` and a UK AISI Webflow CDN asset. The enumeration lists
index entries; report PDFs hanging off a post are invisible to it.
Lost: `PALISADE-2025-08-CABLE`, `UKAISI-2026-04d`.

## E. arXiv not reachable from the org's own index  (4 reports)

The protocol reaches arXiv only via each org's publication list plus citation-chasing. Where the
org does not list its own arXiv output, the paper is missed. Lost: `UKAISI-2025-11`
(CTRL-ALT-DECEIT), `UKAISI-2025-11a`, `TSINGHUACOAI-2023-09-SAFETYBENCH`,
`SHANGHAIAILAB-2026-01-OPENRT`. Note Tsinghua's enumeration *does* include 56 `arxiv.org/abs`
entries, so coverage is partial, not absent — which is harder to detect.

## F. Joint work published only on the partner's domain  (2 reports)

`JOINT-2025-09-CAISIUPDATE` lives on `openai.com`; `UKAISI-2025-07-CYB1` on `peren.gouv.fr`.
Enumerating the lead evaluator's site never finds them.

## G. NOT an enumeration failure — a v10 data defect  (3 reports)

`UKAISI-2024-01` → `time.com`, `KAISI-2025-12-SOC1` → `en.wedoany.com`,
`AUAISI-2026-07` → `cryptobriefing.com`. These rows cite a **news article** as Source URL.
Codebook §9 col 10 requires the evaluator's own report where one exists, and §10 states news is
never admissible as primary. No sweep of the evaluator's site could ever find them.
**Action: re-source each to the evaluator's own publication, or drop the row.**

## Fix list, in priority order

1. Re-enumerate `aisi.gov.uk/work/*`, `holisticai.com/red-teaming/*`, `nist.gov/caisi/*`
2. Add `weval.org` to the CIP venue; re-paginate `blogs.cisco.com/ai`
3. Add a PDF-asset sweep (follow in-page links to `.pdf` on roster domains)
4. Add an arXiv author/affiliation query per roster org, not just the org's own index
5. Cross-domain rule: for joint exercises, enumerate every named party's domain
6. Re-source the 3 news-cited rows (G) — data repair, not enumeration

**Until 1–5 are done, the corpus recall is unknown and the "enumeration is COMPLETE" claim stays
withdrawn.** These 20 are the misses that happened to be visible because v10 already contained
them; the same seven classes will have dropped an unknown number of reports v10 never had.
