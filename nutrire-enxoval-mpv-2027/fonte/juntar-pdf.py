"""Junta os JPG gerados por fonte/gerar-pdf.js num PDF de páginas 1600 × 900.
Uso: python3 fonte/juntar-pdf.py <pasta-dos-jpg> <saída.pdf>"""
import sys, pathlib
from PIL import Image

pasta, saida = pathlib.Path(sys.argv[1]), sys.argv[2]
paginas = [Image.open(f).convert('RGB') for f in sorted(pasta.glob('*.jpg'))]
paginas[0].save(saida, save_all=True, append_images=paginas[1:], resolution=144)
print(saida, len(paginas), 'páginas')
