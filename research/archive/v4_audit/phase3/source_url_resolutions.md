# Source URL policy resolution (rule: Source URL = evaluator's own report when it exists)

Audit: 21/67 finalized rows cite non-institute domains. Web-verified resolutions (2026-07-15):

| Rows | Current source | Evaluator publication exists? | Action |
|---|---|---|---|
| 5 | AISI blog (anonymised) | YES — arXiv 2504.18565 names Claude 3.7 Sonnet | RE-SOURCE to paper |
| 54,55,63,64 | anthropic.com Claude 4 system card | YES — Apollo blog 2025-06-19 "more-capable-models-are-better-at-in-context-scheming" (covers Opus-4-early: fabricated legal docs, self-propagating scripts, advise-against-deployment; released Opus 4 cut scheming ~50%) | RE-SOURCE rows 55/63 (Apollo findings) to Apollo blog; rows 54/64 are Anthropic self-reports (see eligibility) |
| 22,23,24,32,40,46,47,48 | cdn.openai.com GPT-5.3-Codex system card | NO — neither UK AISI nor CAISI published on GPT-5.3-Codex (AISI's per-model OpenAI series starts with GPT-5.5, 2026-04-30) | KEEP system card as primary source; add codebook clause for company-published institute findings |
| 65,66,67,68 | anthropic.com safeguards blog | PARTIAL — AISI companion post 2025-09-13 exists but has NO findings (defers to company blogs); NIST 2025-09-25 same | KEEP Anthropic blog; cite AISI/NIST posts as corroboration |
| 20,37,39 | openai.com us-caisi-uk-aisi-ai-update | PARTIAL — same AISI 2025-09-13 + NIST 2025-09-25 general posts, no findings | KEEP OpenAI blog; cite institute posts as corroboration |
| 21,36 | storage.googleapis.com Gemini 3 Pro FSF report | NO — no UK AISI/Apollo/Vaultis/Dreadnode publication on Gemini 3 Pro exists | KEEP DeepMind PDF; re-label Report ID (currently 'UKAISI-2025-11' mislabels a DeepMind publication) |

Codebook clause to add: "Where the evaluating institute published no standalone report, the company
document that first publishes the institute's findings is the admissible primary source; tag the row
company-published so the circularity (finding-source = response-source) is explicit and countable."
