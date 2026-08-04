/* The tag universe, in 3D — a force-directed graph of tags. Spheres are tags
   (sized by report count); dotted links join tags that co-occur in >= MIN_CO
   shared reports. The layout is driven by those real links, so the most
   connected tags settle in the middle. Falls back silently to the 2D bubble
   chart in app.js if WebGL is unavailable. */
import * as THREE from "three";
import { OrbitControls } from "./vendor/OrbitControls.js";

const V = window.TAGVIZ;
const mount = document.getElementById("tagUniverse3d");
if (!V || !mount) throw new Error("tag viz bridge missing");

function webglOK() {
  try {
    const c = document.createElement("canvas");
    return !!(c.getContext("webgl2") || c.getContext("webgl"));
  } catch { return false; }
}
if (!webglOK()) throw new Error("no WebGL — keeping 2D fallback");

/* deterministic RNG so the layout is stable across visits */
function mulberry32(seed) {
  return function () {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/* ---------- real co-occurrence: pairs of tags sharing >= MIN_CO reports ---------- */
const MIN_CO = 3;
const F = window.AISI.findings;
const reportKey = f => f.rid || f.url || f.id;
const shown = new Set(V.topTags.map(t => t.tag));
const byReport = new Map();
for (const f of F) {
  const k = reportKey(f);
  if (!byReport.has(k)) byReport.set(k, new Set());
  for (const t of f.tags) if (shown.has(t)) byReport.get(k).add(t);
}
const coCount = new Map();
for (const tags of byReport.values()) {
  const list = [...tags].sort();
  for (let i = 0; i < list.length; i++) for (let j = i + 1; j < list.length; j++) {
    const key = list[i] + "|" + list[j];
    coCount.set(key, (coCount.get(key) || 0) + 1);
  }
}

const rOf = p => 3.2 + 2.6 * Math.sqrt(p);
const nodes = V.topTags.map(t => ({ ...t, r: rOf(t.papers), pos: new THREE.Vector3() }));
const nodeIx = new Map(nodes.map((n, i) => [n.tag, i]));
const edges = [];
for (const [key, w] of coCount) {
  if (w < MIN_CO) continue;
  const [a, b] = key.split("|");
  edges.push({ a: nodeIx.get(a), b: nodeIx.get(b), w });
}
for (const n of nodes) { n.deg = 0; n.best = null; }
for (const e of edges) {
  nodes[e.a].deg++; nodes[e.b].deg++;
  for (const [me, other] of [[e.a, e.b], [e.b, e.a]]) {
    if (!nodes[me].best || e.w > nodes[me].best.w) {
      nodes[me].best = { tag: nodes[other].tag, w: e.w };
    }
  }
}

/* ---------- layout: three clusters; each cluster's most-linked tag at its centre ---------- */
const CLUSTER_POS = [
  new THREE.Vector3(-150, 6, -45),
  new THREE.Vector3(145, -8, -55),
  new THREE.Vector3(0, 4, 105),
];
V.TAG_GROUPS.forEach((g, gi) => {
  const items = nodes.filter(n => n.group === g)
    .sort((a, b) => b.deg - a.deg || b.papers - a.papers); // most connected placed first = centre
  const rand = mulberry32(1234 + gi * 999);
  const placed = [];
  for (const n of items) {
    let found = null;
    for (let rad = 0; rad < 420 && !found; rad += 3) {
      for (let t = 0; t < 26 && !found; t++) {
        const dir = new THREE.Vector3(rand() * 2 - 1, (rand() * 2 - 1) * 0.8, rand() * 2 - 1);
        if (dir.lengthSq() < 1e-4) continue;
        const p = dir.setLength(Math.max(rad, 0.01));
        if (placed.every(q => p.distanceTo(q.p) >= q.r + n.r + 2.5)) found = p;
      }
    }
    if (!found) found = new THREE.Vector3(0, 0, 420);
    placed.push({ p: found, r: n.r });
    n.pos.copy(found).add(CLUSTER_POS[gi]);
  }
});

/* ---------- scene ---------- */
const H = 480;
mount.replaceChildren();
mount.style.position = "relative";
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(50, 1, 1, 3000);
camera.position.set(0, 60, 430);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
mount.append(renderer.domElement);
renderer.domElement.style.borderRadius = "10px";
renderer.domElement.setAttribute("role", "img");
renderer.domElement.setAttribute("aria-label",
  "Interactive 3D tag universe: one sphere per tag, sized by report count and clustered by group (models, companies, topics). A 2D table view of the same data is available via the chart's table view toggle.");
renderer.domElement.style.touchAction = "pan-y"; // one finger scrolls the page; two fingers orbit

const hint = document.createElement("div");
hint.textContent = "drag to orbit · scroll to zoom · right-drag to pan · two fingers on touch";
hint.style.cssText = "position:absolute;left:10px;bottom:8px;font-size:11px;color:var(--muted);pointer-events:none";
mount.append(hint);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.06;
controls.minDistance = 90;
controls.maxDistance = 800;
const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
controls.autoRotate = !reducedMotion;
controls.autoRotateSpeed = 0.7;
controls.touches.ONE = null;
controls.touches.TWO = THREE.TOUCH.DOLLY_ROTATE;
renderer.domElement.addEventListener("pointerdown", () => { controls.autoRotate = false; }, { once: true });

scene.add(new THREE.AmbientLight(0xffffff, 0.9));
const key = new THREE.DirectionalLight(0xffffff, 1.6);
key.position.set(120, 180, 220);
scene.add(key);
const rim = new THREE.DirectionalLight(0xffffff, 0.5);
rim.position.set(-150, -60, -120);
scene.add(rim);

/* starfield backdrop */
const starGeo = new THREE.BufferGeometry();
{
  const rand = mulberry32(77);
  const pts = new Float32Array(420 * 3);
  for (let i = 0; i < 420; i++) {
    const v = new THREE.Vector3(rand() * 2 - 1, rand() * 2 - 1, rand() * 2 - 1).setLength(650 + rand() * 450);
    pts.set([v.x, v.y, v.z], i * 3);
  }
  starGeo.setAttribute("position", new THREE.BufferAttribute(pts, 3));
}
const starMat = new THREE.PointsMaterial({ size: 1.6, transparent: true, opacity: 0.45 });
scene.add(new THREE.Points(starGeo, starMat));

/* dotted co-occurrence links */
function edgePositions(list) {
  const arr = new Float32Array(list.length * 6);
  list.forEach((e, i) => {
    arr.set([...nodes[e.a].pos.toArray(), ...nodes[e.b].pos.toArray()], i * 6);
  });
  return arr;
}
const linkGeo = new THREE.BufferGeometry();
linkGeo.setAttribute("position", new THREE.BufferAttribute(edgePositions(edges), 3));
const linkMat = new THREE.LineDashedMaterial({
  color: 0x898781, transparent: true, opacity: 0.38, dashSize: 2.6, gapSize: 3.4,
});
const links = new THREE.LineSegments(linkGeo, linkMat);
links.computeLineDistances();
scene.add(links);

const hiMat = new THREE.LineDashedMaterial({
  color: 0x898781, transparent: true, opacity: 0.95, dashSize: 2.6, gapSize: 3.4,
});
let hiLines = null;
function highlightEdges(nodeIndex) {
  if (hiLines) { hiLines.geometry.dispose(); scene.remove(hiLines); hiLines = null; }
  if (nodeIndex == null) { linkMat.opacity = 0.30; return; }
  const mine = edges.filter(e => e.a === nodeIndex || e.b === nodeIndex);
  if (!mine.length) return;
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.BufferAttribute(edgePositions(mine), 3));
  hiLines = new THREE.LineSegments(g, hiMat);
  hiLines.computeLineDistances();
  scene.add(hiLines);
  linkMat.opacity = 0.10; // recede the rest while one tag is in focus
}

/* tag spheres + billboard labels */
const meshes = [];
const sphereGroup = new THREE.Group();
scene.add(sphereGroup);
nodes.forEach((n, i) => {
  const geo = new THREE.SphereGeometry(n.r, 28, 20);
  const mat = new THREE.MeshStandardMaterial({ roughness: 0.42, metalness: 0.08 });
  const mesh = new THREE.Mesh(geo, mat);
  mesh.position.copy(n.pos);
  mesh.userData = { ...n, ix: i };
  sphereGroup.add(mesh);
  meshes.push(mesh);
});

function makeLabel(text, px, colorCss, haloCss) {
  const pad = 8, font = `600 ${px}px system-ui, -apple-system, sans-serif`;
  const c = document.createElement("canvas");
  const ctx = c.getContext("2d");
  ctx.font = font;
  const w = Math.ceil(ctx.measureText(text).width) + pad * 2;
  c.width = w * 2; c.height = (px + pad * 2) * 2;
  const cx = c.getContext("2d");
  cx.scale(2, 2);
  cx.font = font;
  cx.textBaseline = "middle";
  cx.lineJoin = "round";
  cx.strokeStyle = haloCss;
  cx.lineWidth = 5;
  cx.strokeText(text, pad, (px + pad * 2) / 2);
  cx.fillStyle = colorCss;
  cx.fillText(text, pad, (px + pad * 2) / 2);
  const tex = new THREE.CanvasTexture(c);
  tex.anisotropy = 4;
  const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, transparent: true, depthTest: false }));
  const scale = 0.34;
  sp.scale.set((c.width / 2) * scale, (c.height / 2) * scale, 1);
  return sp;
}

const labelGroup = new THREE.Group();
scene.add(labelGroup);

function buildLabels() {
  labelGroup.children.forEach(sp => { sp.material.map.dispose(); sp.material.dispose(); });
  labelGroup.clear();
  const ink = V.cvar("--ink"), surface = V.cvar("--surface"), ink2 = V.cvar("--ink-2");
  for (const mesh of meshes) {
    const n = mesh.userData;
    // label the bigger tags; tooltip carries the rest (topics are dense, so a higher bar there)
    if (n.papers < (n.group === "Topics & techniques" ? 7 : 3)) continue;
    const sp = makeLabel(n.tag, 15, ink, surface);
    sp.position.copy(n.pos).add(new THREE.Vector3(0, n.r + 7, 0));
    labelGroup.add(sp);
  }
  V.TAG_GROUPS.forEach((g, gi) => {
    const sp = makeLabel(g, 21, ink2, surface);
    sp.position.copy(CLUSTER_POS[gi]).add(new THREE.Vector3(0, -80, 0));
    labelGroup.add(sp);
  });
}

const GROUP_IX = new Map(V.TAG_GROUPS.map((g, i) => [g, i]));
function applyTheme() {
  const colors = V.groupColorVars.map(vn => new THREE.Color(V.cvar(vn)));
  for (const mesh of meshes) {
    mesh.material.color.copy(colors[GROUP_IX.get(mesh.userData.group)]);
    mesh.material.emissive.set(0x000000);
  }
  starMat.color.set(V.cvar("--muted"));
  linkMat.color.set(V.cvar("--muted"));
  hiMat.color.set(V.cvar("--ink-2"));
  buildLabels();
}

/* ---------- interaction ---------- */
const ray = new THREE.Raycaster();
const ptr = new THREE.Vector2();
let hovered = null;
renderer.domElement.addEventListener("pointermove", e => {
  const rect = renderer.domElement.getBoundingClientRect();
  ptr.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
  ptr.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
  ray.setFromCamera(ptr, camera);
  const hit = ray.intersectObjects(meshes)[0];
  const mesh = hit ? hit.object : null;
  if (hovered && hovered !== mesh) {
    hovered.scale.setScalar(1);
    hovered.material.emissive.set(0x000000);
    highlightEdges(null);
    V.hideTip();
    renderer.domElement.style.cursor = "grab";
  }
  hovered = mesh;
  if (mesh) {
    mesh.scale.setScalar(1.12);
    mesh.material.emissive.copy(mesh.material.color).multiplyScalar(0.25);
    highlightEdges(mesh.userData.ix);
    renderer.domElement.style.cursor = "pointer";
    const n = mesh.userData;
    const rows = [
      { color: V.cvar(V.groupColorVars[GROUP_IX.get(n.group)]), value: n.papers, label: n.papers === 1 ? "report" : "reports" },
      { value: n.findings, label: n.findings === 1 ? "finding" : "findings" },
      { value: n.deg, label: `linked tags (≥${MIN_CO} shared reports)` },
    ];
    if (n.best) rows.push({ value: n.best.tag, label: `strongest link (${n.best.w} shared)` });
    V.showTip(e, n.tag, rows);
  }
});
renderer.domElement.addEventListener("pointerleave", () => {
  if (hovered) {
    hovered.scale.setScalar(1);
    hovered.material.emissive.set(0x000000);
    highlightEdges(null);
    hovered = null;
  }
  V.hideTip();
});
let downAt = null;
renderer.domElement.addEventListener("pointerdown", e => { downAt = [e.clientX, e.clientY]; });
renderer.domElement.addEventListener("pointerup", e => {
  if (!downAt || Math.hypot(e.clientX - downAt[0], e.clientY - downAt[1]) > 5) return; // drag, not click
  if (hovered) { V.hideTip(); V.filterTag(hovered.userData.tag); }
});
renderer.domElement.style.cursor = "grab";

/* ---------- size & loop ---------- */
function resize() {
  const w = Math.max(320, mount.clientWidth);
  renderer.setSize(w, H);
  camera.aspect = w / H;
  camera.updateProjectionMatrix();
}
new ResizeObserver(resize).observe(mount);
resize();
applyTheme();

renderer.setAnimationLoop(() => {
  controls.update();
  renderer.render(scene, camera);
});

window.TAGVIZ3D = { active: true, refresh: applyTheme };
