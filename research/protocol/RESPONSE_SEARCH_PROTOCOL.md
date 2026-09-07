# Response & Uptake Search Protocol (Channels A, B, C) — v1.0, 2026-09-07

## Provenance — read this first

**This document is a post-hoc reconstruction, not a pre-registered prompt.** It is written to be
honest about that. `SEARCH_PROTOCOL.md` governed finding *discovery* and was versioned before the
sweeps ran; `severity/severity_prompt_v1.0_FROZEN.txt` was frozen before the severity ensemble
ran. The response search had neither. It was carried out by AI agents working interactively,
against the source classes fixed in rulebook §8/§9/§10, with `scripts/fetch.py` as the shared
retrieval layer and a dated prose log written into `Sources Checked (channel A)` /
`Channel B Evidence` on every row.

The battery below is reconstructed from those logs, which are the primary record and are published
with the dataset. It should be cited as the search *method*, and described as reconstructed. It
must not be described as a frozen prompt, and any claim of exact reproducibility for the searches
already performed would be false: the agents' individual queries were not all captured, and some
searches ran against engines that rate-limited or CAPTCHA-gated them (50 Tier A logs record a
block or budget limit; 58 record a re-run after one).

From v1.0 forward this file is the instruction of record. Future sweeps must follow it verbatim
and log deviations.

## 1. Channel A — company response

Five sources, in order. A `None` requires all five attempted and a dated log; §8: *"A no-response
classification requires a dated search log through the cutoff."*

1. The accountable developer's own newsroom, blog, or research index.
2. Subsequent model and system cards **in the affected model family**, through the cutoff.
3. The developer's safety, responsibility, or deployment-safety hub
   (e.g. `deploymentsafety.openai.com`).
4. Official developer accounts and statements.
5. Open web, used **only to locate a company primary source** — never as the response itself
   (§8b). Query shape: developer name + evaluator name + the finding's specific claim.

**Admissibility (§8b).** Only the company's own primary document counts. A standing policy that
predates the finding is not a response. Third-party reporting that a company responded is not a
response. Work by the company on the same general topic that does not reference the finding is
not a response — recorded in the log as *considered and rejected*, with the reason.

**One accountable company per row (§5).** Where a finding was split by company, each row gets its
own battery. Inheriting a sibling's battery is not permitted: the 2026-09-07 Transluce split found
a battery that had covered OpenAI alone standing behind rows for Meta and Anthropic.

**Earned vs unearned `None`.** If any of the five is blocked (403, CAPTCHA, quota, rate limit),
the `None` is **not earned**. Re-run the blocked source through the `fetch.py` ladder — direct GET
with full browser headers, then PDF/HTML extraction, then the nearest Wayback snapshot — and
record the re-run. A log that records a block with no re-run marks an open item, not a result.

## 2. Channel B — policy uptake

Official parliamentary, congressional, agency, legislative and regulatory sources, across all
three jurisdictions in scope. Query shape: evaluator name, report title, and report ID. General
policy activity on the same topic does not qualify without an explicit reference to the finding,
report, or evaluator. A row with no completed Channel-B search is **missing, not negative**.

## 3. Channel C — independent coverage

Independent media, academic citations, and notable public discussion. Named engines used to date:
the Google News index (verified by direct fetch where the outlet permits), Semantic Scholar by
paper ID, Google Scholar author pages, and web.archive.org for paywalled or moved items. The
evaluator's own publicity and the company's own promotion are not independent coverage.
DuckDuckGo html/lite endpoints were rate-limited and CAPTCHA-gated in this environment; X/Twitter
and Reddit were not systematically accessible. Where a channel could not be searched, the log
says so rather than recording a zero.

## 4. Retrieval layer

All fetching goes through `scripts/fetch.py`, so that a blocked source is never recorded as an
absence. Its ladder exists because a prior pass logged "congress.gov 403" against 172 findings and
concluded the US jurisdiction was unsearchable — the search pages 403 while the documents return
200.

## 5. What is logged, per row

Date of search; which of the five sources were attempted; what was found or not found; any block
and whether it was re-run; and for a rejected candidate, why it was inadmissible. These logs are
the evidence for every `None` in the dataset and are published in full.

## 6. Known limitations of the searches already performed

- No frozen prompt existed, so exact query-level replication is not possible.
- Depth of recording is uneven: 119 of 233 Tier A logs enumerate their sources explicitly; 46 name
  the five-source battery by name.
- 14 of the 114 `no response` rows in the headline population record a block with no documented
  re-run. These are open items, listed in the rulebook changelog.
- No independent replication of the response search has been run, so the dataset carries no
  measured recall bound. A blind re-search of a stratified sample would convert "searched
  thoroughly" into a number, and is the single most useful addition to this protocol.
