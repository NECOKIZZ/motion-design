// kickoff.cash: the 3D layer. Every object is a pure function of time t (seconds),
// rendered on each HyperFrames seek. No clocks, no randomness.
import * as THREE from "three";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";

const W = 1920, H = 1080;
const PURPLE = 0x7b62f6, GREEN = 0x00c805, CREAM = 0xf7f5f0;

// ---------- easing + keyframe helpers ----------
const E = {
  lin: (x) => x,
  in2: (x) => x * x,
  in3: (x) => x * x * x,
  out3: (x) => 1 - Math.pow(1 - x, 3),
  inOut3: (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2),
  inOut2: (x) => (x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2),
  expoOut: (x) => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * x)),
  backOut: (x) => { const s = 1.6; return 1 + (s + 1) * Math.pow(x - 1, 3) + s * Math.pow(x - 1, 2); },
  sine: (x) => -(Math.cos(Math.PI * x) - 1) / 2,
};
const clamp01 = (x) => Math.max(0, Math.min(1, x));
const seg = (t, t0, t1, e = E.inOut3) => (t <= t0 ? 0 : t >= t1 ? 1 : e((t - t0) / (t1 - t0)));
const lerp = (a, b, k) => a + (b - a) * k;
// keys: [[time, [x,y,z] | number, ease]] ; ease shapes the segment arriving at that key
function track(t, keys) {
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 1; i < keys.length; i++) {
    const [t1, v1, e] = keys[i];
    const [t0, v0] = keys[i - 1];
    if (t <= t1) {
      const k = (e || E.inOut3)((t - t0) / (t1 - t0));
      return Array.isArray(v0) ? v0.map((a, j) => lerp(a, v1[j], k)) : lerp(v0, v1, k);
    }
  }
  return keys[keys.length - 1][1];
}

// ---------- renderer / scene ----------
const canvas = document.getElementById("gl");
const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1);
renderer.setSize(W, H, false);
renderer.setClearColor(0x000000, 0);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.outputColorSpace = THREE.SRGBColorSpace;

const scene = new THREE.Scene();
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
scene.environmentIntensity = 0.55;

const camera = new THREE.PerspectiveCamera(32, W / H, 0.1, 200);

const key = new THREE.SpotLight(PURPLE, 260, 40, Math.PI / 5, 0.6, 1.6);
key.position.set(-5, 9, 6);
scene.add(key, key.target);
const rim = new THREE.DirectionalLight(0xdfe6ff, 2.6);
rim.position.set(6, 4, -7);
scene.add(rim);
const fill = new THREE.HemisphereLight(0x9a8cff, 0x050507, 0.35);
scene.add(fill);
const front = new THREE.DirectionalLight(0xffffff, 0.6);
front.position.set(0, 3, 10);
scene.add(front);

// ---------- textures ----------
function canvasTex(w, h, draw, srgb = true) {
  const c = document.createElement("canvas");
  c.width = w; c.height = h;
  draw(c.getContext("2d"), w, h);
  const tex = new THREE.CanvasTexture(c);
  if (srgb) tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 4;
  return tex;
}

// Football: truncated-icosahedron pattern from the nearest of 32 cell centres
// (12 icosahedron vertices = pentagons, 20 face centres = hexagons).
function ballTextures() {
  const ico = new THREE.IcosahedronGeometry(1, 0);
  const pos = ico.attributes.position;
  const verts = [];
  for (let i = 0; i < pos.count; i++) {
    const v = new THREE.Vector3().fromBufferAttribute(pos, i).normalize();
    if (!verts.some((u) => u.distanceTo(v) < 1e-3)) verts.push(v);
  }
  const faces = [];
  for (let i = 0; i < pos.count; i += 3) {
    const c = new THREE.Vector3();
    for (let k = 0; k < 3; k++) c.add(new THREE.Vector3().fromBufferAttribute(pos, i + k));
    faces.push(c.normalize());
  }
  const centres = verts.map((v) => [v, 1]).concat(faces.map((f) => [f, 0]));
  const w = 1024, h = 512;
  const col = document.createElement("canvas"); col.width = w; col.height = h;
  const ctx = col.getContext("2d");
  const img = ctx.createImageData(w, h);
  const rough = document.createElement("canvas"); rough.width = w; rough.height = h;
  const rctx = rough.getContext("2d");
  const rimg = rctx.createImageData(w, h);
  const d = new THREE.Vector3();
  for (let y = 0; y < h; y++) {
    const phi = (y / h) * Math.PI;
    for (let x = 0; x < w; x++) {
      const th = (x / w) * Math.PI * 2;
      d.set(-Math.cos(th) * Math.sin(phi), Math.cos(phi), Math.sin(th) * Math.sin(phi));
      let b1 = -2, b2 = -2, t1 = 0;
      for (const [c, type] of centres) {
        const dot = d.dot(c);
        if (dot > b1) { b2 = b1; b1 = dot; t1 = type; } else if (dot > b2) b2 = dot;
      }
      const seam = b1 - b2 < 0.012;
      let r, g, bl;
      if (seam) { r = 30; g = 26; bl = 40; }
      else if (t1 === 1) { r = 26; g = 20; bl = 46; }      // pentagon: deep ink-purple
      else { r = 236; g = 234; bl = 228; }                   // hexagon: pitch cream
      const o = (y * w + x) * 4;
      img.data[o] = r; img.data[o + 1] = g; img.data[o + 2] = bl; img.data[o + 3] = 255;
      const rv = seam ? 200 : t1 === 1 ? 70 : 95;
      rimg.data[o] = rv; rimg.data[o + 1] = rv; rimg.data[o + 2] = rv; rimg.data[o + 3] = 255;
    }
  }
  ctx.putImageData(img, 0, 0);
  rctx.putImageData(rimg, 0, 0);
  const map = new THREE.CanvasTexture(col); map.colorSpace = THREE.SRGBColorSpace; map.anisotropy = 8;
  const rmap = new THREE.CanvasTexture(rough);
  return { map, rmap };
}

const radialTex = (inner, outer) =>
  canvasTex(256, 256, (c, w, h) => {
    const g = c.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, w / 2);
    g.addColorStop(0, inner); g.addColorStop(1, outer);
    c.fillStyle = g; c.fillRect(0, 0, w, h);
  });

// ---------- objects ----------
const root = new THREE.Group();
scene.add(root);

// Ball
const { map: ballMap, rmap: ballRough } = ballTextures();
const ball = new THREE.Mesh(
  new THREE.SphereGeometry(0.5, 96, 64),
  new THREE.MeshPhysicalMaterial({ map: ballMap, roughnessMap: ballRough, roughness: 1, metalness: 0.05, clearcoat: 1, clearcoatRoughness: 0.12 }),
);
root.add(ball);
const ballShadow = new THREE.Mesh(
  new THREE.PlaneGeometry(1.6, 1.6),
  new THREE.MeshBasicMaterial({ map: radialTex("rgba(0,0,0,0.85)", "rgba(0,0,0,0)"), transparent: true, depthWrite: false }),
);
ballShadow.rotation.x = -Math.PI / 2;
root.add(ballShadow);

// Act 1: the glass pitch disc
const pitchLines = canvasTex(1024, 1024, (c, w) => {
  c.fillStyle = "#000"; c.fillRect(0, 0, w, w);
  c.strokeStyle = "#fff"; c.lineWidth = 6;
  c.beginPath(); c.arc(w / 2, w / 2, w * 0.2, 0, Math.PI * 2); c.stroke();
  c.beginPath(); c.arc(w / 2, w / 2, w * 0.488, 0, Math.PI * 2); c.stroke();
  c.beginPath(); c.moveTo(w * 0.012, w / 2); c.lineTo(w * 0.988, w / 2); c.stroke();
  c.fillStyle = "#fff"; c.beginPath(); c.arc(w / 2, w / 2, 10, 0, Math.PI * 2); c.fill();
});
const disc = new THREE.Group();
const discMesh = new THREE.Mesh(
  new THREE.CylinderGeometry(3.2, 3.2, 0.08, 128),
  new THREE.MeshPhysicalMaterial({ color: 0x15141c, metalness: 0.3, roughness: 0.18, clearcoat: 1, clearcoatRoughness: 0.05, emissive: PURPLE, emissiveMap: pitchLines, emissiveIntensity: 1.4 }),
);
disc.add(discMesh);
const discEdge = new THREE.Mesh(
  new THREE.TorusGeometry(3.2, 0.03, 12, 160),
  new THREE.MeshPhysicalMaterial({ color: 0xbfb4ff, metalness: 1, roughness: 0.2, emissive: PURPLE, emissiveIntensity: 0.6 }),
);
discEdge.rotation.x = Math.PI / 2;
disc.add(discEdge);
const ripple = new THREE.Mesh(
  new THREE.RingGeometry(0.92, 1, 96),
  new THREE.MeshBasicMaterial({ color: 0xb7a8ff, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide }),
);
ripple.rotation.x = -Math.PI / 2;
ripple.position.y = 0.05;
disc.add(ripple);
const ripple2 = ripple.clone(); ripple2.material = ripple.material.clone(); disc.add(ripple2);
disc.position.set(-2.3, 0, 0);
root.add(disc);

// Act 3: the 5x5 scoreline grid (home goals = row, away goals = column)
const grid = new THREE.Group();
const tileGeo = new RoundedBoxGeometry(0.92, 0.24, 0.92, 4, 0.07);
const labelGeo = new THREE.PlaneGeometry(0.8, 0.8);
const tiles = [];
const SP = 1.06;
for (let i = 0; i < 5; i++) {
  for (let j = 0; j < 5; j++) {
    const mat = new THREE.MeshPhysicalMaterial({ color: 0x1a1922, metalness: 0.55, roughness: 0.22, clearcoat: 1, clearcoatRoughness: 0.08, emissive: PURPLE, emissiveIntensity: 0 });
    const m = new THREE.Mesh(tileGeo, mat);
    const lbl = new THREE.Mesh(
      labelGeo,
      new THREE.MeshBasicMaterial({
        map: canvasTex(256, 256, (c, w) => {
          c.clearRect(0, 0, w, w);
          c.fillStyle = "#f7f5f0";
          c.font = "600 104px 'Clash Display'";
          c.textAlign = "center"; c.textBaseline = "middle";
          c.fillText(`${i}-${j}`, w / 2, w / 2 + 6);
        }),
        transparent: true, depthWrite: false, opacity: 0.7,
      }),
    );
    lbl.rotation.x = -Math.PI / 2;
    lbl.position.y = 0.125;
    const g = new THREE.Group();
    g.add(m, lbl);
    g.position.set((j - 2) * SP, 0, (i - 2) * SP);
    grid.add(g);
    tiles.push({ i, j, g, m, lbl });
  }
}
const gridFloor = new THREE.Mesh(
  new THREE.PlaneGeometry(14, 14),
  new THREE.MeshPhysicalMaterial({ color: 0x0c0b10, metalness: 0.4, roughness: 0.3, clearcoat: 1, clearcoatRoughness: 0.1, transparent: true, opacity: 0.9,
    alphaMap: radialTex("#ffffff", "#000000") }),
);
gridFloor.rotation.x = -Math.PI / 2;
gridFloor.position.y = -0.14;
grid.add(gridFloor);
const wave = new THREE.Mesh(
  new THREE.RingGeometry(0.9, 1, 128),
  new THREE.MeshBasicMaterial({ color: 0xc9bdff, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide }),
);
wave.rotation.x = -Math.PI / 2;
wave.position.y = -0.12;
grid.add(wave);
// light pillar over the full-time score
const pillar = new THREE.Mesh(
  new THREE.CylinderGeometry(0.36, 0.44, 5, 48, 1, true),
  new THREE.MeshBasicMaterial({ map: canvasTex(16, 256, (c, w, h) => { const g = c.createLinearGradient(0, 0, 0, h); g.addColorStop(0, "rgba(255,255,255,0)"); g.addColorStop(1, "rgba(255,255,255,1)"); c.fillStyle = g; c.fillRect(0, 0, w, h); }),
    color: 0xfff3dc, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide }),
);
grid.add(pillar);
root.add(grid);

const ACT = { i: 2, j: 0 }, YOU = { i: 2, j: 1 };
const tilePos = (c) => new THREE.Vector3((c.j - 2) * SP, 0, (c.i - 2) * SP);

// Act 5: stake chips (keep the stack)
const chips = new THREE.Group();
const chipGeo = new THREE.CylinderGeometry(0.62, 0.62, 0.13, 72);
const chipMat = new THREE.MeshPhysicalMaterial({ color: 0x18c21c, metalness: 0.85, roughness: 0.22, clearcoat: 1, clearcoatRoughness: 0.1, emissive: GREEN, emissiveIntensity: 0.12 });
const chipRimMat = new THREE.MeshPhysicalMaterial({ color: 0xeaffea, metalness: 1, roughness: 0.18 });
const chipList = [];
for (let k = 0; k < 10; k++) {
  const c = new THREE.Group();
  c.add(new THREE.Mesh(chipGeo, chipMat));
  const band = new THREE.Mesh(new THREE.TorusGeometry(0.62, 0.022, 8, 72), chipRimMat);
  band.rotation.x = Math.PI / 2;
  c.add(band);
  chips.add(c);
  chipList.push(c);
}
chips.position.set(4.6, -1.6, 0);
root.add(chips);

// Act 8: the extruded K (logo face flat and exactly the logo colour; depth in dark metal)
const logo = new THREE.Group();
const ks = new THREE.Shape();
const P = (x, y) => [(x - 250) / 250, (251 - y) / 250];
ks.moveTo(...P(150, 0)); ks.lineTo(...P(500, 502)); ks.lineTo(...P(327.5, 502)); ks.lineTo(...P(150, 251.5));
ks.lineTo(...P(150, 500)); ks.lineTo(...P(0, 500)); ks.lineTo(...P(0, 0)); ks.closePath();
const DEPTH = 0.34;
const kGeo = new THREE.ExtrudeGeometry(ks, { depth: DEPTH, bevelEnabled: true, bevelThickness: 0.025, bevelSize: 0.018, bevelSegments: 3, curveSegments: 8 });
kGeo.translate(0, 0, -DEPTH / 2);
const faceMat = new THREE.MeshBasicMaterial({ color: CREAM });
const sideMat = new THREE.MeshPhysicalMaterial({ color: 0x3a3650, metalness: 1, roughness: 0.2, clearcoat: 1, clearcoatRoughness: 0.08 });
const kMesh = new THREE.Mesh(kGeo, [faceMat, sideMat]);
logo.add(kMesh);
const dotPos = new THREE.Vector3(...P(400, 100), 0);
const dot = new THREE.Group();
const dotGeo = new THREE.CylinderGeometry(0.4, 0.4, DEPTH + 0.05, 96);
const dotMesh = new THREE.Mesh(dotGeo, [sideMat, faceMat, faceMat]);
dotMesh.rotation.x = Math.PI / 2;
dot.add(dotMesh);
dot.position.copy(dotPos);
logo.add(dot);
root.add(logo);

// ---------- per-act state ----------
const v3 = (a) => new THREE.Vector3(a[0], a[1], a[2]);
const tmp = new THREE.Vector3();

function ballDrop(t, t0, y0, yRest, g, bounces) {
  // analytic bounce: fall from y0 at t0, restitution per bounce from list
  const h = y0 - yRest;
  const tFall = Math.sqrt((2 * h) / g);
  let tt = t - t0;
  if (tt < 0) return y0;
  if (tt < tFall) return y0 - 0.5 * g * tt * tt;
  tt -= tFall;
  let v = g * tFall;
  for (const e of bounces) {
    v *= e;
    const air = (2 * v) / g;
    if (tt < air) return yRest + v * tt - 0.5 * g * tt * tt;
    tt -= air;
  }
  return yRest;
}

function renderAt(t) {
  // which acts are live
  const a1 = t < 8.15, a3 = t >= 15.85 && t < 24.15, a5 = t >= 33.4 && t < 40.0, a8 = t >= 51.9;
  disc.visible = a1; grid.visible = a3; chips.visible = a5; logo.visible = a8;
  ball.visible = false; ballShadow.visible = false;
  if (!(a1 || a3 || a5 || a8)) { renderer.clear(); return; }

  let camPos, camTgt;
  if (a1) {
    // Act 1: low hero angle, slow push; ball drops onto the disc and is kicked out at the cut
    camPos = track(t, [[0, [0.2, 1.5, 9.6]], [8, [0.9, 1.9, 8.2], E.lin]]);
    camTgt = track(t, [[0, [-0.6, 0.55, 0]], [8, [-0.9, 0.5, 0], E.lin]]);
    disc.rotation.y = t * 0.05;
    const bx = -2.3, br = 0.5;
    let y = ballDrop(t, 0.3, 6.2, 0.04 + br, 9.5, [0.42, 0.36, 0.3]);
    let x = bx, z = 0.0;
    const kick = seg(t, 7.42, 8.05, E.in3);
    x -= kick * 13; y += kick * 1.6; z += kick * 1.2;
    ball.visible = true; ball.scale.setScalar(1);
    ball.position.set(x, y, z);
    ball.rotation.set(t * 0.9 + kick * 9, 0.6 + t * 0.35, t * 0.2 + kick * 3);
    ballShadow.visible = true;
    const hgt = y - br;
    ballShadow.position.set(x, 0.05, z);
    ballShadow.scale.setScalar(0.7 + hgt * 0.25);
    ballShadow.material.opacity = clamp01(1 - hgt / 5) * (1 - kick);
    // landing ripples at the first two contacts
    const r1 = seg(t, 1.11, 2.4, E.out3), r2 = seg(t, 1.83, 2.9, E.out3);
    ripple.position.set(bx - disc.position.x, 0.05, 0);
    ripple.scale.setScalar(0.4 + r1 * 3.2);
    ripple.material.opacity = t > 1.11 ? 0.9 * (1 - r1) : 0;
    ripple2.position.copy(ripple.position);
    ripple2.scale.setScalar(0.35 + r2 * 2.0);
    ripple2.material.opacity = t > 1.83 ? 0.55 * (1 - r2) : 0;
    // pitch lines wake with the landing
    discMesh.material.emissiveIntensity = 0.5 + 1.4 * seg(t, 1.1, 1.6, E.out3) - 0.5 * seg(t, 1.6, 3.2, E.out3);
    disc.position.y = -0.9 * (1 - seg(t, 0, 1.4, E.out3));
  } else if (a3) {
    // Act 3: tiles rise, camera climbs over the grid; light radiates from the full-time score
    camPos = track(t, [[16.0, [0, 0.9, 8.6]], [18.6, [0.5, 8.4, 6.4], E.inOut3], [23.45, [1.3, 7.8, 5.7], E.lin], [24.1, [0.0, 1.2, 0.75], E.in3]]);
    camTgt = track(t, [[16.0, [0, 0.2, 0]], [18.6, [0, 0, -0.75], E.inOut3], [23.45, [0.1, 0, -0.7], E.lin], [24.1, [0.0, 0.1, 0.0], E.in3]]);
    // zoom-through target: the 2-1 tile
    const you = tilePos(YOU);
    const zk = seg(t, 23.45, 24.1, E.in3);
    camPos = camPos.map((v, k) => v + [you.x, 0, you.z][k] * zk);
    camTgt = camTgt.map((v, k) => v + [you.x, 0, you.z][k] * zk);
    grid.rotation.y = -0.18 + 0.12 * seg(t, 16, 24, E.lin);
    const act = tilePos(ACT);
    for (const tl of tiles) {
      const p = tilePos(tl);
      const dc = Math.hypot(tl.i - 2, tl.j - 2);
      const rise = seg(t, 16.05 + dc * 0.09, 16.75 + dc * 0.09, E.backOut);
      const isAct = tl.i === ACT.i && tl.j === ACT.j;
      const isYou = tl.i === YOU.i && tl.j === YOU.j;
      const dist = Math.hypot(tl.i - ACT.i, tl.j - ACT.j);
      // proximity glow: arrives as a wave, fades with distance
      const arrive = seg(t, 18.45 + dist * 0.28, 18.95 + dist * 0.28, E.out3);
      const glow = Math.exp(-(dist * dist) / 2.2) * arrive;
      let lift = 0;
      const mat = tl.m.material;
      if (isAct) {
        const ig = seg(t, 17.95, 18.25, E.out3);
        mat.emissive.setHex(0xfff1d6);
        mat.emissiveIntensity = 1.6 * ig;
        lift = 0.28 * ig;
        tl.lbl.material.color.setHex(0xffffff).lerp(new THREE.Color(0x2a2340), ig);
      } else if (isYou) {
        const pay = seg(t, 20.0, 20.45, E.out3);
        mat.emissive.setHex(PURPLE).lerp(new THREE.Color(GREEN), pay);
        mat.emissiveIntensity = glow * 1.5 + pay * 1.1;
        lift = 0.2 * pay - 0.06 * seg(t, 19.98, 20.06, E.out3) * (1 - pay);
      } else {
        mat.emissive.setHex(PURPLE);
        mat.emissiveIntensity = glow * 1.5;
        lift = 0.1 * glow;
      }
      tl.g.position.set(p.x, -1.6 * (1 - rise) + lift, p.z);
      tl.g.scale.setScalar(0.6 + 0.4 * rise);
      tl.lbl.material.opacity = 0.35 + 0.6 * Math.max(glow, isAct ? 1 : 0) * rise;
    }
    const w = seg(t, 18.4, 20.6, E.out3);
    wave.position.set(act.x, -0.12, act.z);
    wave.scale.setScalar(0.5 + w * 6.5);
    wave.material.opacity = t > 18.4 ? 0.8 * (1 - w) : 0;
    const pl = seg(t, 17.95, 18.4, E.out3) * (1 - 0.6 * seg(t, 19.2, 21, E.inOut2));
    pillar.position.set(act.x, 2.5 + 0.28, act.z);
    pillar.scale.set(1, pl, 1);
    pillar.material.opacity = 0.2 * pl;
    // the ball comes back and lands on your call
    if (t >= 19.2) {
      ball.visible = true;
      const s = 0.42;
      ball.scale.setScalar(s);
      const rest = 0.12 + 0.2 * seg(t, 20.0, 20.45, E.out3) + 0.5 * s + 0.005;
      const y = ballDrop(t, 19.35, 4.6, 0.12 + 0.5 * s + 0.005, 13, [0.3, 0.25]);
      ball.position.set(you.x, Math.max(y, t > 20.2 ? rest : y), you.z);
      ball.rotation.set(t * 1.3, t * 0.4, 0);
    }
  } else if (a5) {
    // Act 5: stake chips stack up on the beat
    camPos = [0, 1.3, 11];
    camTgt = [0, 0.2, 0];
    chips.rotation.y = 0.3 + t * 0.15;
    chips.position.set(3.95, -1.75 + 0.15 * Math.sin(t * 0.9), 0);
    chipList.forEach((c, k) => {
      const t0 = 34.0 + k * 0.25;
      const land = seg(t, t0, t0 + 0.2, E.in2);
      const settle = seg(t, t0 + 0.2, t0 + 0.42, E.out3);
      const yRest = k * 0.142;
      c.visible = t >= t0 - 0.001;
      c.position.y = yRest + (1 - land) * 2.4 + Math.sin(settle * Math.PI) * 0.05;
      c.rotation.set(0.12 * (1 - land) * ((k % 2) * 2 - 1), k * 0.7, 0.08 * (1 - land));
    });
    // stack exits with the whip at 40
    chips.position.x -= seg(t, 39.7, 40.0, E.in3) * 1.4;
  } else if (a8) {
    // Act 8: the K turns in and locks; the ball flies in and docks as the dot
    camPos = track(t, [[51.9, [0, 0.4, 9.2]], [54.2, [0, 0.35, 8.4], E.out3], [60, [0.25, 0.3, 8.0], E.lin]]);
    camTgt = [0, 0.55, 0];
    const turn = seg(t, 52.05, 54.0, E.out3);
    const lock = seg(t, 54.0, 54.35, E.backOut);
    logo.position.set(0, 1.12, 0);
    logo.scale.setScalar(0.86);
    logo.rotation.set(0.28 * (1 - turn), -1.35 * (1 - turn) + 0.035 * Math.sin((t - 54) * 1.1) * seg(t, 54.4, 56, E.inOut2), 0);
    kMesh.position.z = -0.06 * Math.sin(lock * Math.PI);
    // dot docks
    const dockT = 54.0;
    dot.scale.setScalar(t < dockT ? 0.0001 : 0.85 + 0.15 * seg(t, dockT, dockT + 0.32, E.backOut) + 0.12 * Math.sin(seg(t, dockT, dockT + 0.32) * Math.PI));
    if (t < dockT + 0.05) {
      ball.visible = true;
      logo.updateMatrixWorld();
      const target = dotPos.clone().applyMatrix4(logo.matrixWorld);
      const k = seg(t, 52.7, dockT, E.inOut3);
      const start = new THREE.Vector3(5.5, 2.8, 2.0);
      const p = start.clone().lerp(target, k);
      p.y += Math.sin(k * Math.PI) * 1.1;
      ball.position.copy(p);
      ball.scale.setScalar(lerp(1.0, 0.8 * 0.86, k) * (t > dockT ? 1 - seg(t, dockT, dockT + 0.05) : 1));
      ball.rotation.set(t * 4, t * 2.2, 0);
    }
  }

  camera.position.copy(v3(camPos));
  camera.lookAt(tmp.set(camTgt[0], camTgt[1], camTgt[2]));
  renderer.render(scene, camera);
}

window.__k3d = { renderAt };
window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));

window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["kickoff-3d"] = (async () => {
  try { await document.fonts.load("600 104px 'Clash Display'"); } catch (e) {}
  // repaint labels now the font is present
  for (const tl of tiles) {
    const tex = tl.lbl.material.map;
    const c = tex.image, ctx = c.getContext("2d");
    ctx.clearRect(0, 0, c.width, c.height);
    ctx.fillStyle = "#f7f5f0";
    ctx.font = "600 104px 'Clash Display'";
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText(`${tl.i}-${tl.j}`, c.width / 2, c.height / 2 + 6);
    tex.needsUpdate = true;
  }
  renderer.compile(scene, camera);
  renderAt(window.__hfThreeTime || 0);
})();
