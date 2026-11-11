#!/usr/bin/env python3
"""Monta index.html do deck Nutrire Enxoval MPV 2027 × 75 LAB.

Uso: python3 fonte/montar.py <index.html do deck bombril-comercial-75lab>
O deck de referência fornece os ícones, as telas institucionais da 75 LAB
(propósito, diferencial, vantagens, números, clientes, cases, depoimento e fim)
e a navegação; as telas da Nutrire vêm de fonte/telas-nutrire.html e fonte/fim-nutrire.html.
Concorrentes diretos da Nutrire em pet food (Mars: Whiskas e Pedigree; PremieRpet;
Kelco: Kelcat, Keldog e Pipicat) saem das telas de clientes, cases e vídeos.
"""
import re, sys, time, pathlib

raiz = pathlib.Path(__file__).resolve().parent.parent
ref = pathlib.Path(sys.argv[1]).read_text(encoding='utf8')
versao = time.strftime('%Y%m%d%H%M%S')

# ícones do motor (primeiro <svg> do body) + ícones das peças de PDV
simbolos = re.search(r'<svg width="0" height="0".*?</svg>', ref, re.S).group(0)
pecas = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="p-ponta" viewBox="0 0 48 48"><path d="M10 44V12h28v32M8 12l4-7h24l4 7M10 22h28M10 32h28M6 44h36"/></symbol>
  <symbol id="p-ilha" viewBox="0 0 48 48"><path d="M4 40h40v5H4zM8 40V26h32v14M13 26V14h22v12M18 14V6h12v8"/></symbol>
  <symbol id="p-chao" viewBox="0 0 48 48"><path d="M14 44V4h20v40M14 15h20M14 25h20M14 35h20M10 44h28"/></symbol>
  <symbol id="p-totem" viewBox="0 0 48 48"><path d="M17 44V4h14v40M12 44h24M21 10h6v6h-6zM21 22h6"/></symbol>
  <symbol id="p-cubo" viewBox="0 0 48 48"><path d="M24 4l18 10v20L24 44 6 34V14zM6 14l18 10 18-10M24 24v20"/></symbol>
  <symbol id="p-testeira" viewBox="0 0 48 48"><path d="M4 6h40v12H4zM9 18v26M39 18v26M9 30h30"/></symbol>
  <symbol id="p-faixa" viewBox="0 0 48 48"><path d="M4 12h40M4 28h40M4 28h40v7H4zM10 12V6h8v6M24 12V6h8v6"/></symbol>
  <symbol id="p-balcao" viewBox="0 0 48 48"><path d="M6 44h36M10 44V30h28v14M14 30l3-16h14l3 16M18 22h12"/></symbol>
  <symbol id="p-clip" viewBox="0 0 48 48"><path d="M24 3v42M18 6h12M17 13h14v6H17zM17 25h14v6H17zM17 37h14v6H17z"/></symbol>
  <symbol id="p-wobbler" viewBox="0 0 48 48"><path d="M4 8h22M15 8v10"/><circle cx="24" cy="30" r="12"/><path d="M19 30h10"/></symbol>
  <symbol id="p-stopper" viewBox="0 0 48 48"><path d="M4 8v32M4 24h10"/><path d="M14 10h30v28H14z"/><path d="M20 20h18M20 28h12"/></symbol>
  <symbol id="p-preco" viewBox="0 0 48 48"><path d="M6 8h36v26H6zM12 16h10M12 24h6"/><path d="M28 28V16h8M28 22h6"/><path d="M24 34v10"/></symbol>
  <symbol id="p-mobile" viewBox="0 0 48 48"><path d="M24 2v8M8 10h32M12 10v8M36 10v8M6 18h12v18H6zM30 18h12v18H30z"/></symbol>
  <symbol id="p-adesivo" viewBox="0 0 48 48"><ellipse cx="24" cy="34" rx="20" ry="9"/><path d="M24 6v18M17 17l7 7 7-7"/></symbol>
  <symbol id="p-digital" viewBox="0 0 48 48"><path d="M4 8h40v26H4zM16 42h16M24 34v8M10 26l8-8 6 6 8-10 6 6"/></symbol>
</svg>'''

def secao(rx):
    m = re.search(r'\n  <section ' + rx + r'.*?</section>', ref, re.S)
    if not m:
        raise SystemExit('tela não encontrada: ' + rx)
    return m.group(0)

VID = 'https://projetos.75lab.com.br/institucional-75lab/assets/video/'
reuso = []
for rx in [r'id="proposito"', r'id="diferencial"', r'id="vantagens"', r'class="tela s-num"',
           r'class="tela s-cli2"', r'id="cases-pdv"', r'id="depoimento"']:
    s = secao(rx)
    s = s.replace('(06) Por que a 75 LAB', '(05) Por que a 75 LAB')
    s = s.replace('assets/video/', VID)
    reuso.append(s)

# o depoimento usa só os vídeos publicados no deck institucional
dep = reuso[-1]
dep = re.sub(r'\s*<button class="vid"[^>]*data-src="' + re.escape(VID) + r'(alltak-hausdecor|reel5|reel2)\.mp4".*?</button>', '', dep, flags=re.S)
reuso[-1] = dep
# concorrentes diretos em pet food fora das telas de clientes, cases e vídeos
for k, s in enumerate(reuso):
    for c in ['whiskas', 'pedigree', 'premierpet', 'kelcat', 'keldog', 'pipicat']:
        s = re.sub(r'<div><img src="assets/clientes/' + c + r'\.png"[^>]*></div>', '', s)
    s = s.replace('data-amplia="assets/cases/kelco.jpg" data-legenda="Kelco: displays especiais"', 'data-amplia="assets/cases/semp.jpg" data-legenda="SEMP: totem e display de chão"')
    s = s.replace('<img src="assets/cases/kelco.jpg" alt="Kelco, displays especiais" loading="lazy"><figcaption><b>Kelco</b>Displays especiais</figcaption>', '<img src="assets/cases/semp.jpg" alt="SEMP, totem e display de chão" loading="lazy"><figcaption><b>SEMP</b>Totem e display de chão</figcaption>')
    s = re.sub(r'\s*<button class="vid"[^>]*data-src="' + re.escape(VID) + r'reel6\.mp4".*?</button>', '', s, flags=re.S)
    reuso[k] = s

fim = secao(r'class="tela s-fim"')
fim = fim.replace('(06) Por que a 75 LAB', '(05) Por que a 75 LAB')
fim = fim.replace('para%20o%20grupo%20Bombril', 'Enxoval%20MPV%202027%20da%20Nutrire')
fim = re.sub(r'<div class="bid">.*?</div>', '<div class="bid">Nutrire · Enxoval MPV 2027 · apresentação estratégica · novembro de 2026</div>', fim)

telas = (raiz / 'fonte/telas-nutrire.html').read_text(encoding='utf8')
proximos = (raiz / 'fonte/fim-nutrire.html').read_text(encoding='utf8')

html = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nutrire × 75 LAB · Enxoval MPV 2027</title>
<meta name="description" content="Apresentação estratégica da 75 LAB para a Nutrire: enxoval completo de PDV para 2027 com a Birbo como vitrine, AR e QR Code, engenharia de custo, agência de trade por fee e tecnologia de gestão do ponto de venda.">
<meta name="robots" content="noindex">
<meta property="og:title" content="Nutrire × 75 LAB · Enxoval MPV 2027">
<meta property="og:description" content="Cada pet encontra o seu na gôndola: enxoval, engenharia e tecnologia de PDV para 2027.">
<meta property="og:image" content="https://projetos.75lab.com.br/nutrire-enxoval-mpv-2027/assets/og.jpg">
<meta name="versao" id="versaoDeck" content="{versao}">
<script>
/* A página fica 10 min no cache do navegador (GitHub Pages). Se já existe versão nova publicada, troca de endereço para pular o cache. */
(function(){{var v=document.getElementById('versaoDeck').content;
fetch('versao.txt?t='+Date.now(),{{cache:'no-store'}}).then(function(r){{return r.ok?r.text():''}}).then(function(n){{n=(n||'').trim();
if(n&&n!==v&&new URLSearchParams(location.search).get('v')!==n){{var q=new URLSearchParams(location.search);q.set('v',n);location.replace(location.pathname+'?'+q.toString()+location.hash);}}}}).catch(function(){{}});}})();
</script>
<link rel="icon" href="assets/75lab-lime.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;900&family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/deck.css?v={versao}">
<link rel="stylesheet" href="assets/telas.css?v={versao}">
<link rel="stylesheet" href="assets/nutrire.css?v={versao}">
</head>
<body>

<!-- ícones: traço reto, cantos vivos, como no site -->
{simbolos}
{pecas}

<div id="wrap"><div id="stage" class="t-foto capa">

{telas}
{''.join(reuso)}
{proximos}
{fim}
  <header id="topo">
    <div class="marcas">
      <img class="alp m-escuro" src="assets/nutrire/logo-nutrire-branco.png" alt="Nutrire"><img class="alp m-claro" src="assets/nutrire/logo-nutrire-azul.png" alt="Nutrire">
      <span class="x">×</span>
      <img class="lab m-escuro" src="assets/75lab-lime.png" alt="75 LAB"><img class="lab m-claro" src="assets/75lab-black.png" alt="75 LAB">
    </div>
    <div class="dir"><span class="cap" id="capTxt"></span><a id="btnPdf" href="nutrire-enxoval-mpv-2027.pdf?v={versao}" download="Nutrire x 75 LAB - Enxoval MPV 2027.pdf" data-cursor="Baixar" aria-label="Baixar a apresentação em PDF"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v12M6 10l6 6 6-6M4 20h16"/></svg>PDF</a><button id="btnSumario" data-sumario data-cursor="Abrir"><span><i></i><i></i><i></i></span>Sumário</button></div>
  </header>
  <footer id="rodape">
    <span class="assin">75 LAB · Nutrire · MPV 2027</span>
    <div class="nav"><button id="ant" aria-label="Tela anterior" data-cursor="Voltar">←</button><span id="cont">01</span><button id="prox" aria-label="Próxima tela" data-cursor="Seguir">→</button></div>
  </footer>
  <div id="prog"><i></i></div>
  <div id="wipe" class="wipeDuo"><img src="assets/75lab-black.png" alt="75 LAB"><i>×</i><img class="b" src="assets/nutrire/logo-nutrire-azul.png" alt="Nutrire"></div>
  <nav id="sumario" aria-label="Sumário"><button class="botao mini fechar" data-cursor="Fechar">Fechar ✕</button><h2>Sumário · <span>Nutrire × 75 LAB</span></h2><ol id="sumLista"></ol></nav>
  <div class="grao"></div>
</div></div>

<div id="caixa" role="dialog" aria-label="Imagem ampliada"><button class="fechar" data-cursor="Fechar">Fechar ✕</button><img id="cxImg" alt=""><p id="cxTxt"></p></div>
<div id="cursor"></div><div id="anel"><span id="anelTxt"></span></div>
<div id="gire"><img src="assets/75lab-lime.png" alt="75 LAB"><div class="tel"></div><h3>Gire o celular</h3><p>A apresentação foi desenhada na horizontal. Deitado, o celular mostra a tela inteira.</p><button class="botao mini" id="verAssim">Ver assim mesmo</button></div>

<script src="assets/deck.js?v={versao}"></script>
</body>
</html>
'''
(raiz / 'index.html').write_text(html, encoding='utf8')
(raiz / 'versao.txt').write_text(versao + '\n', encoding='utf8')
print('index.html', len(html), 'versão', versao, 'telas', html.count('class="tela '))
