/* The tag universe, in 3D — orbitable sphere-cloud of tags, clustered by group.
   Falls back silently to the 2D bubble chart in app.js if WebGL is unavailable. */
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

/* ---------- layout: pack each group's tags inside a cluster sphere ---------- */
const rOf = p => 3.2 + 2.6 * Math.sqrt(p);
const CLUSTER_POS = [
  new THREE.Vector3(-150, 6, -45),
  new THREE.Vector3(145, -8, -55),
  new THREE.Vector3(0, 4, 105),
];
const nodes = [];
V.TAG_GROUPS.forEach((g, gi) => {
  const items = V.topTags.filter(t => t.group === g);
  const rand = mulberry32(1234 + gi * 999);
  const clusterR = 14 + 7.5 * Math.cbrt(items.length) * Math.cbrt(items.reduce((a, t) => a + t.papers, 0) / items.length);
  const placed = [];
  for (const t of items) {
    const r = rOf(t.papers);
    let best = null;
    for (let tries = 0; tries < 300 && !best; tries++) {
      const v = new THREE.Vector3(rand() * 2 - 1, rand() * 2 - 1, rand() * 2 - 1);
      if (v.lengthSq() > 1) continue;
      const p = v.multiplyScalar(clusterR * Math.cbrt(rand()) + clusterR * 0.25);
      if (placed.every(q => p.distanceTo(q.p) >= q.r + r + 1.5)) best = p;
    }
    if (!best) best = new THREE.Vector3(0, 0, 0).setLength(clusterR + r);
    placed.push({ p: best, r });
    nodes.push({ ...t, gi, r, pos: best.clone().add(CLUSTER_POS[gi]) });
  }
});

/* ---------- scene ---------- */
const H = 460;
mount.replaceChildren();
mount.style.position = "relative";
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(50, 1, 1, 3000);
camera.position.set(0, 60, 420);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
mount.append(renderer.domElement);
renderer.domElement.style.borderRadius = "10px";
renderer.domElement.style.touchAction = "pan-y"; // one finger scrolls the page; two fingers orbit

const hint = document.createElement("div");
hint.textContent = "drag to orbit · scroll to zoom · right-drag to pan · two fingers on touch";
hint.style.cssText = "position:absolute;left:10px;bottom:8px;font-size:11px;color:var(--muted);pointer-events:none";
mount.append(hint);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.06;
controls.minDistance = 90;
controls.maxDistance = 700;
controls.autoRotate = true;
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

/* tag spheres + billboard labels */
const meshes = [];
const sphereGroup = new THREE.Group();
scene.add(sphereGroup);
for (const n of nodes) {
  const geo = new THREE.SphereGeometry(n.r, 28, 20);
  const mat = new THREE.MeshStandardMaterial({ roughness: 0.42, metalness: 0.08 });
  const mesh = new THREE.Mesh(geo, mat);
  mesh.position.copy(n.pos);
  mesh.userData = n;
  sphereGroup.add(mesh);
  meshes.push(mesh);
}

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
const clusterLabelGroup = new THREE.Group();
scene.add(clusterLabelGroup);

function buildLabels() {
  for (const g of [labelGroup, clusterLabelGroup]) {
    g.children.forEach(sp => { sp.material.map.dispose(); sp.material.dispose(); });
    g.clear();
  }
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
    sp.position.copy(CLUSTER_POS[gi]).add(new THREE.Vector3(0, -78, 0));
    clusterLabelGroup.add(sp);
  });
}

function applyTheme() {
  const colors = V.groupColorVars.map(vn => new THREE.Color(V.cvar(vn)));
  for (const mesh of meshes) {
    mesh.material.color.copy(colors[mesh.userData.gi]);
    mesh.material.emissive.set(0x000000);
  }
  starMat.color.set(V.cvar("--muted"));
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
    V.hideTip();
    renderer.domElement.style.cursor = "grab";
  }
  hovered = mesh;
  if (mesh) {
    mesh.scale.setScalar(1.12);
    mesh.material.emissive.copy(mesh.material.color).multiplyScalar(0.25);
    renderer.domElement.style.cursor = "pointer";
    const n = mesh.userData;
    V.showTip(e, n.tag, [
      { color: V.cvar(V.groupColorVars[n.gi]), value: n.papers, label: n.papers === 1 ? "report" : "reports" },
      { value: n.findings, label: n.findings === 1 ? "finding" : "findings" },
      { value: n.group, label: "" },
    ]);
  }
});
renderer.domElement.addEventListener("pointerleave", () => {
  if (hovered) { hovered.scale.setScalar(1); hovered.material.emissive.set(0x000000); hovered = null; }
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
