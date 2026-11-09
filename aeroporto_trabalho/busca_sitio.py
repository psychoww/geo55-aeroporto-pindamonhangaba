"""Etapa 1 — busca automática do sítio aeroportuário na região de São José dos Campos.

Para cada centro (grade de 300 m) e orientação da pista (0° a 170°, passo de 10°):
  - faixa de pista 2020 x 300 m: ajusta um greide reto com |i| <= 1,0% (declividade efetiva máxima)
    e mede o desvio médio |terreno - greide| -> índice de terraplenagem (m);
  - sítio 3000 x 1500 m (mesma orientação): RMS do terreno em relação a um plano -> relevo do sítio.
Depois filtra uso do solo (WorldCover): sem área urbana, água ou várzea relevante; pouca mata.
Saída: dados/candidatos.json
"""
import json
import numpy as np
from scipy.ndimage import map_coordinates
from dem import carrega_dem, carrega_worldcover, geo2utm, utm2geo, DADOS

LAT_MIN, LAT_MAX = -23.40, -22.85
LON_MIN, LON_MAX = -46.00, -45.35
AEROPORTOS = {'SBSJ São José dos Campos': (-45.8711, -23.2292), 'SBTA Taubaté': (-45.5158, -23.0389)}
DIST_MIN_AEROPORTO = 10000.0
PASSO = 30.0

dem = carrega_dem()
cx = [geo2utm.transform(lo, la) for lo, la in [(LON_MIN, LAT_MIN), (LON_MAX, LAT_MIN), (LON_MIN, LAT_MAX), (LON_MAX, LAT_MAX)]]
X0 = min(c[0] for c in cx); X1 = max(c[0] for c in cx)
Y0 = min(c[1] for c in cx); Y1 = max(c[1] for c in cx)
xs = np.arange(X0, X1, PASSO); ys = np.arange(Y0, Y1, PASSO)
XX, YY = np.meshgrid(xs, ys)
lon, lat = utm2geo.transform(XX, YY)
Z = dem.bilinear(lon, lat)  # grade UTM [iy, ix]
np.savez_compressed(f'{DADOS}/grade_utm30.npz', Z=Z, x0=X0, y0=Y0, passo=PASSO)
# fundo de vale local (mínimo num raio de ~3 km): exclui a planície aluvial do Paraíba (várzea inundável, solo mole)
from scipy.ndimage import minimum_filter
ZMIN = minimum_filter(Z, size=int(6000 / PASSO) + 1, mode='nearest')
ALTURA_MIN_SOBRE_VALE = 20.0


def amostra(px, py):
    return map_coordinates(Z, [(py - Y0) / PASSO, (px - X0) / PASSO], order=1, mode='nearest')


# centros candidatos (margem de 2 km da borda)
cxs = np.arange(X0 + 2000, X1 - 2000, 300.0)
cys = np.arange(Y0 + 2000, Y1 - 2000, 300.0)
CX, CY = [a.ravel() for a in np.meshgrid(cxs, cys)]
ok = np.ones(CX.size, bool)
for nome, (lo, la) in AEROPORTOS.items():
    ax, ay = geo2utm.transform(lo, la)
    ok &= np.hypot(CX - ax, CY - ay) > DIST_MIN_AEROPORTO
CX, CY = CX[ok], CY[ok]

# pontos locais (s ao longo da pista, t transversal)
s_f = np.arange(-1010, 1010.1, 60.0); t_f = np.arange(-150, 150.1, 60.0)
Sf, Tf = [a.ravel() for a in np.meshgrid(s_f, t_f)]
s_s = np.arange(-1500, 1500.1, 150.0); t_s = np.arange(-750, 750.1, 150.0)
Ss, Ts = [a.ravel() for a in np.meshgrid(s_s, t_s)]

resultados = []
for az in range(0, 180, 10):  # azimute da pista (graus a partir do norte)
    ux, uy = np.sin(np.radians(az)), np.cos(np.radians(az))
    vx, vy = uy, -ux
    # faixa
    PX = CX[:, None] + Sf[None] * ux + Tf[None] * vx
    PY = CY[:, None] + Sf[None] * uy + Tf[None] * vy
    zf = amostra(PX.ravel(), PY.ravel()).reshape(PX.shape)
    sm = Sf - Sf.mean()
    b = (zf - zf.mean(1, keepdims=True)) @ sm / (sm @ sm)
    b = np.clip(b, -0.01, 0.01)
    a = (zf - b[:, None] * Sf[None]).mean(1)
    res = zf - (a[:, None] + b[:, None] * Sf[None])
    # greide ótimo em L1 fica perto da mediana; usar desvio médio absoluto em torno da mediana do resíduo
    res = res - np.median(res, axis=1, keepdims=True)
    idx_terra = np.abs(res).mean(1)
    # sítio
    PX = CX[:, None] + Ss[None] * ux + Ts[None] * vx
    PY = CY[:, None] + Ss[None] * uy + Ts[None] * vy
    zs = amostra(PX.ravel(), PY.ravel()).reshape(PX.shape)
    A = np.column_stack([np.ones(Ss.size), Ss, Ts])
    coef, *_ = np.linalg.lstsq(A, zs.T, rcond=None)
    rms_sitio = np.sqrt(((zs - (A @ coef).T) ** 2).mean(1))
    for k in range(CX.size):
        resultados.append((idx_terra[k], rms_sitio[k], CX[k], CY[k], az, b[k], zf[k].mean()))

R = np.array(resultados)
print('avaliações:', len(R))
# melhor orientação por centro
ordem = np.lexsort((R[:, 0], R[:, 2] * 1e7 + R[:, 3]))
R = R[ordem]
_, primeiro = np.unique(R[:, 2] * 1e7 + R[:, 3], return_index=True)
R = R[primeiro]
score = R[:, 0] + 0.3 * R[:, 1]
R = R[np.argsort(score)][:20000]

# uso do solo nos 20000 melhores (só os que passam no filtro da várzea)
wc = carrega_worldcover(LON_MIN - 0.05, LON_MAX + 0.05, LAT_MIN - 0.05, LAT_MAX + 0.05)
s_w = np.arange(-1500, 1500.1, 50.0); t_w = np.arange(-750, 750.1, 50.0)
Sw, Tw = [a.ravel() for a in np.meshgrid(s_w, t_w)]
cands = []
for it, ir, x, y, az, b, zm in R:
    hv = zm - map_coordinates(ZMIN, [[(y - Y0) / PASSO], [(x - X0) / PASSO]], order=1)[0]
    if hv < ALTURA_MIN_SOBRE_VALE:
        continue
    ux, uy = np.sin(np.radians(az)), np.cos(np.radians(az)); vx, vy = uy, -ux
    lo, la = utm2geo.transform(x + Sw * ux + Tw * vx, y + Sw * uy + Tw * vy)
    cls = wc.nearest(lo, la)
    f = {c: float((cls == c).mean()) for c in (10, 20, 30, 40, 50, 60, 80, 90)}
    if f[50] > 0.03 or f[80] + f[90] > 0.03 or f[10] > 0.25:
        continue
    lon_c, lat_c = utm2geo.transform(x, y)
    cands.append(dict(x=x, y=y, lon=lon_c, lat=lat_c, az=az, i_long=b, z_medio=zm,
                      idx_terra=it, rms_sitio=ir, altura_vale=hv, score=it + 0.3 * ir,
                      arvores=f[10], urbano=f[50], agua=f[80] + f[90], pasto=f[30], cultivo=f[40]))

# remove sobrepostos (centros a menos de 2,5 km)
escolhidos = []
for c in sorted(cands, key=lambda c: c['score']):
    if all(np.hypot(c['x'] - e['x'], c['y'] - e['y']) > 2500 for e in escolhidos):
        escolhidos.append(c)
    if len(escolhidos) == 12:
        break
for k, c in enumerate(escolhidos):
    print(f"{k:2d} lat {c['lat']:.4f} lon {c['lon']:.4f} az {c['az']:3.0f} i {c['i_long']*100:+.2f}% z {c['z_medio']:.0f} "
          f"hv {c['altura_vale']:.0f} terra {c['idx_terra']:.2f} m relevo {c['rms_sitio']:.2f} m arv {c['arvores']:.0%} urb {c['urbano']:.0%} "
          f"agua {c['agua']:.0%} pasto {c['pasto']:.0%} cult {c['cultivo']:.0%}")
json.dump(escolhidos, open(f'{DADOS}/candidatos.json', 'w'), indent=1)
