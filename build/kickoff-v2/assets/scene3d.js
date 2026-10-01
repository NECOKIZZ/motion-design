// Kickoff v2 · 3D layer. Pure function of time: every frame is computed from window.K3D_AT(t).
import * as THREE from "three";
import { RoomEnvironment } from "./vendor/addons/RoomEnvironment.js";

const canvas = document.getElementById("three-layer");
const W = 1920, H = 1080;
const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true, preserveDrawingBuffer: true });
renderer.setSize(W, H, false);
renderer.setPixelRatio(1);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.setClearColor(0x000000, 0);

const scene = new THREE.Scene();
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
const camera = new THREE.PerspectiveCamera(30, W / H, 0.1, 200);

const key = new THREE.PointLight(0x7b62f6, 70, 40, 1.6); key.position.set(-4, 5, 6); scene.add(key);
const rim = new THREE.PointLight(0xffffff, 45, 40, 1.6); rim.position.set(5, 2, -4); scene.add(rim);
const fill = new THREE.PointLight(0xa897ff, 20, 30, 1.6); fill.position.set(0, -4, 5); scene.add(fill);
scene.add(new THREE.AmbientLight(0x221a44, 0.6));

// ── the closeness field: fine concentric rings
const rings = new THREE.Group(); scene.add(rings);
const RING_R = [0.55, 0.85, 1.15, 1.45, 1.75, 2.05, 2.35, 2.65, 2.95, 3.25, 3.55, 3.85];
const ringMeshes = RING_R.map((r, i) => {
  const m = new THREE.MeshPhysicalMaterial({
    color: 0x8b74ff, metalness: 0.9, roughness: 0.18, clearcoat: 1, clearcoatRoughness: 0.1,
    emissive: 0x4e3cb5, emissiveIntensity: 0.4, transparent: true, opacity: 1,
  });
  const mesh = new THREE.Mesh(new THREE.TorusGeometry(r, 0.016 + i * 0.0018, 16, 260), m);
  mesh.userData.i = i; rings.add(mesh); return mesh;
});
const medianMat = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0, toneMapped: false });
const median = new THREE.Mesh(new THREE.TorusGeometry(1, 0.022, 16, 300), medianMat);
const medianGlowMat = new THREE.MeshBasicMaterial({ color: 0x7b62f6, transparent: true, opacity: 0, toneMapped: false, blending: THREE.AdditiveBlending, depthWrite: false });
const medianGlow = new THREE.Mesh(new THREE.TorusGeometry(1, 0.07, 16, 300), medianGlowMat);
rings.add(median); rings.add(medianGlow);

// ── the logo: extruded K and the ball as an extruded disc; face = flat white like the mark, sides = dark metal
const logo = new THREE.Group(); scene.add(logo);
const faceMat = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 1, toneMapped: false });
const sideMat = new THREE.MeshPhysicalMaterial({ color: 0x241c3f, metalness: 0.92, roughness: 0.26, clearcoat: 1, transparent: true, opacity: 1 });
const ballFace = faceMat.clone(), ballSide = sideMat.clone();
const S = 1 / 250;
const kShape = new THREE.Shape();
[[150, 0], [500, 502], [327.5, 502], [150, 251.5], [150, 500], [0, 500], [0, 0]].forEach(([x, y], i) => {
  const X = (x - 250) * S, Y = -(y - 251) * S; i ? kShape.lineTo(X, Y) : kShape.moveTo(X, Y);
});
const extrude = { depth: 0.32, bevelEnabled: true, bevelThickness: 0.02, bevelSize: 0.014, bevelSegments: 3, curveSegments: 72 };
const kGeo = new THREE.ExtrudeGeometry(kShape, extrude); kGeo.translate(0, 0, -0.16);
const kGroup = new THREE.Group(); kGroup.add(new THREE.Mesh(kGeo, [faceMat, sideMat])); logo.add(kGroup);
const ballShape = new THREE.Shape(); ballShape.absarc(0, 0, 100 * S, 0, Math.PI * 2, false);
const ballGeo = new THREE.ExtrudeGeometry(ballShape, extrude); ballGeo.translate(0, 0, -0.16);
const ballGroup = new THREE.Group(); ballGroup.add(new THREE.Mesh(ballGeo, [ballFace, ballSide])); scene.add(ballGroup);
const BALL_HOME = new THREE.Vector3((400 - 250) * S, -(100 - 251) * S, 0);

// ── pick tiles for the full-time field (billboards with canvas textures)
const PICKS = window.K3D_PICKS || [];
const tiles = new THREE.Group(); scene.add(tiles);
function tileTexture(score, lit) {
  const c = document.createElement("canvas"); c.width = 400; c.height = 240;
  const g = c.getContext("2d");
  const r = 48;
  g.beginPath(); g.roundRect(6, 6, 388, 228, r);
  const grad = g.createLinearGradient(0, 0, 0, 240);
  grad.addColorStop(0, lit ? "rgba(123,98,246,0.55)" : "rgba(40,36,56,0.92)");
  grad.addColorStop(1, lit ? "rgba(60,44,150,0.75)" : "rgba(18,17,24,0.92)");
  g.fillStyle = grad; g.fill();
  g.lineWidth = 3; g.strokeStyle = lit ? "rgba(200,190,255,0.95)" : "rgba(255,255,255,0.16)"; g.stroke();
  g.fillStyle = "#FFFFFF"; g.textAlign = "center"; g.textBaseline = "middle";
  g.font = '500 112px "Clash Display"'; g.fillText(score, 200, 108);
  g.font = '500 34px "Inter"'; g.fillStyle = lit ? "rgba(255,255,255,0.85)" : "rgba(255,255,255,0.5)"; g.fillText("$10", 200, 186);
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
  return tex;
}
const tileObjs = [];
async function buildTiles() {
  await Promise.all([document.fonts.load('500 112px "Clash Display"'), document.fonts.load('500 34px "Inter"')]);
  PICKS.forEach((p) => {
    const geo = new THREE.PlaneGeometry(1.0, 0.6);
    const base = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ map: tileTexture(p.s, false), transparent: true, toneMapped: false, depthWrite: false }));
    const lit = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ map: tileTexture(p.s, true), transparent: true, toneMapped: false, opacity: 0, depthWrite: false }));
    lit.position.z = 0.001;
    const grp = new THREE.Group(); grp.add(base); grp.add(lit); tiles.add(grp);
    tileObjs.push({ grp, base, lit, p });
  });
}
window.__hf = window.__hf || {}; window.__hf.buildReady = window.__hf.buildReady || {};
const ready = buildTiles();
window.__hf.buildReady["k3d-tiles"] = ready;

const v = (a) => new THREE.Vector3(a[0], a[1], a[2]);
function renderAt(t) {
  const st = window.K3D_AT ? window.K3D_AT(t) : null;
  if (!st || !st.visible) { canvas.style.visibility = "hidden"; return; }
  canvas.style.visibility = "visible";
  camera.position.copy(v(st.cam)); camera.fov = st.fov ?? 30; camera.updateProjectionMatrix(); camera.lookAt(v(st.look));

  rings.visible = st.rings > 0.001;
  rings.position.copy(v(st.ringsPos)); rings.rotation.set(st.ringsRot[0], st.ringsRot[1], st.ringsRot[2]);
  ringMeshes.forEach((m) => {
    const i = m.userData.i;
    const appear = Math.min(1, Math.max(0, st.rings * (RING_R.length + 2) - i));
    const e = 1 - Math.pow(1 - appear, 3);
    m.scale.setScalar(0.7 + 0.3 * e);
    m.material.opacity = e * (st.ringsOp ?? 1);
    // a travelling wave through the field: rings lift in sequence
    m.position.z = st.wave * Math.sin(t * 3.2 - i * 0.75) * 0.12 + st.impact * Math.exp(-i * 0.35) * 0.35;
    m.rotation.set(Math.sin(t * 0.45 + i) * st.wobble, Math.cos(t * 0.38 + i * 1.7) * st.wobble, 0);
    m.material.emissiveIntensity = 0.35 + st.glow * 0.8 + st.impact * Math.exp(-i * 0.5) * 2.5;
  });
  median.scale.setScalar(st.median); medianGlow.scale.setScalar(st.median);
  medianMat.opacity = st.medianOp; medianGlowMat.opacity = st.medianOp * 0.7;

  logo.visible = st.logo > 0.001;
  logo.position.copy(v(st.logoPos)); logo.rotation.set(st.logoRot[0], st.logoRot[1], st.logoRot[2]);
  logo.scale.setScalar(st.logoScale);
  faceMat.opacity = st.logo; sideMat.opacity = st.logo;

  ballGroup.visible = st.ballVis > 0.001;
  logo.updateMatrixWorld(true);
  const home = BALL_HOME.clone().applyMatrix4(logo.matrixWorld);
  ballGroup.position.copy(v(st.ballPos).lerp(home, st.dock));
  ballGroup.rotation.set(st.ballRot[0] * (1 - st.dock) + logo.rotation.x * st.dock, st.ballRot[1] * (1 - st.dock) + logo.rotation.y * st.dock, st.ballRot[2] * (1 - st.dock));
  ballGroup.scale.setScalar(st.ballScale * (1 - st.dock) + st.logoScale * st.dock);
  ballFace.opacity = st.ballVis; ballSide.opacity = st.ballVis;

  tiles.visible = (st.tiles || 0) > 0.001;
  tileObjs.forEach((o, i) => {
    const ts = st.tileState ? st.tileState[i] : null;
    if (!ts) { o.grp.visible = false; return; }
    o.grp.visible = ts.a > 0.001;
    const ang = o.p.ang, rr = o.p.r;
    // tiles stand on the ring plane (in rings' local frame), lifted by y
    const local = new THREE.Vector3(Math.cos(ang) * rr, Math.sin(ang) * rr, 0.42 + ts.lift);
    rings.updateMatrixWorld(true);
    o.grp.position.copy(local.applyMatrix4(rings.matrixWorld));
    o.grp.quaternion.copy(camera.quaternion);
    o.grp.scale.setScalar(ts.s);
    o.base.material.opacity = ts.a * (1 - ts.lit);
    o.lit.material.opacity = ts.a * ts.lit;
  });
  renderer.render(scene, camera);
}
window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
window.__k3dRender = renderAt;
ready.then(() => renderAt(window.__hfThreeTime || 0));
