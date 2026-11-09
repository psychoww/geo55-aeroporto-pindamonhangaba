"""Etapa 1, rodada 4 (global): todos os centros (300 m) x rumos de 0 a 175° (5°).
Critérios: terraplenagem da faixa, OLS (Anexo 14), ruído (urbano nos cones de aproximação de 3 km e na faixa
lateral de 500 m), risco aviário (água a menos de 3 km), mata no sítio, distância de SBSJ/SBTA, fora da várzea."""
import json
import numpy as np
from scipy.ndimage import map_coordinates, minimum_filter
from dem import carrega_worldcover, geo2utm, utm2geo, DADOS
import ols

Z, X0, Y0, P = ols.Z, ols.X0, ols.Y0, ols.P
ZMIN = minimum_filter(Z, size=int(6000 / P) + 1, mode='nearest')
ny, nx = Z.shape
cxs = np.arange(X0 + 4000, X0 + nx * P - 4000, 300.0)
cys = np.arange(Y0 + 4000, Y0 + ny * P - 4000, 300.0)
CX, CY = [a.ravel() for a in np.meshgrid(cxs, cys)]
ok = np.ones(CX.size, bool)
for lo, la in [(-45.8711, -23.2292), (-45.5158, -23.0389)]:
    ax, ay = geo2utm.transform(lo, la)
    ok &= np.hypot(CX - ax, CY - ay) > 10000
hv = map_coordinates(Z, [(CY - Y0) / P, (CX - X0) / P], order=1) - map_coordinates(ZMIN, [(CY - Y0) / P, (CX - X0) / P], order=1)
ok &= hv >= 12
CX, CY, HV = CX[ok], CY[ok], hv[ok]
print('centros:', CX.size)

s_f = np.arange(-1010, 1010.1, 60.0); t_f = np.arange(-150, 150.1, 50.0)
Sf, Tf = [a.ravel() for a in np.meshgrid(s_f, t_f)]
sm = Sf - Sf.mean()
combos = []
for az in range(0, 180, 5):
    ux, uy = np.sin(np.radians(az)), np.cos(np.radians(az)); vx, vy = uy, -ux
    zf = ols.amostra((CX[:, None] + Sf * ux + Tf * vx).ravel(), (CY[:, None] + Sf * uy + Tf * vy).ravel()).reshape(CX.size, -1)
    b = np.clip((zf - zf.mean(1, keepdims=True)) @ sm / (sm @ sm), -0.01, 0.01)
    r = zf - b[:, None] * Sf; r -= np.median(r, 1, keepdims=True)
    it = np.abs(r).mean(1)
    for k in np.where(it < 4.0)[0]:
        combos.append((CX[k], CY[k], az, it[k], b[k], zf[k].mean(), HV[k]))
print('combinações com terra < 4 m:', len(combos))

wc = carrega_worldcover(-46.05, -45.25, -23.50, -22.75)


def grade(L, W, passo):
    s = np.arange(-L / 2, L / 2 + 0.1, passo); t = np.arange(-W / 2, W / 2 + 0.1, passo)
    S, T = np.meshgrid(s, t); return S.ravel(), T.ravel()


Ss, Ts = grade(3000, 1500, 75)
Sa, Ta = grade(6000 + 2020, 600, 75); ma = np.abs(Sa) > 1010            # cones de aproximação (3 km além da faixa)
Sl, Tl = grade(2020, 1300, 75); ml = np.abs(Tl) > 150                     # 500 m de cada lado da faixa
Sb, Tb = grade(6000, 6000, 150)                                           # entorno de 3 km (água)


def cls(x, y, az, S, T):
    ux, uy = np.sin(np.radians(az)), np.cos(np.radians(az)); vx, vy = uy, -ux
    lo, la = utm2geo.transform(x + S * ux + T * vx, y + S * uy + T * vy)
    return wc.nearest(lo, la)


res = []
for x, y, az, it, b, zm, h in combos:
    cs = cls(x, y, az, Ss, Ts)
    urb_s, agua_s, arv_s = (cs == 50).mean(), np.isin(cs, (80, 90)).mean(), (cs == 10).mean()
    if urb_s > 0.03 or agua_s > 0.02 or arv_s > 0.25:
        continue
    ca = cls(x, y, az, Sa[ma], Ta[ma]); cl = cls(x, y, az, Sl[ml], Tl[ml])
    urb_ruido = (np.sum(ca == 50) + np.sum(cl == 50)) / (ca.size + cl.size)
    if urb_ruido > 0.10:
        continue
    o = ols.verifica(x, y, az, passo=150.0)
    if o['area_pen_ha'] > 300:
        continue
    cb = cls(x, y, az, Sb, Tb)
    agua_3km = np.isin(cb, (80,)).mean()
    lon, lat = utm2geo.transform(x, y)
    res.append(dict(x=float(x), y=float(y), lon=float(lon), lat=float(lat), az=az, idx_terra=float(it), i_long=float(b),
                    z_medio=float(zm), altura_vale=float(h), ols_pen=o['pen_max'], ols_area_ha=o['area_pen_ha'],
                    urb_ruido=float(urb_ruido), agua_3km=float(agua_3km), arvores=float(arv_s), urbano=float(urb_s)))
print('aprovadas:', len(res))
for r in res:
    r['score'] = r['idx_terra'] + 0.02 * r['ols_area_ha'] + 0.01 * max(r['ols_pen'], 0) + 20 * r['urb_ruido'] + 30 * r['agua_3km'] + 3 * r['arvores']
res.sort(key=lambda r: r['score'])
esc = []
for c in res:
    if all(np.hypot(c['x'] - e['x'], c['y'] - e['y']) > 2500 for e in esc):
        esc.append(c)
    if len(esc) == 12:
        break
for k, r in enumerate(esc):
    print(f"{k:2d} ({r['lat']:.4f}, {r['lon']:.4f}) az {r['az']} terra {r['idx_terra']:.2f} i {r['i_long']*100:+.2f}% z {r['z_medio']:.0f} hv {r['altura_vale']:.0f} "
          f"OLS {r['ols_pen']:.0f} m/{r['ols_area_ha']:.0f} ha ruido {r['urb_ruido']:.1%} agua3km {r['agua_3km']:.1%} arv {r['arvores']:.0%} score {r['score']:.2f}")
json.dump(esc, open(f'{DADOS}/candidatos_global.json', 'w'), indent=1)
