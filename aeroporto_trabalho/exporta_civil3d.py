"""Arquivos de entrada para o Civil 3D: pontos do terreno (PENZD), imagem georreferenciada (JPG + JGW) e projeto (JSON)."""
import json
import numpy as np
import projeto as p
from imagem import imagem_utm, salva_georref

P = p.pontos_terreno()
with open('civil3d/pontos_terreno_PENZD.csv', 'w') as f:
    for k, (x, y, z) in enumerate(P, 1):
        f.write(f'{k},{x:.3f},{y:.3f},{z:.3f},MDE\n')
print('pontos:', len(P))

# imagem: retângulo local s ±1800, t ±1000 -> caixa UTM
cs = np.array([np.array([p.XC, p.YC]) + a * p.U + b * p.V for a in (-1800, 1800) for b in (-1000, 1000)])
x0, y0 = np.floor(cs.min(0) / 10) * 10; x1, y1 = np.ceil(cs.max(0) / 10) * 10
res = 1.0
img = imagem_utm(x0, y0, x1, y1, res=res, z=17)
salva_georref(img, 'civil3d/imagem_sitio_utm23s.jpg', x0, y1, res)
print('imagem:', img.shape, 'caixa', x0, y0, x1, y1)

g = json.load(open('dados/greide.json'))
json.dump(dict(P0=p.P0.tolist(), PF=p.PF.tolist(), rumo=p.RUMO, comp=p.COMP, pvis=g['pvis'],
               centro=[p.XC, p.YC], img=dict(x0=x0, y0=y0, x1=x1, y1=y1, res=res, w=img.shape[1], h=img.shape[0])),
          open('civil3d/projeto.json', 'w'), indent=1)
