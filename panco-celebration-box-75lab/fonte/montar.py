"""Monta o index.html da apresentação Panco · Celebration Box (modo cleitinho de apresentar).
Usa o deck da agência (../ype-mpv-2027-75lab/assets: deck.css, telas.css, deck.js) e as telas institucionais
da 75 LAB da versão Ypê Frutas Tropicais, adaptadas (capítulos, WhatsApp e assinatura). Nenhuma tela da Ypê entra.
Uso: python3 fonte/montar.py   (a partir da pasta da apresentação)"""
import re, time, pathlib
AQUI = pathlib.Path(__file__).resolve().parent.parent
YPE = (AQUI.parent / 'ype-frutas-tropicais-75lab' / 'index.html').read_text()
TELAS = (AQUI / 'fonte' / 'telas-box.html').read_text()
V = time.strftime('%Y%m%d%H%M%S')

# ícones (svg <symbol>) do deck
i0 = YPE.index('<svg width="0"'); i1 = YPE.index('<div id="wrap">')
icones = YPE[i0:i1].strip()

# telas institucionais da 75 LAB (capítulo 05), sem a tela de próximos passos da Ypê
a = YPE.index('<!-- ===================================================== capítulo 05')
b = YPE.index('<section id="proximos-passos"'); c = YPE.rfind('<section', 0, YPE.index('s-fim')+10)
fim_sec = YPE.index('</section>', c) + len('</section>')
ag = YPE[a:b] + YPE[c:fim_sec]
ag = re.sub(r'<div class="trilha-cap anima d4" data-atual="05">.*?</div>', '<div class="trilha-cap anima d4" data-atual="03"><span data-c="01">01<b>A embalagem</b></span><span data-c="02">02<b>Estrutura</b></span><span data-c="03">03<b>Por que a 75 LAB</b></span></div>', ag, flags=re.S)
for a, b in (('Capítulo 05</b> de 05', 'Capítulo 03</b> de 03'), ('<span class="num-cap sangra">05</span>', '<span class="num-cap sangra">03</span>'), ('(05) Por que a 75 LAB', '(03) Por que a 75 LAB'), ('Capítulo 05 · Por que a 75 LAB', 'Capítulo 03 · Por que a 75 LAB'), ('data-capitulo="05"', 'data-capitulo="03"')):
    ag = ag.replace(a, b)
ag = ag.replace('<li><i>08</i>Próximos passos</li>', '')
ag = ag.replace('Frutas%20Tropicais%20da%20Yp%C3%AA', 'embalagem%20Panco%20Celebration%20Box')
ag = re.sub(r'<div class="bid">.*?</div>', '<div class="bid">Embalagem Panco Celebration Box · novembro de 2026</div>', ag)
assert 'Ypê' not in ag and 'Yp%C3%AA' not in ag, 'sobrou menção à Ypê nas telas da agência'

D = '../ype-mpv-2027-75lab/assets/'
html = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Panco Celebration Box × 75 LAB</title>
<meta name="description" content="Apresentação da 75 LAB para a Panco: Celebration Box, cubo em cartão dobrável com tampa articulada em diagonal e berço dourado.">
<meta name="robots" content="noindex">
<meta name="versao" content="{V}">
<link rel="icon" href="{D}75lab-lime.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;900&family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{D}deck.css?v={V}">
<link rel="stylesheet" href="{D}telas.css?v={V}">
<link rel="stylesheet" href="assets/base.css?v={V}">
<link rel="stylesheet" href="assets/box.css?v={V}">
</head>
<body>
{icones}

<div id="wrap"><div id="stage" class="t-foto capa">

{TELAS}

{ag}

  <header id="topo">
    <div class="marcas">
      <img class="alp" src="assets/img/logo-panco.png" alt="Panco" style="height:44px">
      <span class="x">×</span>
      <img class="lab m-escuro" src="{D}75lab-lime.png" alt="75 LAB"><img class="lab m-claro" src="{D}75lab-black.png" alt="75 LAB">
    </div>
    <div class="dir"><span class="cap" id="capTxt"></span><button id="btnSumario" data-sumario data-cursor="Abrir"><span><i></i><i></i><i></i></span>Sumário</button></div>
  </header>
  <footer id="rodape">
    <span class="assin">75 LAB · Panco Celebration Box</span>
    <div class="nav"><button id="ant" aria-label="Tela anterior" data-cursor="Voltar">←</button><span id="cont">01</span><button id="prox" aria-label="Próxima tela" data-cursor="Seguir">→</button></div>
  </footer>
  <div id="prog"><i></i></div>
  <div id="wipe" class="wipeDuo"><img src="{D}75lab-black.png" alt="75 LAB"><i>×</i><img class="b" src="assets/img/logo-panco.png" alt="Panco"></div>
  <nav id="sumario" aria-label="Sumário"><button class="botao mini fechar" data-cursor="Fechar">Fechar ✕</button><h2>Sumário · <span>Panco × 75 LAB</span></h2><ol id="sumLista"></ol></nav>
  <div class="grao"></div>
</div></div>

<div id="caixa" role="dialog" aria-label="Imagem ampliada"><button class="fechar" data-cursor="Fechar">Fechar ✕</button><img id="cxImg" alt=""><p id="cxTxt"></p></div>
<div id="cursor"></div><div id="anel"><span id="anelTxt"></span></div>
<div id="gire"><img src="{D}75lab-lime.png" alt="75 LAB"><div class="tel"></div><h3>Gire o celular</h3><p>A apresentação foi desenhada na horizontal. Deitado, o celular mostra a tela inteira.</p><button class="botao mini" id="verAssim">Ver assim mesmo</button></div>

<script src="{D}deck.js?v={V}"></script>
<script type="module" src="assets/box.js?v={V}"></script>
</body>
</html>
'''
(AQUI / 'index.html').write_text(html)
print('ok', len(html), 'bytes', html.count('<section'), 'telas')
