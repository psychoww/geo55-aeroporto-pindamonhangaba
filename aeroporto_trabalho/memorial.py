"""Memorial de cálculo de volumes (áreas médias) + ordenadas de Brückner.
Saídas: dados/memorial.json, civil3d/estacas.json (para as linhas de amostragem), Tabelas/memorial_volumes.csv
"""
import csv
import json
import os
import numpy as np
import projeto as p

g = json.load(open('dados/greide.json'))
PVIS = [tuple(x) for x in g['pvis']]
pts = p.estacas_memorial(PVIS)
ests = [e for e, _ in pts]
r = p.volumes(PVIS, ests)

linhas = []
acum_c = acum_a = acum_l = ord_b = 0.0
for k, (e, nome) in enumerate(pts):
    s = r['secoes'][k]
    L = dict(ponto=nome, estaca=p.estaca_txt(e), est_m=e, cota_tn=s['eg_eixo'], cota_greide=float(r['zg'][k]),
             cota_terrapl=float(r['zg'][k] - p.H_PPD), h_eixo=float(r['zg'][k] - p.H_PPD - s['eg_eixo']),
             area_c=s['area_corte'], area_a=s['area_aterro'], larg_limpeza=s['largura_limpeza'],
             off_esq=s['off_esq'], off_dir=s['off_dir'])
    if k == 0:
        L.update(am_c=None, am_a=None, dist=None, vol_c=None, vol_a=None, vol_a_corr=None, vol_l=None)
    else:
        d = e - ests[k - 1]
        amc = (r['ac'][k] + r['ac'][k - 1]) / 2; ama = (r['aa'][k] + r['aa'][k - 1]) / 2
        vc, va = amc * d, ama * d
        vl = p.LIMPEZA * d * (r['secoes'][k]['largura_limpeza'] + r['secoes'][k - 1]['largura_limpeza']) / 2
        acum_c += vc; acum_a += va; acum_l += vl
        ord_b += vc - p.FH * va
        L.update(am_c=amc, am_a=ama, dist=d, vol_c=vc, vol_a=va, vol_a_corr=p.FH * va, vol_l=vl)
    L.update(acum_c=acum_c, acum_a=acum_a, acum_a_corr=p.FH * acum_a, acum_l=acum_l, ordenada=ord_b)
    linhas.append(L)

tot = dict(Vc=acum_c, Va=acum_a, Va_corr=p.FH * acum_a, Vl=acum_l, saldo=acum_c - p.FH * acum_a,
           n_secoes=len(linhas), max_off=max(max(l['off_esq'], l['off_dir']) for l in linhas))
json.dump(dict(pvis=PVIS, curvas=p.curvas(PVIS), linhas=linhas, totais=tot), open('dados/memorial.json', 'w'), indent=1)
json.dump(dict(estacas=[[l['est_m'], l['ponto'], l['estaca']] for l in linhas], largura=float(np.ceil(tot['max_off'] / 10) * 10 + 20)),
          open('civil3d/estacas.json', 'w'), indent=1)

os.makedirs('Tabelas', exist_ok=True)
cols = ['ponto', 'estaca', 'est_m', 'cota_tn', 'cota_greide', 'cota_terrapl', 'area_c', 'area_a', 'am_c', 'am_a', 'dist',
        'vol_c', 'vol_a', 'vol_a_corr', 'acum_c', 'acum_a_corr', 'ordenada', 'larg_limpeza', 'vol_l']
with open('Tabelas/memorial_volumes.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(cols)
    for l in linhas:
        w.writerow(['' if l[c] is None else (f'{l[c]:.3f}'.replace('.', ',') if isinstance(l[c], float) else l[c]) for c in cols])
print(f"seções: {len(linhas)}  Vc = {acum_c:,.0f}  Va = {acum_a:,.0f}  Fh·Va = {p.FH*acum_a:,.0f}  saldo = {acum_c - p.FH*acum_a:,.0f}  limpeza = {acum_l:,.0f} m³")
print('maior offset (m):', round(tot['max_off'], 1))
print('curvas:', [(c['n'], round(c['pcv'], 2), round(c['ptv'], 2), c['L'], round(c['g1'] * 100, 3), round(c['g2'] * 100, 3)) for c in p.curvas(PVIS)])
mista = [l for l in linhas[1:] if l['area_c'] > 50 and l['area_a'] > 50]
print('seções mistas (corte e aterro > 50 m²):', [(l['estaca'], round(l['area_c']), round(l['area_a'])) for l in mista[:12]])
