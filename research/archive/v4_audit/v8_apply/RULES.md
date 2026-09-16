# Evaluating the Evaluators — Current Rules (quick reference)

This is a **live, current-state** rules document — it reflects what the rules ARE right now, not the
history of how they got there (that history lives in `CODEBOOK_v7.md`'s numbered sections and in
`changelog.csv`). Updated immediately whenever a rule changes, added, or is clarified.

---

## 1. Scope (who counts as an evaluator, what counts as a report)

- `Scope = government-AISI`: a real government AI Safety Institute (or equivalent — e.g. EU AI Office,
  genuinely functionally equivalent per its International Network/NAAIMES membership) is the author,
  co-author, or commissioner of the work. Sponsorship/funding/consortium-membership alone does NOT qualify
  (see the Apollo/AISIC, DSRI, and Bengio-report corrections).
- `Scope = third-party-evaluator`: a real, active organization that itself runs empirical AI model
  evaluations (METR, Apollo, Redwood, Shanghai AI Lab, etc.) — no government AISI involved.
- `Scope = company-self-report`: a company evaluating its own model.
- **Hard drop** (not in the dataset at all): reports naming no evaluating agency; reports authored by
  none of {government AISI, evaluation lab, company} (e.g. an independent academic panel, even if
  government-commissioned — see the Bengio "International AI Safety Report" removal); private/unpublished
  evaluations; non-English-only outputs (unless a verified English excerpt exists); fabricated/conflated/
  wrong-sourced content that can't be corrected.

## 2. What earns a row (`Eval? = yes`)

A real, concerning, empirical finding on ANY identifiable subject — a company, a named model, an
open-source/academic tool with no corporate owner, a framework, a process. "No accountable company" is
never a reason to omit a real finding — it only affects `Action Trackable?` (below), never `Eval?`.

## 3. What earns the main accountability table (`Action Trackable? = yes`)

ALL of: (1) `Eval? = yes`, (2) names a specific company/model the response is attributable to (anonymised
= no), (3) demonstrates a concerning result a company response is reasonable to expect. **This does NOT
depend on `Scope`** — a third-party finding with a real, verified company response counts exactly the same
as a government-AISI finding (see the Apollo Claude-4-scheming rows, which grew the table from 50→52 despite
zero AISI involvement). Excluded even when (1)+(2) hold: reassuring-null results, benchmark-score/
relative-uplift findings, comparative rankings, capability-trend/forecasts, methodology/tooling studies
where models are instruments not subjects, company self-classifications, non-frontier models, too-recent
findings.

## 4. One-finding-per-row (split vs. combine)

- **Combine** into one row if the finding is fundamentally ONE technique/phenomenon/benchmark demonstrated
  comparatively across models (e.g. one jailbreak method tested on 5 models; one benchmark's comparative
  ranking).
- **Split** into separate rows if the models represent genuinely DISTINCT, unrelated incidents/scenarios
  that happen to appear in the same report (e.g. two different companies' unrelated payment-handling
  bugs).
- **Reframe** (don't split, don't combine) when one model is the true subject and others are only cited as
  comparators — move comparators from `Models / Systems` into `Notes` as `[Report tested: …]`.

## 5. Column-specific rules

- **Models / Systems**: the finding's actual subject(s) only. Comparators → Notes. "anonymised" if the
  source doesn't name it.
- **Source URL**: the primary source of the FINDING — prefer the evaluator's own paper/report over a
  company's summary of it, where both exist. If the SAME evaluator publishes both a blog and a companion
  academic paper for one finding, prefer the paper (Scholar-indexable) — **but only swap to it if the
  row's `Key Quote` is blank.** If the quote was already independently verified against the blog, leave
  the blog as Source URL and note the companion paper in `Notes` instead — swapping could invalidate a
  verified quote if the paper phrases the same finding differently. Always check first whether the
  "found" companion paper is genuinely the same finding, or a different (broader/narrower/later) paper by
  the same team that happens to share a topic — don't merge or swap on title-similarity alone (see the
  LatticeFlow COMPL-AI-framework-vs-DeepSeek-application case in `CODEBOOK_v7.md` §16).
- **Key Quote**: must be EXACT, character-for-character verbatim from the cited Source URL. No paraphrase,
  no splicing two sentences into one, no borrowing a quote from a different document than the one cited. If
  no verified verbatim text exists, leave blank — never guess or reconstruct.
- **Publication Date**: the source's own stated date. Never a placeholder, never a time component.
- **Domain**: multi-select, controlled vocabulary only (see full list in `CODEBOOK_v7.md` §5).
- **Channel A/B (Company/Policy response)**: company's own primary source only; news quoting a company
  doesn't count. Response Date may legitimately precede Publication Date (pre-deployment evals). A Policy
  Response must be a real, checkable government/regulatory action (a bill, hearing testimony, an agency
  statement, a consultation response) that references THIS finding or its underlying capability — not a
  bill/page that happens to exist on a related topic but never mentions the finding when actually fetched,
  and not the finding's own primary source restated as if it were an independent action.
- **Channel C (Traction/Media/Academic Citations/Social/Verbatim)**: **opportunistic, not exhaustive.** A
  populated cell means "found during construction"; blank means "none found," never "confirmed none
  exists." Every citation claim must carry its own verified inline URL. The finding's own paper citing
  itself is circular and excluded — a genuine third-party citation only. This also applies at the
  version level: a citing entry that turns out to be a different version (preprint vs. published,
  v1 vs. v2) of the *same* paper is NOT a third-party citation — check the underlying paper identity,
  not just the listed title/venue, before counting it.
- **A source can pass an individual fetch check yet still fail independence at the source-*type* level.**
  (Caught 2026-07-19: Resultsense.com's individual articles were live, real, and accurately quoted the
  underlying AISI findings — but the site's own About page discloses "We do not claim to produce original
  journalism," and its AISI articles are bylined "Analysis...Resultsense [via AI Security Institute]," i.e.
  republished blog summaries, not independent reporting. Every citation of it across the dataset was
  rejected.) **`resultsense.com` is excluded dataset-wide as a Media Outlets / Channel C source** — it is
  not independent of the evaluator it's summarizing. Before counting any outlet as independent media, check
  what kind of source it actually is (original reporting vs. syndication/republication/research-partner
  mirror/company's own blog), not just whether the specific page resolves and says the right thing.

## 6. Three different kinds of verification — don't let one substitute for another

- **Evidentiary verification**: is the *evidence* real — does the quote match the source, does the URL
  resolve, does the date line up. This was checked repeatedly across §12/§16/§17/§18.
- **Classification-consistency verification**: does a row's own *classifications* agree with each other —
  e.g. does `Severity=C2` ("not, by itself, alarming" per §4) ever coexist with `Action Trackable?=yes` (a
  row claiming to be alarming enough to warrant a company response)? This was NEVER checked, despite being
  flagged by Stephen Casper in the original v3 review and logged as a "deferred severity re-vote" before
  this entire project began. When it was finally run (2026-07-19), it found 6 main-table rows with exactly
  this contradiction — see `CODEBOOK_v7.md` §20.
- **Accuracy-and-specificity verification**: even when a quote is evidentially real and a row's own labels
  are internally consistent, the *Finding text itself* can still (a) overstate/misrepresent what the source
  says (e.g. "all five models" when the source shows one exception), (b) add unsourced interpretive/policy
  framing the source never states, (c) misattribute a number or mechanism from a sibling finding, or (d) be
  so generic it conveys no checkable claim at all ("VAGUE"). A 321-row sweep of Block B/C on 2026-07-19
  found ~35 such rows — see `CODEBOOK_v7.md` §22. **Doing a lot of one kind of verification does not
  substitute for the others — check all three, periodically, not just when a specific row happens to catch
  someone's eye.**

## 6a. Evidentiary standard (applies everywhere)

- **Never construct a URL from an API/database ID and assume it resolves.** (Caught 2026-07-18: 19 rows'
  `Academic Citations` links were built as `semanticscholar.org/paper/{paperId}` from the Semantic Scholar
  API's response, never live-tested — the page returns HTTP 202/empty to any non-browser client even with
  the fully correct title-slug format. Fixed by linking the actual API endpoint that was used to fetch the
  data, which is confirmed fetchable.) Every URL added to the dataset — not just ones copied from a source
  — must be independently test-fetched before being trusted, including URLs *I* build.
- **A swap is not verified just because its precondition was checked.** (Caught 2026-07-18: 84 Source URLs
  were swapped to companion papers after checking only "is Key Quote blank" — 36 of the 93 rows touched
  turned out to have a real problem the swap logic never checked for: wrong paper matched entirely, paper
  covering different models than the finding claims, or a date that's chronologically impossible against
  the *new* source. Reverted 15, fixed 20 dates, fixed 1 quote.) After ANY swap — URL, date, quote, whatever
  — re-verify the row's full content against the new state, not just the one condition that justified
  making the swap in the first place.
- Every number in a Finding must be checked against the source.
- Every Key Quote must be independently verifiable at the cited URL, not assumed correct because an earlier
  pass added it.
- **A claim of "confirmed working" must mean independently re-tested, not "the API returned data once."**
  Rate-limited/bot-gated services (Semantic Scholar's website, RAND, robustintelligence.com, etc.) can
  return real data on one call and fail on the next — say so explicitly rather than generalizing from a
  single success.
- When something can't be verified (broken URL, rate-limited API, no confirmable replacement), flag it
  honestly (lower `Confidence`, note in `Notes`) rather than guess or fabricate.
- **A new-row ID collision may mean a genuine duplicate or an incomplete existing row — check before
  picking a new ID.** (Caught 2026-07-19: adding new rows from a deep-read sweep, two new Finding IDs
  collided with existing rows from the same report. One collision was a truly unrelated existing finding —
  gave the new content a fresh ID. The other collision was a pre-existing row that had recorded only
  "tested against X" with no result ever filled in — the new finding *completed* that placeholder instead
  of becoming a parallel duplicate row.) When an ID collision fires, read the existing row in full before
  deciding whether to rename, merge, or complete it.
- **An exception to a rule needs its own justification tied to *this specific* case, not evidence of a
  general pattern.** (Caught 2026-07-19: `JOINT-2024-12-BIO2` was kept in the accountability set as an
  exception to the C2-exclusion rule because "a company response existed" — but the response was only
  evidence an evaluation *happened*, not a substantive reply to *this* finding. A response justifies an
  exception only when it's clearly about the specific finding in question.)
- **A Finding's own prose must not overstate, editorialize beyond, or misattribute what its source says —
  even when the underlying quote/URL/date are all individually correct.** (Caught 2026-07-19, ~35 rows: (a)
  generalizing a partial result to "all"/"tested models" when the source names an exception — e.g. one model
  underperformed but the Finding said "all five"; (b) tacking on unsourced interpretive/policy framing the
  source never states — e.g. "national security implications/export-control policy," a specific Act of
  Parliament causally attributed to a page that never mentions it, "first-ever"/"minimal traction" claims
  with no textual support; (c) borrowing or misattributing a specific number/mechanism from a *different*,
  similar-sounding finding in the same report — e.g. a "1.5x" figure or a "git history" mechanism that
  actually belongs to a sibling row; (d) a Key Quote that is real but was pasted from a *different* row in
  the same report than the one it's attached to — check that the quote is not just verbatim-real but
  verbatim-real *for this specific row*.) Every number, mechanism, and interpretive clause in a Finding needs
  its own textual support in the cited source — "the source is legitimate and the quote is real somewhere in
  it" is not sufficient.
- **"Vague" is a real defect distinct from "inaccurate."** A Finding can be 100% evidentially correct and
  still fail to convey a specific, checkable claim (generic restatements like "cooperation with native
  speakers enables more balanced testing" with no concrete detail). When a source's own page has no new
  specifics beyond a finding already captured elsewhere with real numbers, the vague restatement should be
  dropped as non-additive rather than kept as a second, weaker row for the same fact.
- **A stray audit/editorial note can end up saved into the `Finding` field by mistake and needs to be caught
  like any other row** — nothing about the CSV format distinguishes a real finding from a process note typed
  into the wrong cell. (Caught 2026-07-19: `UKAISI-2025-09-GOV2`'s Finding field was literally a leftover
  verification note, not a finding — dropped.)

## 7. Notes field

Reserved for reader-facing context only: comparator flags (`[Report tested: …]`), provenance/confidence
caveats, classification rationale. Process/construction audit-trail entries (quote fixes, scope fixes,
splits) do NOT belong here — that's what `changelog.csv` is for. (Notes was cleaned of ~38% bloat from
stacked process tags on 2026-07-17 for exactly this reason.)

---

*Last updated: 2026-07-19 (Channel B/C robustness sweep). Maintained turn-by-turn as rules change — no separate "background agent" process
does this; there is no tool capability for a subagent to passively watch an ongoing conversation, so this
file is kept current directly, the same way `CODEBOOK_v7.md` has been throughout this project.*
