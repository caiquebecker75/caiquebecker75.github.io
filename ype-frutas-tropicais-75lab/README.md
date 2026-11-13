# Flor de Ypê Frutas Tropicais × 75 LAB · MPV 2027

Versão da apresentação estratégica da 75 LAB para a Ypê com ênfase no lançamento **Flor de Ypê Frutas Tropicais**: enxoval de 10 peças (5 robustas e 5 leves) modeladas em 3D na escala real, com giros 360°. As telas da agência (formas de contratar, metas, cronograma e 75 LAB) são as mesmas da versão geral (`../ype-mpv-2027-75lab`).

Link público: https://projetos.75lab.com.br/ype-frutas-tropicais-75lab/

- `index.html`: a apresentação (palco 1600 × 900). `assets/ft/`: renders, giros 360° (WebP animado), embalagens e KV da linha.
- `fonte/telas-ype.html`: telas (capa, linha, conceito, comunicação, 10 peças, canais, AR/QR, calendário + telas da agência). `fonte/montar.py` monta o `index.html` usando o deck `ype-mpv-2027-75lab` como referência das telas institucionais.

## Roteiro (versão geral, para referência)

| Capítulo | Telas |
|---|---|
| 01 · O desafio | Capa · portfólio Ypê (Ypê, Tixan Ypê, Assolan, Perfex, casa, cuidado pessoal) · seis pontos e seis respostas |
| 02 · Enxoval completo | Plataforma *Qualidade que se vê começa na gôndola* · KV por família (cozinha, lavanderia, casa, cuidado pessoal) · 15 peças em três papéis · peças por canal (atacarejo, hiper, super, vizinhança, digital) · AR e QR Code · calendário com 4 ondas |
| 03 · Formas de contratar | Os três modelos · A: engenharia reversa do enxoval · A: exemplo de revisão · B: agência de trade por fee (Ariuno) · C: tecnologia de gestão do PDV · C: 75 LAB e Involves · o ciclo completo |
| 04 · Metas e cronograma | Metas propostas para 2027 · cronograma de 20/11/2026 à onda 1 em março/2027 |
| 05 · Por que a 75 LAB | Propósito e imprensa · diferencial · vantagens · números · clientes · cases · depoimentos em vídeo · próximos passos · contatos |

## Montar e gerar o PDF

```bash
python3 fonte/montar.py <caminho do index.html do deck bombril-comercial-75lab>
python3 -m http.server 8822
node fonte/gerar-pdf.js http://localhost:8822/ /tmp/paginas-pdf
python3 fonte/juntar-pdf.py /tmp/paginas-pdf ype-mpv-2027-75lab.pdf
```

`montar.py` usa o deck da Bombril só como fonte dos ícones, da navegação e das telas institucionais da 75 LAB. Nenhuma tela, case ou número da Bombril entra no deck da Ypê (concorrente direta em lã de aço e limpeza). Os vídeos de depoimento vêm do deck institucional publicado (`projetos.75lab.com.br/institucional-75lab/assets/video/`).

## Fontes

- Ypê: ype.ind.br, portfólio, notícias e embalagens (consulta em 10/11/2026); Folha Top of Mind 2026 conforme divulgado pela Ypê
- Involves: Involves Stage, informações públicas da empresa na imprensa (Mundo do Marketing, IT Forum, Central do Varejo)
- 75 LAB: 75lab.com.br e Ariuno (números de 28/10/2025 a 27/10/2026)

## Pendências

- **KVs:** conceituais, para alinhar direção com o marketing da Ypê.
- **Números propostos:** economia de 15% a 30%, pacotes de 80/160/320 h e metas de 2027 são propostas da 75 LAB, a validar; valores vão na proposta comercial.
- **Involves:** comparativo com base em informações públicas; condições comerciais da Involves não foram consultadas.
- **Telas de sistema:** painel, QR e Ariuno são telas reais em modo demonstração ou de outros clientes, identificadas como exemplo.
