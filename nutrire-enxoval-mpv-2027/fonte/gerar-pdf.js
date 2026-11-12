// Gera o PDF do deck: cada página é a tela exata (1600x900, em 1,5x), no estado final (?pdf=1).
// As telas de nível do enxoval (leves, intermediárias, grande impacto) viram uma página por peça. Também grava assets/og.jpg a partir da capa.
//   python3 -m http.server 8822   (na pasta do deck)
//   node fonte/gerar-pdf.js [endereço] [pasta-temporária]
//   python3 fonte/juntar-pdf.py <pasta-temporária> nutrire-enxoval-mpv-2027.pdf
const { chromium } = require('playwright');
const fs = require('fs');

const BASE = process.argv[2] || 'http://localhost:8822/';
const PASTA = process.argv[3] || 'paginas-pdf';

(async () => {
  fs.mkdirSync(PASTA, { recursive: true });
  const nav = await chromium.launch();
  const pg = await nav.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1.5 });
  pg.on('pageerror', (e) => console.log('erro na página:', e.message));
  await pg.goto(BASE + '?pdf=1#1', { waitUntil: 'load', timeout: 120000 });
  await pg.evaluate(() => document.fonts.ready);
  const total = await pg.evaluate(() => document.querySelectorAll('.tela').length);
  let pagina = 0;
  const fotografa = async () => {
    await pg.waitForTimeout(600);
    pagina++;
    const nome = `${PASTA}/${String(pagina).padStart(3, '0')}.jpg`;
    await pg.screenshot({ path: nome, type: 'jpeg', quality: 86, timeout: 120000 });
    console.log('página', pagina);
  };
  for (let n = 1; n <= total; n++) {
    await pg.evaluate((n) => { location.hash = '#' + n; }, n);
    await pg.waitForFunction((n) => document.querySelector('#cont').textContent.startsWith(String(n).padStart(2, '0')), n, { timeout: 60000 });
    await pg.evaluate(async () => {
      const t = document.querySelector('.tela.ativa');
      const vis = [...t.querySelectorAll('img')].filter((i) => i.offsetParent !== null);
      vis.forEach((i) => { i.loading = 'eager'; });
      await Promise.race([Promise.all(vis.map((i) => i.complete ? 0 : new Promise((r) => { i.onload = i.onerror = r; }))), new Promise((r) => setTimeout(r, 10000))]);
    });
    const abas = await pg.evaluate(() => ['s-bn1','s-bn2','s-bn3'].some((c) => document.querySelector('.tela.ativa').classList.contains(c)) ? document.querySelectorAll('.tela.ativa [data-aba]').length : 0);
    if (abas) {
      for (let k = 0; k < abas; k++) {
        await pg.evaluate((k) => document.querySelectorAll('.tela.ativa [data-aba]')[k].click(), k);
        await fotografa();
      }
    } else {
      await fotografa();
    }
    if (n === 1) await pg.screenshot({ path: 'assets/og.jpg', type: 'jpeg', quality: 82, clip: { x: 0, y: 0, width: 1600, height: 840 } });
  }
  await nav.close();
})();
