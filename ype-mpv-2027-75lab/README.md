# Ypê × 75 LAB · MPV 2027

Apresentação estratégica da 75 LAB para a Ypê: como ajudar as marcas Ypê a performar melhor no ponto de venda em 2027. Reunião de 20/11/2026 com Andrea Salgueiro e Marcela Mariano.

Link público (depois de publicado no GitHub Pages): https://projetos.75lab.com.br/ype-mpv-2027-75lab/

- `index.html`: a apresentação (palco fixo 1600 × 900 escalado, 32 telas). Setas, espaço, roda do mouse ou deslizar navegam; o botão Sumário abre o índice; toda imagem com lupa amplia.
- `ype-mpv-2027-75lab.pdf`: o deck em PDF (35 páginas: o KV ganha uma página por família).
- `assets/`: motor do deck (`deck.css`, `deck.js`, `telas.css`, iguais aos decks Bombril e institucional), `ype.css` com as telas deste projeto, embalagens Ypê (`assets/ype/`) e ativos da 75 LAB.
- `fonte/`: `telas-ype.html` e `fim-ype.html` (conteúdo), `montar.py` (monta o `index.html`), `gerar-pdf.js` e `juntar-pdf.py` (PDF).

## Roteiro: 32 telas, 5 capítulos

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
