# Bacio di Latte · MPVD 2027 · Bacio di Latte × 75LAB

Apresentação HTML da proposta 75LAB para o **MPVD 2027 da Bacio di Latte**: *a mesma gelateria em 12 mil lugares*. Um sistema de PDV que leva o padrão da gelateria a cada freezer, carrinho e ponto de venda, e prova isso com dados.

## Conteúdo: 31 telas em 6 blocos

1. **Abertura:** capa e agenda.
2. **Contexto:** a Bacio em números, o mercado de sorvetes, a saída da Häagen-Dazs (ago/2026) e a concorrência.
3. **Diagnóstico:** a tensão escala × padrão, o insight central (a Bacio é julgada pelo freezer que não controla), seis insights com evidência e a jornada do shopper.
4. **Estratégia:** a oportunidade, De → Para → Através de, cinco pilares (Reconhecer, Escolher, Garantir, Conectar, Aprender) e o território “A Vitrine Vai Até Você”.
5. **Solução:** KV aprovado, as 21 peças aprovadas do enxoval (freezer vertical VF50, freezers horizontais e ilha, corredor e gôndola, praia), clusters A/B/C, planograma por sabor, ambulante, QR Code, rastreamento, guia online e painel.
6. **Execução:** KPIs, pré-mortem de riscos, roadmap com gate de piloto, próximos passos e fontes.

Os slides com dados trazem a fonte no rodapé; o último slide lista os links. As notas do apresentador ficam no HTML, ocultas (`aside.notes`).

## Navegação

Cada tela é um palco 16:9 de 1920 × 1080 que escala para caber na janela. Avança com → ↓ PageDown espaço, volta com ← ↑ PageUp, Home/End vão ao início e ao fim; também pelos botões no canto inferior direito ou deslizando o dedo. Deep link: `#s5`. Imprimir (Ctrl+P) gera uma tela por página.

## Estrutura

```
index.html          apresentação (gerado)
src/deck.json       ordem e títulos das telas
src/slides/*.html   uma tela por arquivo
src/shell.html      CSS e navegação
src/build.py        gera index.html
imagens/            KV, renders aprovados das peças (P01–P19, PDV-1–PDV-5), selo −18 °C e embalagens
```

## Rebuild

```bash
python3 src/build.py src index.html
```

## Pendências de conteúdo

- Imagens das 21 peças aprovadas em 12/nov/2026; Lote 5 (wobbler de lançamento e versão condomínio) suspenso pelo cliente.
- Medidas de campo (VF50, NF40, carrinho e stopper), 3D em escala real, executivo e artes finais.
- Logo 75LAB.
- Conferir links e preços de varejo antes de enviar ao cliente.
