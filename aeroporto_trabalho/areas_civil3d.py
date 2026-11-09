"""Áreas de corte e aterro das seções extraídas do Civil 3D (TN_limpo x TERRAPLENAGEM) e comparação com o motor Python.
Saída: dados/areas_civil3d.json"""
import json
import numpy as np

D = np.genfromtxt('civil3d/secoes_civil3d.csv', delimiter=';', skip_header=1)
M = json.load(open('dados/memorial.json'))
res = {}
for e in np.unique(D[:, 0]):
    d = D[D[:, 0] == e]
    d = d[np.argsort(d[:, 1])]
    m = ~np.isnan(d[:, 3]) & ~np.isnan(d[:, 2])
    o, zl, zt = d[m, 1], d[m, 2], d[m, 3]
    diff = zl - zt
    ac = np.trapezoid(np.clip(diff, 0, None), o); aa = np.trapezoid(np.clip(-diff, 0, None), o)
    res[round(float(e), 3)] = dict(ac=float(ac), aa=float(aa), dl_esq=float(d[0, 4]), dl_dir=float(d[0, 5]))
L = M['linhas']
dif_c, dif_a = [], []
Vc = Va = 0.0
prev = None
for l in L:
    r = res.get(round(l['est_m'], 3))
    l['area_c_c3d'] = r['ac']; l['area_a_c3d'] = r['aa']
    dif_c.append(r['ac'] - l['area_c']); dif_a.append(r['aa'] - l['area_a'])
    if prev is not None:
        dd = l['est_m'] - prev['est_m']
        Vc += dd * (r['ac'] + prev['area_c_c3d']) / 2; Va += dd * (r['aa'] + prev['area_a_c3d']) / 2
    prev = l
t = M['totais']
print(f'áreas: dif. média corte {np.mean(np.abs(dif_c)):.2f} m² (máx {np.max(np.abs(dif_c)):.2f}); aterro {np.mean(np.abs(dif_a)):.2f} m² (máx {np.max(np.abs(dif_a)):.2f})')
print(f'volumes Civil 3D (áreas médias): Vc = {Vc:,.0f}  Va = {Va:,.0f}   | Python: Vc = {t["Vc"]:,.0f}  Va = {t["Va"]:,.0f}')
print(f'diferença: corte {100*(Vc/t["Vc"]-1):+.2f}%  aterro {100*(Va/t["Va"]-1):+.2f}%')
json.dump(dict(por_estaca={str(k): v for k, v in res.items()}, Vc=Vc, Va=Va), open('dados/areas_civil3d.json', 'w'), indent=1)
