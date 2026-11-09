"""Otimização do greide da PPD (cotas dos PIVs em estacas fixas) — saída: dados/greide.json

Objetivo: menor volume total (corte + aterro) com o greide compensado (corte = Fh x aterro, sem empréstimo).
Restrições do enunciado: |i| <= 1,5%; declividade efetiva (Δz/comprimento da PPD) <= 1,0%; |Δi| <= 1,5%.
Complemento (Anexo 14/RBAC 154, código 4): raio vertical >= 30 000 m (L = R·|Δi|) e distância entre PIVs
>= 30 000·(|Δi1| + |Δi2|), mínimo 45 m; rampa <= 0,8% no primeiro e no último quarto da PPD.
"""
import json
import sys
import numpy as np
from scipy.optimize import minimize
import projeto as p

N = int(sys.argv[1]) if len(sys.argv) > 1 else 7
E = np.linspace(0, p.COMP, N)
E = np.round(E / 20) * 20  # PIVs em estacas inteiras
EST = np.arange(0, p.COMP + 0.1, 20.0)
EG = {e: p.eg_secao(e) for e in EST}
Q1, Q3 = 60 + 1900 / 4, 1960 - 1900 / 4


def pvis_de(z, arred=False):
    g = np.diff(z) / np.diff(E)
    L = [0.0] + [p.R_VERT * abs(g[k] - g[k - 1]) for k in range(1, N - 1)] + [0.0]
    if arred:
        L = [0.0] + [max(40.0, np.ceil(l / 20) * 20) if l > 1e-6 else 0.0 for l in L[1:-1]] + [0.0]
    return [(E[k], z[k], L[k]) for k in range(N)]


def vols(z):
    pv = pvis_de(z)
    zg = p.greide(pv, EST)
    ac = np.empty(EST.size); aa = np.empty(EST.size)
    for k, e in enumerate(EST):
        s = p.secao(e, zg[k], EG[e]); ac[k] = s['area_corte']; aa[k] = s['area_aterro']
    Vc = np.sum(20 * (ac[1:] + ac[:-1]) / 2); Va = np.sum(20 * (aa[1:] + aa[:-1]) / 2)
    return Vc, Va


def obj(z):
    Vc, Va = vols(z)
    return (Vc + Va) / 1e5


def cons(z):
    g = np.diff(z) / np.diff(E)
    dg = np.diff(g)
    c = []
    c += list(0.015 - np.abs(g))
    c += list(0.015 - np.abs(dg))
    zr = p.greide(pvis_de(z), np.arange(60, 1960.1, 10))
    c.append(0.01 - (zr.max() - zr.min()) / 1900)
    for k in range(1, N - 2):   # distância entre PIVs
        c.append((E[k + 1] - E[k]) - max(45.0, p.R_VERT * (abs(dg[k - 1]) + abs(dg[k]))))
    # quartos extremos da PPD: 0,8%
    for k in range(N - 1):
        if E[k] < Q1 or E[k + 1] > Q3:
            c.append(0.008 - abs(g[k]))
    Vc, Va = vols(z)
    c.append((Vc - p.FH * Va) / 1e4)          # sem empréstimo
    c.append((0.01 * Vc - (Vc - p.FH * Va)) / 1e4)  # sobra de corte <= 1%
    return np.array(c)


z0 = np.full(N, 557.5)
best = None
for z_ini in (z0, np.interp(E, EST, [np.median(EG[e][np.abs(p.OFF) <= 150]) for e in EST])):
    r = minimize(obj, z_ini, method='SLSQP', constraints=[{'type': 'ineq', 'fun': cons}],
                 options=dict(maxiter=300, ftol=1e-6, eps=1e-3))
    print(r.message, r.fun, np.round(r.x, 3))
    if best is None or (r.fun < best.fun and np.all(cons(r.x) > -1e-4)):
        best = r
z = best.x
pv = pvis_de(z, arred=True)
g = np.diff(z) / np.diff(E)
Vc, Va = vols(z)
print('PIVs:', [(round(a), round(b, 3), c) for a, b, c in pv])
print('rampas %:', np.round(g * 100, 3), 'Δi %:', np.round(np.diff(g) * 100, 3))
print(f'Vc = {Vc:,.0f}  Va = {Va:,.0f}  Fh*Va = {p.FH*Va:,.0f}  total = {Vc+Va:,.0f}')
print('restrições (mín.):', cons(z).min())
json.dump(dict(pvis=[[float(a), float(b), float(c)] for a, b, c in pv], Vc=Vc, Va=Va, N=N), open('dados/greide.json', 'w'), indent=1)
