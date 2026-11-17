"""Áreas de corte/aterro entre TN_limpo e a superfície Datum do corredor (seções do SL - PPD exportadas por
civil3d_corredor_secoes.ps1) e volumes pelas áreas médias; compara com dados/areas_civil3d.json (memorial).
Saída: dados/corredor_volumes.json"""
import csv
import json
from collections import defaultdict
import numpy as np
from projeto import FH

S = defaultdict(lambda: defaultdict(list))
for r in csv.DictReader(open('civil3d/secoes_corredor.csv', encoding='utf-8')):
    S[float(r['estaca'])][r['fonte']].append([float(r[k]) for k in ('x1', 'z1', 'x2', 'z2')])


def polilinha(links):
    x = np.array([v for l in links for v in (l[0], l[2])]); z = np.array([v for l in links for v in (l[1], l[3])])
    o = np.argsort(x, kind='stable'); return x[o], z[o]


res = {}
for est in sorted(S):
    xt, zt = polilinha(S[est]['TN_limpo']); xd, zd = polilinha(S[est]['Datum'])
    x = np.linspace(xd.min(), xd.max(), int((xd.max() - xd.min()) / 0.02) + 1)
    dz = np.interp(x, xt, zt) - np.interp(x, xd, zd)
    # Fora da faixa (|x| > 150 m) a seção da Datum segue nos taludes das estacas vizinhas (TIN entre seções com
    # pés de talude diferentes) e depois liga até a ponta da linha: corta cada lado no 1º cruzamento com o TN_limpo.
    manter = np.abs(x) <= 150.0
    for lado in (1, -1):
        idx = np.where(lado * x > 150.0)[0]
        idx = idx if lado == 1 else idx[::-1]
        if len(idx):
            s0 = np.sign(dz[idx[0]])
            for k in idx:
                if np.sign(dz[k]) != s0:
                    break
                manter[k] = True
    dz = np.where(manter, dz, 0.0)
    res[est] = dict(ac=float(np.trapezoid(np.clip(dz, 0, None), x)), aa=float(np.trapezoid(np.clip(-dz, 0, None), x)),
                    dl_esq=float(xd.min()), dl_dir=float(xd.max()))

est = sorted(res); Vc = Va = 0.0
for a, b in zip(est, est[1:]):
    d = b - a; Vc += (res[a]['ac'] + res[b]['ac']) / 2 * d; Va += (res[a]['aa'] + res[b]['aa']) / 2 * d

M = json.load(open('dados/areas_civil3d.json'))
Vc0, Va0 = M['Vc'], M['Va']
print(f'seções: {len(est)}  ({est[0]:.0f} a {est[-1]:.0f} m)')
print(f'Corredor:  Vc = {Vc:12,.0f}  Va = {Va:12,.0f}  Fh*Va = {FH*Va:12,.0f}  saldo = {Vc-FH*Va:+10,.0f}')
print(f'Memorial:  Vc = {Vc0:12,.0f}  Va = {Va0:12,.0f}  Fh*Va = {FH*Va0:12,.0f}  saldo = {Vc0-FH*Va0:+10,.0f}')
print(f'Diferença: Vc {100*(Vc/Vc0-1):+.2f}%   Va {100*(Va/Va0-1):+.2f}%')
dif = sorted(((abs(res[e]['ac'] - M['por_estaca'][str(e)]['ac']) + abs(res[e]['aa'] - M['por_estaca'][str(e)]['aa']), e)
              for e in est if str(e) in M['por_estaca']), reverse=True)[:5]
for d, e in dif:
    m = M['por_estaca'][str(e)]
    print(f'  est {e:7.1f}: corredor ac {res[e]["ac"]:7.2f} aa {res[e]["aa"]:7.2f} | memorial ac {m["ac"]:7.2f} aa {m["aa"]:7.2f}')
e = 1040.0
if e in res:
    print(f'par à mão 52: corredor ac {res[e]["ac"]:.2f} aa {res[e]["aa"]:.2f}')
json.dump(dict(por_estaca={str(k): v for k, v in res.items()}, Vc=Vc, Va=Va, Fh=FH), open('dados/corredor_volumes.json', 'w'), indent=1)
