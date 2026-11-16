/* Panco · embalagem 2 · antiprisma escudo — modelo 3D da montagem real da faca.
   Corpo: quadros simulados (fold_frames.bin) da tira de escudos e lâminas se curvando até fechar o anel
   (vincos curvos, papel quase inextensível). Abas: corpos rígidos girando nos vincos retos da faca.
   Tudo é comandado por um único progresso p (0 = faca planificada, 1 = caixa montada). */
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const BASE = new URL('.', import.meta.url).href;
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const seg = (p, a, b) => clamp((p - a) / (b - a));
const ease = t => t < .5 ? 4*t*t*t : 1 - Math.pow(-2*t + 2, 3)/2;      // easeInOutCubic
export const easeOut = t => 1 - Math.pow(1 - t, 3);

/* ---------- linha do tempo da montagem (sequência física) ---------- */
export const ETAPAS = [
  { p: 0.00, t: 'Faca planificada', d: 'Uma única peça de cartão: 8 painéis, vincos curvos, abas e travas.' },
  { p: 0.25, t: 'Início da montagem', d: 'A faca fica em pé e os vincos curvos começam a dobrar.' },
  { p: 0.50, t: 'Estrutura em 3D', d: 'O anel fecha na aba de cola: o único ponto de cola da caixa.' },
  { p: 0.75, t: 'Fechamento dos encaixes', d: 'Fundo 1-2-3 travado sem cola; contrapós entram no topo.' },
  { p: 1.00, t: 'Embalagem montada', d: 'Tampa com lingueta fecha a caixa. Pronta para a gôndola.' },
];
const TL = {
  stand: [0.04, 0.17], curl: [0.17, 0.50], glue: [0.40, 0.475],
  botSmall: [0.53, 0.63], botBig: [0.61, 0.72], dust: [0.73, 0.82], lid: [0.82, 0.95], tuck: [0.87, 0.97],
};

/* ---------- geometria das abas, igual à faca_r0.py ---------- */
function flapPolys(A, S) {
  const B = k => [k*A, 0], T = k => [A/2 + k*A, S];
  const P = {};
  const D2 = A/2, TUCK = 25, DUST = 60;
  for (let k = 0; k < 4; k++) {
    const [xa] = B(k), [xb] = B(k+1);
    if (k % 2 === 0) P['bot'+k] = [[xa,0],[xa+2,-D2+10],[xa+A*.35,-D2],[xa+A*.35,-D2-14],[xb-A*.35,-D2-14],[xb-A*.35,-D2],[xb-2,-D2+10],[xb,0]];
    else { const dd = D2*.75, xc = (xa+xb)/2;
      P['bot'+k] = [[xa,0],[xa+dd*.6,-dd],[xc-15,-dd],[xc-15,-dd+18],[xc+15,-dd+18],[xc+15,-dd],[xb-dd*.6,-dd],[xb,0]]; }
  }
  for (const i of [0, 2]) { const p = T(i), q = T(i+1);
    P['dust'+i] = [p,[p[0]+3,p[1]+3],[p[0]+18,p[1]+DUST],[q[0]-18,q[1]+DUST],[q[0]-3,q[1]+3],q]; }
  const x0 = T(1)[0], x1 = T(2)[0], lt = S + A;
  P.lid = [[x0,S],[x1,S],[x1,lt],[x0,lt]];
  const tk = [[x0,lt],[x0+2,lt+TUCK-6]];
  for (let a = 0; a <= 90; a += 15) tk.push([x0+8+6*Math.cos((180-a)*Math.PI/180), lt+TUCK-6+6*Math.sin((180-a)*Math.PI/180)]);
  for (let a = 0; a <= 90; a += 15) tk.push([x1-8+6*Math.cos((90-a)*Math.PI/180), lt+TUCK-6+6*Math.sin((90-a)*Math.PI/180)]);
  tk.push([x1-2,lt+TUCK-6],[x1,lt]);
  P.tuck = tk;
  return P;
}

export async function loadBox(base = BASE + '3d/') {
  const [meta, buf] = await Promise.all([
    fetch(base + 'fold_meta.json').then(r => r.json()),
    fetch(base + 'fold_frames.bin').then(r => r.arrayBuffer())]);
  const nf = meta.alphas.length, nv = meta.nv, all = new Float32Array(buf);
  meta.frames = Array.from({ length: nf }, (_, i) => all.subarray(i*nv*3, (i+1)*nv*3));
  return meta;
}

/* ---------- materiais ---------- */
const texCache = {};
export function loadSkin(name, renderer) {
  if (texCache[name]) return texCache[name];
  const L = new THREE.TextureLoader(), ld = f => L.load(BASE + 'tex/' + name + '_' + f + '.jpg');
  const map = ld('albedo'), orm = ld('orm'), bump = ld('bump');
  map.colorSpace = THREE.SRGBColorSpace;
  const an = renderer ? renderer.capabilities.getMaxAnisotropy() : 8;
  for (const t of [map, orm, bump]) t.anisotropy = Math.min(16, an);
  return texCache[name] = { map, orm, bump };
}
function makeMaterials(skin, envMap) {
  const art = new THREE.MeshStandardMaterial({ map: skin.map, roughnessMap: skin.orm, metalnessMap: skin.orm, roughness: 1, metalness: 1,
    bumpMap: skin.bump, bumpScale: .5, envMap, envMapIntensity: 1.6, side: THREE.FrontSide });
  const inside = new THREE.MeshStandardMaterial({ color: 0xe9e2d4, roughness: .92, metalness: 0, side: THREE.BackSide, envMap, envMapIntensity: .6 });
  return { art, inside };
}

/* ---------- caixa ---------- */
export class PancoBox {
  constructor(meta, skin, envMap) {
    this.m = meta; const A = meta.A, S = meta.S, nv = meta.nv;
    this.group = new THREE.Group(); this.mat = makeMaterials(skin, envMap);
    this.pos = new Float32Array(nv*3);
    const net = meta.net, uvOf = (x, y) => [(x - meta.orig[0]) / meta.canvas[0], (y - meta.orig[1]) / meta.canvas[1]];
    this.uvOf = uvOf;
    // corpo: uma malha por painel (dobra nítida), triângulos orientados com o lado impresso na frente
    const byPanel = {};
    meta.tri.forEach((t, i) => {
      let [a, b, c] = t; const cr = (net[b][0]-net[a][0])*(net[c][1]-net[a][1]) - (net[b][1]-net[a][1])*(net[c][0]-net[a][0]);
      if (cr < 0) [b, c] = [c, b];
      (byPanel[meta.panel[i]] = byPanel[meta.panel[i]] || []).push(a, b, c);
    });
    this.panels = [];
    for (const pid in byPanel) {
      const idx = byPanel[pid], map = new Map(), loc = [];
      idx.forEach(v => { if (!map.has(v)) { map.set(v, loc.length); loc.push(v); } });
      const g = new THREE.BufferGeometry(), P = new Float32Array(loc.length*3), U = new Float32Array(loc.length*2);
      loc.forEach((v, j) => { U.set(meta.uv[v], j*2); });
      g.setAttribute('position', new THREE.BufferAttribute(P, 3)); g.setAttribute('uv', new THREE.BufferAttribute(U, 2));
      g.setIndex(idx.map(v => map.get(v)));
      this.addMesh(g); this.panels.push({ g, loc });
    }
    // dobradiças (vincos retos) a partir dos vértices do corpo
    const near = (x, y, filt) => { let bi = -1, bd = 1e9; for (let v = 0; v < nv; v++) { if (filt && !filt(v)) continue;
      const d = (net[v][0]-x)**2 + (net[v][1]-y)**2; if (d < bd) { bd = d; bi = v; } } return bi; };
    const ends = (list, k) => { const L = list.filter(r => r[1] === k); return [L.find(r => r[2] === 0)[0], L.find(r => r[2] === 1)[0]]; };
    const hinge = (list, k, inward) => { const [a, b] = ends(list, k), mx = (net[a][0]+net[b][0])/2, my = (net[a][1]+net[b][1])/2;
      return { a, b, ref: near(mx, my + inward) }; };
    const polys = flapPolys(A, S);
    this.flaps = [];
    const addFlap = (name, poly, h, win, beta, lift) => {
      const f = this.flapMesh(name, poly, h); Object.assign(f, { win, beta, lift }); this.flaps.push(f); return f; };
    for (let k = 0; k < 4; k++) addFlap('bot'+k, polys['bot'+k], hinge(meta.bot, k, 25), k % 2 ? TL.botSmall : TL.botBig, 'flat', k % 2 ? .35 : .9);
    addFlap('dust0', polys.dust0, hinge(meta.top, 0, -25), TL.dust, 'flat', -.7);
    addFlap('dust2', polys.dust2, hinge(meta.top, 2, -25), TL.dust, 'flat', -.7);
    this.lid = addFlap('lid', polys.lid, hinge(meta.top, 1, -25), TL.lid, 'flat', .15);
    // lingueta: articula na borda de cima da tampa
    const lt = S + A; this.tuck = this.flapMesh('tuck', polys.tuck, { a: -1, b: -1, ref: -1, n0: [A/2+A, lt], n1: [A/2+2*A, lt], inN: [0, -1] });
    // aba de cola: faixa de 15 mm ao longo do vinco curvo da lâmina 1
    this.buildGlue(near);
    this.p = -1; this.center = new THREE.Vector3(); this.radius = 300;
  }
  addMesh(g) { const a = new THREE.Mesh(g, this.mat.art), b = new THREE.Mesh(g, this.mat.inside);
    a.castShadow = b.castShadow = true; this.group.add(a, b); }
  flapMesh(name, poly, h) {
    const net = this.m.net;
    const n0 = h.n0 || net[h.a], n1 = h.n1 || net[h.b];
    const ex = n1[0]-n0[0], ey = n1[1]-n0[1], L = Math.hypot(ex, ey), e = [ex/L, ey/L];
    let u = h.inN; if (!u) { const r = net[h.ref]; let ux = r[0]-n0[0], uy = r[1]-n0[1]; const d = ux*e[0]+uy*e[1]; ux -= d*e[0]; uy -= d*e[1]; const l = Math.hypot(ux, uy); u = [ux/l, uy/l]; }
    // coordenadas locais (s ao longo do vinco, t para fora) de cada ponto do polígono
    h.sgn = Math.sign(e[0]*u[1] - e[1]*u[0]) || 1;                 // lado impresso = sgn * (e x u)
    const st = poly.map(([x, y]) => [(x-n0[0])*e[0] + (y-n0[1])*e[1], -((x-n0[0])*u[0] + (y-n0[1])*u[1])]);
    const tris = THREE.ShapeUtils.triangulateShape(poly.map(p => new THREE.Vector2(p[0], p[1])), []);
    const idx = []; tris.forEach(([a, b, c]) => { const cr = (poly[b][0]-poly[a][0])*(poly[c][1]-poly[a][1]) - (poly[b][1]-poly[a][1])*(poly[c][0]-poly[a][0]);
      cr < 0 ? idx.push(a, c, b) : idx.push(a, b, c); });
    const g = new THREE.BufferGeometry(), U = new Float32Array(poly.length*2);
    poly.forEach((p, j) => U.set(this.uvOf(p[0], p[1]), j*2));
    g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(poly.length*3), 3));
    g.setAttribute('uv', new THREE.BufferAttribute(U, 2)); g.setIndex(idx);
    this.addMesh(g);
    return { name, g, st, h };
  }
  buildGlue(near) {
    const m = this.m, net = m.net, B = m.seamB, n = B.length, GL = 15, cut = Math.round(n*.08);
    this.glue = { rows: [] };
    const P = [], U = [], I = [];
    for (let i = 0; i < n; i++) {
      const v = B[i], pv = net[B[Math.max(0, i-1)]], nx = net[B[Math.min(n-1, i+1)]];
      let tx = nx[0]-pv[0], ty = nx[1]-pv[1]; const tl = Math.hypot(tx, ty); tx /= tl; ty /= tl;
      // interior da lâmina 1 (lado +x da borda esquerda) e do escudo 4 (lado -x da borda direita, no outro extremo da faca)
      // a lâmina 1 fica à direita (+x) da borda esquerda da faca; o escudo 4 fica à esquerda (-x) da borda direita
      const inB = near(net[v][0] + 8, net[v][1]);
      let nxo = -ty, nyo = tx; if (nxo > 0) { nxo = -nxo; nyo = -nyo; }          // normal para fora (-x)
      const a = m.seamA[i], inA = near(net[a][0] - 8, net[a][1]);
      const w = (i < cut || i > n-1-cut) ? 0 : GL;
      this.glue.rows.push({ v, a, inB, inA, w });
      const o = [net[v][0] + nxo*w, net[v][1] + nyo*w];
      P.push(0,0,0, 0,0,0); U.push(...this.uvOf(...net[v]), ...this.uvOf(...o));
      if (i < n-1) { const k = i*2; I.push(k, k+1, k+2, k+1, k+3, k+2); }
    }
    // orientação: lado impresso para fora
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(P, 3));
    g.setAttribute('uv', new THREE.Float32BufferAttribute(U, 2)); g.setIndex(I);
    this.glue.g = g; this.addMesh(g); this.glue.gamma = null;
  }
  vtx(v, out = new THREE.Vector3()) { return out.fromArray(this.pos, v*3); }
  /* corpo no progresso p: quadro simulado interpolado + faca deitando/levantando */
  bodyAt(p) {
    const m = this.m, fr = m.frames, nf = fr.length, nv = m.nv;
    const c = ease(seg(p, ...TL.curl)), al = c*90;
    let i = 0; while (i < nf-2 && m.alphas[i+1] <= al) i++;
    const a0 = m.alphas[i], a1 = m.alphas[i+1], w = clamp((al - a0)/(a1 - a0));
    const F0 = fr[i], F1 = fr[i+1], P = this.pos;
    for (let k = 0; k < nv*3; k++) P[k] = F0[k] + (F1[k]-F0[k])*w;
    return al;
  }
  setProgress(p) {
    p = clamp(p); if (p === this.p) return; this.p = p;
    this.bodyAt(p);
    const P = this.pos, net = this.m.net, nv = this.m.nv;
    // faca deitada -> em pé (gira no eixo x, em torno da linha da base)
    const phi = (1 - ease(seg(p, ...TL.stand))) * -Math.PI/2;
    if (phi !== 0) { const cs = Math.cos(phi), sn = Math.sin(phi);
      for (let v = 0; v < nv; v++) { const y = P[v*3+1], z = P[v*3+2]; P[v*3+1] = y*cs - z*sn; P[v*3+2] = y*sn + z*cs; } }
    for (const pn of this.panels) { const a = pn.g.attributes.position.array; pn.loc.forEach((v, j) => { a[j*3] = P[v*3]; a[j*3+1] = P[v*3+1]; a[j*3+2] = P[v*3+2]; });
      pn.g.attributes.position.needsUpdate = true; pn.g.computeVertexNormals(); pn.g.computeBoundingSphere(); }
    const V = (v) => new THREE.Vector3(P[v*3], P[v*3+1], P[v*3+2]);
    // abas rígidas
    const frameOf = (h) => {
      const a = V(h.a), b = V(h.b), r = V(h.ref), e = b.clone().sub(a).normalize();
      const u = r.clone().sub(a); u.addScaledVector(e, -u.dot(e)).normalize();
      const n = new THREE.Vector3().crossVectors(e, u).multiplyScalar(h.sgn); // normal do lado impresso
      return { a, e, u, n };
    };
    const place = (f, F, beta, lift) => {
      const d = F.u.clone().multiplyScalar(-Math.cos(beta)).addScaledVector(F.n, -Math.sin(beta));
      const arr = f.g.attributes.position.array;
      f.st.forEach(([s, t], j) => { const q = F.a.clone().addScaledVector(F.e, s).addScaledVector(d, t); q.z += lift; q.toArray(arr, j*3); });
      f.g.attributes.position.needsUpdate = true; f.g.computeVertexNormals(); f.g.computeBoundingSphere();
      return d;
    };
    const betaFlat = (F) => { let b = Math.atan2(-F.u.z, F.n.z); if (b < 0) b += Math.PI; return b; };
    for (const f of this.flaps) {
      const F = frameOf(f.h), g = ease(seg(p, ...f.win));
      const bf = betaFlat(F) * (f.name.startsWith('bot') ? .985 : 1);
      const d = place(f, F, bf*g, f.lift*g);
      if (f.name === 'lid') {
        // lingueta: dobra para dentro da caixa a partir da borda da tampa
        const nl = new THREE.Vector3().crossVectors(F.e, d);                // normal impressa da tampa
        const end = F.a.clone().addScaledVector(d, this.m.A); end.z += f.lift*g;
        const gm = ease(seg(p, ...TL.tuck)) * Math.PI/2 * .97;
        const dt = d.clone().multiplyScalar(Math.cos(gm)).addScaledVector(nl, -Math.sin(gm));
        const arr = this.tuck.g.attributes.position.array, lt = this.m.S + this.m.A, x0 = this.m.A/2 + this.m.A;
        const poly = this.tuckPoly || (this.tuckPoly = flapPolys(this.m.A, this.m.S).tuck);
        poly.forEach(([x, y], j) => { const q = end.clone().addScaledVector(F.e, x - x0).addScaledVector(dt, y - lt); q.toArray(arr, j*3); });
        this.tuck.g.attributes.position.needsUpdate = true; this.tuck.g.computeVertexNormals(); this.tuck.g.computeBoundingSphere();
      }
    }
    this.placeGlue(p);
    // centraliza no xy e apoia no chão
    const box = new THREE.Box3();
    this.group.children.forEach(o => { o.geometry.computeBoundingBox(); box.union(o.geometry.boundingBox); });
    const c = box.getCenter(new THREE.Vector3());
    this.group.position.set(-c.x, -c.y, -box.min.z);
    this.size = box.getSize(new THREE.Vector3()); this.radius = this.size.length()/2;
  }
  placeGlue(p) {
    const P = this.pos, V = v => new THREE.Vector3(P[v*3], P[v*3+1], P[v*3+2]);
    const G = this.glue, rows = G.rows, n = rows.length, arr = G.g.attributes.position.array;
    const gg = ease(seg(p, ...TL.glue));
    // depois de colada, a aba fica por dentro do escudo: some para não aparecer como filete na frente
    this.group.children.forEach(o => { if (o.geometry === G.g) o.visible = gg < .999; });
    if (!G.gamma) {
      // ângulo final de cada linha: a aba encosta por dentro do escudo 4 com a caixa fechada
      const save = this.pos.slice(); const fr = this.m.frames[this.m.frames.length-1]; this.pos.set(fr);
      G.gamma = rows.map((r, i) => { const L = this.localGlue(i); const XA = V(r.a), dA = V(r.inA).sub(XA);
        dA.addScaledVector(L.tau, -dA.dot(L.tau)).normalize(); return Math.atan2(-dA.dot(L.n), dA.dot(L.c)); });
      this.pos.set(save);
    }
    const ctr = new THREE.Vector3(); for (let i = 0; i < n; i++) ctr.add(V(rows[i].v)); ctr.divideScalar(n);
    rows.forEach((r, i) => {
      const L = this.localGlue(i), gm = G.gamma[i]*gg;
      const d = L.c.clone().multiplyScalar(Math.cos(gm)).addScaledVector(L.n, -Math.sin(gm));
      const X = V(r.v); X.toArray(arr, i*6);
      const o = X.clone().addScaledVector(d, r.w); o.addScaledVector(L.n, -.6*gg); o.toArray(arr, i*6+3);
    });
    G.g.attributes.position.needsUpdate = true; G.g.computeVertexNormals(); G.g.computeBoundingSphere();
  }
  localGlue(i) {
    const P = this.pos, V = v => new THREE.Vector3(P[v*3], P[v*3+1], P[v*3+2]), rows = this.glue.rows, n = rows.length;
    const tau = V(rows[Math.min(n-1, i+1)].v).sub(V(rows[Math.max(0, i-1)].v)).normalize();
    const X = V(rows[i].v), u = V(rows[i].inB).sub(X); u.addScaledVector(tau, -u.dot(tau)).normalize();
    // lado impresso: mesma regra das abas (n = u x e) com e = tau
    const nrm = new THREE.Vector3().crossVectors(u, tau);
    const netv = this.m.net, a = netv[rows[Math.max(0, i-1)].v], b = netv[rows[Math.min(n-1, i+1)].v], r = netv[rows[i].inB], x = netv[rows[i].v];
    const ez = (b[0]-a[0]), ey = (b[1]-a[1]), uz = r[0]-x[0], uy = r[1]-x[1];
    if (uz*ey - uy*ez < 0) nrm.negate();
    return { tau, n: nrm, c: u.clone().negate() };
  }
}

/* ---------- palco: renderer, luz aprovada, chão com sombra suave ---------- */
export class Palco {
  constructor(el, { fundo = null, sombra = .25, exposicao = -0.75, ouro = false } = {}) {
    this.el = el;
    const r = this.r = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
    r.toneMapping = THREE.NeutralToneMapping; r.outputColorSpace = THREE.SRGBColorSpace; r.toneMappingExposure = Math.pow(2, exposicao);
    r.shadowMap.enabled = true; r.shadowMap.type = THREE.VSMShadowMap;
    el.appendChild(r.domElement);
    const s = this.scene = new THREE.Scene(); if (fundo) s.background = new THREE.Color(fundo);
    s.environment = ouro ? Palco.estudioOuro(r) : new THREE.PMREMGenerator(r).fromScene(new RoomEnvironment(), .04).texture; s.environmentIntensity = 1;
    s.add(new THREE.HemisphereLight(0xffffff, 0x8a8a8a, ouro ? 1.25 : 1.6));
    const dl = new THREE.DirectionalLight(0xffffff, 2.2); dl.position.set(300, -500, 600); s.add(dl);
    const dl2 = new THREE.DirectionalLight(0xffffff, .8); dl2.position.set(-400, 300, 200); s.add(dl2);
    const sh = (pos, rad) => { const L = new THREE.DirectionalLight(0xffffff, 1e-4); L.position.set(...pos); L.castShadow = true;
      L.shadow.mapSize.set(2048, 2048); const c = L.shadow.camera; c.left = c.bottom = -700; c.right = c.top = 700; c.near = 10; c.far = 4000;
      L.shadow.radius = rad; L.shadow.blurSamples = 24; L.shadow.bias = -.0005; s.add(L); };
    sh([300, -500, 600], 22); sh([0, 0, 1200], 30);
    const chao = this.chao = new THREE.Mesh(new THREE.PlaneGeometry(8000, 8000), new THREE.ShadowMaterial({ opacity: sombra }));
    chao.receiveShadow = true; chao.position.z = -.3; s.add(chao);
    this.cam = new THREE.PerspectiveCamera(28, 16/9, 5, 20000); this.cam.up.set(0, 0, 1);
    this.ctl = new OrbitControls(this.cam, r.domElement); this.ctl.enableDamping = true; this.ctl.dampingFactor = .08;
    this.ctl.minDistance = 250; this.ctl.maxDistance = 3200; this.ctl.maxPolarAngle = Math.PI*.495; this.ctl.enablePan = false;
    this.tween = null; this.vivo = false; this.onFrame = null;
    this.resize(); new ResizeObserver(() => this.resize()).observe(el);
  }
  /* estúdio escuro com faixas de softbox em volta (acima e abaixo do horizonte): o foil reflete faixas de luz
     em qualquer ângulo, com degradê do claro ao escuro, como dourado de verdade */
  static estudioOuro(r) {
    const est = new THREE.Scene(); est.background = new THREE.Color(0x1a0a06);
    const sb = (w, h, pos, cor, int) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color: new THREE.Color(cor).multiplyScalar(int), side: THREE.DoubleSide }));
      m.position.set(...pos); m.lookAt(0, 0, 0); est.add(m); };
    for (let k = 0; k < 8; k++) { const a = (k*45 + 22.5)*Math.PI/180, i = k % 2 ? 2.2 : 4.2;
      sb(2.6, 3.4, [8*Math.cos(a), 8*Math.sin(a), 3.6], 0xffecd0, i);       // faixas altas (escudos)
      sb(3.2, 3.0, [8*Math.cos(a + .39), 8*Math.sin(a + .39), -3.8], 0xffe2b8, i*1.4); }   // rebatedores baixos (lâminas)
    sb(9, 9, [0, 0, 11], 0xffffff, .9);
    return new THREE.PMREMGenerator(r).fromScene(est, .02).texture;
  }
  resize() { const w = this.el.clientWidth || 1600, h = this.el.clientHeight || 900;
    const esc = this.el.getBoundingClientRect().width / w || 1;
    this.r.setPixelRatio(Math.min(2, (devicePixelRatio || 1) * Math.max(.5, esc)));
    this.r.setSize(w, h, false); this.r.domElement.style.width = '100%'; this.r.domElement.style.height = '100%';
    this.cam.aspect = w/h; this.cam.updateProjectionMatrix(); }
  /* posição de câmera por azimute/elevação/distância em volta de um alvo */
  static pose(az, el, d, alvo = [0, 0, 85]) { const a = az*Math.PI/180, e = el*Math.PI/180;
    return { pos: new THREE.Vector3(alvo[0] + d*Math.cos(e)*Math.cos(a), alvo[1] + d*Math.cos(e)*Math.sin(a), alvo[2] + d*Math.sin(e)), alvo: new THREE.Vector3(...alvo) }; }
  setPose(P) { this.cam.position.copy(P.pos); this.ctl.target.copy(P.alvo); this.ctl.update(); }
  /* movimento de câmera de cinema: arco suave em volta do alvo (interpola em coordenadas esféricas) */
  voar(P, dur = 1600) {
    const c0 = this.ctl.target.clone(), p0 = this.cam.position.clone(), c1 = P.alvo, p1 = P.pos;
    const sph = (p, c) => new THREE.Spherical().setFromVector3(p.clone().sub(c).applyAxisAngle(new THREE.Vector3(1, 0, 0), -Math.PI/2));
    const s0 = sph(p0, c0), s1 = sph(p1, c1);
    let dth = s1.theta - s0.theta; if (dth > Math.PI) dth -= 2*Math.PI; if (dth < -Math.PI) dth += 2*Math.PI;
    const t0 = performance.now();
    this.tween = (now) => { const k = clamp((now - t0)/dur), e = ease(k);
      const c = c0.clone().lerp(c1, e);
      const s = new THREE.Spherical(s0.radius + (s1.radius - s0.radius)*e, s0.phi + (s1.phi - s0.phi)*e, s0.theta + dth*e);
      this.cam.position.setFromSpherical(s).applyAxisAngle(new THREE.Vector3(1, 0, 0), Math.PI/2).add(c); this.ctl.target.copy(c);
      if (k >= 1) this.tween = null; };
    return new Promise(res => setTimeout(res, dur));
  }
  ligar() { if (this.vivo) return; this.vivo = true; const loop = (t) => { if (!this.vivo) return;
      if (this.tween) this.tween(t); if (this.onFrame) this.onFrame(t); this.ctl.update(); this.r.render(this.scene, this.cam); requestAnimationFrame(loop); };
    requestAnimationFrame(loop); }
  desligar() { this.vivo = false; }
}
