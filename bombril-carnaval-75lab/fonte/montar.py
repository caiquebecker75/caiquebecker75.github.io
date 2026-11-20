# -*- coding: utf-8 -*-
"""BOM003 · monta a apresentação do Carnaval Bombril 2027 sobre o deck da agência (base: bombril-cadeirinha-75lab).
Gera index.html (abre direto no navegador) e artifact.html (página para publicar como Artifact)."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
REF = open(sys.argv[1], encoding='utf-8').read()
ICONES = REF[REF.index('<svg width="0" height="0"'):REF.index('</svg>') + 6]
CAPS = [('01', 'O brilho'), ('02', 'Na gôndola'), ('03', 'Peças de impacto'), ('04', 'A ilha'), ('05', 'Na rua e no time'), ('06', 'Por que a 75 LAB')]
def trilha(at): return '<div class="trilha-cap anima d4" data-atual="%s">%s</div>' % (at, ''.join('<span data-c="%s">%s<b>%s</b></span>' % (n, n, t) for n, t in CAPS))
def cap(n, tit, lead, itens):
    return '''<section id="cap-%s" class="tela s-cap" data-tema="lime" data-titulo="Capítulo %s · %s" data-cap="(%s) %s" data-capitulo="%s">
    <span class="num-cap sangra">%s</span>
    <div class="texto"><span class="eyebrow anima"><b>Capítulo %s</b> de 06</span><h2 class="anima d1">%s</h2><p class="lead anima d2">%s</p></div>
    <ol class="dentro anima d3">%s</ol>%s</section>''' % (n, n, tit, n, tit, n, n, n, tit, lead, ''.join('<li><i>%02d</i>%s</li>' % (i + 1, t) for i, t in enumerate(itens)), trilha(n))
def fig(src, leg): return '<figure class="amplia" data-amplia="assets/img/%s.webp" data-legenda="%s" data-cursor="Ampliar"><img src="assets/img/%s.webp" alt="%s" loading="lazy"></figure>' % (src, leg, src, leg)
def core(id_, capn, tit, eyebrow, h2, lead, abas, ficha, tema='escuro', exe=None):
    """abas: [(rótulo, imagem ou ('vid', arquivo), legenda)]"""
    bts = ''.join('<button data-aba="%d" class="%s" data-cursor="Ver"><i>%02d</i><b>%s</b></button>' % (i, 'on' if i == 0 else '', i + 1, a[0]) for i, a in enumerate(abas))
    pns = ''
    for i, (rot, src, leg) in enumerate(abas):
        if isinstance(src, tuple): m = '<figure><video src="assets/vid/%s.mp4" poster="assets/img/%s.webp" muted loop playsinline preload="metadata" aria-label="%s"></video></figure>' % (src[1], src[2] if len(src) > 2 else 'display-cheio', rot)
        else: m = fig(src, rot)
        pns += '<div data-painel="%d" class="%s">%s<p>%s</p></div>' % (i, 'on' if i == 0 else '', m, leg)
    fc = ''.join('<dt>%s</dt><dd>%s</dd>' % f for f in ficha)
    bx = ('<button class="bt-exec anima d3" type="button" data-exec="%s" data-cursor="Em breve"><svg viewBox="0 0 48 48" aria-hidden="true"><use href="#i-arquivo"/></svg><span><b>Mini executivo</b><i>medidas macro para cotação · em breve</i></span></button>' % exe) if exe else ''
    return '''<section id="%s" class="tela s-core n" data-tema="%s" data-titulo="%s" data-cap="%s">
    <div class="caixa"><div class="gr-core">
      <div class="txt-core"><span class="eyebrow anima">%s</span><h2 class="anima">%s</h2><p class="lead anima d1">%s</p>
        <div class="abas-b vers anima d2">%s</div>
        <dl class="ficha-core anima d3">%s</dl>%s</div>
      <div class="paineis foto-core anima dir d1">%s</div>
    </div></div></section>''' % (id_, tema, tit, capn, eyebrow, h2, lead, bts, fc, bx, pns)
T = []
# ---------------------------------------------------------------- capa
MQ = ''.join('<span>%s</span>' % t for t in ['Bombril faz seu Carnaval brilhar', 'Na rua', 'Na loja', 'Nas redes', 'O brilho é da Bombril', 'Carnaval 2027'] * 3)
T.append('''<section id="capa" class="tela s-capa capa-kv ativa" data-tema="lime" data-titulo="Capa" data-cap="">
    <div class="kv-cam conf sangra" aria-hidden="true"></div><div class="kv-cam logo sangra" role="img" aria-label="Bombril em lantejoulas"></div><div class="kv-cam frase sangra" role="img" aria-label="Faz seu Carnaval brilhar"></div>
    <div class="texto">
      <h1 class="so-leitor">Bombril faz seu Carnaval brilhar</h1>
      <span class="eyebrow anima"><b>(Carnaval 2027)</b> Bombril · Trade marketing</span>
      <p class="lead anima d2">Da rua ao caixa, a loja inteira em lantejoula · criação, produção e ativação 75 LAB</p>
      <div class="acoes anima d3"><button class="botao cheio seta" data-ir="cap-01" data-cursor="Ir">Começar</button></div>
    </div>
    <span class="rot sangra anima d4">75 LAB · Concorrência Bombril · Nov/26</span>
    <div class="marquee sangra"><div>%s</div></div>
  </section>''' % MQ)
# ---------------------------------------------------------------- 01 · o brilho
T.append(cap('01', 'O brilho', 'O brilho é da Bombril desde 1948.<br>No Carnaval, ele sai de casa e vai para a avenida.', ['O KV: a base vestida de lantejoula', 'A linguagem em quatro elementos', 'Uma campanha modular']))
T.append('''<section id="kv" class="tela v2-split n" data-tema="escuro" data-titulo="O KV" data-cap="(01) O brilho">
  <div class="caixa"><div class="cn-kv">
    <figure class="anima amplia" data-amplia="assets/img/kv.webp" data-legenda="KV Bombril Carnaval 2027" data-cursor="Ampliar"><img src="assets/img/kv.webp" alt="KV Bombril Carnaval 2027"></figure>
    <div><span class="eyebrow anima"><b>KV</b> Carnaval 2027</span>
      <h2 class="anima">Recebemos a base. <span class="brilha">Vestimos de Carnaval.</span></h2>
      <p class="lead anima d1">A Bombril nos entregou o logo em lantejoulas e a frase da campanha. A partir deles, criamos o universo que leva esse brilho para a loja inteira.</p>
      <ul class="cn-pontos anima d2">
        <li><b>Fundo em lantejoula amarela</b>O amarelo da embalagem vira tecido de fantasia. A marca passa a ocupar a loja inteira, e o brilho deixa de ser só gráfico.</li>
        <li><b>Confete vermelho metalizado</b>Os dois tons da Bombril, sem cor emprestada. De longe, é Bombril antes de ser Carnaval.</li>
        <li><b>Plumas</b>Acrescentamos um elemento para compor as peças. As plumas dão volume e silhueta às testeiras e fazem o logo virar destaque de escola de samba.</li>
      </ul></div>
  </div></div></section>''')
T.append('''<section id="linguagem" class="tela v2-split n" data-tema="claro" data-titulo="A linguagem" data-cap="(01) O brilho">
  <div class="caixa"><h2 class="anima">Quatro elementos, <span class="onda t-teal">todas as peças.</span></h2>
    <div class="cn-4 anima d1">
      <div><div class="cn-fig lant"></div><h3>Lantejoula</h3><p>O fundo de todas as peças. Impressa em 4 cores, sem custo de acabamento especial: brilha na arte, em qualquer substrato.</p></div>
      <div><div class="cn-fig"><img src="assets/img/logo.webp" alt="Logo Bombril em lantejoulas" loading="lazy"></div><h3>Logo em lantejoulas</h3><p>Sempre inteiro, sempre o maior elemento. Nas peças de impacto, vira aplique retroiluminado.</p></div>
      <div><div class="cn-fig"><img src="assets/img/plumas.webp" alt="Plumas vermelhas e amarelas" loading="lazy"></div><h3>Plumas</h3><p>A faca especial das testeiras. Recortadas em PETG transparente, parecem flutuar acima do móvel.</p></div>
      <div><div class="cn-fig"><img src="assets/img/frase.webp" alt="Faz seu Carnaval brilhar" loading="lazy"></div><h3>A frase</h3><p>“Faz seu Carnaval brilhar” fecha a leitura em toda face visível: marca em cima, chamada embaixo.</p></div>
    </div></div></section>''')
T.append('''<section id="estrategia" class="tela v2-split n" data-tema="escuro" data-titulo="Uma campanha modular" data-cap="(01) O brilho">
  <div class="caixa"><span class="eyebrow anima">Onde investir mais, onde ganhar escala</span>
    <h2 class="anima">Uma campanha modular, <span class="t-lime">do linear ao grande impacto.</span></h2>
    <div class="cn-kits anima d1">
      <div class="v2-card"><span class="eti">Kit nacional · todas as lojas</span><h3>Na gôndola</h3><ul><li>Faixa de gôndola em L, 40 x 5 cm</li><li>Wobbler 15 x 15 cm, com faca especial</li><li>Gargaleira 6,5 x 18 cm</li><li>Forração de ponto extra</li></ul></div>
      <div class="v2-card escuro"><span class="eti">Kit de impacto · lojas-chave</span><h3>No ponto extra</h3><ul><li>Ponta de gôndola retrátil, que se ajusta à gôndola de cada loja</li><li>Display de chão em polionda, 3 prateleiras</li><li>Lateral trocável pelo compre e ganhe</li></ul></div>
      <div class="v2-card ouro"><span class="eti">Praças prioritárias</span><h3>Grande impacto</h3><ul><li>Uma ilha promocional para as praças prioritárias</li><li>Feita com os mesmos módulos do kit</li><li>Pronta para se personalizar em cada praça</li></ul></div>
    </div>
    <p class="v2-leg anima d2">As peças compartilham arte, substratos e facas: o que se produz para uma serve à outra, e o investimento cresce em degraus, não em saltos.</p>
  </div></section>''')
# ---------------------------------------------------------------- 02 · na gôndola
T.append(cap('02', 'Na gôndola', 'O kit nacional: quatro peças leves, baratas e rápidas, para vestir o linear de qualquer loja.', ['Faixa de gôndola', 'Wobbler', 'Gargaleira', 'Forração de ponto extra']))
T.append(core('leves', '(02) Na gôndola', 'O kit nacional', 'Kit nacional · canal direto e indireto', 'O linear inteiro <span class="t-lime">em lantejoula.</span>', 'Peças que viajam planas, instalam em segundos e funcionam em qualquer rede.',
    [('Faixa de gôndola', 'faixa', 'A faixa é uma peça em L que vai em cima da prateleira: o pé deita sob os produtos e a frente em lantejoula fica em pé na borda, com o logo subindo como um recorte.'),
     ('Faixa no módulo', 'faixa-geral', 'Duas faixas de 40 cm por prateleira cobrem um módulo de 1 m.'),
     ('Wobbler', 'wobbler', 'Pende da borda da prateleira, na altura dos olhos. Faca especial, com os confetes fazendo parte do recorte.'),
     ('Gargaleira', 'gargaleira', 'A campanha na embalagem: de frente e de lado. O furo veste o gargalo e o vinco, logo abaixo dele, dobra a parte de cima para trás.'),
     ('Forração', 'forracao', 'Envolve a pilha de pallets, rente à borda. A arte é contínua: onde acaba uma, começa a outra.')],
    [('Faixa', '40 x 5 cm · PS 1 mm, em L'), ('Wobbler', '15 x 15 cm · PS 1 mm com haste'), ('Gargaleira', '6,5 x 18 cm · cartão 300 g'), ('Forração', 'módulo de 100 x 50 cm · filme contínuo')]))
# ---------------------------------------------------------------- 03 · peças de impacto
T.append(cap('03', 'Peças de impacto', 'Duas peças que seguram o ponto extra sozinhas, pensadas para produzir rápido e montar sem ferramenta.', ['Ponta de gôndola retrátil', 'A ponta em movimento', 'Display de chão']))
T.append(core('ponta', '(03) Peças de impacto', 'Ponta de gôndola retrátil', 'Carenagem de gôndola', 'Uma peça, <span class="t-lime">todas as gôndolas.</span>', 'Quatro quadrantes deslizam na largura e na altura. Os apliques ficam por cima e escondem as emendas: em qualquer tamanho, a peça parece inteira.',
    [('Em movimento', ('vid', 'ponta-expansao', 'ponta-persp'), 'A carenagem expande e retrai na largura e na altura, para vestir a gôndola de cada loja.'),
     ('Perspectiva', 'ponta-persp', 'Abastecida com Limpol Perfumes, 5 fragrâncias em blocos verticais, com a faixa de gôndola na frente das prateleiras.'),
     ('Testeira iluminada', 'ponta-testeira', 'O logo é um aplique afastado, com LED atrás: a luz cai sobre a base e as plumas, como um letreiro.'),
     ('Lateral', 'ponta-lateral', 'A lateral é um aplique removível. Sai a arte da campanha, entra o compre e ganhe.')],
    [('Largura', 'de 104 a 134 cm'), ('Altura', 'de 148 a 190 cm'), ('Base', 'polionda 4 mm impressa'), ('Apliques', 'plumas e logo em PETG; logo com LED')], exe='ponta'))
T.append('''<section id="ponta-mov" class="tela s-can n" data-tema="escuro" data-titulo="A ponta em movimento" data-cap="(03) Peças de impacto">
    <div class="caixa"><div class="gr-can">
      <div class="lado-can"><h2 class="anima">Ela se ajusta. <span class="t-lime">E troca de assunto.</span></h2>
        <div class="abas-b lista-cen anima d1"><button data-aba="0" class="on" data-cursor="Ver"><i>01</i><b>Expande e retrai</b></button><button data-aba="1" class="" data-cursor="Ver"><i>02</i><b>Troca da lateral</b></button><button data-aba="2" class="" data-cursor="Ver"><i>03</i><b>Peças separadas</b></button></div>
        <div class="paineis txt-can anima d2"><div data-painel="0" class="on"><p>A mesma carenagem veste uma gôndola de 1 m ou de 1,30 m, baixa ou alta. Um só item no CD para todas as lojas.</p></div><div data-painel="1" class=""><p>O aplique lateral sai e entra o do compre e ganhe: a promoção ganha visibilidade sem produzir outra peça.</p></div><div data-painel="2" class=""><p>O que compõe a carenagem: quatro cantos e duas réguas de coluna na base, e por cima os apliques da testeira, do logo, das laterais e da base inferior.</p></div></div></div>
      <div class="paineis palco-can anima dir d1"><div data-p2="0" class="on"><video src="assets/vid/ponta-expansao.mp4" poster="assets/img/ponta-persp.webp" muted loop playsinline preload="metadata" aria-label="Animação: a ponta expande e retrai"></video></div><div data-p2="1" class=""><video src="assets/vid/ponta-troca.mp4" poster="assets/img/ponta-lateral.webp" muted loop playsinline preload="metadata" aria-label="Animação: troca da lateral pelo compre e ganhe"></video></div><div data-p2="2" class=""><video src="assets/vid/ponta-explode.mp4" poster="assets/img/ponta-persp.webp" muted loop playsinline preload="metadata" aria-label="Animação: a ponta se abre nas peças que a compõem"></video></div></div>
    </div></div></section>''')
T.append(core('display', '(03) Peças de impacto', 'Display de chão', 'Display de chão · polionda', 'Simples de montar, <span class="t-lime">impossível de ignorar.</span>', 'Três prateleiras com a faixa de lantejoula na frente e o logo como aba. As costas sobem em plumas, com margem transparente só onde a faca precisa.',
    [('Girando', ('vid', 'display-giro', 'display-cheio'), 'A peça gira devagar, de um lado ao outro, sempre de frente para o shopper.'),
     ('Abastecido', 'display-cheio', 'Limpol Perfumes: 5 fragrâncias por prateleira, 5 de fundo.'),
     ('Vazio', 'display-vazio', 'Interno todo amarelo, base no tom da arte e pés pretos redondos.'),
     ('Testeira', 'display-testeira', 'O logo é um aplique à frente das plumas.'),
    ],
    [('Medida', '63,6 x 53 x 186,7 cm'), ('Prateleiras', '3, com vão de 37 cm'), ('Material', 'polionda 4 mm'), ('Abastece', '75 frascos de 500 ml')], tema='claro', exe='display'))
# ---------------------------------------------------------------- 04 · a ilha
T.append(cap('04', 'A ilha', 'A peça que faz a loja inteira entrar no Carnaval: um portal que se atravessa.', ['A ilha nacional', 'Do que ela é feita', 'Pronta para se personalizar']))
T.append(core('ilha', '(04) A ilha', 'A ilha nacional', 'Ilha promocional · praças prioritárias', 'Um portal de Carnaval <span class="t-lime">no meio da loja.</span>', 'Doze displays em quatro fileiras, de costas uns para os outros, unidos por dois arcos. O shopper entra, compra dos dois lados e sai do outro.',
    [('Girando', ('vid', 'ilha-giro', 'ilha-persp'), 'A ilha de todos os lados: dois portais, quatro fileiras de displays e o adesivo que une tudo.'),
     ('Perspectiva', 'ilha-persp', 'Limpol e Mon Bijou voltados para fora, lã de aço Bombril no corredor.'),
     ('Entrada', 'ilha-frente', 'Logo e plumas em dois apliques. O vão tem 150 x 209 cm.'),
     ('Lateral', 'ilha-lado', 'Cada fileira de três displays ganha uma testeira única, com logo iluminado.'),
     ('De cima', 'ilha-topo', 'O adesivo redondo unifica tudo e marca a entrada e a saída.'),
     ('Vazia', 'ilha-vazia', 'A estrutura sem produto: base reta com fitilhos vermelhos e dourados.'),
    ],
    [('Área', 'adesivo de 480 cm de diâmetro'), ('Portal', '313 cm de largura, plumas a 324 cm'), ('Corredor', '145 cm livres'), ('Displays', '12, em polionda')], exe='ilha'))
T.append('''<section id="ilha-partes" class="tela v2-split n" data-tema="claro" data-titulo="Do que ela é feita" data-cap="(04) A ilha">
  <div class="caixa"><h2 class="anima">Grande no impacto, <span class="onda t-teal">simples na conta.</span></h2>
    <div class="v2-nums anima d1">
      <div><b>12</b><span>displays de chão</span><i>o mesmo módulo do kit de impacto, com base reta</i></div>
      <div><b>2</b><span>portais</span><i>caixa de 6 cm, arte nos dois lados</i></div>
      <div><b>4</b><span>testeiras de grupo</span><i>a testeira da ponta de gôndola, ampliada</i></div>
      <div class="lime"><b>6</b><span>logos iluminados</span><i>apliques com LED atrás, mais a fita de LED nas bordas dos arcos</i></div>
      <div><b>1</b><span>adesivo de chão</span><i>redondo, com quatro logos</i></div>
      <div><b>0</b><span>peça exclusiva de estrutura</span><i>tudo deriva das peças que já estão no kit</i></div>
    </div>
    <p class="v2-leg anima d2">Na base de cada display, fitilhos metalizados vermelhos e dourados substituem a frente impressa: movimento e brilho de verdade, com material de baixo custo.</p>
  </div></section>''')
T.append('''<section id="regional" class="tela v2-split n" data-tema="escuro" data-titulo="Pronta para se personalizar" data-cap="(04) A ilha">
  <div class="caixa"><span class="eyebrow anima">Personalização por praça</span>
    <h2 class="anima">Uma única estrutura, <span class="brilha">pronta para vestir cada praça.</span></h2>
    <div class="cn-reg anima d1">
      <div class="ilha"><span>Estrutura-base · igual em todo o Brasil</span><img src="assets/img/ilha-vazia.webp" alt="Ilha nacional, estrutura-base" loading="lazy"></div>
      <div style="display:flex;flex-direction:column;gap:22px;min-height:0;justify-content:center">
        <p class="lead" style="font-size:22px;line-height:1.45;max-width:760px">A ilha nasce como uma estrutura modular e padronizada. Sobre ela, cada praça prioritária pode ganhar a própria identidade, com as referências do seu Carnaval, sem alterar nada do que já foi produzido.</p>
        <ul class="cn-pontos">
          <li><b>Troca de testeiras</b>As testeiras dos grupos de displays e os apliques do portal são peças separadas da estrutura. Cada praça pode receber a sua arte.</li>
          <li><b>Elementos cenográficos</b>O interior da ilha e a base dos displays recebem adereços próprios de cada festa, no lugar ou ao lado dos fitilhos.</li>
          <li><b>A mesma base</b>Portal, displays e adesivo de chão continuam iguais em todas as lojas: uma só produção, com ganho de escala.</li>
        </ul>
      </div>
    </div>
    <p class="v2-leg anima d2">A estrutura entra em produção de imediato. As artes e os adereços de cada praça correm em paralelo e viajam como kit leve: personalizar é trocar chapas, sem mexer em nada estrutural.</p>
  </div></section>''')
# ---------------------------------------------------------------- 05 · na rua e no time
T.append(cap('05', 'Na rua e no time', 'A campanha veste quem atende e quem circula: o brilho chega à loja antes do shopper entrar.', ['Uniformes', 'Ativação ambulante']))
T.append('''<section id="uniformes" class="tela v2-split n" data-tema="claro" data-titulo="Uniformes" data-cap="(05) Na rua e no time">
  <div class="caixa"><h2 class="anima">Dois modelos, <span class="onda t-teal">a mesma fantasia.</span></h2>
    <div class="v2-trio anima d1">
      <div>%s<p><b>Abadá</b> · Demonstradoras · camiseta em lantejoula e confete</p></div>
      <div>%s<p><b>Abadá</b> · Demonstradoras · versão regata</p></div>
      <div>%s<p><b>Camiseta</b> · Promotores · saia de fitilhos opcional</p></div>
    </div>
    <p class="v2-leg anima d2">Conceitos de figurino. O abadá das demonstradoras leva o acabamento mais elaborado; a camiseta dos promotores mantém a identidade com custo de grande tiragem.</p></div></section>''' % (fig('abada-1', 'Abadá das demonstradoras'), fig('abada-2', 'Abadá, versão regata'), fig('camiseta', 'Camiseta dos promotores')))
T.append('''<section id="ativacao" class="tela v2-split n" data-tema="escuro" data-titulo="Ativação ambulante" data-cap="(05) Na rua e no time">
  <div class="caixa"><h2 class="anima">O motoboy vira <span class="t-lime">destaque de bloco.</span></h2>
    <div class="v2-trio anima d1" style="grid-template-columns:repeat(4,1fr)">
      <div>%s<p><b>Capacete</b> · com plumas</p></div>
      <div>%s<p><b>Bag</b> · com fitilhos</p></div>
      <div>%s<p><b>Colete + pirulito</b> · frente</p></div>
      <div>%s<p><b>Colete + pirulito</b> · costas</p></div>
    </div>
    <p class="v2-leg anima d2">Conceitos de caracterização. A equipe chega à loja como parte da festa: chama atenção no estacionamento e conduz o shopper até a exposição da marca.</p></div></section>''' % (fig('capacete', 'Capacete com plumas'), fig('bag', 'Bag com fitilhos'), fig('colete-frente', 'Colete com pirulito, frente'), fig('colete-verso', 'Colete com pirulito, costas')))
T.append('''<section id="fim" class="tela s-capa fim" data-tema="foto" data-titulo="Fechamento" data-cap="">
    <div class="faixa-lant sangra"></div><div class="foto sangra" role="img" aria-label="Testeira iluminada"></div><div class="veu sangra"></div>
    <div class="texto"><span class="eyebrow anima"><b>(Fechamento)</b> Carnaval 2027</span>
      <h1 class="anima d1">A ideia<br>precisa<br><span class="brilha">brilhar</span></h1>
      <p class="lead anima d2">O orçamento precisa fazer sentido · e a operação precisa acontecer</p>
      <div class="acoes anima d3"><button class="botao cheio" data-ir="capa" data-cursor="Voltar">Voltar ao início</button><button class="botao seta" data-ir="ilha" data-cursor="Ver">Rever a ilha</button></div></div>
    <div class="marquee sangra"><div>%s</div></div>
  </section>''' % MQ)
T.append(cap('06', 'Por que a 75 LAB', 'Quem somos e as provas de que a operação acontece.', ['Propósito e imprensa', 'Diferencial', 'Vantagens competitivas', 'Nossos números', 'Clientes', 'Cases de ponto de venda', 'Depoimentos em vídeo']))
INST = open(os.path.join(HERE, 'inst.html'), encoding='utf-8').read(); INST_ART = open(os.path.join(HERE, 'inst_art.html'), encoding='utf-8').read()
T += ['<section ' + x for x in INST.split('<section ')[1:]]
ORDEM = ['capa', 'cap-01', 'kv', 'linguagem', 'estrategia', 'cap-02', 'leves', 'cap-03', 'ponta', 'ponta-mov', 'display', 'cap-04', 'ilha', 'ilha-partes', 'regional', 'cap-05', 'uniformes', 'ativacao', 'fim', 'cap-06', 'proposito', 'diferencial', 'vantagens', 'numeros', 'clientes', 'cases-pdv', 'depoimento', 'contato']
ID = lambda t: re.search(r'<section id="([^"]+)"', t).group(1)
assert sorted(ID(t) for t in T) == sorted(ORDEM), [ID(t) for t in T]
T.sort(key=lambda t: ORDEM.index(ID(t)))
CHROME = '''  <header id="topo">
    <div class="marcas"><img class="alp" src="assets/marcas/logo-bombril.webp" alt="Bombril"><span class="x">×</span><img class="lab m-escuro" src="assets/75lab-lime.png" alt="75 LAB"><img class="lab m-claro" src="assets/75lab-black.png" alt="75 LAB"></div>
    <div class="dir"><span class="cap" id="capTxt"></span><button id="btnSumario" data-sumario data-cursor="Abrir"><span><i></i><i></i><i></i></span>Sumário</button></div>
  </header>
  <footer id="rodape"><span class="assin">75 LAB · Bombril · Carnaval 2027</span>
    <div class="nav"><button id="ant" aria-label="Tela anterior" data-cursor="Voltar">←</button><span id="cont">01 / %02d</span><button id="prox" aria-label="Próxima tela" data-cursor="Seguir">→</button></div></footer>
  <div id="prog"><i></i></div>
  <div id="wipe" class="wipeDuo"><img src="assets/75lab-black.png" alt="75 LAB"><i>×</i><img class="b" src="assets/marcas/logo-bombril.webp" alt="Bombril"></div>
  <nav id="sumario" aria-label="Sumário"><button class="botao mini fechar" data-cursor="Fechar">Fechar ✕</button><h2>Sumário · <span>Carnaval Bombril 2027</span></h2><ol id="sumLista"></ol></nav>
  <canvas id="confete" aria-hidden="true"></canvas>
  <div class="grao"></div>''' % len(T)
POS = '''<div id="caixa" role="dialog" aria-label="Imagem ampliada"><button class="fechar" data-cursor="Fechar">Fechar ✕</button><img id="cxImg" alt=""><p id="cxTxt"></p></div>
<div id="cursor"></div><div id="anel"><span id="anelTxt"></span></div>
<div id="gire"><img src="assets/75lab-lime.png" alt="75 LAB"><div class="tel"></div><h3>Gire o celular</h3><p>A apresentação foi desenhada na horizontal. Deitado, o celular mostra a tela inteira.</p><button class="botao mini" id="verAssim">Ver assim mesmo</button></div>'''
HEAD = '''<title>Carnaval Bombril 2027</title>
<meta name="description" content="Apresentação da 75 LAB para a concorrência de trade marketing do Carnaval Bombril 2027.">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;900&family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/deck.css"><link rel="stylesheet" href="assets/bombril.css"><link rel="stylesheet" href="assets/v2.css"><link rel="stylesheet" href="assets/carnaval.css">'''
def corpo(TT): return ICONES + '\n<div id="wrap"><div id="stage" class="t-lime capa">\n' + '\n'.join(TT) + '\n' + CHROME + '\n</div></div>\n' + POS + '\n<script src="assets/deck.js"></script>\n<script src="assets/carnaval.js"></script>\n'
BODY = ICONES + '\n<div id="wrap"><div id="stage" class="t-lime capa">\n' + '\n'.join(T) + '\n' + CHROME + '\n</div></div>\n' + POS + '\n<script src="assets/deck.js"></script>\n<script src="assets/carnaval.js"></script>\n'
full = '<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<link rel="icon" href="assets/75lab-lime.png">\n' + HEAD + '\n</head>\n<body>\n' + BODY + '</body>\n</html>\n'
for bad in ('Cadeirinha', 'Assaí', 'cadeirinha', 'Ypê', 'Frutas Tropicais'): assert bad not in full, bad
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(full)
TA = [t for t in T if ID(t) in ORDEM[:ORDEM.index('cap-06') + 1]] + ['<section ' + x for x in INST_ART.split('<section ')[1:]]
art = HEAD + '\n<style>html,body{height:100%;background:#1A0305}</style>\n' + corpo(TA)
open(os.path.join(ROOT, 'artifact.html'), 'w', encoding='utf-8').write(art)
print(len(T), 'telas', len(full))
