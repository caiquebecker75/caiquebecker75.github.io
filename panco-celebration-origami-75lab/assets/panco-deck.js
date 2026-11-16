/* Modo cleitinho de apresentar — camada sobre o deck da agência (deck.js):
   1) telas com ESTADOS: o Avançar/Voltar percorre os enquadramentos da tela antes de trocar de tela;
   2) telas 3D vivas (renderizam só quando ativas);
   3) montagem da embalagem por linha do tempo única (slider = scrubbing, botões usam a mesma linha). */
import * as THREE from 'three';
import { loadBox, loadSkin, PancoBox, Palco, ETAPAS, easeOut } from './panco3d.js';

const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const telas = $$('.tela');
const ativa = () => $('.tela.ativa');

/* ---------------------------------------------------------- 1) estados por tela */
const estados = new Map();          // id da tela -> { n, i, ir(i, imediato) }
export function registrar(id, cfg) { estados.set(id, Object.assign({ i: 0 }, cfg)); }
function passo(dir) {
  const t = ativa(); const e = t && estados.get(t.id); if (!e) return false;
  const j = e.i + dir; if (j < 0 || j >= e.n) return false;
  e.i = j; e.ir(j); return true;
}
const AV = ['ArrowRight', 'PageDown', ' ', 'Enter'], VO = ['ArrowLeft', 'PageUp', 'Backspace'];
addEventListener('keydown', ev => {
  if ($('#sumario.aberto') || $('#caixa.aberta')) return;
  if (ev.target.closest && ev.target.closest('input,textarea')) return;
  const d = AV.includes(ev.key) ? 1 : VO.includes(ev.key) ? -1 : 0;
  if (d && passo(d)) { ev.preventDefault(); ev.stopImmediatePropagation(); }
}, true);
document.addEventListener('click', ev => {
  const b = ev.target.closest('#prox,#ant'); if (b) { if (passo(b.id === 'prox' ? 1 : -1)) { ev.stopImmediatePropagation(); ev.preventDefault(); } return; }
  const t = ativa(); if (!t || !estados.has(t.id) || !ev.target.closest('#wrap')) return;
  if (ev.target.closest('.rola,a,button,input,.amplia,[data-cursor],#sumario,model-viewer')) return;
  if (passo(ev.clientX > innerWidth/2 ? 1 : -1)) { ev.stopImmediatePropagation(); ev.preventDefault(); }
}, true);

/* entrada na tela: avançando começa no 1º estado, voltando começa no último */
let anterior = telas.findIndex(t => t.classList.contains('ativa'));
const aoAtivar = new Map(), aoSair = new Map();
new MutationObserver(() => {
  const i = telas.findIndex(t => t.classList.contains('ativa')); if (i === anterior || i < 0) return;
  const velha = telas[anterior], nova = telas[i];
  if (velha && aoSair.has(velha.id)) aoSair.get(velha.id)();
  const e = estados.get(nova.id); if (e) { e.i = i > anterior ? 0 : e.n - 1; e.ir(e.i, true); }
  if (aoAtivar.has(nova.id)) aoAtivar.get(nova.id)(i > anterior);
  anterior = i;
}).observe($('#stage'), { subtree: true, attributes: true, attributeFilter: ['class'] });

/* ---------------------------------------------------------- 2) telas 3D */
const meta = await loadBox();
const SABORES = { brownie: 'Brownie', banoffee: 'Banoffee', tiramissu: 'Tiramissu' };

function montarSabores(el, palco, caixa, onTroca) {
  if (!el) return;
  el.innerHTML = Object.entries(SABORES).map(([k, n], j) => `<button data-s="${k}" class="${j === 1 ? '' : ''}">${n}</button>`).join('');
  const marca = s => $$('button', el).forEach(b => b.classList.toggle('on', b.dataset.s === s));
  $$('button', el).forEach(b => b.addEventListener('click', ev => { ev.stopPropagation();
    const sk = loadSkin(b.dataset.s, palco.r); Object.assign(caixa.mat.art, { map: sk.map, roughnessMap: sk.orm, metalnessMap: sk.orm, bumpMap: sk.bump });
    caixa.mat.art.needsUpdate = true; marca(b.dataset.s); onTroca && onTroca(b.dataset.s); }));
  marca('brownie');
}

/* --- tela "a embalagem em 3D": enquadramentos de câmera --- */
{
  const tela = $('#design-3d');
  if (tela) {
    const el = $('.pk-3d', tela), palco = new Palco(el, { ouro: true, sombra: .3 });
    const caixa = new PancoBox(meta, loadSkin('brownie', palco.r), palco.scene.environment);
    caixa.setProgress(1); palco.scene.add(caixa.group);
    const desloca = () => { const w = el.clientWidth || 1600, h = el.clientHeight || 900; palco.cam.setViewOffset(w, h, -w*.12, -h*.02, w, h); };
    desloca(); new ResizeObserver(desloca).observe(el);
    const POSES = [
      Palco.pose(-66, 12, 860, [0, 0, 64]),      // visão geral: 100% frontal, como na capa
      Palco.pose(-90, 3, 545, [0, 0, 76]),      // zoom no appeal: o panetone aberto, sem cortar a ponta do escudo
      Palco.pose(105, 68, 640, [0, 0, 140]),    // vista superior: tampa girada 45°, recortes
      Palco.pose(0, 6, 540, [0, 0, 84]),       // detalhe lateral: "Fermentação natural, 48 h" no centro
    ];
    const C = JSON.parse($('script[type="application/json"]', tela).textContent);
    const call = $('.pk-callout', tela), pass = $('.pk-passos', tela);
    pass.innerHTML = C.map((c, j) => `<button data-j="${j}"><span>${String(j+1).padStart(2, '0')} · ${c.k}</span><i></i></button>`).join('');
    const mostrar = (j) => { call.innerHTML = `<span class="k">${C[j].k}</span><b>${C[j].b}</b><p>${C[j].p}</p>`;
      call.classList.remove('troca'); void call.offsetWidth; call.classList.add('troca');
      $$('button', pass).forEach(b => b.classList.toggle('on', +b.dataset.j === j)); };
    const ir = (j, imediato) => { mostrar(j); if (imediato) palco.setPose(POSES[j]); else palco.voar(POSES[j], j === 2 || anteriorJ === 2 ? 2200 : 1800); anteriorJ = j; };
    let anteriorJ = 0;
    registrar('design-3d', { n: POSES.length, ir });
    $$('button', pass).forEach(b => b.addEventListener('click', ev => { ev.stopPropagation(); const e = estados.get('design-3d'); e.i = +b.dataset.j; ir(e.i); }));
    montarSabores($('.pk-sabores', tela), palco, caixa);
    palco.setPose(POSES[0]); mostrar(0);
    // giro lento de vitrine enquanto a câmera está parada na visão geral
    palco.ctl.addEventListener('start', () => palco.arrastando = true); palco.ctl.addEventListener('end', () => palco.arrastando = false);
    window.__design = { palco, caixa, ir, POSES };
    aoAtivar.set('design-3d', () => palco.ligar()); aoSair.set('design-3d', () => palco.desligar());
    if (tela.classList.contains('ativa')) palco.ligar();
  }
}

/* --- tela de engenharia: montar / desmontar / planificar com scrubbing --- */
{
  const tela = $('#montagem');
  if (tela) {
    const el = $('.pk-3d', tela), palco = new Palco(el, { sombra: .22, ouro: true });
    const caixa = new PancoBox(meta, loadSkin('brownie', palco.r), palco.scene.environment);
    palco.scene.add(caixa.group); palco.ctl.enableZoom = false; palco.ctl.enableDamping = false;
    const desloca = () => { const w = el.clientWidth || 1600, h = el.clientHeight || 900; palco.cam.setViewOffset(w, h, -w*.04, h*.03, w, h); };
    desloca(); new ResizeObserver(desloca).observe(el);
    const rng = $('input[type=range]', tela), pct = $('.pk-pct', tela), cap = $('.pk-callout', tela), marcas = $('.pk-marcas', tela);
    const CURTO = ['Faca', 'Início', 'Estrutura 3D', 'Encaixes', 'Montada'];
    marcas.innerHTML = ETAPAS.map((e, j) => `<button data-p="${e.p}" style="left:${e.p*100}%" title="${e.t}">${Math.round(e.p*100)}% · ${CURTO[j]}</button>`).join('');
    let p = 1, anim = null, etapaAtual = -1, az = -38;
    const etapa = () => { let k = 0; ETAPAS.forEach((e, j) => { if (p >= e.p - .001) k = j; }); return k; };
    const aplicar = () => {
      caixa.setProgress(p); rng.value = Math.round(p*1000); rng.style.setProperty('--v', (p*100) + '%');
      pct.firstChild.nodeValue = Math.round(p*100) + '%';
      const k = etapa(); $$('button', marcas).forEach((b, j) => b.classList.toggle('on', j === k));
      if (k !== etapaAtual) { etapaAtual = k; cap.innerHTML = `<span class="k">Etapa ${k+1} de ${ETAPAS.length}</span><b>${ETAPAS[k].t}</b><p>${ETAPAS[k].d}</p>`;
        cap.classList.remove('troca'); void cap.offsetWidth; cap.classList.add('troca'); }
    };
    // câmera acompanha o tamanho da peça (faca aberta x caixa) e sobe quando a faca está deitada
    // enquadra a esfera que envolve a peça (faca aberta, tira em pé ou caixa), com folga para a interface
    // a câmera termina 100% frontal no escudo do sabor; enquanto monta, fica em 3/4 para mostrar as dobras
    const azAlvo = () => -50 - 40*Math.min(1, Math.max(0, (p - .62)/.38));
    const empe = () => { const t = Math.min(1, Math.max(0, (p - .04)/.13)); return t*t*(3 - 2*t); };   // 0 = faca deitada, 1 = em pé
    const alvoCam = () => { const R = caixa.radius, el = 9 + 36*Math.max(0, 1 - p/.16);
      return { d: Math.min(2800, Math.max(520, R/Math.sin(14*Math.PI/180)*(.8 + .1*empe()))), el, z: caixa.size.z*.5 }; };
    // faca deitada recebe a luz de cima de frente e lava o vermelho: a luz acompanha a montagem
    const luzes = []; palco.scene.traverse(o => { if (o.isLight && o.intensity > .01) luzes.push([o, o.intensity]); });
    const luz = () => { const f = .58 + .42*empe(); luzes.forEach(([o, i]) => o.intensity = i*f); };
    const sph = { d: 900, el: 22 }; let livre = false;
    let tAnt = 0;
    palco.onFrame = (t = performance.now()) => {
      const dt = tAnt ? Math.min(1000, t - tAnt) : 16; tAnt = t; const k = 1 - Math.exp(-dt/220);   // segue o relógio, não os quadros
      luz(); const a = alvoCam(); sph.d += (a.d - sph.d)*k; if (!palco.arrastando) sph.el += (a.el - sph.el)*k;
      const off = palco.cam.position.clone().sub(palco.ctl.target); let azAtual = Math.atan2(off.y, off.x)*180/Math.PI;
      if (palco.arrastando) livre = true;
      if (!livre) { let dz = azAlvo() - azAtual; dz = ((dz + 540) % 360) - 180; azAtual += dz*k; }
      const elAtual = palco.arrastando ? Math.asin(Math.max(-1, Math.min(1, off.z/off.length())))*180/Math.PI : sph.el;
      if (palco.arrastando) sph.el = elAtual;
      const P = Palco.pose(azAtual, sph.el, sph.d, [0, 0, palco.ctl.target.z + (a.z - palco.ctl.target.z)*k]);
      palco.cam.position.copy(P.pos); palco.ctl.target.copy(P.alvo);
      if (anim) anim(performance.now());
    };
    palco.ctl.addEventListener('start', () => palco.arrastando = true); palco.ctl.addEventListener('end', () => palco.arrastando = false);
    const animar = (alvo, durMax = 7000) => new Promise(res => {
      const p0 = p, dur = Math.max(700, Math.abs(alvo - p0)*durMax), t0 = performance.now();
      anim = (t) => { const k = Math.min(1, (t - t0)/dur); p = p0 + (alvo - p0)*(k < .5 ? 2*k*k : 1 - Math.pow(-2*k + 2, 2)/2); aplicar();
        if (k >= 1) { anim = null; res(); } };
    });
    const parar = () => { anim = null; $$('.pk-btns button', tela).forEach(b => b.classList.remove('on')); };
    rng.addEventListener('input', ev => { ev.stopPropagation(); parar(); p = rng.value/1000; aplicar(); });
    ['click', 'keydown', 'pointerdown'].forEach(t => rng.addEventListener(t, e => e.stopPropagation()));
    $$('button', marcas).forEach(b => b.addEventListener('click', ev => { ev.stopPropagation(); parar(); animar(+b.dataset.p, 5000); }));
    const acao = {
      abrir: () => animar(.72, 4000), planificar: () => animar(0), montar: () => animar(1), reiniciar: () => { parar(); livre = false; p = 1; aplicar(); sph.el = alvoCam().el; palco.setPose(Palco.pose(-90, sph.el, alvoCam().d, [0, 0, 85])); },
      auto: async (b) => { livre = false; p = 0; aplicar(); sph.el = alvoCam().el; sph.d = alvoCam().d; palco.setPose(Palco.pose(-50, sph.el, sph.d, [0, 0, caixa.size.z*.5]));
        await new Promise(r => setTimeout(r, 900)); await animar(1, 11000); b && b.classList.remove('on'); },
    };
    $$('.pk-btns button', tela).forEach(b => b.addEventListener('click', ev => { ev.stopPropagation(); parar(); b.classList.add('on');
      Promise.resolve(acao[b.dataset.a](b)).then(() => { if (b.dataset.a !== 'auto') b.classList.remove('on'); }); }));
    montarSabores($('.pk-sabores', tela), palco, caixa);
    aplicar(); palco.setPose(Palco.pose(-90, alvoCam().el, alvoCam().d, [0, 0, 85]));
    // ao entrar na tela: começa planificada e monta sozinha
    const autoBtn = $('.pk-btns button[data-a=auto]', tela);
    const iniciar = () => { parar(); autoBtn.classList.add('on'); acao.auto(autoBtn); };
    aoAtivar.set('montagem', () => { palco.ligar(); iniciar(); }); aoSair.set('montagem', () => { palco.desligar(); parar(); });
    if (tela.classList.contains('ativa')) { palco.ligar(); iniciar(); }
    window.__montagem = { palco, caixa, set: v => { parar(); p = v; aplicar(); }, animar, onFrame: () => palco.onFrame() };
  }
}


/* --- tela "na gôndola": pilhas de 3 caixas girando em 3D (fluido, sem GIF), com ampliar --- */
{
  const tela = $('#gondola');
  if (tela) {
    const cards = $$('.pk-giro figure', tela), palcos = [];
    cards.forEach(fig => {
      const el = $('.cena', fig), palco = new Palco(el, { ouro: true, sombra: .3 });
      palco.ctl.enableZoom = false;
      const pilha = new THREE.Group(), skin = loadSkin(fig.dataset.sabor, palco.r);
      let z = 0;
      [0, 45, 180].forEach(rot => { const b = new PancoBox(meta, skin, palco.scene.environment); b.setProgress(1);
        const g = new THREE.Group(); g.add(b.group); g.position.z = z; g.rotation.z = rot*Math.PI/180; z += b.size.z + .8; pilha.add(g); });
      palco.scene.add(pilha);
      const ajusta = () => { const grande = fig.classList.contains('grande');
        palco.setPose(Palco.pose(-90, grande ? 12 : 8, grande ? 1150 : 1270, [0, 0, z/2])); };
      ajusta();
      let tA = 0; palco.onFrame = (t = performance.now()) => { const dt = tA ? Math.min(100, t - tA) : 16; tA = t; if (!palco.arrastando) pilha.rotation.z += .00036*dt; };
      palco.ctl.addEventListener('start', () => palco.arrastando = true); palco.ctl.addEventListener('end', () => palco.arrastando = false);
      $('.amp', fig).addEventListener('click', ev => { ev.stopPropagation(); const g = !fig.classList.contains('grande');
        cards.forEach(f => f.classList.toggle('grande', false)); fig.classList.toggle('grande', g); $('.pk-giro', tela).classList.toggle('tem-grande', g);
        $('.amp', fig).textContent = g ? 'Fechar ✕' : 'Ampliar ⤢'; setTimeout(() => { palco.resize(); ajusta(); }, 30); });
      palcos.push(palco);
    });
    addEventListener('keydown', e => { if (e.key === 'Escape' && $('.pk-giro.tem-grande', tela)) { e.stopImmediatePropagation(); $('.grande .amp', tela).click(); } }, true);
    aoAtivar.set('gondola', () => palcos.forEach(p => p.ligar()));
    aoSair.set('gondola', () => palcos.forEach(p => p.desligar()));
    if (tela.classList.contains('ativa')) palcos.forEach(p => p.ligar());
    window.__gondola = { palcos };
  }
}

/* --- AR: model-viewer carregado só quando a tela abre --- */
{
  const tela = $('#ar');
  if (tela) {
    const liga = () => {
      if (!document.querySelector('script[src*="model-viewer"]')) { const sc = document.createElement('script'); sc.type = 'module'; sc.src = 'assets/vendor/model-viewer.min.js'; document.head.appendChild(sc); }
      const mv = $('model-viewer', tela); if (!mv.getAttribute('src')) { mv.setAttribute('src', mv.dataset.src); mv.setAttribute('ios-src', mv.dataset.ios); }
      const q = $('.q', tela); if (q && !q.dataset.ok && window.qrcode) { q.dataset.ok = 1;
        const qr = qrcode(0, 'M'); qr.addData(q.dataset.url || location.href.split('#')[0]); qr.make();
        q.innerHTML = qr.createSvgTag({ cellSize: 6, margin: 0, scalable: true }); }
    };
    aoAtivar.set('ar', liga); if (tela.classList.contains('ativa')) liga();
  }
}
window.__pk = { estados, registrar };
