# -*- coding: utf-8 -*-
"""HAV009 · Havaianas Aura Dia das Mães · apresentação interna sobre o deck da agência (base: bombril-carnaval-75lab).
Racional do KV primeiro, depois as peças uma a uma (só azul, com giro 360° na ilha). Gera index.html."""
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
MQ = ''.join('<span>%s</span>' % t for t in ['Dia das Mães, tem Havaianas pra presente', 'Novas Havaianas Aura', 'Loja própria', 'B2B alimentar', 'Da vitrine ao carrinho'] * 3)
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
T.append(cap('01', 'A ideia', 'Antes das peças, a ideia: de onde partimos, como levamos o KV da Aura para o Dia das Mães e a ordem de leitura das peças.', ['O ponto de partida', 'A ideia e os ajustes no KV', 'A hierarquia da informação', 'A variação com imagem']))
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
      <div class="kv"><img src="assets/img/kv-azul.webp" alt="KV com a ordem de leitura marcada"><b style="left:31%;top:20%">1</b><b style="left:60%;top:9%">2</b><b style="left:14%;top:58%">3</b><b style="left:31%;top:90%">4</b></div>
      <ol>
        <li><i>1</i><span><b>Marca</b>Havaianas é sempre o maior elemento, dentro do selo.</span></li>
        <li><i>2</i><span><b>Data e chamada</b>“Dia das Mães, tem … pra presente” abraça a marca no selo.</span></li>
        <li><i>3</i><span><b>Produto</b>Os pares nos frames, de frente para o shopper: a Aura é o presente.</span></li>
        <li><i>4</i><span><b>Assinatura</b>Novas Havaianas Aura, no rodapé de cada peça.</span></li>
      </ol>
    </div>
    <p class="v2-leg anima d2">De cima para baixo: marca, data, produto, lançamento. Seguimos essa ordem em toda face visível, da testeira da ilha ao wobbler de 15 cm.</p>
  </div></section>''')
T.append('''<section id="kv-imagem" class="tela v2-split n" data-tema="escuro" data-titulo="KV com imagem" data-cap="(01) A ideia">
  <div class="caixa"><div class="cn-kv">
    <figure class="anima amplia" data-amplia="assets/img/kv-imagem.webp" data-legenda="KV Dia das Mães · variação com imagem" data-cursor="Ampliar"><img src="assets/img/kv-imagem.webp" alt="KV Dia das Mães, variação com imagem"></figure>
    <div><span class="eyebrow anima"><b>Variação</b> KV com imagem</span>
      <h2 class="anima">O mesmo KV, <span class="t-lime">com o produto no pé.</span></h2>
      <p class="lead anima d1">Quando a peça tem área para foto, a moldura abre uma janela à esquerda com a Aura em uso. O selo, os frames e a assinatura continuam no mesmo lugar e na mesma ordem.</p>
      <ul class="cn-pontos anima d2">
        <li><b>Onde usar</b>Peças com espaço lateral: laterais da ilha e da ponta de gôndola, vitrine e mídia.</li>
        <li><b>O que não muda</b>A ordem de leitura: marca, data, produto e lançamento.</li>
      </ul></div>
  </div></div></section>''')
# ------------------------------------------------------------ 02 · lojas próprias
T.append(cap('02', 'Lojas próprias', 'Da vitrine ao caixa: o presente começa na rua e termina embalado na mão da cliente.', ['Mesa Big Hello', 'Big Hello nas mesas das lojas', 'Glorifier de prateleira', 'Vitrine', 'Gift Station modular', 'Embalagens']))
T.append(core('mesa', '(02) Lojas próprias', 'Mesa Big Hello', 'Loja própria · LP01 · Big Hello · móvel novo', 'O presente <span class="t-lime">logo na entrada.</span>', 'Base azul sobre pés reguláveis, com dois tampos de madeira. A chamada sai da testeira em relevo, como letra caixa. Três frames com os Charms e seus precificadores, quatro Glossy em caixas abertas e o laço dourado fechando a base como um presente.',
    [('Frontal', 'mesa-r5-1', 'Frontal: chamada em relevo, frames dos Charms e as caixas abertas dos Glossy.'), ('3/4', 'mesa-r5-2', 'Os dois tampos de madeira e o laço dourado na base.'),
     ('Chamada em relevo', 'mesa-r5-relevo', 'Logo com 2 cm de relevo; moldura e textos com 1,2 cm.'), ('Caixas abertas', 'mesa-r5-caixas', 'Degrau de baixo: quatro Glossy em caixas abertas, com cetim, fita e laço.'),
     ('Caixas · 3/4', 'mesa-r5-caixas2', 'As caixas abertas em 3/4.'), ('Close da caixa', 'mesa-r5-caixa', 'O par deitado no cetim.'),
     ('Caixa e envelope', 'mesa-r5-envelope', 'Nas laterais: caixa aberta inclinada e a caixa envelope com a fita passando pela alça.'), ('Precificadores', 'mesa-r5-preco', 'Plaquinha de acrílico em L à frente de cada frame.'), ('Pés reguláveis', 'mesa-r5-pes', 'A mesa fica 3 cm acima do piso, sobre sapatas niveladoras.')],
    [('Planta', '202 x 110 cm'), ('Base', 'azul, 2 tampos de madeira, pés reguláveis'), ('Chamada', 'relevo de 1,2 a 2 cm'), ('Produto', '3 Charms em frames, 4 Glossy em caixas')]))
T.append(core('mesa-lojas', '(02) Lojas próprias', 'Big Hello nas mesas das lojas', 'Loja própria · Big Hello · mesas atuais', 'A mesma ideia, <span class="t-lime">na mesa que a loja já tem.</span>', 'Para as lojas que usam a mesa atual: uma peça em L de PS veste a mesa, com a chamada em letra caixa e a moldura invertida no avental. Uma carenagem única abraça os dois caixotes com os Glossy, e os Charms ficam nos frames.',
    [('Sem apoios', 'loja-a-1', 'Mesa central com os dois caixotes no pé, a peça em L e os frames.'), ('Sem apoios · 3/4', 'loja-a-2', 'A mesa se estende para trás; a peça ocupa a frente.'),
     ('Avental e caixotes', 'loja-a-avental', 'Moldura invertida no avental e a carenagem dos caixotes com o lockup.'), ('Tags de preço', 'loja-a-tags', 'Tag pequena em haste, presa por dentro do caixote, ao lado de cada cor.'),
     ('Peça em L', 'loja-a-l', 'Fundo em duas camadas, logo e lettering em letra caixa fina.'),
     ('Com apoios', 'loja-b-1', 'Versão com dois apoios laterais: caixa de presente aberta e caixa envelope.'), ('Com apoios · 3/4', 'loja-b-2', 'A versão com apoios em 3/4.'),
     ('Apoio lateral', 'loja-b-apoio', 'Caixa aberta inclinada sobre calço de acrílico e envelope com a fita na alça.'), ('Pés', 'loja-b-pes', 'Pés de madeira inclinados, no estilo das mesas da loja.')],
    [('Mesa', '122 x 150 x 78 cm (a confirmar)'), ('Caixotes', '2, na largura da mesa'), ('Peça em L', 'PS, chamada em letra caixa'), ('Produto', '4 Glossy nos caixotes, 3 Charms nos frames')]))
T.append(core('prateleira', '(02) Lojas próprias', 'Glorifier de prateleira', 'Loja própria · prateleira da parede ripada', 'O espaço da Aura <span class="t-lime">na parede.</span>', 'A peça em L em versão reduzida, sobre a prateleira da parede ripada: três frames estreitos com um chinelo de cada cor, a frase no avental e uma tag de preço. Embaixo, as gancheiras com os três Charms.',
    [('Frontal', 'prat-1', 'A peça sobre a prateleira, com as gancheiras embaixo.'), ('3/4', 'prat-2', 'A peça em 3/4.'),
     ('Peça em L', 'prat-l', 'Frames de um chinelo, com a mesma moldura reduzida.'), ('Avental e frase', 'prat-frase', 'Moldura invertida com Novas Havaianas Aura em relevo fino.')],
    [('Peça', '84 cm de largura, PS'), ('Frames', '3, um chinelo de cada cor'), ('Preço', '1 tag em L'), ('Gancheiras', '3 fileiras de Charms')]))
T.append(core('vitrine', '(02) Lojas próprias', 'Vitrine', 'Loja própria · vitrine', 'A vitrine vira <span class="t-lime">uma caixa de presente.</span>', 'No fundo, três bases em camadas: as imagens dos dois lados, a moldura creme e a base azul com o lockup em relevo e LED nas laterais. Na frente, a mesa com as caixas abertas, os frames e os presentes brancos com fita azul.',
    [('Frontal', 'vit5-1', 'A vitrine inteira: as três bases em camadas atrás da mesa.'), ('3/4', 'vit5-2', 'A vitrine em 3/4: a profundidade entre as camadas.'),
     ('Centro', 'vit5-close', 'O lockup em relevo sobre a base azul e a mesa com as caixas abertas.'), ('Bases e LED', 'vit5-led', 'O LED sai das laterais da base azul e lava o painel de imagem.')],
    [('Base', 'vitrine padrão das lojas'), ('Fundo', '3 camadas: imagens, creme e azul'), ('Lockup', 'em relevo, LED nas laterais da base azul'), ('Cenografia', 'presentes brancos com fita azul')]))
T.append(core('gift', '(02) Lojas próprias', 'Gift Station modular', 'Loja própria · LP13 · ativação', 'Onde o presente <span class="t-lime">é embalado.</span>', 'Um sistema de peças soltas: os mesmos acessórios vivem na estrutura de metalon azul ou em cima do balcão da loja. Na estrutura, a testeira leva a mensagem em letra caixa; no balcão, ela vira uma base em L de PS.',
    [('Estrutura', 'gs3-g-1', 'Versão completa: estrutura de metalon azul, testeira em letra caixa, gaveteiro e os acessórios.'), ('Estrutura · 3/4', 'gs3-g-2', 'A estrutura em 3/4.'),
     ('Testeira', 'gs3-g-testeira', 'Selo, Espaço Presente e a frase em letra caixa.'), ('Bancada', 'gs3-g-bancada', 'Porta-sedas, bandejas de acrílico, torre de fitas e porta-caixas sobre o gaveteiro.'),
     ('No balcão', 'gs3-b-1', 'Loja menor: sem a estrutura, os mesmos acessórios ambientam o balcão da loja.'), ('Balcão · 3/4', 'gs3-b-2', 'O balcão em 3/4.'),
     ('Base em L', 'gs3-b-l', 'A testeira vira uma base em L de PS, com as bandejas na frente.'), ('Acessórios no balcão', 'gs3-b-mod', 'Torre de fitas, porta-caixas e porta-envelopes.'),
     ('Line-up', 'gs3-lineup', 'Todas as peças do sistema, separadas.'), ('Acessórios', 'gs3-acessorios', 'Os acessórios soltos: porta-sedas, torre de fitas, base em L, bandejas, porta-caixas e porta-envelopes.'),
     ('Cartão', 'cartao-mockup', 'Cartão de Dia das Mães que acompanha o presente.')],
    [('Estrutura', 'metalon azul, 115 x 42 x 236 cm'), ('Balcão', 'base em L de PS, 100 x 61 cm'), ('Acessórios', '5 módulos soltos'), ('Cartão', 'Dia das Mães, acompanha o presente')]))
T.append(core('embalagens', '(02) Lojas próprias', 'Embalagens', 'Loja própria · embalagens', 'O KV vai <span class="t-lime">para casa.</span>', 'Dois caminhos para a sacola: impressa com a arte da campanha, ou a sacola vermelha vigente com uma solapa promocional de fechamento. Caixas só no vermelho, com luvas de borda creme; caixa envelope com a alça no topo.',
    [('Sacola impressa', 'sac5-imp-1', 'Sacolas P, M e G impressas com a moldura e o lockup da campanha.'),
     ('Solapa', 'sac5-sol-1', 'Sacola vermelha vigente fechada com a solapa promocional: aba com a moldura invertida em duas camadas e rasgo para as alças.'),
     ('Caixas', 'pack-az-1', 'Caixas vermelhas com as luvas e a caixa envelope com alça.')],
    [('Caixas', 'vermelhas, com ou sem luva'), ('Envelope', '26 x 9 x 46 cm, alça no topo'), ('Sacolas', 'P, M e G, impressa ou com solapa'), ('Solapa', 'papel-cartão, 2 camadas, faca especial')]))
# ------------------------------------------------------------ 03 · B2B
T.append(cap('03', 'B2B alimentar', 'No supermercado a Aura disputa atenção: peças que param o carrinho e mostram o par de perto.', ['Ponta de gôndola', 'Ilha com cubos giratórios', 'Peças leves']))
T.append(core('ilha', '(03) B2B alimentar', 'Ilha', 'B2B alimentar · BA08', 'Cubos que giram, <span class="t-lime">produto que se pega.</span>', 'Peça central com os cubos giratórios no recorte, laterais em três camadas com a foto, pares presos direto na peça e adesivo de chão redondo.',
    [('Frontal', 'ilha-az-1', 'De frente: peça central com a testeira, lateral com a foto e os cubos.'), ('3/4', 'ilha-az-2', 'As laterais em três camadas e o adesivo de chão.'), ('Cubos', 'ilha-az-3', 'Os três cubos giratórios com os cards dos pares.')],
    [('Altura', '263,5 cm no topo da peça central'), ('Adesivo', 'chão, Ø 2,68 m'), ('Laterais', '3 camadas com a foto do KV'), ('Produto', 'pares presos na peça, cubos giratórios')]))
T.append(core('ponta', '(03) B2B alimentar', 'Ponta de gôndola', 'B2B alimentar · BA07', 'O racional da campanha, <span class="t-lime">na ponta.</span>', 'Testeira com a chamada e a borda em relevo e laterais em camadas com a imagem da campanha. Charms na frente e Glossy na lateral, presos direto na base de trás.',
    [('Frontal', 'ponta5-1', 'Frontal: testeira com a chamada em relevo e os Charms.'), ('Esquerda', 'ponta5-2', 'A lateral cobre a gancheira.'), ('Direita', 'ponta5-3', 'A lateral direita com a imagem e os Glossy.')],
    [('Largura', '120 cm'), ('Laterais', 'em camadas, com a imagem da campanha'), ('Testeira', 'chamada e borda em relevo'), ('Produto', 'pares presos na base de trás')]))
def bn_fig(src, leg):
    return '<figure class="amplia" data-amplia="assets/img/%s.webp" data-legenda="%s" data-cursor="Ampliar"><img src="assets/img/%s.webp" alt="%s" loading="lazy"><figcaption>%s</figcaption></figure>' % (src, leg, src, leg, leg.split(' · ')[-1])
LEVES = [  # (nome, medida, chave das imagens, [(dt, dd)])
    ('Testeira de gôndola', '100 x 30 cm', 'testeira', [('Onde', 'No topo do módulo, projetada à frente em dois braços de aço encaixados na cremalheira'), ('Material', 'PS 2 mm, impressão 4/0, faca no contorno da moldura'), ('Medida', '100 x 30 cm')]),
    ('Stopper', '30 x 90 cm', 'stopper', [('Onde', 'Perpendicular à gôndola, preso no trilho de preço pelo lado reto'), ('Material', 'PS 2 mm, impressão 4/4, faca no contorno'), ('Medida', '30 x 90 cm')]),
    ('Wobbler', '15 x 15 cm', 'wobbler', [('Onde', 'Na frente da prateleira, na altura dos olhos'), ('Material', 'PS 1 mm, impressão 4/0, haste de acrílico'), ('Medida', '15 x 15 cm')]),
    ('Clip strip', 'cartela + 5 pares', 'clip', [('Onde', 'Na emenda entre dois módulos, preso no trilho'), ('Material', 'Tira em PS 1 mm e cartela em PS 2 mm, 4/4'), ('Capacidade', '5 pares Aura')]),
    ('Moldura de gôndola', '67 x 188 cm', 'moldura', [('Onde', 'Do topo à base do módulo, emoldurando os pares da Havaianas'), ('Material', 'PS 2 mm, impressão 4/0, janela vazada'), ('Medida', '67 x 188 cm')]),
    ('Tag', '18 x 10 cm', 'tag', [('Onde', 'No gancho, à frente do primeiro par'), ('Material', 'PS 1 mm, impressão 4/4, faca com gancho'), ('Medida', '18 x 10 cm')]),
    ('Placa de carrinho', '30 x 30 cm', 'carrinho', [('Onde', 'Na frente do carrinho, fixada na grade'), ('Material', 'PS 2 mm, impressão 4/0, abraçadeiras'), ('Medida', '30 x 30 cm')]),
]
def fotos_cor(k, cor):
    fs = [('carrinho-%s' % cor, 'Aplicada')] if k == 'carrinho' else [('leve-%s-solo-%s' % (k, cor), 'A peça'), ('leve-%s-aplic-%s' % (k, cor), 'Aplicada')]
    fs = [f for f in fs if IMG(f[0])]
    return '<div class="bn-fotos %s cobre" data-cor="%s">%s</div>' % ('duas' if len(fs) > 1 else 'uma', cor, ''.join(bn_fig(a, b) for a, b in fs)) if fs else ''
bts = ''.join('<button data-aba class="%s" data-cursor="Ver"><i>%02d</i><b>%s</b><small>%s</small></button>' % ('on' if q == 0 else '', q + 1, n, m) for q, (n, m, k, fc) in enumerate(LEVES))
pns = ''.join('<div class="bn-p %s" data-painel data-ver="az">%s<div class="bn-ficha"><h3>%s</h3><dl>%s</dl></div></div>' % (
    'on' if q == 0 else '', fotos_cor(k, 'az'), n, ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % x for x in fc)) for q, (n, m, k, fc) in enumerate(LEVES))
T.append('''<section id="leves" class="tela s-bniv n" data-tema="escuro" data-titulo="Peças leves" data-cap="(03) B2B alimentar">
  <div class="caixa"><div class="bn-gr">
    <div class="bn-esq"><span class="eyebrow anima"><b>B2B alimentar</b> · kit de gôndola</span>
      <h2 class="anima d1">Peças <span class="t-lime">leves</span></h2>
      <p class="anima d1">O selo funciona em qualquer tamanho: cada peça leva a marca e a data para toda loja. Em cada uma, a peça sozinha e a peça aplicada.</p>
      <div class="bn-lista anima d2">%s</div></div>
    <div class="bn-palco anima d2">%s</div>
  </div></div></section>''' % (bts, pns))
# ------------------------------------------------------------ 04 · próximos passos
T.append(cap('04', 'Próximos passos', 'Da aprovação à loja montada.', ['Aprovação', 'Executivos e artes finais', 'Produção e implantação']))
T.append('''<section id="proximos" class="tela v2-split n" data-tema="escuro" data-titulo="Próximos passos" data-cap="(04) Próximos passos">
  <div class="caixa"><span class="eyebrow anima">Próximos passos</span>
    <h2 class="anima">Da aprovação <span class="t-lime">à loja.</span></h2>
    <ol class="hv-pas anima d1">
      <li>Aprovação das peças e do KV.</li>
      <li>Ajustes finos das peças e renders finais.</li>
      <li>Executivo de cada peça: medidas, materiais e quantidades.</li>
      <li>Artes finais de todas as faces e embalagens.</li>
      <li>Cotação, produção e implantação nas lojas.</li>
    </ol></div></section>''')
T.append('''<section id="fim" class="tela s-capa fim" data-tema="claro" data-titulo="Fechamento" data-cap="">
    <div class="foto sangra" role="img" aria-label="KV Dia das Mães"></div><div class="veu sangra"></div>
    <div class="texto"><span class="eyebrow anima"><b>(Fechamento)</b> Dia das Mães</span>
      <h1 class="anima d1">Tem<br>Havaianas<br><span class="brilha">pra presente</span></h1>
      <p class="lead anima d2">Um sistema · da vitrine ao carrinho</p>
      <div class="acoes anima d3"><button class="botao cheio" data-ir="capa" data-cursor="Voltar">Voltar ao início</button><button class="botao seta" data-ir="kv-ideia" data-cursor="Ver">Rever a ideia</button></div></div>
    <div class="marquee sangra"><div>%s</div></div>
  </section>''' % MQ)
ORDEM = ['capa', 'cap-01', 'kv-recebido', 'kv-ideia', 'hierarquia', 'kv-imagem', 'cap-02', 'mesa', 'mesa-lojas', 'prateleira', 'vitrine', 'gift', 'embalagens', 'cap-03', 'ponta', 'ilha', 'leves', 'cap-04', 'proximos', 'fim']
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
BODY = ICONES + '\n<div id="wrap"><div id="stage" class="t-lime capa">\n' + '\n'.join(T) + '\n' + CHROME + '\n</div></div>\n' + POS + '\n<script src="assets/deck.js"></script>\n<script src="assets/havaianas.js?v=' + VER + '"></script>\n'
full = '<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<link rel="icon" href="assets/75lab-lime.png">\n' + HEAD + '\n</head>\n<body>\n' + BODY + '</body>\n</html>\n'
for bad in ('Bombril', 'Carnaval', 'Limpol', 'lantejoula'): assert bad not in full, bad
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(full)
print(len(T), 'telas', len(full))
