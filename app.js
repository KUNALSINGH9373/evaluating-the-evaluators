/* Evaluating the Evaluators — dashboard engine (no dependencies). */
(function () {
"use strict";

const DATA = window.AISI;
const F = DATA.findings;
const M = DATA.meta;
const TRACK = F.filter(f => f.track === "yes");

/* ---------- theme ---------- */
const root = document.documentElement;
const themeParam = new URLSearchParams(location.search).get("theme");
const stored = themeParam || localStorage.getItem("theme");
if (stored === "light" || stored === "dark") root.dataset.theme = stored;
document.getElementById("themeToggle").addEventListener("click", () => {
  const dark = getComputedStyle(root).colorScheme.includes("dark");
  const next = dark ? "light" : "dark";
  root.dataset.theme = next;
  localStorage.setItem("theme", next);
  renderAllCharts();
});

function cvar(name) {
  return getComputedStyle(root).getPropertyValue(name).trim();
}

/* ---------- generic DOM helpers (textContent only — labels are untrusted) ---------- */
function h(tag, attrs, ...kids) {
  const n = document.createElement(tag);
  if (attrs) for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") n.className = v;
    else if (k.startsWith("on")) n.addEventListener(k.slice(2), v);
    else n.setAttribute(k, v);
  }
  for (const kid of kids) {
    if (kid == null) continue;
    n.append(typeof kid === "string" ? document.createTextNode(kid) : kid);
  }
  return n;
}
const SVGNS = "http://www.w3.org/2000/svg";
function s(tag, attrs, ...kids) {
  const n = document.createElementNS(SVGNS, tag);
  if (attrs) for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
  for (const kid of kids) n.append(kid);
  return n;
}

/* ---------- tooltip ---------- */
const tip = document.getElementById("tooltip");
function showTip(evt, title, rows) {
  tip.replaceChildren();
  if (title) tip.append(h("div", { class: "t-title" }, title));
  for (const r of rows) {
    const row = h("div", { class: "t-row" });
    if (r.color) row.append(h("span", { class: "t-key", style: `background:${r.color}` }));
    row.append(h("span", { class: "t-val" }, String(r.value)));
    if (r.label) row.append(h("span", { class: "t-lbl" }, r.label));
    tip.append(row);
  }
  tip.style.display = "block";
  moveTip(evt);
}
function moveTip(evt) {
  const pad = 14;
  const w = tip.offsetWidth, hh = tip.offsetHeight;
  let x = evt.clientX + pad, y = evt.clientY + pad;
  if (x + w > innerWidth - 8) x = evt.clientX - w - pad;
  if (y + hh > innerHeight - 8) y = evt.clientY - hh - pad;
  tip.style.left = x + "px";
  tip.style.top = y + "px";
}
function hideTip() { tip.style.display = "none"; }
function hoverable(node, title, rows) {
  node.addEventListener("pointerenter", e => showTip(e, title, rows));
  node.addEventListener("pointermove", moveTip);
  node.addEventListener("pointerleave", hideTip);
  node.setAttribute("tabindex", "0");
  node.addEventListener("focus", () => {
    const r = node.getBoundingClientRect();
    showTip({ clientX: r.right, clientY: r.top }, title, rows);
  });
  node.addEventListener("blur", hideTip);
}

/* ---------- bar path helpers (4px rounded data end, square baseline) ---------- */
function barRight(x, y, w, hgt, r) {
  r = Math.max(0, Math.min(r, w, hgt / 2));
  return `M${x},${y} h${w - r} a${r},${r} 0 0 1 ${r},${r} v${hgt - 2 * r} a${r},${r} 0 0 1 ${-r},${r} h${-(w - r)} z`;
}
function barTop(x, y, w, hgt, r) {
  r = Math.max(0, Math.min(r, hgt, w / 2));
  return `M${x},${y + r} a${r},${r} 0 0 1 ${r},${-r} h${w - 2 * r} a${r},${r} 0 0 1 ${r},${r} v${hgt - r} h${-w} z`;
}

/* ---------- number helpers ---------- */
const pct = (a, b) => Math.round((a / b) * 100);

/* ================= hero, tiles, insights ================= */
const noRespPct = pct(M.noResponse, M.trackable);
document.getElementById("heroNum").textContent = noRespPct + "%";
document.getElementById("heroCaption").textContent =
  `of trackable findings received no documented company response (${M.noResponse} of ${M.trackable})`;
document.getElementById("asof").textContent =
  `${M.totalFindings} findings · ${M.reports} reports · ${M.dateMin.slice(0, 7)} to ${M.dateMax.slice(0, 7)} · dataset v6, verified 2026-07-16`;

const tiles = [
  { label: "Findings tracked", value: M.totalFindings, sub: `${M.reports} reports` },
  { label: "Accountability set", value: M.trackable, sub: "trackable findings" },
  { label: "No response", value: M.noResponse, sub: `${noRespPct}% of the set` },
  { label: "Substantive responses", value: M.substantive, sub: `${pct(M.substantive, M.trackable)}% of the set` },
  { label: "C1 unanswered", value: M.c1NoResponse, sub: `of ${M.trackableC1} severe findings` },
  { label: "Median response lag", value: M.medianLag + " days", sub: `n = ${M.lagN} responses` },
];
document.getElementById("tiles").append(
  ...tiles.map(t => h("div", { class: "tile" },
    h("div", { class: "label" }, t.label),
    h("div", { class: "value" }, String(t.value)),
    h("div", { class: "sub" }, t.sub)))
);

const polTouched = F.filter(f => ["Binding requirement", "In guidance", "Cited"].includes(f.pol)).length;
const ukCount = F.filter(f => f.instGroup === "UK AISI").length;
const insights = [
  [`${M.noResponse} of ${M.trackable} accountability-set findings (${noRespPct}%) `,
   "have no documented company response of any kind — no blog post, system-card note, or filing that engages with the finding."],
  [`Half of the most severe findings went unanswered: `,
   `${M.c1NoResponse} of ${M.trackableC1} C1 findings (a dangerous-capability threshold demonstrated) drew no company response.`],
  [`When companies do respond, they respond fast — median lag ${M.medianLag} days. `,
   "Most engagement happens pre-deployment, when companies see findings before publication (negative lags are genuine)."],
  [`Findings travel to policy more readily than to companies: `,
   `${polTouched} findings were cited in or shaped official guidance or binding requirements, versus ${M.anyResponse} company responses in the accountability set.`],
  [`UK AISI produced ${ukCount} of ${M.totalFindings} findings (${pct(ukCount, M.totalFindings)}%) `,
   "— half the public output of the entire government-AISI network."],
];
document.getElementById("insightList").append(
  ...insights.map(([strong, rest]) => h("div", { class: "insight" }, h("strong", null, strong), rest))
);

/* ================= chart data ================= */
function countBy(arr, key) {
  const m = new Map();
  for (const x of arr) {
    const k = key(x);
    if (k == null) continue;
    m.set(k, (m.get(k) || 0) + 1);
  }
  return m;
}

const ACTIONS = ["Substantive", "Partial", "Acknowledged", "None"];
const NATURES = ["capability-finding", "methodology", "governance", "capability-trend"];
const NATURE_LABEL = {
  "capability-finding": "Capability finding", methodology: "Methodology",
  governance: "Governance", "capability-trend": "Capability trend",
};
const nature = f => NATURES.find(n => f.ftype.includes(n)) || null;

const funnelRows = [
  { label: "All findings", value: M.totalFindings },
  { label: "Empirical model findings", value: M.empirical },
  { label: "Accountability set", value: M.trackable },
  { label: "Any documented response", value: M.anyResponse },
  { label: "Substantive response", value: M.substantive },
];

const sevActionRows = ["C1", "C2"].map(sev => ({
  label: sev === "C1" ? "C1 · threshold demonstrated" : "C2 · partial / lower severity",
  segs: ACTIONS.map(a => ({
    name: a,
    value: TRACK.filter(f => f.sev === sev && f.action === a).length,
  })),
}));

const PROP_ORDER = ["Accountability gap (no action)", "Under-response (gap)", "Proportionate", "Proportionate (Cat2)", "Too-recent (unobservable)"];
const propCounts = countBy(TRACK, f => f.prop || null);
const propRows = PROP_ORDER.filter(p => propCounts.has(p))
  .map(p => ({ label: p, value: propCounts.get(p) }));

const quarters = [];
{
  const qs = [...new Set(F.map(f => f.q).filter(Boolean))].sort();
  let [y, q] = [+qs[0].slice(0, 4), +qs[0].slice(6)];
  const [ey, eq] = [+qs[qs.length - 1].slice(0, 4), +qs[qs.length - 1].slice(6)];
  while (y < ey || (y === ey && q <= eq)) {
    quarters.push(`${y}-Q${q}`);
    q++; if (q === 5) { q = 1; y++; }
  }
}
const timelineCols = quarters.map(q => ({
  label: q,
  segs: NATURES.map(n => ({
    name: NATURE_LABEL[n],
    value: F.filter(f => f.q === q && nature(f) === n).length,
  })),
}));

const domCounts = [...countBy(F.flatMap(f => f.dom.map(d => ({ d }))), x => x.d)]
  .sort((a, b) => b[1] - a[1]);
const domRows = domCounts.slice(0, 12).map(([label, value]) => ({ label, value }));
const domOther = domCounts.slice(12).reduce((a, [, v]) => a + v, 0);
if (domOther) domRows.push({ label: "Other", value: domOther });

const instRows = [...countBy(F, f => f.instGroup)]
  .sort((a, b) => b[1] - a[1]).map(([label, value]) => ({ label, value }));

const lagPoints = TRACK.filter(f => f.lag != null)
  .map(f => ({ f, lag: f.lag })).sort((a, b) => a.lag - b.lag);

/* ---- tags: papers (distinct reports) and findings per tag ---- */
const reportKey = f => f.rid || f.url || f.id;
const ORG_TAGS = new Set([
  "anthropic", "openai", "deepseek", "meta", "google", "google-deepmind", "deepmind",
  "mistral", "xai", "alibaba", "moonshot-ai", "moonshot", "cohere", "microsoft", "amazon",
  "uk-aisi", "us-caisi", "securebio", "apollo-research", "gray-swan", "thorn", "nist",
  "imda", "sgaisi", "j-aisi", "k-aisi", "inesia", "peren", "eu-ai-office",
]);
const MODEL_RE = /^(gpt|claude|gemini|llama|grok|kimi|qwen|o[0-9]|deepseek-[rv]|mistral-(large|small|medium|nemo)|phi-|command|codestral|pixtral)/;
function tagGroup(t) {
  if (ORG_TAGS.has(t)) return "Companies & orgs";
  if (MODEL_RE.test(t)) return "Models & systems";
  return "Topics & techniques";
}
const TAG_GROUPS = ["Models & systems", "Companies & orgs", "Topics & techniques"];
const tagMap = new Map();
for (const f of F) for (const t of f.tags) {
  if (!tagMap.has(t)) tagMap.set(t, { tag: t, group: tagGroup(t), papers: new Set(), findings: 0 });
  const e = tagMap.get(t);
  e.papers.add(reportKey(f));
  e.findings++;
}
const tagStats = [...tagMap.values()]
  .map(e => ({ tag: e.tag, group: e.group, papers: e.papers.size, findings: e.findings }))
  .sort((a, b) => b.papers - a.papers || b.findings - a.findings);
const TAG_QUOTA = { "Models & systems": 18, "Companies & orgs": 12, "Topics & techniques": 26 };
const topTags = TAG_GROUPS.flatMap(g =>
  tagStats.filter(t => t.group === g).slice(0, TAG_QUOTA[g]));

const modelStats = tagStats.filter(t => t.group === "Models & systems");
const modelRows = modelStats.slice(0, 15)
  .sort((a, b) => b.findings - a.findings)
  .map(t => ({ label: t.tag, value: t.findings, papers: t.papers }));
document.getElementById("tiles").append(h("div", { class: "tile" },
  h("div", { class: "label" }, "Named models evaluated"),
  h("div", { class: "value" }, String(modelStats.length)),
  h("div", { class: "sub" }, "distinct versions, from tags")));

/* ---- reports per year, by institution group ---- */
const YEAR_GROUPS = ["UK AISI", "US CAISI", "Joint / multi-party", "Other / not recorded"];
const foldGroup = g => YEAR_GROUPS.includes(g) ? g : "Other / not recorded";
const reportsSeen = new Map();
for (const f of F) {
  const k = reportKey(f);
  if (!reportsSeen.has(k) && f.date) {
    reportsSeen.set(k, { year: f.date.slice(0, 4), group: foldGroup(f.instGroup) });
  }
}
const years = [...new Set([...reportsSeen.values()].map(r => r.year))].sort();
const yearCols = years.map(y => ({
  label: y,
  segs: YEAR_GROUPS.map(g => ({
    name: g,
    value: [...reportsSeen.values()].filter(r => r.year === y && r.group === g).length,
  })),
}));

/* ================= chart renderers ================= */
const MB = { barH: 22, gap: 12, labelW: 210, valueW: 44, rx: 4 };

function renderHBars(mount, rows, colorVar, tipTitle) {
  mount.replaceChildren();
  const color = cvar(colorVar), surface = cvar("--surface");
  const W = Math.max(320, mount.clientWidth);
  const labelW = Math.min(MB.labelW, W * 0.42);
  const plotW = W - labelW - MB.valueW;
  const rowH = MB.barH + MB.gap;
  const H = rows.length * rowH;
  const max = Math.max(...rows.map(r => r.value), 1);
  const svg = s("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img" });
  rows.forEach((r, i) => {
    const y = i * rowH + MB.gap / 2;
    const w = Math.max(2, (r.value / max) * plotW);
    const lbl = s("text", {
      x: labelW - 10, y: y + MB.barH / 2 + 4, "text-anchor": "end",
      fill: cvar("--ink-2"), "font-size": "12",
    }, r.label);
    const bar = s("path", { d: barRight(labelW, y, w, MB.barH, MB.rx), fill: color });
    const val = s("text", {
      x: labelW + w + 8, y: y + MB.barH / 2 + 4,
      fill: cvar("--ink"), "font-size": "12", "font-weight": "650",
    }, String(r.value));
    const hit = s("rect", { x: 0, y: i * rowH, width: W, height: rowH, fill: "transparent" });
    hoverable(hit, tipTitle, [{ color, value: r.value, label: r.label }]);
    svg.append(lbl, bar, val, hit);
  });
  svg.append(s("line", { x1: labelW, y1: 0, x2: labelW, y2: H, stroke: cvar("--axis"), "stroke-width": 1 }));
  mount.append(svg);
  void surface;
}

function renderStackedH(mount, rows, colorVars, tipTitle) {
  mount.replaceChildren();
  const colors = colorVars.map(cvar), surface = cvar("--surface");
  const W = Math.max(320, mount.clientWidth);
  const labelW = Math.min(230, W * 0.44);
  const plotW = W - labelW - MB.valueW;
  const rowH = MB.barH + 16;
  const H = rows.length * rowH;
  const max = Math.max(...rows.map(r => r.segs.reduce((a, x) => a + x.value, 0)), 1);
  const svg = s("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img" });
  rows.forEach((r, i) => {
    const y = i * rowH + 8;
    const total = r.segs.reduce((a, x) => a + x.value, 0);
    svg.append(s("text", {
      x: labelW - 10, y: y + MB.barH / 2 + 4, "text-anchor": "end",
      fill: cvar("--ink-2"), "font-size": "12",
    }, r.label));
    let x = labelW;
    const nonZero = r.segs.filter(g => g.value > 0);
    r.segs.forEach((seg, j) => {
      if (!seg.value) return;
      const w = (seg.value / max) * plotW;
      const isLast = seg === nonZero[nonZero.length - 1];
      const shape = isLast
        ? s("path", { d: barRight(x, y, Math.max(2, w - 2), MB.barH, MB.rx), fill: colors[j] })
        : s("rect", { x, y, width: Math.max(2, w - 2), height: MB.barH, fill: colors[j] });
      hoverable(shape, `${tipTitle} — ${r.label}`,
        r.segs.filter(g => g.value > 0).map(g => ({
          color: colors[r.segs.indexOf(g)], value: g.value, label: g.name,
        })));
      svg.append(shape);
      if (w > 26) svg.append(s("text", {
        x: x + w / 2 - 1, y: y + MB.barH / 2 + 4, "text-anchor": "middle",
        fill: relievedInk(colors[j]), "font-size": "11", "font-weight": "600",
      }, String(seg.value)));
      x += w;
    });
    svg.append(s("text", {
      x: x + 8, y: y + MB.barH / 2 + 4, fill: cvar("--ink"),
      "font-size": "12", "font-weight": "650",
    }, String(total)));
  });
  svg.append(s("line", { x1: labelW, y1: 0, x2: labelW, y2: H, stroke: cvar("--axis"), "stroke-width": 1 }));
  mount.append(svg);
  void surface;
}

/* pick white/ink for a label inside a colored fill by luminance */
function relievedInk(hex) {
  const n = hex.replace("#", "");
  const [r, g, b] = [0, 2, 4].map(i => parseInt(n.slice(i, i + 2), 16) / 255);
  const lum = 0.2126 * r + 0.7152 * g + 0.0722 * b;
  return lum > 0.55 ? "#0b0b0b" : "#ffffff";
}

function renderColumns(mount, cols, colorVars, xfmt) {
  xfmt = xfmt || (lbl => { const [yy, qq] = lbl.split("-"); return `${qq} '${yy.slice(2)}`; });
  mount.replaceChildren();
  const colors = colorVars.map(cvar);
  const W = Math.max(320, mount.clientWidth);
  const H = 240, padL = 34, padB = 26, padT = 8;
  const plotW = W - padL - 8, plotH = H - padT - padB;
  const max = Math.max(...cols.map(c => c.segs.reduce((a, x) => a + x.value, 0)), 1);
  const yMax = Math.ceil(max / 10) * 10;
  const slot = plotW / cols.length;
  const colW = Math.min(24, slot * 0.62);
  const svg = s("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img" });
  for (let t = 0; t <= yMax; t += yMax / 2) {
    const y = padT + plotH - (t / yMax) * plotH;
    svg.append(s("line", { x1: padL, y1: y, x2: W - 8, y2: y, stroke: cvar("--grid"), "stroke-width": 1 }));
    svg.append(s("text", { x: padL - 6, y: y + 4, "text-anchor": "end", fill: cvar("--muted"), "font-size": "11" }, String(t)));
  }
  cols.forEach((c, i) => {
    const cx = padL + i * slot + (slot - colW) / 2;
    let yCursor = padT + plotH;
    const total = c.segs.reduce((a, x) => a + x.value, 0);
    const nonZero = c.segs.filter(g => g.value > 0);
    c.segs.forEach((seg, j) => {
      if (!seg.value) return;
      const hSeg = (seg.value / yMax) * plotH;
      yCursor -= hSeg;
      const isTop = seg === nonZero[nonZero.length - 1];
      const gap = isTop ? 0 : 2;
      const shape = isTop
        ? s("path", { d: barTop(cx, yCursor, colW, hSeg, MB.rx), fill: colors[j] })
        : s("rect", { x: cx, y: yCursor + gap, width: colW, height: Math.max(1, hSeg - gap), fill: colors[j] });
      svg.append(shape);
    });
    const hit = s("rect", { x: padL + i * slot, y: padT, width: slot, height: plotH + padB, fill: "transparent" });
    hoverable(hit, c.label, c.segs.filter(g => g.value > 0).map((g) => ({
      color: colors[c.segs.indexOf(g)], value: g.value, label: g.name,
    })).concat([{ value: total, label: "total" }]));
    svg.append(hit);
    const every = slot > 46 ? 1 : 2;
    if (i % every === 0) {
      svg.append(s("text", {
        x: cx + colW / 2, y: H - 8, "text-anchor": "middle",
        fill: cvar("--muted"), "font-size": "10.5",
      }, xfmt(c.label)));
    }
  });
  svg.append(s("line", { x1: padL, y1: padT + plotH, x2: W - 8, y2: padT + plotH, stroke: cvar("--axis"), "stroke-width": 1 }));
  mount.append(svg);
}

/* packed-bubble cluster map: one bubble per tag, sized by paper count, clustered by group */
function renderBubbles(mount, tags, groupVars) {
  mount.replaceChildren();
  const surface = cvar("--surface");
  const W = Math.max(360, mount.clientWidth);
  const rOf = v => 7 + 5.6 * Math.sqrt(v);

  // greedy spiral packing per group
  const clusters = TAG_GROUPS.map(g => {
    const items = tags.filter(t => t.group === g).map(t => ({ ...t, r: rOf(t.papers) }));
    const placed = [];
    for (const it of items) {
      if (!placed.length) { it.x = 0; it.y = 0; placed.push(it); continue; }
      let a = 0, rad = placed[0].r + it.r;
      for (let step = 0; step < 4000; step++) {
        const x = Math.cos(a) * rad, y = Math.sin(a) * rad * 0.72;
        if (placed.every(p => Math.hypot(p.x - x, p.y - y) >= p.r + it.r + 2.5)) {
          it.x = x; it.y = y; placed.push(it); break;
        }
        a += 0.37; rad += 0.55;
      }
      if (it.x === undefined) { it.x = rad; it.y = 0; placed.push(it); }
    }
    const minX = Math.min(...placed.map(p => p.x - p.r)), maxX = Math.max(...placed.map(p => p.x + p.r));
    const minY = Math.min(...placed.map(p => p.y - p.r)), maxY = Math.max(...placed.map(p => p.y + p.r));
    return { g, placed, w: maxX - minX, hgt: maxY - minY, minX, minY };
  });

  const GAP = 34, padT = 10, labelH = 26;
  const rawW = clusters.reduce((a, c) => a + c.w, 0) + GAP * (clusters.length - 1);
  const k = Math.min(1, (W - 20) / rawW);
  const H = Math.max(...clusters.map(c => c.hgt)) * k + padT + labelH + 8;
  const svg = s("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img" });
  let xCursor = (W - rawW * k) / 2;
  clusters.forEach((c, gi) => {
    const color = cvar(groupVars[gi]);
    const midY = padT + (Math.max(...clusters.map(x => x.hgt)) * k) / 2;
    for (const p of c.placed.slice().sort((a, b) => b.r - a.r)) {
      const cx = xCursor + (p.x - c.minX) * k;
      const cy = midY + (p.y - (c.minY + c.hgt / 2)) * k;
      const r = p.r * k;
      const dot = s("circle", { cx, cy, r, fill: color, stroke: surface, "stroke-width": 2 });
      hoverable(dot, p.tag, [
        { color, value: p.papers, label: p.papers === 1 ? "report" : "reports" },
        { value: p.findings, label: p.findings === 1 ? "finding" : "findings" },
        { value: c.g, label: "" },
      ]);
      svg.append(dot);
      const name = p.tag;
      if (name.length * 5.1 < r * 2) {
        svg.append(s("text", {
          x: cx, y: cy + 3.5, "text-anchor": "middle", "pointer-events": "none",
          fill: relievedInk(color), "font-size": "10", "font-weight": "600",
        }, name));
      }
    }
    svg.append(s("text", {
      x: xCursor + (c.w * k) / 2, y: H - 8, "text-anchor": "middle",
      fill: cvar("--ink-2"), "font-size": "12", "font-weight": "600",
    }, c.g));
    xCursor += c.w * k + GAP;
  });
  mount.append(svg);
}

function renderDotPlot(mount, points, colorVar) {
  mount.replaceChildren();
  const color = cvar(colorVar), surface = cvar("--surface");
  const W = Math.max(320, mount.clientWidth);
  const H = 190, padL = 12, padR = 12, padB = 30, padT = 12;
  const plotW = W - padL - padR;
  const lo = Math.min(...points.map(p => p.lag), 0) - 2;
  const hi = Math.max(...points.map(p => p.lag), 0) + 2;
  const xOf = v => padL + ((v - lo) / (hi - lo)) * plotW;
  const svg = s("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img" });
  for (let t = Math.ceil(lo / 7) * 7; t <= hi; t += 7) {
    svg.append(s("line", { x1: xOf(t), y1: padT, x2: xOf(t), y2: H - padB, stroke: cvar("--grid"), "stroke-width": 1 }));
    svg.append(s("text", { x: xOf(t), y: H - 10, "text-anchor": "middle", fill: cvar("--muted"), "font-size": "11" }, String(t)));
  }
  svg.append(s("line", { x1: xOf(0), y1: padT, x2: xOf(0), y2: H - padB, stroke: cvar("--axis"), "stroke-width": 1.5 }));
  svg.append(s("text", { x: xOf(0) + 4, y: padT + 10, fill: cvar("--muted"), "font-size": "10.5" }, "published"));
  const stacks = new Map();
  const r = 5;
  for (const p of points) {
    const key = Math.round(xOf(p.lag) / (r * 2));
    const lvl = stacks.get(key) || 0;
    stacks.set(key, lvl + 1);
    const cy = H - padB - 12 - lvl * (r * 2 + 3);
    const dot = s("circle", {
      cx: xOf(p.lag), cy, r, fill: color, stroke: surface, "stroke-width": 2,
    });
    const hit = s("circle", { cx: xOf(p.lag), cy, r: 12, fill: "transparent" });
    hoverable(hit, p.f.id, [
      { color, value: `${p.lag} days`, label: "lag" },
      { value: p.f.models || "—", label: "" },
      { value: p.f.action, label: "action level" },
    ]);
    svg.append(dot, hit);
  }
  mount.append(svg);
}

/* ================= chart cards ================= */
const ORD_VARS = ["--ord1", "--ord2", "--ord3", "--ord4"];
const CAT_VARS = ["--blue", "--green", "--magenta", "--yellow"];

const charts = [
  {
    title: "The accountability funnel",
    sub: "From every published finding down to a substantive company response",
    wide: false,
    render(mount) { renderHBars(mount, funnelRows, "--blue", "Findings"); },
    table: () => [["Stage", "Findings"], ...funnelRows.map(r => [r.label, r.value])],
  },
  {
    title: "Severity vs. company response",
    sub: "Accountability set (46 findings) — response level by demonstrated severity",
    wide: false,
    legend: ACTIONS.map((a, i) => ({ name: a, varName: ORD_VARS[i], shape: "rect" })),
    render(mount) { renderStackedH(mount, sevActionRows, ORD_VARS, "Response"); },
    table: () => [["Severity", ...ACTIONS], ...sevActionRows.map(r => [r.label, ...r.segs.map(x => x.value)])],
  },
  {
    title: "What government AISIs publish, by quarter",
    sub: "All 281 findings by the nature of the finding",
    wide: true,
    legend: NATURES.map((n, i) => ({ name: NATURE_LABEL[n], varName: CAT_VARS[i], shape: "rect" })),
    render(mount) { renderColumns(mount, timelineCols, CAT_VARS); },
    table: () => [["Quarter", ...NATURES.map(n => NATURE_LABEL[n])],
      ...timelineCols.map(c => [c.label, ...c.segs.map(x => x.value)])],
  },
  {
    title: "Outcomes in the accountability set",
    sub: "Proportionality of response, given severity",
    wide: false,
    render(mount) { renderHBars(mount, propRows, "--violet", "Findings"); },
    table: () => [["Outcome", "Findings"], ...propRows.map(r => [r.label, r.value])],
  },
  {
    title: "Response lag",
    sub: "Days from publication to company response (negative = pre-deployment engagement)",
    wide: false,
    render(mount) { renderDotPlot(mount, lagPoints, "--aqua"); },
    table: () => [["Finding", "Lag (days)", "Action level"],
      ...lagPoints.map(p => [p.f.id, p.lag, p.f.action])],
  },
  {
    title: "Reports released per year",
    sub: `Distinct reports by evaluating institution · 2026 is partial (through ${M.dateMax.slice(0, 7)})`,
    wide: false,
    legend: YEAR_GROUPS.map((g, i) => ({ name: g, varName: CAT_VARS[i], shape: "rect" })),
    render(mount) { renderColumns(mount, yearCols, CAT_VARS, y => y); },
    table: () => [["Year", ...YEAR_GROUPS, "Total"],
      ...yearCols.map(c => [c.label, ...c.segs.map(x => x.value),
        c.segs.reduce((a, x) => a + x.value, 0)])],
  },
  {
    title: "Most-evaluated models",
    sub: `Findings per named model, from finding-level tags · ${modelStats.length} distinct named models in the dataset`,
    wide: false,
    render(mount) { renderHBars(mount, modelRows, "--magenta", "Findings"); },
    table: () => [["Model", "Findings", "Reports"], ...modelRows.map(r => [r.label, r.value, r.papers])],
  },
  {
    title: "The tag universe",
    sub: "One sphere per tag, sized by the number of reports it appears in · drag to orbit, scroll to zoom, right-drag to pan · click a tag to filter the explorer",
    wide: true,
    legend: TAG_GROUPS.map((g, i) => ({ name: g, varName: CAT_VARS[i], shape: "rect" })),
    render(mount) {
      mount.id = "tagUniverse3d";
      if (window.TAGVIZ3D && window.TAGVIZ3D.active) { window.TAGVIZ3D.refresh(); return; }
      renderBubbles(mount, topTags, CAT_VARS);
    },
    table: () => [["Tag", "Group", "Reports", "Findings"],
      ...topTags.map(t => [t.tag, t.group, t.papers, t.findings])],
  },
  {
    title: "Findings by domain",
    sub: "Multi-domain findings count once per domain",
    wide: false,
    render(mount) { renderHBars(mount, domRows, "--green", "Findings"); },
    table: () => [["Domain", "Findings"], ...domRows.map(r => [r.label, r.value])],
  },
  {
    title: "Findings by institution",
    sub: "Grouped; 'Not recorded' rows come from the completeness audit",
    wide: false,
    render(mount) { renderHBars(mount, instRows, "--orange", "Findings"); },
    table: () => [["Institution", "Findings"], ...instRows.map(r => [r.label, r.value])],
  },
];

const chartGrid = document.getElementById("chartGrid");
const mounts = [];
for (const c of charts) {
  const mount = h("div", { class: "plot" });
  mounts.push({ c, mount });
  const card = h("div", { class: "card" + (c.wide ? " wide" : "") },
    h("h3", null, c.title),
    h("div", { class: "sub" }, c.sub));
  if (c.legend) {
    card.append(h("div", { class: "legend" }, ...c.legend.map(k =>
      h("span", { class: "key" },
        h("span", { class: k.shape === "line" ? "linekey" : "swatch", style: `background:var(${k.varName})` }),
        k.name))));
  }
  card.append(mount);
  const tbl = c.table();
  const [head, ...body] = tbl;
  card.append(h("details", { class: "tblview" },
    h("summary", null, "Table view"),
    h("table", null,
      h("thead", null, h("tr", null, ...head.map(x => h("th", null, String(x))))),
      h("tbody", null, ...body.map(row => h("tr", null, ...row.map(x => h("td", null, String(x)))))))));
  chartGrid.append(card);
}

function renderAllCharts() {
  for (const { c, mount } of mounts) c.render(mount);
}
renderAllCharts();
let resizeT;
addEventListener("resize", () => { clearTimeout(resizeT); resizeT = setTimeout(renderAllCharts, 150); });

/* ================= explorer ================= */
const els = {
  search: document.getElementById("fSearch"),
  scope: document.getElementById("fScope"),
  inst: document.getElementById("fInst"),
  sev: document.getElementById("fSev"),
  action: document.getElementById("fAction"),
  domain: document.getElementById("fDomain"),
  track: document.getElementById("fTrack"),
  tbody: document.getElementById("tbody"),
  count: document.getElementById("countNote"),
  more: document.getElementById("loadMore"),
};

function fillSelect(sel, label, values) {
  sel.append(h("option", { value: "" }, label));
  for (const v of values) sel.append(h("option", { value: v }, v));
}
fillSelect(els.scope, "All scopes", ["government-AISI", "third-party-evaluator", "company-self-report"]);
fillSelect(els.inst, "All institutions", instRows.map(r => r.label));
fillSelect(els.sev, "All severities", ["C1", "C2", "Not coded"]);
fillSelect(els.action, "All response levels", [...ACTIONS, "No response expected"]);
fillSelect(els.domain, "All domains", domCounts.map(([d]) => d));

let shown = 50;
const PAGE = 50;

function matches(f) {
  const q = els.search.value.trim().toLowerCase();
  if (q) {
    const hay = `${f.id} ${f.title} ${f.finding} ${f.models} ${f.inst} ${f.resp} ${f.tags.join(" ")}`.toLowerCase();
    if (!hay.includes(q)) return false;
  }
  if (els.scope.value && f.scope !== els.scope.value) return false;
  if (els.inst.value && f.instGroup !== els.inst.value) return false;
  if (els.sev.value === "Not coded" ? f.sev : (els.sev.value && f.sev !== els.sev.value)) return false;
  if (els.action.value === "No response expected" ? f.action : (els.action.value && f.action !== els.action.value)) return false;
  if (els.domain.value && !f.dom.includes(els.domain.value)) return false;
  if (els.track.checked && f.track !== "yes") return false;
  return true;
}

function sevPill(f) {
  if (!f.sev) return h("span", { class: "pill" }, "—");
  return h("span", { class: "pill " + f.sev.toLowerCase() }, f.sev + (f.sevProv ? "*" : ""));
}
function actionPill(f) {
  if (!f.action) return h("span", { class: "pill" }, "n/a");
  return h("span", { class: "pill act-" + f.action }, f.action);
}

function detailRow(f) {
  const td = h("td", { colspan: "6" });
  td.append(h("div", null, h("strong", null, f.id + " — " + (f.title || "Untitled report"))));
  td.append(h("p", { style: "margin:8px 0 0" }, f.finding));
  if (f.quote) td.append(h("blockquote", { class: "kq" }, "“" + f.quote + "”"));
  if (f.resp) {
    td.append(h("p", { style: "margin-top:10px" },
      h("strong", null, "Company response: "), f.resp,
      f.respDate ? ` (${f.respDate}${f.lag != null ? `, lag ${f.lag} days` : ""})` : ""));
  }
  const meta = h("div", { class: "detail-grid" });
  const pairs = [
    ["Institution", f.inst || "Not recorded"],
    ["Published", f.date || "—"],
    ["Domain", f.dom.join(", ") || "—"],
    ["Access", f.access || "—"],
    ["Finding type", f.ftype.join(", ") || "—"],
    ["Scope", f.scope || "—"],
    ["Attribution", f.attr || "—"],
    ["Policy level", f.pol || "—"],
    ["Proportionality", f.prop || "—"],
    ["Confidence", f.conf || "—"],
  ];
  for (const [k, v] of pairs) meta.append(h("div", null, h("div", { class: "k" }, k), h("div", null, v)));
  td.append(meta);
  if (f.url && /^https?:\/\//.test(f.url)) {
    td.append(h("p", { style: "margin-top:10px" },
      h("a", { href: f.url, target: "_blank", rel: "noopener noreferrer" }, "Source report ↗")));
  }
  return h("tr", { class: "detail" }, td);
}

let openId = null;
function renderTable() {
  const rows = F.filter(matches).sort((a, b) => (b.date || "").localeCompare(a.date || ""));
  els.count.textContent = `${rows.length} of ${F.length} findings` +
    (els.track.checked ? " (accountability set)" : "") +
    (rows.some(f => f.sevProv) ? " · * = provisional severity" : "");
  els.tbody.replaceChildren();
  for (const f of rows.slice(0, shown)) {
    const tr = h("tr", { class: "datarow" + (openId === f.id ? " open" : "") },
      h("td", { style: "white-space:nowrap" }, f.date || "—"),
      h("td", null, f.instGroup),
      h("td", null,
        h("div", { style: "max-width:420px" },
          f.finding.length > 160 ? f.finding.slice(0, 157) + "…" : f.finding)),
      h("td", null, f.models ? (f.models.length > 40 ? f.models.slice(0, 37) + "…" : f.models) : "—"),
      h("td", null, sevPill(f)),
      h("td", null, actionPill(f)));
    tr.addEventListener("click", () => {
      openId = openId === f.id ? null : f.id;
      renderTable();
    });
    els.tbody.append(tr);
    if (openId === f.id) els.tbody.append(detailRow(f));
  }
  els.more.style.display = rows.length > shown ? "block" : "none";
}
for (const el of [els.scope, els.inst, els.sev, els.action, els.domain, els.track]) {
  el.addEventListener("change", () => { shown = PAGE; openId = null; renderTable(); });
}
els.search.addEventListener("input", () => { shown = PAGE; openId = null; renderTable(); });
els.more.addEventListener("click", () => { shown += PAGE; renderTable(); });
renderTable();

/* bridge for the 3D tag-universe module (tags3d.js) */
window.TAGVIZ = {
  topTags, TAG_GROUPS, groupColorVars: CAT_VARS, cvar,
  showTip, moveTip, hideTip,
  filterTag(tag) {
    els.search.value = tag;
    shown = PAGE; openId = null;
    renderTable();
    document.getElementById("explorer").scrollIntoView({ behavior: "smooth" });
  },
};

})();
