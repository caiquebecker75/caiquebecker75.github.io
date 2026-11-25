# -*- coding: utf-8 -*-
"""HAV009 · Havaianas Aura Dia das Mães · apresentação interna sobre o deck da agência (base: bombril-carnaval-75lab).
Racional do KV primeiro, depois as peças uma a uma (azul e rosa, com giro 360°). Gera index.html."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
REF = open(sys.argv[1], encoding='utf-8').read()
ICONES = REF[REF.index('<svg width="0" height="0"'):REF.index('</svg>') + 6]
IMG = lambda n: os.path.exists(os.path.join(ROOT, 'assets/img/%s.webp' % n))
VID = lambda n: os.path.exists(os.path.join(ROOT, 'assets/vid/%s.mp4' % n))
CAPS = [('01', 'A ideia'), ('02', 'Lojas próprias'), ('03', 'B2B alimentar'), ('04', 'Próximos passos')]
def trilha(at): return '<div class="trilha-cap anima d4" data-atual="%s">%s</div>' % (at, ''.join('<span data-c="%s">%s<b>%s</b></span>' % (n, n, t) for n, t in CAPS))
def cap(n, tit, lead, itens, extra=''):
    return '''<section id="cap-%s" class="tela s-cap %s" data-tema="lime" data-titulo="Capítulo %s · %s" data-cap="(%s) %s" data-capitulo="%s">
    <span class="num-cap sangra">%s</span>
    <div class="texto"><span class="eyebrow anima"><b>Capítulo %s</b> de 04</span><h2 class="anima d1">%s</h2><p class="lead anima d2">%s</p></div>
    <ol class="dentro anima d3">%s</ol>%s</section>''' % (n, extra, n, tit, n, tit, n, n, n, tit, lead, ''.join('<li><i>%02d</i>%s</li>' % (i + 1, t) for i, t in enumerate(itens)), trilha(n))
def fig(src, leg): return '<figure class="amplia" data-amplia="assets/img/%s.webp" data-legenda="%s" data-cursor="Ampliar"><img src="assets/img/%s.webp" alt="%s" loading="lazy"></figure>' % (src, leg, src, leg)
def core(id_, capn, tit, eyebrow, h2, lead, abas, ficha, tema='escuro'):
    """abas: [(rótulo, imagem ou ('vid', arquivo, poster), legenda)]; abas sem arquivo ficam de fora."""
    abas = [a for a in abas if (VID(a[1][1]) if isinstance(a[1], tuple) else IMG(a[1]))]
    bts = ''.join('<button data-aba="%d" class="%s" data-cursor="Ver"><i>%02d</i><b>%s</b></button>' % (i, 'on' if i == 0 else '', i + 1, a[0]) for i, a in enumerate(abas))
    pns = ''
    for i, (rot, src, leg) in enumerate(abas):
        if isinstance(src, tuple): m = '<figure><video src="assets/vid/%s.mp4" poster="assets/img/%s.webp" muted loop playsinline preload="metadata" aria-label="%s"></video></figure>' % (src[1], src[2], rot)
        else: m = fig(src, rot)
        pns += '<div data-painel="%d" class="%s">%s<p>%s</p></div>' % (i, 'on' if i == 0 else '', m, leg)
    fc = ''.join('<dt>%s</dt><dd>%s</dd>' % f for f in ficha)
    return '''<section id="%s" class="tela s-core n" data-tema="%s" data-titulo="%s" data-cap="%s">
    <div class="caixa"><div class="gr-core">
      <div class="txt-core"><span class="eyebrow anima">%s</span><h2 class="anima">%s</h2><p class="lead anima d1">%s</p>
        <div class="abas-b vers anima d2">%s</div>
        <dl class="ficha-core anima d3">%s</dl></div>
      <div class="paineis foto-core anima dir d1">%s</div>
    </div></div></section>''' % (id_, tema, tit, capn, eyebrow, h2, lead, bts, fc, pns)
def giro(p, cor, poster):
    return ('Girando', ('vid', '%s-giro-%s' % (p, cor), poster), 'A peça girando 360°, para ver todos os lados.')
T = []
MQ = ''.join('<span>%s</span>' % t for t in ['Dia das Mães, tem Havaianas pra presente', 'Novas Havaianas Aura', 'Loja própria', 'B2B alimentar', 'Caminho azul', 'Caminho rosa'] * 3)
T.append('''<section id="capa" class="tela s-capa ativa" data-tema="foto" data-titulo="Capa" data-cap="">
    <div class="foto sangra" role="img" aria-label="KV de lançamento Havaianas Aura"></div><div class="veu sangra"></div>
    <div class="texto">
      <span class="eyebrow anima"><b>(HAV009)</b> BID Havaianas · Dia das Mães</span>
      <h1 class="anima d1">Aura<br>pra<br><span class="brilha">presente</span></h1>
      <p class="lead anima d2">Dia das Mães · o KV e as peças de loja própria e B2B · 75 LAB</p>
      <div class="acoes anima d3"><button class="botao cheio seta" data-ir="cap-01" data-cursor="Ir">Começar</button></div>
    </div>
    <span class="rot sangra anima d4">75 LAB · Havaianas · Nov/26</span>
    <div class="marquee sangra"><div>%s</div></div>
  </section>''' % MQ)
# ------------------------------------------------------------ 01 · a ideia
T.append(cap('01', 'A ideia', 'Antes das peças, a ideia: de onde partimos, como levamos o KV da Aura para o Dia das Mães e os dois caminhos de cor.', ['O ponto de partida', 'A ideia e os ajustes no KV', 'A hierarquia da informação', 'Dois caminhos: azul e rosa']))
T.append('''<section id="kv-recebido" class="tela v2-split n" data-tema="escuro" data-titulo="O ponto de partida" data-cap="(01) A ideia">
  <div class="caixa"><div class="cn-kv">
    <figure class="anima amplia" data-amplia="assets/img/kv-recebido.webp" data-legenda="KV de lançamento Havaianas Aura" data-cursor="Ampliar"><img src="assets/img/kv-recebido.webp" alt="KV de lançamento Havaianas Aura"></figure>
    <div><span class="eyebrow anima"><b>Ponto de partida</b> o KV da Aura</span>
      <h2 class="anima">Partimos do KV <span class="t-lime">de lançamento.</span></h2>
      <p class="lead anima d1">O KV global da Aura: os três Charms em cards art déco sobre o azul, o logo “new havaianas Aura” e a frase em inglês.</p>
      <ul class="cn-pontos anima d2">
        <li><b>O que já funcionava</b>O azul, os cards art déco que emolduram o produto e a fotografia dos pares. É a base de tudo, e foi mantida.</li>
        <li><b>O que a data pede</b>O KV fala de lançamento. Para o Dia das Mães, ele precisa falar de presente, com uma frase em português que o shopper lê em dois segundos.</li>
        <li><b>A nossa proposta</b>Levar esse KV para a data sem perder a cara da Aura: mesma família visual, mensagem nova.</li>
      </ul></div>
  </div></div></section>''')
T.append('''<section id="kv-ideia" class="tela v2-split n" data-tema="claro" data-titulo="A ideia" data-cap="(01) A ideia">
  <div class="caixa"><div class="cn-kv">
    <figure class="anima amplia" data-amplia="assets/img/kv-azul.webp" data-legenda="KV 75 LAB · Dia das Mães, tem Havaianas pra presente" data-cursor="Ampliar"><img src="assets/img/kv-azul.webp" alt="KV Dia das Mães, tem Havaianas pra presente"></figure>
    <div><span class="eyebrow anima"><b>A ideia</b> Dia das Mães</span>
      <h2 class="anima">Dia das Mães, tem Havaianas <span class="t-verm">pra presente.</span></h2>
      <p class="lead anima d1">A Aura vira o presente: os cards do KV viram a moldura do presente, com caixa vermelha, fita e laço dourado. Para isso, quatro ajustes no KV da Aura:</p>
      <ul class="cn-pontos anima d2">
        <li><b>A borda</b>O KV recortado na faca art déco dos cards vira o contorno das testeiras, do adesivo de vidro e das laterais.</li>
        <li><b>A frase</b>Sai o inglês, entra “Dia das Mães, tem Havaianas pra presente”: data, marca e solução numa leitura só.</li>
        <li><b>O selo</b>A moldurinha do logo amarra frase e marca e funciona sozinha nas peças pequenas.</li>
        <li><b>A assinatura</b>“Novas Havaianas Aura” desce para o rodapé, sem disputar com a data.</li>
      </ul></div>
  </div></div></section>''')
T.append('''<section id="hierarquia" class="tela v2-split n" data-tema="claro" data-titulo="A hierarquia" data-cap="(01) A ideia">
  <div class="caixa"><span class="eyebrow anima">Ordem de leitura</span>
    <h2 class="anima">Uma ordem de leitura <span class="t-verm">para todas as peças.</span></h2>
    <div class="hv-hier anima d1">
      <div class="kv"><img src="assets/img/kv-azul.webp" alt="KV com a ordem de leitura marcada"><b style="left:31%;top:20%">1</b><b style="left:66%;top:8%">2</b><b style="left:14%;top:58%">3</b><b style="left:31%;top:90%">4</b></div>
      <ol>
        <li><i>1</i><span><b>Marca</b>Havaianas é sempre o maior elemento, dentro do selo.</span></li>
        <li><i>2</i><span><b>Data e chamada</b>“Dia das Mães, tem … pra presente” abraça a marca no selo.</span></li>
        <li><i>3</i><span><b>Produto</b>Os pares nos frames, de frente para o shopper: a Aura é o presente.</span></li>
        <li><i>4</i><span><b>Assinatura</b>Novas Havaianas Aura, no rodapé de cada peça.</span></li>
      </ol>
    </div>
    <p class="v2-leg anima d2">De cima para baixo: marca, data, produto, lançamento. Seguimos essa ordem em toda face visível, da testeira da ilha ao wobbler de 15 cm.</p>
  </div></section>''')
T.append('''<section id="caminhos" class="tela v2-split n" data-tema="claro" data-titulo="Dois caminhos" data-cap="(01) A ideia">
  <div class="caixa"><span class="eyebrow anima">Dois caminhos · azul e rosa</span>
    <h2 class="anima">O mesmo sistema, <span class="t-rosa">em rosa.</span></h2>
    <div class="hv-hier anima d1">
      <div class="kv"><img src="assets/img/kv-rosa.webp" alt="KV caminho rosa"></div>
      <ol>
        <li><i>A</i><span><b>Por que dois caminhos</b>O azul é fiel ao KV global da Aura e garante a marca. O rosa leva o mesmo sistema para o universo da data. Todas as peças foram feitas nas duas cores.</span></li>
        <li><i>B</i><span><b>O rosa conecta com as mães</b>Afeto, carinho e presente: sentimos que é o caminho que mais fala com o Dia das Mães.</span></li>
        <li><i>C</i><span><b>Conversa com o produto</b>Combina com o rosa e o nude dos pares e da fotografia.</span></li>
        <li><i>D</i><span><b>Só muda a cor mestre</b>Textos em branco, a moldurinha do logo acompanha e, na ilha, o laço vira bordô.</span></li>
      </ol>
    </div>
    <p class="v2-leg anima d2">Nas páginas das peças, cada uma aparece nas duas versões, em abas: azul e rosa.</p>
  </div></section>''')
# ------------------------------------------------------------ 02 · lojas próprias
T.append(cap('02', 'Lojas próprias', 'Da vitrine ao caixa: o presente começa na rua e termina embalado na mão da cliente.', ['Mesa Big Hello', 'Vitrine', 'Gift Station', 'Embalagens'], 'rosa'))
T.append(core('mesa', '(02) Lojas próprias', 'Mesa Big Hello', 'Loja própria · LP01 · Big Hello', 'O presente <span class="t-lime">logo na entrada.</span>', 'Base azul com dois tampos de madeira, testeira em duas camadas com o selo, 3 frames com os Charms e 4 Glossy em caixas abertas. O laço dourado fecha a base como um presente.',
    [('Azul', 'mesa-az-1', 'Frontal: testeira com o selo, frames dos Charms e as caixas abertas dos Glossy.'), ('Azul · 3/4', 'mesa-az-2', 'Os dois tampos de madeira e o laço dourado na base.'),
     ('Rosa', 'mesa-rs-1', 'O mesmo móvel no caminho rosa.'), ('Rosa · 3/4', 'mesa-rs-2', 'Rosa em 3/4.')],
    [('Planta', '202 x 110 cm'), ('Base', 'azul (ou rosa) com 2 tampos de madeira'), ('Produto', '3 Charms em frames, 4 Glossy em caixas'), ('Acabamento', 'laço dourado na base')]))
T.append(core('vitrine', '(02) Lojas próprias', 'Vitrine', 'Loja própria · vitrine', 'A vitrine vira <span class="t-lime">uma caixa de presente.</span>', 'Adesivo de vidro com a moldura do KV de fora a fora e o fundo vazado, para a loja aparecer. Na frente, a mesa com as caixas abertas, os frames e os presentes cenográficos vermelhos dos dois lados.',
    [('Azul', 'vit-az-1', 'A vitrine inteira: o adesivo recorta o vidro na forma da moldura.'), ('Azul · mesa', 'vit-az-2', 'A mesa da vitrine: 4 caixas abertas, 3 frames e a faixa Novas Havaianas Aura.'),
     ('Rosa', 'vit-rs-1', 'A mesma vitrine no caminho rosa.'), ('Rosa · mesa', 'vit-rs-2', 'Mesa da vitrine em rosa.')],
    [('Base', 'vitrine padrão das lojas'), ('Adesivo', 'vinil no vidro, recorte da moldura'), ('Mesa', '146 cm, 4 caixas abertas, 3 frames'), ('Cenografia', 'presentes vermelhos com laço dourado')], tema='claro'))
T.append(core('gift', '(02) Lojas próprias', 'Gift Station', 'Loja própria · LP13 · ativação', 'Onde o presente <span class="t-lime">é embalado.</span>', 'Gift Station em metalon vermelho com a testeira Espaço Presente na arte do KV. Caixas de presente compõem os lados, duas de um e três do outro, sem outra cenografia.',
    [('Azul', 'gift-az-1', 'Frontal: a testeira Espaço Presente.'), ('Azul · 3/4', 'gift-az-2', 'As caixas de presente nos dois lados.'),
     ('Rosa', 'gift-rs-1', 'A Gift Station no caminho rosa.'), ('Rosa · 3/4', 'gift-rs-2', 'Rosa em 3/4.')],
    [('Estrutura', 'metalon vermelho'), ('Testeira', 'arte do KV, azul ou rosa'), ('Cenografia', '5 caixas de presente (2 + 3)'), ('Uso', 'a equipe embala na hora')]))
T.append(core('embalagens', '(02) Lojas próprias', 'Embalagens', 'Loja própria · embalagens', 'O KV vai <span class="t-lime">para casa.</span>', 'Caixas só no vermelho; luvas com o card do KV de borda creme; caixa envelope com a alça no topo; sacolas P, M e G. No caminho rosa, o card vira rosa.',
    [('Azul · caixas', 'pack-az-1', 'Caixas vermelhas com as luvas e a caixa envelope com alça.'), ('Azul · sacolas', 'pack-az-2', 'Sacolas P, M e G com o card do KV.'),
     ('Rosa · caixas', 'pack-rs-1', 'Luvas no caminho rosa.'), ('Rosa · sacolas', 'pack-rs-2', 'Sacolas no caminho rosa.')],
    [('Caixas', 'vermelhas, com ou sem luva'), ('Envelope', '26 x 9 x 46 cm, alça no topo'), ('Sacolas', 'P, M e G'), ('Laço', 'fita dourada')], tema='claro'))
# ------------------------------------------------------------ 03 · B2B
T.append(cap('03', 'B2B alimentar', 'No supermercado a Aura disputa atenção: peças que param o carrinho e mostram o par de perto.', ['Ilha com cubos giratórios', 'Ponta de gôndola', 'Peças leves']))
T.append(core('ilha', '(03) B2B alimentar', 'Ilha', 'B2B alimentar · BA08', 'Cubos que giram, <span class="t-lime">produto que se pega.</span>', 'Peça central com os cubos giratórios no recorte, laterais em três camadas com a foto, pares presos direto na peça e adesivo de chão redondo.',
    [('Azul', 'ilha-az-1', 'De frente: peça central com a testeira, lateral com a foto e os cubos.'), ('Azul · 3/4', 'ilha-az-2', 'As laterais em três camadas e o adesivo de chão.'), ('Cubos', 'ilha-az-3', 'Os três cubos giratórios com os cards dos pares.'),
     ('Rosa', 'ilha-rs-1', 'A ilha no caminho rosa, com o laço bordô.'), ('Rosa · 3/4', 'ilha-rs-2', 'Rosa em 3/4.'), ('Giro 360°', 'ilha-giro', 'A ilha girando: peça central, laterais e adesivo de chão de todos os lados.'), ('Cubos girando', 'ilha-cubos-giro', 'Os três cubos giram no eixo preso na base e no braço de cima.')],
    [('Altura', '263,5 cm no topo da peça central'), ('Adesivo', 'chão, Ø 2,68 m'), ('Laterais', '3 camadas com a foto do KV'), ('Produto', 'pares presos na peça, cubos giratórios')]))
T.append(core('ponta', '(03) B2B alimentar', 'Ponta de gôndola', 'B2B alimentar · BA07', 'O mesmo racional, <span class="t-lime">na ponta.</span>', 'Lateral em três camadas com a foto do KV e testeira com o topo da arte da ilha. Charms na frente e Glossy na lateral, presos direto na base de trás.',
    [('Azul', 'ponta-az-1', 'Frontal: testeira com o selo e os Charms.'), ('Azul · esquerda', 'ponta-az-2', 'A lateral cobre a gancheira.'), ('Azul · direita', 'ponta-az-3', 'Os Glossy na lateral.'),
     ('Rosa', 'ponta-rs-1', 'A ponta no caminho rosa.'), ('Rosa · 3/4', 'ponta-rs-2', 'Rosa em 3/4.')],
    [('Largura', '120 cm'), ('Laterais', '3 camadas, arte da ilha'), ('Testeira', 'topo da arte da ilha'), ('Produto', 'pares presos na base de trás')], tema='claro'))
T.append(core('leves', '(03) B2B alimentar', 'Peças leves', 'B2B alimentar · kit de gôndola', 'O selo funciona <span class="t-lime">em qualquer tamanho.</span>', 'Stopper, wobbler, clip strip com os pares e placa de carrinho: o kit leve leva a marca e a data para toda loja.',
    [('Azul · gôndola', 'leves-az-1', 'O kit aplicado numa gôndola vazia: clip strip, wobbler e stopper.'), ('Azul · detalhe', 'leves-az-2', 'Clip strip com a cartela e o stopper.'), ('Azul · carrinho', 'carrinho-az', 'Placa de carrinho 30 x 30 cm.'),
     ('Rosa · gôndola', 'leves-rs-1', 'O kit no caminho rosa.'), ('Rosa · detalhe', 'leves-rs-2', 'Clip strip e stopper em rosa.'), ('Rosa · carrinho', 'carrinho-rs', 'Placa de carrinho em rosa.')],
    [('Stopper', '30 x 90 cm'), ('Wobbler', '15 x 15 cm'), ('Clip strip', 'cartela de 16 cm, 5 pares'), ('Carrinho', 'placa 30 x 30 cm')]))
# ------------------------------------------------------------ 04 · próximos passos
T.append(cap('04', 'Próximos passos', 'Da escolha do caminho à loja montada.', ['Escolha do caminho', 'Executivos e artes finais', 'Produção e implantação']))
T.append('''<section id="proximos" class="tela v2-split n" data-tema="escuro" data-titulo="Próximos passos" data-cap="(04) Próximos passos">
  <div class="caixa"><span class="eyebrow anima">Próximos passos</span>
    <h2 class="anima">Da aprovação <span class="t-lime">à loja.</span></h2>
    <ol class="hv-pas anima d1">
      <li>Escolha do caminho de cor: azul, rosa ou os dois por canal.</li>
      <li>Ajustes finos das peças e renders finais.</li>
      <li>Executivo de cada peça: medidas, materiais e quantidades.</li>
      <li>Artes finais de todas as faces e embalagens.</li>
      <li>Cotação, produção e implantação nas lojas.</li>
    </ol></div></section>''')
T.append('''<section id="fim" class="tela s-capa fim" data-tema="foto" data-titulo="Fechamento" data-cap="">
    <div class="foto sangra" role="img" aria-label="KV rosa"></div><div class="veu sangra"></div>
    <div class="texto"><span class="eyebrow anima"><b>(Fechamento)</b> Dia das Mães</span>
      <h1 class="anima d1">Tem<br>Havaianas<br><span class="brilha">pra presente</span></h1>
      <p class="lead anima d2">Um sistema, duas cores · da vitrine ao carrinho</p>
      <div class="acoes anima d3"><button class="botao cheio" data-ir="capa" data-cursor="Voltar">Voltar ao início</button><button class="botao seta" data-ir="caminhos" data-cursor="Ver">Rever os caminhos</button></div></div>
    <div class="marquee sangra"><div>%s</div></div>
  </section>''' % MQ)
ORDEM = ['capa', 'cap-01', 'kv-recebido', 'kv-ideia', 'hierarquia', 'caminhos', 'cap-02', 'mesa', 'vitrine', 'gift', 'embalagens', 'cap-03', 'ilha', 'ponta', 'leves', 'cap-04', 'proximos', 'fim']
ID = lambda t: re.search(r'<section id="([^"]+)"', t).group(1)
assert sorted(ID(t) for t in T) == sorted(ORDEM), [ID(t) for t in T]
T.sort(key=lambda t: ORDEM.index(ID(t)))
CHROME = '''  <header id="topo">
    <div class="marcas"><img class="alp m-escuro" src="assets/marcas/havaianas-creme.webp" alt="Havaianas"><img class="alp m-claro" src="assets/marcas/havaianas-vermelho.webp" alt="Havaianas"><span class="x">×</span><img class="lab m-escuro" src="assets/75lab-lime.png" alt="75 LAB"><img class="lab m-claro" src="assets/75lab-black.png" alt="75 LAB"></div>
    <div class="dir"><span class="cap" id="capTxt"></span><button id="btnSumario" data-sumario data-cursor="Abrir"><span><i></i><i></i><i></i></span>Sumário</button></div>
  </header>
  <footer id="rodape"><span class="assin">75 LAB · Havaianas · Aura Dia das Mães</span>
    <div class="nav"><button id="ant" aria-label="Tela anterior" data-cursor="Voltar">←</button><span id="cont">01 / %02d</span><button id="prox" aria-label="Próxima tela" data-cursor="Seguir">→</button></div></footer>
  <div id="prog"><i></i></div>
  <div id="wipe" class="wipeDuo"><img src="assets/75lab-black.png" alt="75 LAB"><i>×</i><img class="b" src="assets/marcas/havaianas-vermelho.webp" alt="Havaianas"></div>
  <nav id="sumario" aria-label="Sumário"><button class="botao mini fechar" data-cursor="Fechar">Fechar ✕</button><h2>Sumário · <span>Havaianas Aura Dia das Mães</span></h2><ol id="sumLista"></ol></nav>
  <div class="grao"></div>''' % len(T)
POS = '''<div id="caixa" role="dialog" aria-label="Imagem ampliada"><button class="fechar" data-cursor="Fechar">Fechar ✕</button><img id="cxImg" alt=""><p id="cxTxt"></p></div>
<div id="cursor"></div><div id="anel"><span id="anelTxt"></span></div>
<div id="gire"><img src="assets/75lab-lime.png" alt="75 LAB"><div class="tel"></div><h3>Gire o celular</h3><p>A apresentação foi desenhada na horizontal. Deitado, o celular mostra a tela inteira.</p><button class="botao mini" id="verAssim">Ver assim mesmo</button></div>'''
import time
VER = time.strftime('%Y%m%d%H%M')
HEAD = '''<title>Havaianas Aura Dia das Mães</title>
<meta name="description" content="75 LAB · Havaianas Aura Dia das Mães: o KV e as peças de loja própria e B2B.">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;900&family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/deck.css"><link rel="stylesheet" href="assets/bombril.css"><link rel="stylesheet" href="assets/v2.css"><link rel="stylesheet" href="assets/havaianas.css?v=VERSAO">'''.replace('VERSAO', VER)
BODY = ICONES + '\n<div id="wrap"><div id="stage" class="t-lime capa">\n' + '\n'.join(T) + '\n' + CHROME + '\n</div></div>\n' + POS + '\n<script src="assets/deck.js"></script>\n'
full = '<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<link rel="icon" href="assets/75lab-lime.png">\n' + HEAD + '\n</head>\n<body>\n' + BODY + '</body>\n</html>\n'
for bad in ('Bombril', 'Carnaval', 'Limpol', 'lantejoula'): assert bad not in full, bad
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(full)
print(len(T), 'telas', len(full))
