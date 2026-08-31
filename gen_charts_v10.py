"""Generate v10 report charts: static matplotlib PNGs, light background, large fonts."""
import csv, re
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

OUT = '/Users/kunalsingh/Desktop/v10_charts'
CSV = '/Users/kunalsingh/evaluating-the-evaluators/v10.csv'

rows = list(csv.DictReader(open(CSV)))

# ---- style: light background, large fonts (noticeably bigger than v9), thin clean marks ----
plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'savefig.facecolor': 'white',
    'font.family': 'sans-serif',
    'font.sans-serif': ['Helvetica Neue', 'Arial', 'DejaVu Sans'],
    'font.size': 16,
    'axes.titlesize': 22,
    'axes.titleweight': 'bold',
    'axes.labelsize': 17,
    'xtick.labelsize': 15,
    'ytick.labelsize': 15,
    'legend.fontsize': 15,
    'axes.edgecolor': '#333333',
    'axes.linewidth': 1.0,
    'text.color': '#1a1a1a',
    'axes.labelcolor': '#1a1a1a',
    'xtick.color': '#333333',
    'ytick.color': '#333333',
})

BLUE = '#0072B2'       # single-hue magnitude color (Okabe-Ito blue)
GOOD = '#009E73'        # Okabe-Ito bluish green
WARNING = '#E69F00'     # Okabe-Ito orange
CRITICAL = '#D55E00'    # Okabe-Ito vermillion
GRID = '#E5E5E5'

def clean_axes(ax, horizontal=False):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    if horizontal:
        ax.spines['left'].set_visible(False)
        ax.xaxis.grid(True, color=GRID, linewidth=1.0, zorder=0)
        ax.yaxis.grid(False)
        ax.set_axisbelow(True)
    else:
        ax.spines['left'].set_visible(False)
        ax.yaxis.grid(True, color=GRID, linewidth=1.0, zorder=0)
        ax.xaxis.grid(False)
        ax.set_axisbelow(True)

def savefig(fig, name):
    fig.tight_layout()
    fig.savefig(f'{OUT}/{name}.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print('wrote', name)

# =========================================================================
# 1) Findings per institution (top 11 + Other, alias-consolidated)
# =========================================================================
ALIASES = {
    'UK AI Security Institute (UK AISI)': 'UK AISI',
    'UK AI Security Institute': 'UK AISI',
    'US Center for AI Standards and Innovation (CAISI), NIST': 'US CAISI',
    'NIST/US CAISI': 'US CAISI',
    'Shanghai Artificial Intelligence Laboratory': 'Shanghai AI Lab',
    'Shanghai AI Laboratory (AI45 Lab)': 'Shanghai AI Lab',
    'Shanghai AI Laboratory': 'Shanghai AI Lab',
    'Shanghai AI Laboratory / AI45 Lab': 'Shanghai AI Lab',
}
inst_counter = Counter(ALIASES.get(r['Institution'], r['Institution']) for r in rows)
TOP_N = 11
top_inst = inst_counter.most_common(TOP_N)
other_count = sum(c for k, c in inst_counter.items() if k not in dict(top_inst))
other_orgs = len([k for k in inst_counter if k not in dict(top_inst)])
# sort the named institutions ascending (largest on top); "Other" always pinned at the bottom,
# in a muted gray so it reads as an aggregate bucket, not a peer institution.
named = sorted(top_inst, key=lambda x: x[1])
labels = [f'Other ({other_orgs} orgs/collaborations)'] + [k for k, c in named]
values = [other_count] + [c for k, c in named]
colors1 = ['#B0B0B0'] + [BLUE] * len(named)

fig, ax = plt.subplots(figsize=(11, 8))
bars = ax.barh(labels, values, color=colors1, height=0.65, zorder=3)
for b, v in zip(bars, values):
    ax.text(v + max(values)*0.012, b.get_y() + b.get_height()/2, str(v),
            va='center', ha='left', fontsize=15, color='#1a1a1a', fontweight='bold')
ax.set_xlabel('Findings')
ax.set_title('Findings per Institution', pad=16)
ax.set_xlim(0, max(values) * 1.12)
clean_axes(ax, horizontal=True)
savefig(fig, '01_findings_per_institution')

# =========================================================================
# 2) Findings per model developer (multi-label; a finding may count >1x)
# =========================================================================
DEVS = [
    ('OpenAI', re.compile(r'ChatGPT|\bGPT|\bo1\b|\bo3\b|\bo4-mini\b|OpenAI|codex', re.I)),
    ('Anthropic', re.compile(r'Claude|Anthropic', re.I)),
    ('Google', re.compile(r'Gemini|Google|PaLM|Gemma', re.I)),
    ('Meta', re.compile(r'Llama|Meta\b', re.I)),
    ('DeepSeek', re.compile(r'DeepSeek', re.I)),
    ('Alibaba', re.compile(r'Qwen|Alibaba', re.I)),
    ('Moonshot AI', re.compile(r'Kimi|Moonshot', re.I)),
    ('Mistral', re.compile(r'Mistral', re.I)),
    ('xAI', re.compile(r'Grok|xAI', re.I)),
]
def devs_for(text):
    found = [name for name, pat in DEVS if pat.search(text)]
    return found or ['Other/Unspecified']

dev_counter = Counter()
for r in rows:
    for d in set(devs_for(r['Models / Systems'])):
        dev_counter[d] += 1

named_devs = sorted([(k, v) for k, v in dev_counter.items() if k != 'Other/Unspecified'], key=lambda x: x[1])
other_dev_count = dev_counter.get('Other/Unspecified', 0)
labels2 = ['Other/Unspecified (anonymised or aggregate)'] + [k for k, v in named_devs]
values2 = [other_dev_count] + [v for k, v in named_devs]
colors2 = ['#B0B0B0'] + [BLUE] * len(named_devs)

fig, ax = plt.subplots(figsize=(11, 7))
bars = ax.barh(labels2, values2, color=colors2, height=0.6, zorder=3)
for b, v in zip(bars, values2):
    ax.text(v + max(values2)*0.012, b.get_y() + b.get_height()/2, str(v),
            va='center', ha='left', fontsize=15, color='#1a1a1a', fontweight='bold')
ax.set_xlabel('Findings naming this developer\'s model(s)')
ax.set_title('Findings per Model Developer', pad=16)
ax.set_xlim(0, max(values2) * 1.15)
clean_axes(ax, horizontal=True)
fig.text(0.02, -0.02, 'Note: findings naming multiple developers\' models are counted once per developer named; counts do not sum to 456.',
          fontsize=12, color='#666666', ha='left')
savefig(fig, '02_findings_per_model_developer')

# =========================================================================
# 3) Findings per access type
# =========================================================================
acc_counter = Counter(r['Access Type'] for r in rows)
acc_order = ['Post-deployment', 'Pre-deployment', 'Mixed', 'Aggregate', 'N/A']
labels3 = [a for a in acc_order if a in acc_counter]
values3 = [acc_counter[a] for a in labels3]

fig, ax = plt.subplots(figsize=(10, 6.5))
bars = ax.bar(labels3, values3, color=BLUE, width=0.55, zorder=3)
for b, v in zip(bars, values3):
    ax.text(b.get_x() + b.get_width()/2, v + max(values3)*0.015, str(v),
            ha='center', va='bottom', fontsize=15, color='#1a1a1a', fontweight='bold')
ax.set_ylabel('Findings')
ax.set_title('Findings per Access Type', pad=16)
ax.set_ylim(0, max(values3) * 1.15)
clean_axes(ax, horizontal=False)
savefig(fig, '03_findings_per_access_type')

# =========================================================================
# 4) Headline outcome distribution — Tier A + C1 only (n=78), matching the
#    paper's established headline-stat convention — status colors
# =========================================================================
tierA = [r for r in rows if r['Proportionality']]
tierA_C1 = [r for r in tierA if r['Severity (C1/C2) majority'] == 'C1']
prop_counter = Counter(r['Proportionality'] for r in tierA_C1)
prop_order = ['Proportionate', 'Under-response (gap)', 'Accountability gap (no action)']
prop_colors = {'Proportionate': GOOD, 'Under-response (gap)': WARNING, 'Accountability gap (no action)': CRITICAL}
labels4 = prop_order
values4 = [prop_counter[l] for l in labels4]
colors4 = [prop_colors[l] for l in labels4]
pct4 = [v/len(tierA_C1)*100 for v in values4]

fig, ax = plt.subplots(figsize=(10.5, 6.5))
bars = ax.bar(labels4, values4, color=colors4, width=0.55, zorder=3)
for b, v, p in zip(bars, values4, pct4):
    ax.text(b.get_x() + b.get_width()/2, v + max(values4)*0.015, f'{v} ({p:.0f}%)',
            ha='center', va='bottom', fontsize=15, color='#1a1a1a', fontweight='bold')
ax.set_ylabel('Findings')
ax.set_title(f'Headline Outcome Distribution — Tier A, C1 Findings (n={len(tierA_C1)})', pad=16)
ax.set_ylim(0, max(values4) * 1.18)
clean_axes(ax, horizontal=False)
ax.set_xticklabels(labels4, fontsize=14)
savefig(fig, '04_headline_outcome_distribution')

# =========================================================================
# 5) Pre vs post deployment substantive-response rate (Tier A only)
# =========================================================================
def rate(access_type):
    sub = [r for r in tierA if r['Access Type'] == access_type]
    n = len(sub)
    prop = sum(1 for r in sub if r['Proportionality'] == 'Proportionate')
    return prop, n, (prop/n*100 if n else 0)

pre_prop, pre_n, pre_pct = rate('Pre-deployment')
post_prop, post_n, post_pct = rate('Post-deployment')

labels5 = [f'Pre-deployment\n(n={pre_n})', f'Post-deployment\n(n={post_n})']
values5 = [pre_pct, post_pct]
counts5 = [pre_prop, post_prop]
colors5 = ['#0072B2', '#56B4E9']

fig, ax = plt.subplots(figsize=(8.5, 7))
bars = ax.bar(labels5, values5, color=colors5, width=0.5, zorder=3)
for b, v, c in zip(bars, values5, counts5):
    ax.text(b.get_x() + b.get_width()/2, v + 1.5, f'{v:.0f}%\n({c} findings)',
            ha='center', va='bottom', fontsize=16, color='#1a1a1a', fontweight='bold')
ax.set_ylabel('Substantive response rate')
ax.set_title('Substantive Response Rate: Pre- vs Post-Deployment', pad=16)
ax.set_ylim(0, max(values5) * 1.4)
ax.yaxis.set_major_formatter(lambda x, pos: f'{x:.0f}%')
clean_axes(ax, horizontal=False)
savefig(fig, '05_pre_vs_post_deployment_response_rate')

# =========================================================================
# 6) Findings per year
# =========================================================================
year_counter = Counter(r['Publication Date'][:4] for r in rows if r['Publication Date'])
labels6 = sorted(year_counter.keys())
values6 = [year_counter[y] for y in labels6]

fig, ax = plt.subplots(figsize=(9, 6.5))
bars = ax.bar(labels6, values6, color=BLUE, width=0.55, zorder=3)
for b, v in zip(bars, values6):
    ax.text(b.get_x() + b.get_width()/2, v + max(values6)*0.015, str(v),
            ha='center', va='bottom', fontsize=15, color='#1a1a1a', fontweight='bold')
ax.set_ylabel('Findings')
ax.set_title('Findings per Year', pad=16)
ax.set_ylim(0, max(values6) * 1.15)
clean_axes(ax, horizontal=False)
savefig(fig, '06_findings_per_year')

print('\nAll charts written to', OUT)
