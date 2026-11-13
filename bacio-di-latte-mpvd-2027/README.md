# Bacio di Latte · MPVD 2027 · Bacio di Latte × 75LAB

Apresentação HTML da proposta 75LAB para o **MPVD 2027 da Bacio di Latte**: *a mesma gelateria em 12 mil lugares*.

- **Link:** https://projetos.75lab.com.br/bacio-di-latte-mpvd-2027/

## Narrativa: 16 telas

| # | Capítulo | Takeaway |
| --- | --- | --- |
| 01 | Abertura | Trailer: 200+ gelaterias → 12 mil freezers → nenhum com balconista |
| 02 | Abertura | Agenda em trilha: sete capítulos até o piloto |
| 03 | Leitura do desafio | O pedido são seis entregas; o desafio é o padrão Bacio fora da loja |
| 04 | Contexto | A Bacio cresce como rede de varejo num mercado grande e pulverizado |
| 05 | Contexto | O premium ficou sem dono; ninguém une escala e gelateria no freezer |
| 06 | Shopper | A decisão acontece em segundos, com a porta aberta |
| 07 | Insight | A Bacio é julgada pelo freezer que não controla |
| 08 | Estratégia | Como podemos… De → Para → Através de + cinco pilares |
| 09 | Estratégia | Território: a vitrine vai até você |
| 10 | Solução | Revelação: o freezer vira vitrine (21 peças aprovadas) |
| 11 | Solução | Galeria das 21 peças, com ampliação e navegação |
| 12 | Solução | Planograma por sabor e kits por cluster |
| 13 | Solução | Ambulante e QR: a gelateria continua na areia e no celular |
| 14 | Rastreamento | Plano 75LAB One Shot e On Timing + fluxo display → decisão |
| 15 | Próximos passos | Cronograma com gate e o que o gate mede |
| 16 | Próximos passos | Encerramento e contatos |

## Arquitetura

HTML, CSS e JavaScript puros, sem build e sem dependências (só Google Fonts: Fraunces e DM Sans).

```
index.html            as 16 telas
assets/css/app.css    direção de arte, animações, celular, reduced-motion
assets/js/app.js      navegação, capítulos, contadores, lightbox, cursor
assets/img/75lab.png  logo 75LAB (aplicado por máscara, muda de cor com o fundo)
imagens/              KV, renders aprovados (P01–P19, PDV-1–PDV-5), selo e embalagens
```

- **Palco 16:9** de 1920 × 1080 que escala para a janela; no celular (≤ 900 px) vira rolagem vertical com revelação por seção.
- **Navegação:** setas, espaço, PageUp/PageDown, Home/End, roda do mouse, clique na metade direita (avança) ou esquerda (volta), botões, deslize no touch, menu de capítulos (botão ou tecla M), deep link `#s5`.
- **Movimento:** fundo vivo (blobs, grid, grão), cortina entre capítulos, títulos com revelação por palavra, números com contagem, traços SVG que se desenham, ícones com microanimação em loop.
- **Imagens:** todas ampliam em lightbox com anterior/próxima (setas), Esc ou clique fora fecha.
- **Cursor personalizado** só em mouse; vira “AMPLIAR” sobre imagens.
- Respeita `prefers-reduced-motion`.

## Pendências

- Logo oficial vetorial da Bacio di Latte (o cabeçalho usa o nome em tipografia).
- Dados institucionais da 75LAB: razão social, CNPJ, endereço e telefone.
- Medidas de campo das peças (VF50, NF40, carrinho, stopper) antes do executivo.
- Modelo do canal ambulante (próprio, revenda ou evento).
- Durações e datas do cronograma.
- Sem modelos 3D fornecidos: não há visualizador 3D nem AR.
- Telas do QR e do painel são simulações de interface.

## Fontes

- Exame (2025): plano da Bacio para 2025 · lançamento do Ciocchino Pistacchio
- MilkPoint e Portal Mais 360 (2026): Nova York e projeção de R$ 1,5 bi
- Money Times e SA+ Varejo: freezer em supermercado
- Mercado&Consumo (2025): loja de picolés · (set/2026) Magnum em farmácias
- ABIS, Retrospectiva 2025 · Abrasorvete via BHB Food
- Bloomberg Línea e Forbes Brasil (2026): saída da Häagen-Dazs
- Mundo do Marketing (2026): Magnum, IA e freezers como retail media
- Preços: Angeloni, Prado Supermercados, Zona Sul (nov/2026)
- KV e enxoval aprovados: 75LAB, 12/nov/2026
