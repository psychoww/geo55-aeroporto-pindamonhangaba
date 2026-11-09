"""Mosaico dos candidatos: imagem de satélite + contorno do sítio (3000x1500) e da faixa (2020x300)."""
import json
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from imagem import imagem_utm
from dem import DADOS

c = json.load(open(f'{DADOS}/candidatos.json'))
ids = [int(a) for a in sys.argv[1:]] or list(range(6))
fig, axs = plt.subplots(2, (len(ids) + 1) // 2, figsize=(7 * ((len(ids) + 1) // 2), 13))
for ax, k in zip(axs.ravel(), ids):
    d = c[k]
    h = 2200
    img = imagem_utm(d['x'] - h, d['y'] - h, d['x'] + h, d['y'] + h, res=8.0, z=15)
    ax.imshow(img, extent=[-h, h, -h, h])
    u = np.array([np.sin(np.radians(d['az'])), np.cos(np.radians(d['az']))]); v = np.array([u[1], -u[0]])
    for L, W, cor in [(3000, 1500, 'yellow'), (2020, 300, 'red'), (1900, 45, 'white')]:
        cs = [(-L / 2, -W / 2), (L / 2, -W / 2), (L / 2, W / 2), (-L / 2, W / 2), (-L / 2, -W / 2)]
        P = np.array([s * u + t * v for s, t in cs])
        ax.plot(P[:, 0], P[:, 1], color=cor, lw=1.2)
    ax.set_title(f"#{k} ({d['lat']:.4f}, {d['lon']:.4f}) az {d['az']:.0f}° terra {d['idx_terra']:.2f} m relevo {d['rms_sitio']:.1f} m", fontsize=9)
    ax.set_xticks([]); ax.set_yticks([])
plt.tight_layout()
plt.savefig(f'{DADOS}/candidatos.png', dpi=80)
print('ok')
