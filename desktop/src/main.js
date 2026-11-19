import * as THREE from "three";
import "./style.css";

// CodePaws: stylized, warm low-poly world. Geometry is procedural so the game
// ships without large external model files and stays friendly to modest PCs.
const root = document.querySelector("#scene");
const scene = new THREE.Scene();
scene.background = new THREE.Color("#a9d9e2");
scene.fog = new THREE.FogExp2("#b9d9d5", 0.0027);

const camera = new THREE.PerspectiveCamera(55, 1, 0.1, 650);
const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.12;
root.appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight("#e8f7ff", "#667d52", 1.65));
const sun = new THREE.DirectionalLight("#fff0d2", 2.5);
sun.position.set(-48, 85, 42);
sun.castShadow = true;
sun.shadow.mapSize.set(1536, 1536);
sun.shadow.camera.left = -100;
sun.shadow.camera.right = 100;
sun.shadow.camera.top = 100;
sun.shadow.camera.bottom = -100;
sun.shadow.normalBias = 0.035;
scene.add(sun);

const mat = (color, roughness = 0.9, extra = {}) =>
  new THREE.MeshStandardMaterial({ color, roughness, ...extra });
const M = {
  grass: mat("#83b875"), grassLight: mat("#9bc985"), grassDark: mat("#608f62"),
  path: mat("#d7bd91"), pathEdge: mat("#b99a70"), water: mat("#64b8c5", 0.23, { metalness: 0.08 }),
  wood: mat("#80543b"), woodLight: mat("#b27a51"), leaf1: mat("#4d875b"),
  leaf2: mat("#6c9e68"), leaf3: mat("#86ad70"), stone: mat("#879b91"),
  cream: mat("#f1dfbd"), roof: mat("#bd7159"), glass: mat("#8ac9d2", 0.22, { metalness: 0.08 }),
  dark: mat("#31444a"), flowerPink: mat("#e9a0a3"), flowerYellow: mat("#f3d47d"),
  snow: mat("#f0f3e8")
};

function mesh(geometry, material, x = 0, y = 0, z = 0, parent = scene) {
  const o = new THREE.Mesh(geometry, material);
  o.position.set(x, y, z);
  o.castShadow = true;
  o.receiveShadow = true;
  parent.add(o);
  return o;
}
function box(parent, x, y, z, w, h, d, material, bevel = false) {
  const g = new THREE.BoxGeometry(w, h, d);
  if (bevel) {
    const e = new THREE.EdgesGeometry(g);
    const o = mesh(g, material, x, y, z, parent);
    const lines = new THREE.LineSegments(e, new THREE.LineBasicMaterial({ color: "#ffffff", transparent: true, opacity: 0.1 }));
    o.add(lines);
    return o;
  }
  return mesh(g, material, x, y, z, parent);
}
function cylinder(parent, x, y, z, rTop, rBottom, h, material, sides = 9) {
  return mesh(new THREE.CylinderGeometry(rTop, rBottom, h, sides), material, x, y, z, parent);
}
function sphere(parent, x, y, z, sx, sy, sz, material, detail = 12) {
  const o = mesh(new THREE.SphereGeometry(1, detail, Math.max(8, detail - 2)), material, x, y, z, parent);
  o.scale.set(sx, sy, sz);
  return o;
}
function group(parent = scene, x = 0, y = 0, z = 0) {
  const g = new THREE.Group();
  g.position.set(x, y, z);
  parent.add(g);
  return g;
}
function curveTube(points, radius, material, parent = scene, segments = 80) {
  const curve = new THREE.CatmullRomCurve3(points.map(p => new THREE.Vector3(...p)));
  return mesh(new THREE.TubeGeometry(curve, segments, radius, 7, false), material, 0, 0, 0, parent);
}
function seeded(n) {
  const x = Math.sin(n * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x);
}

// Soft rolling terrain with subtle vertex variation.
const groundGeo = new THREE.PlaneGeometry(300, 300, 72, 72);
const pos = groundGeo.attributes.position;
for (let i = 0; i < pos.count; i++) {
  const x = pos.getX(i), y = pos.getY(i);
  pos.setZ(i, Math.sin(x * 0.045) * 0.22 + Math.cos(y * 0.052) * 0.2 + Math.sin((x + y) * 0.025) * 0.24);
}
groundGeo.computeVertexNormals();
const ground = mesh(groundGeo, M.grass, 0, -0.12, 0);
ground.rotation.x = -Math.PI / 2;
ground.receiveShadow = true;

// Curving roads with lighter shoulders and small stone edging.
function road(points, width) {
  const curve = new THREE.CatmullRomCurve3(points.map(p => new THREE.Vector3(p[0], 0.012, p[1])));
  const geometry = new THREE.ExtrudeGeometry(new THREE.Shape([
    new THREE.Vector2(-width / 2, 0), new THREE.Vector2(width / 2, 0),
    new THREE.Vector2(width / 2, 0.06), new THREE.Vector2(-width / 2, 0.06)
  ]), { steps: 100, bevelEnabled: false, extrudePath: curve });
  const roadMesh = mesh(geometry, M.path);
  roadMesh.receiveShadow = true;
}
road([[-2, 80], [0, 40], [1, 5], [0, -25], [-12, -60], [-28, -105]], 8);
road([[-90, -18], [-48, -12], [-12, -10], [25, -14], [78, -24]], 6);
road([[0, -12], [26, -5], [52, 10], [78, 25]], 5);

// Lake, pebble shore, reeds and a little wooden pier.
const lake = mesh(new THREE.CircleGeometry(16, 64), M.water, 31, 0.035, 15);
lake.rotation.x = -Math.PI / 2;
lake.scale.set(1.3, 0.78, 1);
const shoreMat = mat("#c6b68e");
const shore = mesh(new THREE.RingGeometry(15.8, 17.5, 64), shoreMat, 31, 0.025, 15);
shore.rotation.x = -Math.PI / 2;
shore.scale.set(1.3, 0.78, 1);
const pier = group(scene, 31, 0.22, 0);
box(pier, 0, 0.15, -10, 4.2, 0.3, 11, M.woodLight);
for (let i = -1; i <= 1; i += 2) {
  for (let z = -14; z <= -7; z += 3.2) cylinder(pier, i * 1.55, -0.35, z, 0.14, 0.16, 1.4, M.wood, 8);
}
for (let i = 0; i < 22; i++) {
  const a = i * 2.399;
  const r = 16 + seeded(i) * 2;
  const x = 31 + Math.cos(a) * r * 1.28;
  const z = 15 + Math.sin(a) * r * 0.78;
  if (i % 2 === 0) {
    cylinder(scene, x, 0.38, z, 0.045, 0.07, 0.8, M.grassDark, 5).rotation.z = seeded(i + 9) * 0.3;
    sphere(scene, x, 0.78, z, 0.16, 0.12, 0.16, i % 4 ? M.flowerYellow : M.flowerPink, 8);
  }
}

// Detailed low-poly trees: trunk, layered crowns, branch hints and roots.
function tree(x, z, scale = 1, variant = 0) {
  const t = group(scene, x, 0, z);
  cylinder(t, 0, 1.25 * scale, 0, 0.25 * scale, 0.38 * scale, 2.5 * scale, M.wood, 8);
  for (let k = 0; k < 3; k++) {
    const a = k * Math.PI * 2 / 3;
    const branch = cylinder(t, Math.cos(a) * 0.38 * scale, (1.75 + k * 0.18) * scale, Math.sin(a) * 0.38 * scale, 0.09 * scale, 0.14 * scale, 1.15 * scale, M.woodLight, 6);
    branch.rotation.z = Math.cos(a) * -0.55;
    branch.rotation.x = Math.sin(a) * 0.55;
  }
  const crownMat = [M.leaf1, M.leaf2, M.leaf3][variant % 3];
  const crown = sphere(t, 0, 3.05 * scale, 0, 1.35 * scale, 1.42 * scale, 1.25 * scale, crownMat, 9);
  crown.rotation.y = seeded(Math.round(x * 4 + z)) * 2;
  sphere(t, -0.72 * scale, 2.75 * scale, 0.1 * scale, 0.82 * scale, 0.88 * scale, 0.82 * scale, crownMat, 8);
  sphere(t, 0.68 * scale, 2.8 * scale, -0.18 * scale, 0.85 * scale, 0.9 * scale, 0.82 * scale, crownMat, 8);
  return t;
}

// A small collection of different house silhouettes with doors, windows,
// roof trim, chimneys, flower boxes and porch posts.
function house(x, z, wallColor = "#f0d9ad", scale = 1, roofColor = "#bd7159", rotation = 0) {
  const h = group(scene, x, 0, z);
  h.rotation.y = rotation;
  const wall = mat(wallColor);
  const roof = mat(roofColor);
  box(h, 0, 1.65 * scale, 0, 7 * scale, 3.3 * scale, 6 * scale, wall);
  // Gable roof made from two broad sloping planes.
  const roofA = box(h, -1.78 * scale, 3.55 * scale, 0, 4.25 * scale, 0.22 * scale, 6.8 * scale, roof);
  roofA.rotation.z = -0.66;
  const roofB = box(h, 1.78 * scale, 3.55 * scale, 0, 4.25 * scale, 0.22 * scale, 6.8 * scale, roof);
  roofB.rotation.z = 0.66;
  box(h, 0, 1.08 * scale, -3.06 * scale, 1.15 * scale, 2.15 * scale, 0.13 * scale, M.wood);
  sphere(h, 0.34 * scale, 1.08 * scale, -3.15 * scale, 0.055 * scale, 0.055 * scale, 0.035 * scale, M.flowerYellow, 8);
  for (const wx of [-2.05, 2.05]) {
    box(h, wx * scale, 2.12 * scale, -3.08 * scale, 1.25 * scale, 1.05 * scale, 0.13 * scale, M.glass);
    box(h, wx * scale, 2.12 * scale, -3.17 * scale, 0.09 * scale, 1.18 * scale, 0.08 * scale, M.cream);
    box(h, wx * scale, 2.12 * scale, -3.17 * scale, 1.36 * scale, 0.09 * scale, 0.08 * scale, M.cream);
    box(h, wx * scale, 1.52 * scale, -3.25 * scale, 1.5 * scale, 0.18 * scale, 0.42 * scale, M.woodLight);
    for (let j = 0; j < 3; j++) sphere(h, (wx - 0.42 + j * 0.42) * scale, 1.78 * scale, -3.3 * scale, 0.13 * scale, 0.12 * scale, 0.13 * scale, j % 2 ? M.flowerPink : M.flowerYellow, 7);
  }
  box(h, 2.55 * scale, 4.15 * scale, 1.3 * scale, 0.85 * scale, 1.6 * scale, 0.9 * scale, M.wood);
  cylinder(h, 2.55 * scale, 5.05 * scale, 1.3 * scale, 0.48 * scale, 0.48 * scale, 0.25 * scale, M.stone, 8);
  // Porch canopy and posts.
  box(h, 0, 2.48 * scale, -4.0 * scale, 3.1 * scale, 0.2 * scale, 2.0 * scale, roof);
  for (const px of [-1.35, 1.35]) cylinder(h, px * scale, 1.2 * scale, -4.65 * scale, 0.075 * scale, 0.075 * scale, 2.4 * scale, M.cream, 7);
  return h;
}

// Mountain ranges with layered ridges, angular rock faces and snow caps.
function mountain(x, z, radius, height, color, seed) {
  const g = new THREE.ConeGeometry(radius, height, 7, 3);
  const p = g.attributes.position;
  for (let i = 0; i < p.count; i++) {
    const y = p.getY(i);
    const wobble = 1 + 0.1 * Math.sin(i * 8.31 + seed) + 0.05 * Math.cos(i * 3.7 + seed);
    p.setX(i, p.getX(i) * wobble);
    p.setZ(i, p.getZ(i) * wobble);
    if (y < height * 0.25 - height / 2) p.setY(i, y + Math.sin(i * 4 + seed) * 0.7);
  }
  g.computeVertexNormals();
  const m = mesh(g, mat(color, 1, { flatShading: true }), x, height / 2 - 0.3, z);
  m.rotation.y = seed;
  const cap = mesh(new THREE.ConeGeometry(radius * 0.31, height * 0.24, 7, 1), M.snow, x - radius * 0.05, height * 0.88, z - radius * 0.03);
  cap.rotation.y = seed;
  // Rock outcrops at the base.
  for (let i = 0; i < 4; i++) {
    const a = i * Math.PI / 2 + seed;
    const rock = sphere(scene, x + Math.cos(a) * radius * 0.72, 1.3, z + Math.sin(a) * radius * 0.72, radius * 0.22, 1.5, radius * 0.24, M.stone, 7);
    rock.rotation.z = seeded(i + seed) * 0.35;
  }
}

// Town square, benches, lanterns, fences, shrubs and colorful planting.
house(-13, -7, "#f2d7a7", 1.22, "#bd7159", 0.02);
house(14, -25, "#d7e5d0", 1.05, "#6f8e75", -0.08);
house(-27, -27, "#e9c5b5", 0.92, "#8c7185", 0.12);
house(30, -8, "#f1e3c1", 0.92, "#bd815d", -0.12);
house(-51, -42, "#e8c6a8", 0.82, "#8b6e60");
house(-31, -49, "#d3dfcb", 0.82, "#b66f59");
house(-9, -46, "#e8d9ad", 0.82, "#748b70");
house(15, -49, "#d9d8eb", 0.82, "#8b789b");
house(39, -42, "#e9c6b5", 0.82, "#b66f59");

const square = group(scene, 2, 0, -15);
box(square, 0, 0.06, 0, 15, 0.12, 13, M.path);
cylinder(square, 0, 0.4, 0, 1.6, 1.9, 0.65, M.stone, 12);
cylinder(square, 0, 1.0, 0, 0.18, 0.25, 1.0, M.stone, 9);
sphere(square, 0, 1.62, 0, 0.58, 0.48, 0.58, M.water, 12);
for (let i = 0; i < 4; i++) {
  const a = i * Math.PI / 2;
  const bench = group(square, Math.cos(a) * 5.5, 0, Math.sin(a) * 4.6);
  box(bench, 0, 0.65, 0, 2.5, 0.18, 0.65, M.woodLight);
  for (const bx of [-0.9, 0.9]) box(bench, bx, 0.35, 0, 0.16, 0.55, 0.55, M.wood);
}
function lamp(x, z) {
  const l = group(scene, x, 0, z);
  cylinder(l, 0, 1.65, 0, 0.08, 0.12, 3.3, M.dark, 8);
  sphere(l, 0, 3.45, 0, 0.42, 0.48, 0.42, M.cream, 8);
  const glow = new THREE.PointLight("#ffe4a8", 0.5, 9);
  glow.position.set(0, 3.45, 0);
  l.add(glow);
}
for (const p of [[-8,-19],[12,-19],[-8,-4],[12,-4],[-42,-20],[48,-28]]) lamp(...p);

// Dense but deliberately irregular tree belts and scattered flower patches.
for (let i = 0; i < 105; i++) {
  const x = -112 + seeded(i + 2) * 224;
  const z = -112 + seeded(i + 117) * 224;
  const nearTown = x > -62 && x < 48 && z > -58 && z < 8;
  const nearLake = Math.abs((x - 31) / 1.3) < 23 && Math.abs((z - 15) / 0.78) < 23;
  const nearRoad = Math.abs(x) < 6 || (Math.abs(z + 12) < 5 && x > -90 && x < 80);
  if (!nearTown && !nearLake && !nearRoad) tree(x, z, 0.7 + seeded(i + 8) * 0.85, i % 3);
}
for (let i = 0; i < 65; i++) {
  const x = -65 + seeded(i + 301) * 130;
  const z = -70 + seeded(i + 410) * 130;
  if (Math.abs(x) < 8 && z > -65 && z < 70) continue;
  const flower = sphere(scene, x, 0.23, z, 0.12, 0.11, 0.12, i % 3 ? M.flowerYellow : M.flowerPink, 7);
  flower.castShadow = false;
  cylinder(scene, x, 0.12, z, 0.025, 0.035, 0.24, M.grassDark, 5);
}
for (let i = 0; i < 9; i++) {
  const x = -118 + i * 29;
  mountain(x, -133 - seeded(i + 501) * 14, 20 + seeded(i + 511) * 10, 48 + seeded(i + 521) * 34, ["#789b8d", "#849f91", "#91aa9c"][i % 3], seeded(i + 531) * 2);
  mountain(x + 13, 132, 24, 58 + seeded(i + 541) * 28, "#78968c", seeded(i + 551) * 2);
}

// Distant fluffy clouds: low-cost layered spheres.
const cloudMat = new THREE.MeshStandardMaterial({ color: "#f3f6e9", roughness: 1, transparent: true, opacity: 0.82 });
for (let i = 0; i < 13; i++) {
  const c = group(scene, -130 + i * 22, 43 + seeded(i + 610) * 17, -105 + seeded(i + 620) * 190);
  for (let j = 0; j < 4; j++) sphere(c, (j - 1.5) * 2.3, seeded(i * 5 + j) * 1.2, 0, 2.8, 1.1 + seeded(j + i) * 0.5, 1.7, cloudMat, 9).castShadow = false;
}

// Player avatar with layered clothing, face, hair and a small backpack.
const player = group(scene, 0, 0, 12);
const skin = mat("#efc49e");
const outfit = mat("#e5a85f");
const pants = mat("#526d7c");
const hair = mat("#594b43");
sphere(player, 0, 1.42, 0, 0.47, 0.57, 0.35, outfit, 14);
sphere(player, 0, 2.12, -0.015, 0.4, 0.43, 0.37, skin, 14);
sphere(player, 0, 2.43, 0.04, 0.43, 0.22, 0.39, hair, 12);
sphere(player, -0.39, 2.12, 0.02, 0.12, 0.19, 0.12, skin, 9);
sphere(player, 0.39, 2.12, 0.02, 0.12, 0.19, 0.12, skin, 9);
for (const x of [-0.14, 0.14]) sphere(player, x, 2.12, -0.35, 0.055, 0.075, 0.035, M.dark, 8);
curveTube([[0,1.98,-0.36],[0.08,1.94,-0.38],[0.16,1.98,-0.36]], 0.025, mat("#a75e53"), player, 8);
sphere(player, 0, 1.45, 0.38, 0.3, 0.42, 0.2, mat("#8b6752"), 10);
for (const x of [-0.22, 0.22]) {
  const leg = cylinder(player, x, 0.52, 0, 0.14, 0.17, 0.82, pants, 8);
  leg.rotation.z = x * 0.16;
  sphere(player, x, 0.13, -0.06, 0.2, 0.13, 0.32, M.dark, 9);
}
for (const x of [-0.55, 0.55]) {
  const arm = cylinder(player, x, 1.42, 0, 0.12, 0.15, 0.72, outfit, 8);
  arm.rotation.z = x * 0.5;
}

// Distinct mascot silhouettes: each friend gets its own ears, fins, tail,
// antennae or shell details instead of sharing one generic blob.
const petData = [
  ["Py", "#55a86b", "snake"], ["Ferris", "#d66b54", "crab"], ["Gopher", "#66a9c8", "gopher"], ["Duke", "#d9a05c", "coffee"],
  ["Moby", "#5aaac7", "whale"], ["Mona", "#a78ac9", "octopus"], ["Tanuki", "#d48c57", "raccoon"], ["ElePHPant", "#8e9bd4", "elephant"],
  ["Kodee", "#a18bdb", "robot"], ["Camel", "#b88b62", "camel"]
];
const pets = petData.map(([name, color, kind], i) => {
  const g = group(scene, -7 + (i % 5) * 3.5, 0, -2 - Math.floor(i / 5) * 5);
  const bodyMat = mat(color, 0.72);
  const creamMat = mat("#f7e9ce");
  sphere(g, 0, 0.72, 0, 0.62, 0.58, 0.55, bodyMat, 14);
  sphere(g, 0, 1.34, -0.06, 0.43, 0.43, 0.4, bodyMat, 14);
  // Friendly eyes and muzzle.
  for (const ex of [-0.16, 0.16]) sphere(g, ex, 1.4, -0.42, 0.065, 0.085, 0.04, M.dark, 9);
  sphere(g, 0, 1.19, -0.43, 0.19, 0.13, 0.1, creamMat, 10);
  sphere(g, 0, 1.24, -0.525, 0.055, 0.045, 0.035, M.dark, 8);
  // Four tiny feet.
  for (const fx of [-0.34, 0.34]) for (const fz of [-0.28, 0.28]) sphere(g, fx, 0.18, fz, 0.16, 0.18, 0.17, bodyMat, 8);
  if (kind === "snake") {
    sphere(g, 0, 1.72, 0.1, 0.2, 0.34, 0.2, bodyMat, 10);
    const tail = curveTube([[0,0.5,0.4],[0.4,0.35,0.7],[0.65,0.2,0.9],[0.9,0.28,0.75]], 0.13, bodyMat, g, 16);
    tail.castShadow = true;
  } else if (kind === "crab") {
    for (const sx of [-1,1]) {
      const claw = sphere(g, sx * 0.78, 1.45, 0, 0.25, 0.22, 0.22, bodyMat, 9);
      const arm = cylinder(g, sx * 0.62, 1.25, 0, 0.09, 0.1, 0.5, bodyMat, 7); arm.rotation.z = sx * 0.7;
      cylinder(g, sx * 0.26, 1.82, -0.05, 0.045, 0.055, 0.35, bodyMat, 7);
      sphere(g, sx * 0.26, 2.02, -0.05, 0.11, 0.11, 0.11, creamMat, 8);
    }
    sphere(g, 0, 0.78, 0.4, 0.45, 0.3, 0.25, mat("#f1a17e"), 10);
  } else if (kind === "gopher") {
    for (const sx of [-1,1]) sphere(g, sx * 0.3, 1.73, -0.04, 0.16, 0.24, 0.14, bodyMat, 9);
    sphere(g, 0, 0.85, -0.48, 0.2, 0.18, 0.12, creamMat, 9);
  } else if (kind === "coffee") {
    cylinder(g, 0, 1.48, -0.03, 0.4, 0.36, 0.65, creamMat, 12);
    cylinder(g, 0, 1.83, -0.03, 0.39, 0.39, 0.08, mat("#8d5a3d"), 12);
    const handle = mesh(new THREE.TorusGeometry(0.22, 0.07, 8, 14), creamMat, 0.43, 1.48, -0.03, g);
    handle.rotation.y = Math.PI / 2;
    cylinder(g, 0.08, 2.0, -0.03, 0.035, 0.035, 0.4, mat("#f5f0dc"), 7).rotation.z = 0.5;
  } else if (kind === "whale") {
    sphere(g, 0, 1.2, 0.5, 0.42, 0.13, 0.65, bodyMat, 10);
    const fin = mesh(new THREE.ConeGeometry(0.27, 0.65, 5), bodyMat, 0, 1.0, 0.62, g); fin.rotation.x = 1.3;
    for (const sx of [-1,1]) {
      const flipper = mesh(new THREE.ConeGeometry(0.22, 0.72, 5), bodyMat, sx * 0.6, 0.55, 0.12, g);
      flipper.rotation.z = sx * 1.1; flipper.rotation.x = 0.5;
    }
  } else if (kind === "octopus") {
    for (let t = 0; t < 8; t++) {
      const a = t * Math.PI / 4;
      curveTube([[Math.cos(a)*0.25,0.52,Math.sin(a)*0.25],[Math.cos(a)*0.58,0.25,Math.sin(a)*0.58],[Math.cos(a)*0.82,0.16,Math.sin(a)*0.82]], 0.09, bodyMat, g, 10);
    }
  } else if (kind === "raccoon") {
    for (const sx of [-1,1]) sphere(g, sx * 0.27, 1.72, 0, 0.16, 0.25, 0.13, bodyMat, 8);
    sphere(g, 0, 0.62, 0.57, 0.18, 0.18, 0.5, mat("#66545a"), 10);
    for (let s = 0; s < 3; s++) sphere(g, 0, 0.58, 0.32 + s * 0.2, 0.19, 0.19, 0.08, s % 2 ? creamMat : M.dark, 8);
    for (const sx of [-1,1]) sphere(g, sx * 0.16, 1.4, -0.44, 0.12, 0.09, 0.035, M.dark, 8);
  } else if (kind === "elephant") {
    for (const sx of [-1,1]) sphere(g, sx * 0.48, 1.3, -0.05, 0.28, 0.34, 0.12, bodyMat, 9);
    curveTube([[0,1.2,-0.42],[0,0.92,-0.62],[0.12,0.7,-0.62],[0.2,0.78,-0.62]], 0.14, bodyMat, g, 14);
    sphere(g, 0.02, 1.73, 0.02, 0.12, 0.12, 0.12, creamMat, 8);
  } else if (kind === "robot") {
    const screen = box(g, 0, 1.35, -0.42, 0.52, 0.32, 0.08, mat("#9fe2d4"));
    screen.material.emissive = new THREE.Color("#397c70");
    cylinder(g, 0, 1.86, 0, 0.035, 0.035, 0.42, bodyMat, 7);
    sphere(g, 0, 2.1, 0, 0.12, 0.12, 0.12, M.flowerYellow, 8);
    for (const sx of [-1,1]) box(g, sx * 0.7, 0.8, 0, 0.2, 0.6, 0.22, bodyMat);
  } else if (kind === "camel") {
    sphere(g, -0.2, 1.28, 0.15, 0.22, 0.32, 0.22, bodyMat, 9);
    sphere(g, 0.22, 1.28, 0.15, 0.22, 0.32, 0.22, bodyMat, 9);
    curveTube([[0,1.0,0],[0.15,1.5,0],[0.38,1.7,0],[0.48,1.45,0]], 0.16, bodyMat, g, 12);
    sphere(g, 0.5, 1.45, -0.03, 0.28, 0.22, 0.24, bodyMat, 9);
    for (const sx of [-1,1]) sphere(g, sx * 0.27, 1.72, -0.02, 0.08, 0.18, 0.08, bodyMat, 8);
  }
  g.userData.kind = kind;
  return { name, kind, group: g, hunger: 18, happiness: 86 };
});

// Camera and movement: independent yaw, no camera snapping on keyboard input.
let yaw = 0;
let pitch = 0.27;
let dragging = false;
let lastX = 0, lastY = 0;
const keys = new Set();
window.addEventListener("keydown", e => {
  if (["KeyW","KeyA","KeyS","KeyD","ArrowUp","ArrowDown","ArrowLeft","ArrowRight"].includes(e.code)) {
    keys.add(e.code); e.preventDefault();
  }
});
window.addEventListener("keyup", e => keys.delete(e.code));
window.addEventListener("blur", () => keys.clear());
renderer.domElement.addEventListener("pointerdown", e => {
  dragging = true; lastX = e.clientX; lastY = e.clientY;
  renderer.domElement.setPointerCapture(e.pointerId);
});
renderer.domElement.addEventListener("pointerup", () => dragging = false);
renderer.domElement.addEventListener("pointercancel", () => dragging = false);
renderer.domElement.addEventListener("pointermove", e => {
  if (!dragging) return;
  yaw -= (e.clientX - lastX) * 0.0032;
  pitch = THREE.MathUtils.clamp(pitch + (e.clientY - lastY) * 0.0025, -0.08, 0.8);
  lastX = e.clientX; lastY = e.clientY;
});

const target = new THREE.Vector3();
const clock = new THREE.Clock();
function resize() {
  const w = root.clientWidth || window.innerWidth;
  const h = root.clientHeight || window.innerHeight;
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  renderer.setSize(w, h, false);
}
window.addEventListener("resize", resize);
resize();

let selectedPet = 0;
let saved = {};
try { saved = JSON.parse(localStorage.getItem("codepaws-save") || "{}"); } catch { saved = {}; }
if (Number.isInteger(saved.selectedPet)) selectedPet = THREE.MathUtils.clamp(saved.selectedPet, 0, pets.length - 1);
if (Array.isArray(saved.pets)) {
  for (const state of saved.pets) {
    const pet = pets.find(p => p.name === state.name);
    if (pet) { pet.hunger = state.hunger ?? pet.hunger; pet.happiness = state.happiness ?? pet.happiness; }
  }
}
function showPet() {
  const pet = pets[selectedPet];
  document.querySelector("#pet-name").textContent = pet.name;
  document.querySelector("#pet-avatar").textContent = ({Py:"🐍",Ferris:"🦀",Gopher:"🐹",Duke:"☕",Moby:"🐳",Mona:"🐙",Tanuki:"🦝",ElePHPant:"🐘",Kodee:"🤖",Camel:"🐪"})[pet.name] || "🐾";
  document.querySelector("#pet-mood").textContent = pet.hunger > 65 ? "Tiene un poquito de hambre" : "Con ganas de explorar";
}
showPet();
function saveGame() {
  localStorage.setItem("codepaws-save", JSON.stringify({
    selectedPet,
    pets: pets.map(p => ({ name: p.name, hunger: p.hunger, happiness: p.happiness }))
  }));
}
document.querySelector("#feed-button").addEventListener("click", () => {
  const pet = pets[selectedPet];
  pet.hunger = Math.max(0, pet.hunger - 28);
  pet.happiness = Math.min(100, pet.happiness + 5);
  document.querySelector("#pet-mood").textContent = pet.name + " disfrutó su snack ✨";
  const toast = document.querySelector("#toast");
  toast.textContent = "¡Qué rico! " + pet.name + " está más feliz.";
  toast.classList.add("visible");
  window.setTimeout(() => toast.classList.remove("visible"), 2200);
  saveGame();
});
document.querySelector("#sound-toggle").addEventListener("click", e => {
  e.currentTarget.classList.toggle("muted");
  e.currentTarget.textContent = e.currentTarget.classList.contains("muted") ? "♪" : "♫";
});

function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.04);
  const forward = new THREE.Vector3(-Math.sin(yaw), 0, -Math.cos(yaw));
  const right = new THREE.Vector3(Math.cos(yaw), 0, -Math.sin(yaw));
  const move = new THREE.Vector3();
  if (keys.has("KeyW") || keys.has("ArrowUp")) move.add(forward);
  if (keys.has("KeyS") || keys.has("ArrowDown")) move.sub(forward);
  if (keys.has("KeyD") || keys.has("ArrowRight")) move.add(right);
  if (keys.has("KeyA") || keys.has("ArrowLeft")) move.sub(right);
  if (move.lengthSq() > 0) {
    move.normalize().multiplyScalar(8.2 * dt);
    player.position.add(move);
    player.rotation.y = Math.atan2(move.x, move.z);
  }
  player.position.x = THREE.MathUtils.clamp(player.position.x, -132, 132);
  player.position.z = THREE.MathUtils.clamp(player.position.z, -132, 132);
  pets.forEach((pet, i) => {
    pet.group.position.y = Math.sin(clock.elapsedTime * 2.0 + i * 0.7) * 0.055;
    pet.group.rotation.y = Math.sin(clock.elapsedTime * 0.45 + i) * 0.16;
  });
  target.copy(player.position).add(new THREE.Vector3(0, 1.2, 0));
  const distance = 10.5;
  camera.position.set(
    target.x + Math.sin(yaw) * Math.cos(pitch) * distance,
    target.y + Math.sin(pitch) * distance + 2.0,
    target.z + Math.cos(yaw) * Math.cos(pitch) * distance
  );
  camera.lookAt(target);
  renderer.render(scene, camera);
}
animate();
