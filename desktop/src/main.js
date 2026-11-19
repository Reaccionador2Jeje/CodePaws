import * as THREE from "three";
import "./style.css";

const root = document.querySelector("#scene");
const scene = new THREE.Scene();
scene.background = new THREE.Color("#a8d5dc");
scene.fog = new THREE.Fog("#a8d5dc", 75, 230);

const camera = new THREE.PerspectiveCamera(58, 1, 0.1, 500);
const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "low-power" });
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.6));
renderer.shadowMap.enabled = false;
renderer.outputColorSpace = THREE.SRGBColorSpace;
root.appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight("#e7f8ff", "#647b53", 2.0));
const sun = new THREE.DirectionalLight("#fff0ce", 2.2);
sun.position.set(-35, 65, 25);
scene.add(sun);

const mats = {
  grass: new THREE.MeshStandardMaterial({ color: "#82ad72", roughness: 1 }),
  path: new THREE.MeshStandardMaterial({ color: "#d8bd91", roughness: 1 }),
  water: new THREE.MeshStandardMaterial({ color: "#69b9c6", roughness: 0.3, metalness: 0.05 }),
  wood: new THREE.MeshStandardMaterial({ color: "#98694c" }),
  leaf: new THREE.MeshStandardMaterial({ color: "#477c58" }),
  roof: new THREE.MeshStandardMaterial({ color: "#c9785c" }),
  wall: new THREE.MeshStandardMaterial({ color: "#f0d9ad" }),
  stone: new THREE.MeshStandardMaterial({ color: "#a2b2aa" })
};

function addMesh(geometry, material, x, y, z, parent = scene) {
  const mesh = new THREE.Mesh(geometry, material);
  mesh.position.set(x, y, z);
  parent.add(mesh);
  return mesh;
}
function box(x, y, z, w, h, d, color, parent = scene) {
  return addMesh(new THREE.BoxGeometry(w, h, d), new THREE.MeshStandardMaterial({ color, roughness: 0.9 }), x, y, z, parent);
}
function tree(x, z, scale = 1) {
  addMesh(new THREE.CylinderGeometry(0.22 * scale, 0.3 * scale, 2.2 * scale, 7), mats.wood, x, 1.1 * scale, z);
  const crown = new THREE.MeshStandardMaterial({ color: ["#477c58", "#5b9060", "#6d9e68"][Math.floor(Math.random() * 3)] });
  addMesh(new THREE.IcosahedronGeometry(1.25 * scale, 1), crown, x, 2.65 * scale, z);
  addMesh(new THREE.IcosahedronGeometry(0.8 * scale, 1), crown, x + 0.55 * scale, 2.25 * scale, z + 0.2 * scale);
}
function house(x, z, color = "#f0d9ad", scale = 1) {
  box(x, 1.65 * scale, z, 6 * scale, 3.3 * scale, 5 * scale, color);
  const roof = addMesh(new THREE.ConeGeometry(4.7 * scale, 2.7 * scale, 4), new THREE.MeshStandardMaterial({ color: "#bd7159" }), x, 4.45 * scale, z);
  roof.rotation.y = Math.PI / 4;
  box(x, 1.05 * scale, z - 2.53 * scale, 1.05 * scale, 2.1 * scale, 0.12 * scale, "#81583f");
  box(x - 1.7 * scale, 2.1 * scale, z - 2.57 * scale, 1.1 * scale, 0.9 * scale, 0.1 * scale, "#83c3d0");
}
function mountain(x, z, radius, height, color) {
  const geometry = new THREE.ConeGeometry(radius, height, 7, 1);
  const mesh = addMesh(geometry, new THREE.MeshStandardMaterial({ color, flatShading: true }), x, height / 2 - 1, z);
  mesh.rotation.y = Math.random() * 1.5;
  const snow = addMesh(new THREE.ConeGeometry(radius * 0.26, height * 0.22, 7), new THREE.MeshStandardMaterial({ color: "#e7f0e9", flatShading: true }), x, height * 0.88, z);
  snow.rotation.y = mesh.rotation.y;
}

addMesh(new THREE.PlaneGeometry(260, 260), mats.grass, 0, -0.08, 0).rotation.x = -Math.PI / 2;
box(0, 0.015, 8, 8, 0.05, 130, "#d8bd91");
box(0, 0.02, -12, 95, 0.05, 7, "#d8bd91");
addMesh(new THREE.CircleGeometry(11, 32), mats.water, 27, 0.02, 14).rotation.x = -Math.PI / 2;
for (let i = 0; i < 13; i++) {
  const angle = (i / 13) * Math.PI * 2;
  tree(27 + Math.cos(angle) * 14, 14 + Math.sin(angle) * 12, 0.8 + Math.random() * 0.35);
}
house(-12, -5, "#f3d5a5", 1.25);
house(14, -23, "#d6e5d4", 1);
house(-24, -24, "#e9c5b4", 0.9);
house(28, -9, "#f1e2bd", 0.9);
for (let i = 0; i < 7; i++) {
  const x = -43 + i * 13;
  house(x, -39 - (i % 2) * 8, ["#e8c6a8", "#d3dfcb", "#e8d9ad"][i % 3], 0.8);
}
for (let i = 0; i < 10; i++) {
  const side = i % 2 ? 1 : -1;
  tree(side * (13 + Math.random() * 58), -60 + Math.random() * 120, 0.75 + Math.random() * 0.7);
}
for (let i = 0; i < 11; i++) {
  const x = -115 + i * 23;
  mountain(x, -104 - Math.random() * 15, 15 + Math.random() * 9, 35 + Math.random() * 25, ["#789b8d", "#849f91", "#91aa9c"][i % 3]);
  mountain(x + 10, 105, 18, 42 + Math.random() * 20, "#78968c");
}

const player = new THREE.Group();
const playerBody = addMesh(new THREE.CapsuleGeometry(0.48, 0.75, 4, 8), new THREE.MeshStandardMaterial({ color: "#e8b875" }), 0, 0.85, 0, player);
const playerHead = addMesh(new THREE.SphereGeometry(0.42, 16, 12), new THREE.MeshStandardMaterial({ color: "#f6d3ad" }), 0, 1.75, 0, player);
addMesh(new THREE.SphereGeometry(0.075, 8, 8), new THREE.MeshStandardMaterial({ color: "#28343a" }), -0.14, 1.8, -0.36, player);
addMesh(new THREE.SphereGeometry(0.075, 8, 8), new THREE.MeshStandardMaterial({ color: "#28343a" }), 0.14, 1.8, -0.36, player);
player.position.set(0, 0, 12);
scene.add(player);

const petData = [
  ["Py", "#55a86b"], ["Ferris", "#d66b54"], ["Gopher", "#66a9c8"], ["Duke", "#d9a05c"],
  ["Moby", "#5aaac7"], ["Mona", "#a78ac9"], ["Tanuki", "#d48c57"], ["ElePHPant", "#8e9bd4"],
  ["Kodee", "#a18bdb"], ["Camel", "#b88b62"]
];
const pets = petData.map(([name, color], i) => {
  const group = new THREE.Group();
  const material = new THREE.MeshStandardMaterial({ color, roughness: 0.78 });
  addMesh(new THREE.SphereGeometry(0.58, 16, 12), material, 0, 0.62, 0, group);
  addMesh(new THREE.SphereGeometry(0.38, 16, 12), material, 0, 1.18, -0.08, group);
  const eyeMat = new THREE.MeshStandardMaterial({ color: "#243039" });
  addMesh(new THREE.SphereGeometry(0.055, 8, 8), eyeMat, -0.13, 1.22, -0.41, group);
  addMesh(new THREE.SphereGeometry(0.055, 8, 8), eyeMat, 0.13, 1.22, -0.41, group);
  group.position.set(-5 + (i % 5) * 2.5, 0, -1 - Math.floor(i / 5) * 4);
  scene.add(group);
  return { name, group, hunger: 18, happiness: 86 };
});

let yaw = 0;
let pitch = 0.32;
let dragging = false;
let lastX = 0;
let lastY = 0;
const keys = new Set();
window.addEventListener("keydown", e => { if (["KeyW","KeyA","KeyS","KeyD","ArrowUp","ArrowDown","ArrowLeft","ArrowRight"].includes(e.code)) { keys.add(e.code); e.preventDefault(); } });
window.addEventListener("keyup", e => keys.delete(e.code));
renderer.domElement.addEventListener("pointerdown", e => { dragging = true; lastX = e.clientX; lastY = e.clientY; renderer.domElement.setPointerCapture(e.pointerId); });
renderer.domElement.addEventListener("pointerup", () => dragging = false);
renderer.domElement.addEventListener("pointermove", e => {
  if (!dragging) return;
  yaw -= (e.clientX - lastX) * 0.004;
  pitch = THREE.MathUtils.clamp(pitch + (e.clientY - lastY) * 0.003, -0.05, 0.85);
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
const saved = JSON.parse(localStorage.getItem("codepaws-save") || "{}");
if (Number.isInteger(saved.selectedPet)) selectedPet = Math.max(0, Math.min(pets.length - 1, saved.selectedPet));
function showPet() {
  const pet = pets[selectedPet];
  document.querySelector("#pet-name").textContent = pet.name;
  document.querySelector("#pet-avatar").textContent = ({Py:"🐍",Ferris:"🦀",Gopher:"🐹",Duke:"☕",Moby:"🐳",Mona:"🐙",Tanuki:"🦝",ElePHPant:"🐘",Kodee:"🤖",Camel:"🐪"})[pet.name] || "🐾";
  document.querySelector("#pet-mood").textContent = pet.hunger > 65 ? "Tiene un poquito de hambre" : "Con ganas de explorar";
}
showPet();
document.querySelector("#feed-button").addEventListener("click", () => {
  const pet = pets[selectedPet];
  pet.hunger = Math.max(0, pet.hunger - 28);
  pet.happiness = Math.min(100, pet.happiness + 5);
  document.querySelector("#pet-mood").textContent = pet.name + " disfrutó su snack ✨";
  const toast = document.querySelector("#toast");
  toast.textContent = "¡Qué rico! " + pet.name + " está más feliz.";
  toast.classList.add("visible");
  window.setTimeout(() => toast.classList.remove("visible"), 2200);
  localStorage.setItem("codepaws-save", JSON.stringify({ selectedPet, pets: pets.map(p => ({ name: p.name, hunger: p.hunger, happiness: p.happiness })) }));
});
document.querySelector("#pet-card");
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
    move.normalize().multiplyScalar(9 * dt);
    player.position.add(move);
    player.rotation.y = Math.atan2(move.x, move.z);
  }
  player.position.x = THREE.MathUtils.clamp(player.position.x, -115, 115);
  player.position.z = THREE.MathUtils.clamp(player.position.z, -115, 115);
  pets.forEach((pet, i) => {
    pet.group.position.y = Math.sin(clock.elapsedTime * 2 + i) * 0.08;
    pet.group.rotation.y = Math.sin(clock.elapsedTime * 0.45 + i) * 0.25;
  });
  target.copy(player.position).add(new THREE.Vector3(0, 1.1, 0));
  const distance = 10;
  camera.position.set(
    target.x + Math.sin(yaw) * Math.cos(pitch) * distance,
    target.y + Math.sin(pitch) * distance + 2.1,
    target.z + Math.cos(yaw) * Math.cos(pitch) * distance
  );
  camera.lookAt(target);
  renderer.render(scene, camera);
}
animate();
