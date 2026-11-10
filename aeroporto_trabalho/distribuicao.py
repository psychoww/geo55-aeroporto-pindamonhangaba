"""Distribuição de massas da PPD: linhas de compensação (LC), bota-fora, empréstimo e momento de transporte.

1. Grava Tabelas/entrada_diagrama_massas.csv no formato do programa da aula de 20/10 (../diagrama_massas/),
   com as áreas das seções do Civil 3D. O mesmo arquivo abre na interface: diagrama_massas('...csv', 'Fh', 1.25, 'DMT', 150).
2. Roda distribuicao_massas.m (MATLAB, funções dm_*.m do programa) -> dados/distribuicao.json.
3. Figura figuras/11_distribuicao.png.

DMT de bota-fora e empréstimo = 150 m (aula 8). Variante: o empréstimo também custa a escavação. Com os preços do
exercício 6 da lista do B2 (escavação R$ 3,20/m³; transporte R$ 1,60/(m³·km)), escavar 1 m³ custa o mesmo que
transportá-lo 2 000 m; somando 150 m do bota-fora e 150 m do empréstimo, cada m³ que deixa de ser compensado custa
2 300 m de transporte, ou 1 150 m por parcela externa (bota-fora + empréstimo) -> DMT externa equivalente 1 150 m.
"""
import json
import os
import subprocess
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import projeto as p

DEXT, CUSTO_ESC, CUSTO_TR = 150.0, 3.20, 1.60
DEXT_ECO = (2 * DEXT + 1000 * CUSTO_ESC / CUSTO_TR) / 2

M = json.load(open('dados/memorial.json'))
C3 = json.load(open('dados/areas_civil3d.json'))['por_estaca']
os.makedirs('Tabelas', exist_ok=True)
with open('Tabelas/entrada_diagrama_massas.csv', 'w', encoding='utf-8') as f:
    f.write('Ponto;Distancia (m);Corte (m2);Aterro (m2)\n')
    for l in M['linhas']:
        c = C3[str(round(l['est_m'], 3))]
        f.write(f"{l['ponto']};{l['est_m']:.3f};{round(c['ac'], 2):.2f};{round(c['aa'], 2):.2f}\n".replace('.', ','))

MATLAB = r'C:\Program Files\MATLAB\R2026a\bin\matlab.exe'
cmd = (f"distribuicao_massas('Tabelas/entrada_diagrama_massas.csv', {p.FH}, {DEXT}, 'dados/distribuicao.json', {DEXT_ECO})")
if '--so-figura' not in sys.argv:          # --so-figura: reaproveita dados/distribuicao.json (sem MATLAB)
    r = subprocess.run([MATLAB, '-batch', cmd], capture_output=True, text=True, encoding='utf-8', errors='replace')
    print(r.stdout[-3000:], r.stderr[-2000:])
R = json.load(open('dados/distribuicao.json', encoding='utf-8'))

# ---------------------------------------------------------------- figura
import paleta
from paleta import CORTE, ATERRO, INK, MUTED, MARF, ALERTA as VERM
paleta.aplica()
x = np.array(R['x']); O = np.array(R['O'])


def lista(v):
    return v if isinstance(v, list) else ([] if v is None else [v])


def painel(ax, c, titulo):
    ax.plot(x, O / 1000, color=INK, lw=2, zorder=3)
    for w in lista(c['ondas']):
        m = (x >= w['ini']) & (x <= w['fim'])
        xs = np.concatenate([[w['ini']], x[m], [w['fim']]])
        ys = np.interp(xs, x, O)
        ax.fill_between(xs / 1, ys / 1000, w['lpk'] / 1000, color=CORTE if w['sinal'] > 0 else ATERRO, alpha=0.25, lw=0)
        if w['V'] < 10000:
            continue
        ax.annotate(f"V = {w['V'] / 1000:,.0f} mil m³\nDMT = {w['DMT']:,.0f} m".replace(',', '.'),
                    (w['xpk'], (w['ypk'] + w['lpk']) / 2000), ha='center', va='center', fontsize=9, color=INK)
    S = np.array(c['S'], float).reshape(-1, 3)
    for de, ate, cota in S:
        ax.plot([de, ate], [cota / 1000] * 2, color=VERM, lw=2.2, zorder=4)
    for e in lista(c['ext']):
        if e['V'] < 5000:
            continue
        xe = (e['de'] + e['ate']) / 2
        ax.annotate(f"{e['tipo']}\n{e['V'] / 1000:,.0f} mil m³".replace(',', '.'), (xe, np.interp(xe, x, O) / 1000),
                    xytext=(0, -34 if e['tipo'] == 'Empréstimo' else 22), textcoords='offset points', ha='center', fontsize=8.5,
                    color=VERM, arrowprops=dict(arrowstyle='-', color=VERM, lw=0.8))
    ax.axhline(0, color=MUTED, lw=0.6, ls=':')
    ax.set_ylabel('Ordenada (×10³ m³)')
    ax.set_title(titulo + f" — MT = {c['MT'] / 1e6:.2f}".replace('.', ',') + '×10⁶ m³·dam', loc='left')


c1 = R['cenarios']['eco_aula']; c2 = R['cenarios']['livre']; ce = R['cenarios']['eco']
fig, axs = plt.subplots(2, 1, figsize=(13, 8.4), sharex=True)
painel(axs[0], c1, 'Recomendada: 1 LC do P0 ao PF (compensa tudo)')
painel(axs[1], c2, 'Ótimo do modelo da aula (bota-fora e empréstimo a 150 m)')
axs[1].set_xlabel('Distância ao P0 (m)')
fig.tight_layout()
fig.savefig('figuras/11_distribuicao.png', bbox_inches='tight', facecolor=MARF)
print('ok figuras/11_distribuicao.png')
for k, c in R['cenarios'].items():
    print(f"{k:12s} MT {c['MT']:>14,.0f}  int {c['MTint']:>12,.0f}  ext {c['MText']:>12,.0f}  BF {c['Vbf']:>10,.0f}  EMP {c['Vemp']:>10,.0f}  "
          f"Vint {c['Vint']:>10,.0f}  DMTmed {c['DMTmedia']:>6,.0f}  LCs {np.array(c['S']).reshape(-1, 3).shape[0]}")
