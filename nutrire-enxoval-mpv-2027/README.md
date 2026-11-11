# Nutrire × 75 LAB · Enxoval MPV 2027

Apresentação estratégica da 75 LAB para a Nutrire (Unicharm): enxoval completo de ponto de venda para 2027, com a Birbo como primeira vitrine. Pitch para Ricardo Maciel, sem apresentação presencial (o deck precisa parar de pé sozinho).

Link público: https://projetos.75lab.com.br/nutrire-enxoval-mpv-2027/

- `index.html`: a apresentação (palco fixo 1600 × 900 escalado, 33 telas). Setas, espaço, roda do mouse ou deslizar navegam; o botão Sumário abre o índice; toda imagem com lupa amplia.
- `nutrire-enxoval-mpv-2027.pdf`: o deck em PDF (36 páginas: o KV ganha uma página por família).
- `assets/`: motor do deck (`deck.css`, `deck.js`, `telas.css`, iguais aos decks Ypê, Bombril e institucional), `nutrire.css` com as telas deste projeto, embalagens Nutrire e Birbo (`assets/nutrire/`) e ativos da 75 LAB.
- `fonte/`: `telas-nutrire.html` e `fim-nutrire.html` (conteúdo), `montar.py` (monta o `index.html`), `gerar-pdf.js` e `juntar-pdf.py` (PDF).

## Roteiro: 33 telas, 5 capítulos

| Capítulo | Telas |
|---|---|
| 01 · O desafio | Capa · portfólio Nutrire (Birbo, Monello, Select by Monello, Monello Bites, Bolt, Bandit, Bancat, Unicharm) · Birbo, a vitrine (9 receitas, 9 cores) · seis pontos e seis respostas |
| 02 · Enxoval completo | Plataforma criativa · KV por família (Birbo cães, Birbo gatos, Monello e Select, Bites e volume: espaços reservados para a criação) · 15 peças em três papéis · peças por canal (pet shop, redes, agropet, super e atacarejo, digital) · AR e QR Code · calendário com 4 ondas |
| 03 · Formas de contratar | Os três modelos · A: engenharia de enxoval · A: exemplo de revisão · B: agência de trade por fee (Ariuno) · C: tecnologia de gestão do PDV · C: 75 LAB e Involves · o ciclo completo |
| 04 · Metas e cronograma | Metas propostas para 2027 · cronograma de 13/11/2026 à onda 1 em março/2027 |
| 05 · Por que a 75 LAB | Propósito e imprensa · diferencial · vantagens · números · clientes · cases · depoimentos em vídeo · próximos passos · contatos |

## Montar e gerar o PDF

```bash
python3 fonte/montar.py <caminho do index.html do deck bombril-comercial-75lab>
python3 -m http.server 8822
node fonte/gerar-pdf.js http://localhost:8822/ /tmp/paginas-pdf
python3 fonte/juntar-pdf.py /tmp/paginas-pdf nutrire-enxoval-mpv-2027.pdf
```

`montar.py` usa o deck da Bombril só como fonte dos ícones, da navegação e das telas institucionais da 75 LAB. Concorrentes diretos da Nutrire em pet food saem das telas reaproveitadas: Whiskas e Pedigree (Mars), PremieRpet, Kelcat, Keldog e Pipicat (Kelco), o case Kelco (trocado pelo case SEMP) e o vídeo do display Kelco. As telas de celular do AR e QR foram refeitas com conteúdo Birbo (as originais eram de um projeto Mars).

## Fontes

- Nutrire: nutrire.ind.br, portfólio, páginas da Birbo e embalagens (consulta em 10/11/2026)
- Unicharm / Business Wire, 15/05/2026 (compra de 100% da Nutrire; pet care de 17% para 20% das vendas até 2030)
- Mercado: estimativa de canais publicada pela Gironews, 2026 (48% em pequenos e médios pet shops)
- Involves: Involves Stage, informações públicas da empresa na imprensa (Mundo do Marketing, IT Forum, Central do Varejo)
- 75 LAB: 75lab.com.br e Ariuno (números de 28/10/2025 a 27/10/2026)

## Pendências

- **KV e peças:** em criação pelo time de criação da 75 LAB. A tela de KV tem espaços reservados por família; entram as artes finais quando chegarem.
- **Números propostos:** economia de 15% a 30%, pacotes de 80/160/320 h e metas de 2027 são propostas da 75 LAB, a validar; valores vão na proposta comercial.
- **Canal supermercado e atacarejo:** entra se a Nutrire confirmar o canal para 2027.
- **Conflito de conta:** a 75 LAB atende Nestlé Purina; alinhar com a diretoria antes do envio.
- **Telas de sistema:** painel, QR e Ariuno são telas em modo demonstração ou ilustrativas, identificadas como exemplo.
