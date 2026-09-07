#!/usr/bin/env python3
"""Build the publication-ready Tier A table.

V13 stays the audit copy: it keeps the search logs, the dated re-run markers and the coding
rulings, which are what make the dataset checkable. This script derives the table that goes in
the paper — the same rows and the same analytical columns, with the internal apparatus removed.

Three kinds of removal, and nothing else:
  1. columns that exist only for internal working or that carry no information on Tier A
  2. bracketed coder notes that log process (re-runs, provenance, moves) - editorial
     insertions inside quotations, e.g. "[Claude Mythos 5]", are KEPT, since deleting them
     would alter a verbatim
  3. search apparatus inside evidence cells (query strings, API names, HTTP statuses,
     dates checked) and the many spellings of "nothing found", normalised to one form
"""
import sys, re, csv, collections
sys.path.insert(0, '/Users/kunalsingh/MATS/Research/AISI_Evals/scripts')
import dataset_source as ds
import openpyxl

DROP = {
    'Sources Checked (channel A)':  'internal search log: five-source battery, dated re-runs, coding rulings',
    'Human':                        'mirrors the ensemble on every row; publishing it would imply human validation that has not been done',
    'Eval? (trackable)':            'constant "yes" on Tier A - no information',
    'Action Trackable?':            'constant "yes" on Tier A - no information',
    'Tags':                         'internal keywording, applied to 168 of 231 rows',
}

# bracketed notes that log process rather than clarify a quotation
NOTE = re.compile(r'\[\s*(?:'
    r'ADDED\b|RE-?RUN\b|CHANNEL\s+[ABC]\b|Channel\s+[ABC]\s+(?:re-run|searched|battery)|'
    r'Moved from|moved from|Tier justification|publication_date|Character-exact from|'
    r'Verified character-exact|repointed|superseding'
    r')[^\]]*\]', re.I)

# leading search apparatus in evidence / coverage cells
APPARATUS = [
    re.compile(r'^Coverage index:\s*[^.]*?\([^)]*\)\.\s*', re.I),
    re.compile(r'^[^.]*?\b(?:Graph API|RSS|Algolia API)\b[^.]*?\b(?:returned HTTP \d+|queried|checked)\b[^.]*?\.\s*', re.I),
    re.compile(r'^Article URLs are Google News redirects[^.]*\.\s*', re.I),
    re.compile(r'\s*\((?:checked|queried|as of|window)\s+20\d\d-\d\d-\d\d[^)]*\)', re.I),
    re.compile(r'\s*\([^)]*\bAPI\b[^)]*checked[^)]*\)', re.I),
    # leading "<source> (query params, checked <date>):" provenance stamps
    re.compile(r'^(?:OpenAlex|Google Scholar|Semantic Scholar|Hacker News|arXiv|Google News|'
               r'Crossref|Reddit|X/Twitter|LessWrong)\s*\([^)]*\)\s*[:,-]\s*', re.I),
    # any remaining parenthetical whose whole content is search apparatus
    re.compile(r'\s*\((?:[^)]*?(?:checked|queried|from_publication_date|rate-limited|no key|'
               r'HTTP \d{3}|Algolia|Graph API|RSS)[^)]*?)\)', re.I),
    re.compile(r'^[^.:]{0,40}\b(?:re-?searched|battery executed)\b[^.]*\.\s*', re.I),
]
# every spelling of "we looked and found nothing"
NOTFOUND = re.compile(r'^(?:Not found|None located|No coverage located|None found|Not located)\b.*$', re.I | re.S)

# Cleaning is whitelisted, never blanket. Anything holding a quotation, a code, a date or a
# number is left byte-identical: a first pass stripped the minus sign off 11 negative `Lag (days)`
# values and an em-dash off the end of a Channel C quote, because it trimmed trailing punctuation
# on every column.
NEVER = ('Finding ID','Report ID','Institution','Institution Type','Report Title','Publication Date',
         'Domain','Models / Systems','Access Type','Source URL','Finding','Finding Quote',
         'Severity (C1/C2) majority','Sonnet5 vote','GPT-5.5 vote','Gemini3.1 vote','Attribution',
         'Channel A Verbatim','Response Date','Lag (days)','Action Level','Policy Level',
         'Channel C Verbatim','Proportionality','Finding Type','Scope')
# process notes stripped from these (prose and evidence fields only)
NOTE_COLS = ('Company Response','Policy Response','Channel B Verbatim',
             'Channel A Evidence','Channel B Evidence','Media Outlets',
             'Academic Citations','Social Highlights')
# search apparatus + "nothing found" normalisation applied to these
APPARATUS_COLS = ('Media Outlets','Academic Citations','Social Highlights',
                  'Channel A Evidence','Channel B Evidence')

def clean(col, v):
    if not v or col in NEVER:
        return v or ''
    if col in NOTE_COLS:
        v = NOTE.sub('', v)
    if col in APPARATUS_COLS:
        if NOTFOUND.match(v.strip()):
            return 'None located'
        for p in APPARATUS:
            v = p.sub('', v)
    v = re.sub(r'\s*;\s*;\s*', '; ', v)
    v = re.sub(r'\s+', ' ', v).strip()      # whitespace only - no punctuation trimming
    return v

R = ds.rows()
tier = lambda d: 'A' if d.get('Eval? (trackable)','').lower()=='yes' and d.get('Action Trackable?','').lower()=='yes' else ('B' if d.get('Eval? (trackable)','').lower()=='yes' else 'C')
A = [d for d in R if tier(d)=='A']
cols = [c for c in A[0] if c not in DROP]

stats = collections.Counter()
out = []
for d in A:
    row = {}
    for c in cols:
        before = d.get(c,'') or ''
        after = clean(c, before)
        if after != before:
            stats[c] += 1
        row[c] = after
    out.append(row)

wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'TierA_paper'
ws.append(cols)
for r in out: ws.append([r[c] for c in cols])
ws.freeze_panes = 'A2'
wb.save('/Users/kunalsingh/MATS/Research/AISI_Evals/paper/TierA_paper_table.xlsx')
with open('/Users/kunalsingh/MATS/Research/AISI_Evals/paper/TierA_paper_table.csv','w',newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(out)

print(f"Tier A publication table: {len(out)} rows x {len(cols)} columns")
print(f"\ncolumns dropped ({len(DROP)}):")
for k,v in DROP.items(): print(f"   {k:30s} {v}")
print(f"\ncells cleaned:")
for k,v in stats.most_common(): print(f"   {v:4d}  {k}")
print(f"\n   total {sum(stats.values())} cells changed")
