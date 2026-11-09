"""Etapa 1, rodada 2: busca com obstáculos (OLS) como critério.
Orientações de 30° a 80° (eixo do vale do Paraíba, que também é o do vento predominante ENE).
Filtros: fora da várzea (>= 15 m acima do fundo de vale em raio de 3 km), uso do solo, distância de SBSJ/SBTA,
e baixa penetração nas OLS. Critério: índice de terraplenagem da faixa + penalidade de OLS."""
import json
import numpy as np
from scipy.ndimage import map_coordinates, minimum_filter
from dem import carrega_worldcover, geo2utm, utm2geo, DADOS
import ols

Z, X0, Y0, P = ols.Z, ols.X0, ols.Y0, ols.P
ZMIN = minimum_filter(Z, size=int(6000 / P) + 1, mode='nearest')
amostra = ols.amostra
AEROPORTOS = {'SBSJ': (-45.8711, -23.2292), 'SBTA': (-45.5158, -23.0389)}

ny, nx = Z.shape
cxs = np.arange(X0 + 2000, X0 + nx * P - 2000, 300.0)
cys = np.arange(Y0 + 2000, Y0 + ny * P - 2000, 300.0)
CX, CY = [a.ravel() for a in np.meshgrid(cxs, cys)]
ok = np.ones(CX.size, bool)
for lo, la in AEROPORTOS.values():
    ax, ay = geo2utm.transform(lo, la)
    ok &= np.hypot(CX - ax, CY - ay) > 10000
CX, CY = CX[ok], CY[ok]

s_f = np.arange(-1010, 1010.1, 60.0); t_f = np.arange(-150, 150.1, 60.0)
Sf, Tf = [a.ravel() for a in np.meshgrid(s_f, t_f)]
best = None
for az in range(30, 81, 10):
    ux, uy = np.sin(np.radians(az)), np.cos(np.radians(az)); vx, vy = uy, -ux
    zf = amostra((CX[:, None] + Sf * ux + Tf * vx).ravel(), (CY[:, None] + Sf * uy + Tf * vy).ravel()).reshape(CX.size, -1)
    sm = Sf - Sf.mean()
    b = np.clip((zf - zf.mean(1, keepdims=True)) @ sm / (sm @ sm), -0.01, 0.01)
    res = zf - b[:, None] * Sf
    res -= np.median(res, 1, keepdims=True)
    it = np.abs(res).mean(1)
    zm = zf.mean(1)
    hv = zm - map_coordinates(ZMIN, [(CY - Y0) / P, (CX - X0) / P], order=1)
    lin = np.column_stack([it, np.full(CX.size, az), b, zm, hv])
    if best is None:
        best = lin
    else:
        troca = lin[:, 0] < best[:, 0]
        best[troca] = lin[troca]

m = (best[:, 4] >= 15) & (best[:, 0] < 3.0)
print('centros fora da várzea com terra < 3 m:', m.sum())
idx = np.where(m)[0]
LON_MIN, LON_MAX, LAT_MIN, LAT_MAX = -46.05, -45.30, -23.45, -22.80
wc = carrega_worldcover(LON_MIN, LON_MAX, LAT_MIN, LAT_MAX)
s_w = np.arange(-1500, 1500.1, 75.0); t_w = np.arange(-750, 750.1, 75.0)
Sw, Tw = [a.ravel() for a in np.meshgrid(s_w, t_w)]
cands = []
for k in idx:
    it, az, b, zm, hv = best[k]
    x, y = CX[k], CY[k]
    ux, uy = np.sin(np.radians(az)), np.cos(np.radians(az)); vx, vy = uy, -ux
    lo, la = utm2geo.transform(x + Sw * ux + Tw * vx, y + Sw * uy + Tw * vy)
    cls = wc.nearest(lo, la)
    f = {c: float((cls == c).mean()) for c in (10, 30, 40, 50, 80, 90)}
    if f[50] > 0.03 or f[80] + f[90] > 0.03 or f[10] > 0.25:
        continue
    r = ols.verifica(x, y, az, passo=150.0)
    lon_c, lat_c = utm2geo.transform(x, y)
    cands.append(dict(x=float(x), y=float(y), lon=float(lon_c), lat=float(lat_c), az=float(az), i_long=float(b), z_medio=float(zm),
                      altura_vale=float(hv), idx_terra=float(it), ols_pen=r['pen_max'], ols_area_ha=r['area_pen_ha'],
                      arvores=f[10], urbano=f[50], agua=f[80] + f[90], pasto=f[30], cultivo=f[40]))
print('após uso do solo:', len(cands))
for c in cands:
    c['score'] = c['idx_terra'] + 0.05 * c['ols_area_ha'] + 0.02 * max(c['ols_pen'], 0)
esc = []
for c in sorted(cands, key=lambda c: c['score']):
    if all(np.hypot(c['x'] - e['x'], c['y'] - e['y']) > 2500 for e in esc):
        esc.append(c)
    if len(esc) == 12:
        break
for k, c in enumerate(esc):
    print(f"{k:2d} ({c['lat']:.4f}, {c['lon']:.4f}) az {c['az']:.0f} i {c['i_long']*100:+.2f}% z {c['z_medio']:.0f} hv {c['altura_vale']:.0f} "
          f"terra {c['idx_terra']:.2f} OLS {c['ols_pen']:.0f} m/{c['ols_area_ha']:.0f} ha arv {c['arvores']:.0%} urb {c['urbano']:.0%} pasto {c['pasto']:.0%} cult {c['cultivo']:.0%}")
json.dump(esc, open(f'{DADOS}/candidatos2.json', 'w'), indent=1)
