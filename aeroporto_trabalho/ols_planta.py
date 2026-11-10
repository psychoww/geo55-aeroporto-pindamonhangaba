"""Mapa em planta das penetrações nas superfícies limitadoras de obstáculos (Anexo 14, código 4, precisão CAT I) para o
sítio de projeto.py: relevo em cinza, contornos das superfícies e, em cor, quanto o terreno (DSM) passa acima delas.
Saída: figuras/16_ols_planta.png e o resumo por superfície no terminal."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
import paleta
from paleta import IND, MARF, MUTED, ALERTA
import ols
import projeto as p

paleta.aplica()
passo = 60.0
s = np.arange(-16000, 16000.1, passo); t = np.arange(-7000, 7000.1, passo)
S, T = np.meshgrid(s, t)
X = p.XC + S * p.U[0] + T * p.V[0]; Y = p.YC + S * p.U[1] + T * p.V[1]
# terreno direto dos tiles Copernicus (S23 e S24 cobrem −22° a −24°): a grade da busca (dados/grade_utm30.npz) termina
# em −22,85° e não cobre as superfícies ao norte de C1
from dem import carrega_dem, utm2geo
_dem = carrega_dem()
_lo, _la = utm2geo.transform(X.ravel(), Y.ravel())
z = np.asarray(_dem.bilinear(_lo, _la), float).reshape(S.shape)
fora = ~np.isfinite(z) | (_la.reshape(S.shape) > -22.0005)
mf = (np.abs(S) <= 1010) & (np.abs(T) <= 150)
ze = z[mf].mean()
sup = ols.superficie(S, T, ze)
pen = np.where(~mf & ~fora & np.isfinite(sup), z - sup, np.nan)
ds = np.maximum(np.abs(S) - 1010, 0); at = np.abs(T)
apr = (ds > 0) & (at <= 150 + 0.15 * ds) & (ds <= 15000)
dist = np.hypot(ds, np.maximum(at - 150, 0))
grupos = {'aproximação': apr, 'horizontal interna (+45 m, 4 km)': (dist <= 4000) & ~apr & ~mf,
          'cônica (5%)': (dist > 4000) & (dist <= 6000) & ~apr}
for nome, m in grupos.items():
    pm = np.where(m, pen, np.nan)
    print(f'{nome:34s} máx {np.nanmax(pm):6.1f} m   área furada {np.nansum(pm > 0) * passo ** 2 / 1e4:6.0f} ha')

ls = LightSource(azdeg=315, altdeg=40)
fig, ax = plt.subplots(figsize=(13, 6.4))
ext = [s[0] / 1000, s[-1] / 1000, t[0] / 1000, t[-1] / 1000]
rgb = ls.shade(z, cmap=plt.cm.bone, vert_exag=3, blend_mode='soft', vmin=480, vmax=900); rgb[fora] = (1.0, 0.984, 0.96, 1.0)
ax.imshow(rgb, extent=ext, origin='lower')
im = ax.imshow(np.where(pen > 0, pen, np.nan), extent=ext, origin='lower', cmap=plt.cm.OrRd, vmin=0, vmax=max(50, np.nanmax(pen)), alpha=0.9)
ax.contour(S / 1000, T / 1000, dist, levels=[4000, 6000], colors=[IND], linewidths=1.2, linestyles=['-', '--'])
for sg in (1, -1):
    ss = np.array([1.010, 16.0]); ax.plot(sg * ss, 0.150 + 0.15 * (ss - 1.010), color=IND, lw=1); ax.plot(sg * ss, -0.150 - 0.15 * (ss - 1.010), color=IND, lw=1)
ax.add_patch(plt.Rectangle((-1.01, -0.15), 2.02, 0.30, color=ALERTA, lw=0))
cb = fig.colorbar(im, ax=ax, shrink=0.8, pad=0.01); cb.set_label('terreno acima da superfície (m)')
ax.set_xlabel('ao longo do rumo 060° (km; NE à direita)'); ax.set_ylabel('transversal (km; NW em cima)'); ax.invert_yaxis()
tot = np.nansum(pen > 0) * passo ** 2 / 1e4
ax.set_title(f'Superfícies limitadoras em planta: {tot:.0f} ha de terreno acima delas (máx. {np.nanmax(pen):.0f} m)', loc='left')
ax.text(ext[0] + 0.2, ext[3] - 0.3, 'linha cheia: horizontal interna (4 km); tracejada: limite da cônica; cunhas: aproximação', color=MARF, fontsize=9)
fig.savefig('figuras/16_ols_planta.png', bbox_inches='tight', facecolor=MARF); print('ok figuras/16_ols_planta.png')
