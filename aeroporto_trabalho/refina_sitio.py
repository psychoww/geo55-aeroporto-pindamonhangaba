"""Etapa 1, rodada 3: refinamento local em torno do melhor candidato (entre Taubaté e Pindamonhangaba)."""
import json, sys
import numpy as np
import ols
from dem import carrega_worldcover, utm2geo, DADOS

c0 = json.load(open(f'{DADOS}/candidatos2.json'))[0]
wc = carrega_worldcover(-45.65, -45.35, -23.05, -22.80)
s_f = np.arange(-1010, 1010.1, 30.0); t_f = np.arange(-150, 150.1, 30.0)
Sf, Tf = [a.ravel() for a in np.meshgrid(s_f, t_f)]
s_w = np.arange(-1500, 1500.1, 50.0); t_w = np.arange(-750, 750.1, 50.0)
Sw, Tw = [a.ravel() for a in np.meshgrid(s_w, t_w)]
out = []
for dx in np.arange(-3000, 3001, 150):
    for dy in np.arange(-3000, 3001, 150):
        x, y = c0['x'] + dx, c0['y'] + dy
        for az in range(30, 91, 5):
            ux, uy = np.sin(np.radians(az)), np.cos(np.radians(az)); vx, vy = uy, -ux
            zf = ols.amostra(x + Sf * ux + Tf * vx, y + Sf * uy + Tf * vy)
            sm = Sf - Sf.mean()
            b = np.clip((zf - zf.mean()) @ sm / (sm @ sm), -0.01, 0.01)
            r = zf - b * Sf; r -= np.median(r)
            it = np.abs(r).mean()
            if it > 3.5:
                continue
            out.append((x, y, az, it, b, zf.mean()))
print('combinações:', len(out))
out.sort(key=lambda o: o[3])
res = []
for x, y, az, it, b, zm in out:
    ux, uy = np.sin(np.radians(az)), np.cos(np.radians(az)); vx, vy = uy, -ux
    lo, la = utm2geo.transform(x + Sw * ux + Tw * vx, y + Sw * uy + Tw * vy)
    cls = wc.nearest(lo, la)
    urb, agua, arv = (cls == 50).mean(), ((cls == 80) | (cls == 90)).mean(), (cls == 10).mean()
    # faixa de pista (2020 x 300) sem urbano/água
    lo2, la2 = utm2geo.transform(x + Sf * ux + Tf * vx, y + Sf * uy + Tf * vy)
    cf = wc.nearest(lo2, la2)
    if urb > 0.02 or agua > 0.02 or ((cf == 50) | (cf == 80) | (cf == 90)).mean() > 0.0:
        continue
    o = ols.verifica(x, y, az, passo=150.0)
    lon, lat = utm2geo.transform(x, y)
    res.append(dict(x=float(x), y=float(y), lon=float(lon), lat=float(lat), az=az, idx_terra=float(it), i_long=float(b), z_medio=float(zm),
                    ols_pen=o['pen_max'], ols_area_ha=o['area_pen_ha'], ze=o['ze'], urbano=float(urb), agua=float(agua), arvores=float(arv)))
for r in res:
    r['score'] = r['idx_terra'] + 0.05 * r['ols_area_ha'] + 0.02 * max(r['ols_pen'], 0)
res.sort(key=lambda r: r['score'])
for r in res[:15]:
    print(f"({r['lat']:.4f}, {r['lon']:.4f}) az {r['az']} terra {r['idx_terra']:.2f} i {r['i_long']*100:+.2f}% OLS {r['ols_pen']:.1f} m/{r['ols_area_ha']:.1f} ha urb {r['urbano']:.1%} agua {r['agua']:.1%} arv {r['arvores']:.0%} score {r['score']:.2f}")
json.dump(res[:30], open(f'{DADOS}/refino.json', 'w'), indent=1)
