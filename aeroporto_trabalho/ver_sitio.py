"""Figura do sítio escolhido: imagem + sítio, faixa, PPD e contorno da horizontal interna (4 km)."""
import json, sys
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from imagem import imagem_utm
from dem import geo2utm
lat, lon, az = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
h = float(sys.argv[4]) if len(sys.argv) > 4 else 3500
out = sys.argv[5] if len(sys.argv) > 5 else 'dados/sitio.png'
x, y = geo2utm.transform(lon, lat)
img = imagem_utm(x - h, y - h, x + h, y + h, res=h / 900, z=16 if h < 3000 else 15)
fig, ax = plt.subplots(figsize=(11, 11))
ax.imshow(img, extent=[-h, h, -h, h])
u = np.array([np.sin(np.radians(az)), np.cos(np.radians(az))]); v = np.array([u[1], -u[0]])
for L, W, cor in [(3000, 1500, 'yellow'), (2020, 300, 'red'), (1900, 45, 'white')]:
    cs = [(-L/2, -W/2), (L/2, -W/2), (L/2, W/2), (-L/2, W/2), (-L/2, -W/2)]
    P = np.array([s*u + t*v for s, t in cs]); ax.plot(P[:, 0], P[:, 1], color=cor, lw=1.5)
th = np.linspace(0, 2*np.pi, 200)
ax.set_xlim(-h, h); ax.set_ylim(-h, h); ax.set_title(f'({lat}, {lon}) rumo {az}°')
plt.tight_layout(); plt.savefig(out, dpi=90); print(out)
