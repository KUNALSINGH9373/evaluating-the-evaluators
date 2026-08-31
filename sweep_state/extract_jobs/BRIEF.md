# Extraction brief — "Evaluating the Evaluators" v10

You are extracting **findings** from evaluation reports into the dataset's 40-column schema.
Work only on the venue worklist you were given. Do not touch any other file.

## Input

Your worklist CSV: `venue, item_title, url, publication_date, cached_text_path`.
`cached_text_path` is already-extracted plain text — **use it**. Only fetch the URL if that column
is empty (then: `curl -sL --max-time 25 -A "Mozilla/5.0" -o /tmp/x.bin URL` and, for a PDF,
`pdftotext -q /tmp/x.bin /tmp/x.txt`). Never trust WebFetch for PDFs — it silently returns
plausible-sounding wrong answers on this corpus.

## What counts as a FINDING (§2) — all three must hold

1. **Asserted by the evaluator** — not a summary of someone else's work, not a comparator cited in passing.
2. **Evidence-backed in that report** — a measured result, observed behaviour, or documented process
   fact. Opinions, recommendations, forward-looking plans and product announcements are NOT findings.
3. **Independently codeable** — it would warrant its own response.

Qualifying kinds: empirical model findings (**including reassuring nulls**), methodology/tooling
findings, governance/process findings.

## One finding per row — split & club (§5, §5.1)

- **Different companies never share a row.** If a report reports the same result for Claude and
  GPT-5, that is two rows.
- **Club** findings that would draw the *same* response from *one* company.
- **Split** findings that warrant distinct responses (capability vs safeguard failure; different domains).
- **Comparators/baselines are never rows** → put them in `Notes` as `[Report tested: …]`.
- Separate reports are always separate rows, even for the same benchmark family.

## Tier (§4) — set two columns

| Tier | `Eval? (trackable)` | `Action Trackable?` | Meaning |
|---|---|---|---|
| A | `yes` | `yes` | Empirical model finding + names a specific company/model + concerning, so a response is reasonable to expect |
| B | `yes` | `no` | Concerning but no accountable party: anonymised models, reassuring nulls, non-frontier, capability trends, comparative rankings |
| C | `no` | *(blank)* | Not an empirical model finding — methodology, framework, governance |

Tier A condition 3 **excludes**: reassuring nulls, benchmark scores with no dangerous threshold
crossed, inconclusive results, comparative rankings, capability trends, models used as instruments
of a methodology study, company self-classifications, non-frontier models.

## Scope (§1)

`government-AISI` if a government AI Safety Institute authored or co-authored; otherwise
`third-party-evaluator`. Your venues are third-party unless a government AISI is a named co-author.

## Columns you must fill

`Finding ID` (`PREFIX-YYYY-MM-DDDn`; DDD ∈ JAI CYB BIO ALI AUT SOC HUM GOV), `Report ID`
(`PREFIX-YYYY-MM`, same for all findings from one report), `Institution` (the **evaluating** body),
`Institution Type`, `Report Title `  *(note the trailing space)*, `Publication Date` (`YYYY-MM-DD`
or `YYYY-MM`, source-verified), `Domain` (Cyber/Bio-Chem/Alignment/Jailbreaks/Autonomy/Societal/
Human Influence + governance sub-types; never blank), `Models / Systems` (the **subject** models
only; `anonymised` if unnamed), `Access Type` (Pre-deployment/Post-deployment/Mixed/Aggregate/N/A),
`Source URL`, `Finding` (1–2 sentences, every number verified against the text, no overstatement),
`Finding Quote` (**verbatim** from the report), `Eval? (trackable)`, `Action Trackable?`,
`Finding Type` (exactly one of capability-finding/methodology/capability-trend/governance, plus
modifiers: anonymised-model, reassuring-null, company-self-report, non-frontier, company-published),
`Tags`, `Scope`, `Notes`.

**Leave blank:** all severity columns, all Channel A/B/C columns, `Attribution`, `Action Level`,
`Proportionality`, `Lag (days)`. Put `TODO severity ensemble + Channel A/B/C.` at the end of `Notes`.

## Hard rules — these are where mistakes happen

- **Never invent a number or a quote.** Every figure in `Finding` must appear in the source text.
  If you cannot find a measured result, the row is Tier B or C, or not a finding at all.
- **Benchmark usage is not a finding by the benchmark's author.** "We evaluated on 350 questions
  from SecureBio" is the publisher's finding, not SecureBio's.
- If a page is a **placeholder** (lorem ipsum), a **product announcement**, a **podcast**, a
  **newsletter summarising others' work**, or an **administrative document**, record it in your
  report as excluded — do not create a row.
- If the cached text is nav-only or unreadable, mark it `FETCH-FAILED` in your report; do not guess.

## Output

Write **one CSV** to `/Users/kunalsingh/evaluating-the-evaluators/sweep_state/extract_jobs/out_<key>.csv`
with exactly this header row (copy it verbatim):

```
Finding ID,Report ID,Institution,Institution Type,Report Title ,Publication Date,Domain,Models / Systems,Access Type,Source URL,Finding,Finding Quote,Severity (C1/C2) majority,Sonnet5 vote,GPT-5.5 vote,Gemini3.1 vote,Attribution,Company Response,Channel A Verbatim,Response Date,Lag (days),Channel A Evidence,Action Level,Sources Checked (channel A),Policy Level,Policy Response,Channel B Verbatim,Channel B Evidence,Media Outlets,Academic Citations,Social Highlights,Channel C Verbatim,Proportionality,,Eval? (trackable),Action Trackable?,Finding Type,Tags,Scope,Notes
```

Then reply with a short report: rows produced, reports covered, reports excluded and why, anything
you could not read, and any judgement call you were unsure about. Be explicit about uncertainty —
a flagged doubt is far more useful than a confident guess.
