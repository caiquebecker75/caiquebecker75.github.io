/* Panco Celebration Box — telas com estados (o Avançar percorre as imagens da tela antes de trocar de tela).
   Mesmo princípio do modo cleitinho de apresentar da Celebration Origami, sem 3D ao vivo:
   cada estado é uma imagem do render do projeto, com transição suave e legenda. */
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const telas = $$('.tela'), ativa = () => $('.tela.ativa');
const estados = new Map();

function passo(dir) {
  const t = ativa(), e = t && estados.get(t.id); if (!e) return false;
  const j = e.i + dir; if (j < 0 || j >= e.n) return false;
  e.i = j; e.ir(j); return true;
}
const AV = ['ArrowRight', 'PageDown', ' ', 'Enter'], VO = ['ArrowLeft', 'PageUp', 'Backspace'];
addEventListener('keydown', ev => {
  if ($('#sumario.aberto') || $('#caixa.aberta')) return;
  const d = AV.includes(ev.key) ? 1 : VO.includes(ev.key) ? -1 : 0;
  if (d && passo(d)) { ev.preventDefault(); ev.stopImmediatePropagation(); }
}, true);
document.addEventListener('click', ev => {
  const b = ev.target.closest('#prox,#ant');
  if (b) { if (passo(b.id === 'prox' ? 1 : -1)) { ev.stopImmediatePropagation(); ev.preventDefault(); } return; }
  const t = ativa(); if (!t || !estados.has(t.id) || !ev.target.closest('#wrap')) return;
  if (ev.target.closest('a,button,input,.amplia,[data-cursor],#sumario')) return;
  if (passo(ev.clientX > innerWidth/2 ? 1 : -1)) { ev.stopImmediatePropagation(); ev.preventDefault(); }
}, true);

/* tela com sequência: .seq contém <figure data-k data-t data-d> por estado; .seq-passos lista clicável */
$$('.tela[data-estados]').forEach(tela => {
  const figs = $$('.seq figure', tela), lista = $('.seq-passos', tela), cap = $('.seq-cap', tela);
  lista.innerHTML = figs.map((f, j) => `<button data-j="${j}"><i>${String(j+1).padStart(2, '0')}</i><span>${f.dataset.k}</span></button>`).join('');
  const ir = (j) => {
    figs.forEach((f, k) => f.classList.toggle('on', k === j));
    $$('button', lista).forEach((b, k) => { b.classList.toggle('on', k === j); b.classList.toggle('feito', k < j); });
    if (cap) { cap.innerHTML = `<span class="k">${figs[j].dataset.k}</span><b>${figs[j].dataset.t}</b><p>${figs[j].dataset.d}</p>`;
      cap.classList.remove('troca'); void cap.offsetWidth; cap.classList.add('troca'); }
  };
  estados.set(tela.id, { n: figs.length, i: 0, ir });
  $$('button', lista).forEach(b => b.addEventListener('click', ev => { ev.stopPropagation(); const e = estados.get(tela.id); e.i = +b.dataset.j; ir(e.i); }));
  ir(0);
});

/* ao entrar na tela: avançando começa no 1º estado, voltando começa no último */
let anterior = telas.findIndex(t => t.classList.contains('ativa'));
new MutationObserver(() => {
  const i = telas.findIndex(t => t.classList.contains('ativa')); if (i === anterior || i < 0) return;
  const e = estados.get(telas[i].id); if (e) { e.i = i > anterior ? 0 : e.n - 1; e.ir(e.i); }
  anterior = i;
}).observe($('#stage'), { subtree: true, attributes: true, attributeFilter: ['class'] });
window.__box = { estados };
