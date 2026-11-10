"""Ranqueamento MESA (capítulo V do manual) dos sítios candidatos tirados de dados/mesa.json (mesa_sitio.py).

1. Candidatos: das combinações viáveis que respeitam URB (≥ 2 km da mancha urbana), sítios distintos (centros a
   ≥ SEP m) em ordem de nota preliminar. URB só seria flexibilizado se não houvesse área viável (manual, III-1.1);
   como há, os sítios colados à cidade (inclusive o da prévia) ficam numa lista à parte, de eliminados por URB.
2. Métricas: TOPVol, RUI, DIS, ACE (GEO e DIP sem dado: iguais para todos, não mudam a ordem).
3. Normalização (1/x)/Σ(1/x) (menor é melhor; Tabelas V-6/V-7). Harmonização: RUI usa x + 1 ha (evita dividir por
   zero); DIS e ACE têm piso de 1 km (abaixo disso o acesso é equivalente e 1/x explodiria).
4. Nota = Σ peso × métrica normalizada (Tabela V-8), pesos do vetor final do exemplo (Tabela V-3).
5. Sensibilidade (Figura V-8): cada peso de 0 a 100%, os outros reescalados na mesma proporção.
Saídas: dados/mesa_ranking.json, figuras/12_mesa_azimute.png, 13_mesa_candidatos.png, 14_mesa_sensibilidade.png.
"""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from dem import utm2geo
from imagem import imagem_utm
import projeto as p

plt.rcParams.update({'font.family': ['Bahnschrift', 'Segoe UI', 'Arial'], 'axes.unicode_minus': False, 'font.size': 11,
                     'axes.spines.top': False, 'axes.spines.right': False})
OURO, AZUL, CINZA, NAVY, MUTED = '#C99A06', '#1F4FD8', '#8C919B', '#13306B', '#5B6270'
SEP, N_URB, SEP_FLEX, N_FLEX = 500.0, 8, 1000.0, 6

d = json.load(open('dados/mesa.json', encoding='utf-8'))
PESOS = d['parametros']['PESOS']
CRIT = ['GEO', 'TOPVol', 'RUI', 'DIS', 'ACE', 'DIP']


def metricas(r):
    return dict(GEO=1.0, TOPVol=r['TOPVol'], RUI=r['RUI'] + 1.0, DIS=max(r['DIS'], 1.0), ACE=max(r['ACE'], 1.0), DIP=1.0)


def notas(lista, pesos):
    M = np.array([[metricas(r)[c] for c in CRIT] for r in lista])
    inv = 1.0 / M
    N = inv / inv.sum(0)
    w = np.array([pesos[c] for c in CRIT])
    return N, N @ w


V = d['viaveis']
_, pre = notas(V, PESOS)
ordem = np.argsort(-pre)


def escolhe(filtro, n, ja, sep=SEP):
    out = []
    for k in ordem:
        r = V[k]
        if not filtro(r):
            continue
        if all(np.hypot(r['x'] - q['x'], r['y'] - q['y']) >= sep for q in ja + out):
            out.append(r)
        if len(out) == n:
            break
    return out


cand = escolhe(lambda r: r['dURB'] >= 2000, N_URB, [])
elim = escolhe(lambda r: r['dURB'] < 2000, N_FLEX, cand, SEP_FLEX)
atual = d['atual']; atual['nome'] = 'Prévia (atual)'
for i, r in enumerate(cand, 1):
    r['nome'] = f'C{i}'
for i, r in enumerate(elim, 1):
    r['nome'] = f'E{i}'
lista = cand
N, S = notas(lista, PESOS)
for r, n, s in zip(lista, N, S):
    r['norm'] = {c: float(v) for c, v in zip(CRIT, n)}
    r['nota'] = float(s)
    lo, la = utm2geo.transform(r['x'], r['y']); r['lat'], r['lon'] = float(la), float(lo)
    r['desloc_km'] = float(np.hypot(r['x'] - p.XC, r['y'] - p.YC) / 1000)
rank = sorted(lista, key=lambda r: -r['nota'])
for r in elim + [atual]:
    lo, la = utm2geo.transform(r['x'], r['y']); r['lat'], r['lon'] = float(la), float(lo)
    r['desloc_km'] = float(np.hypot(r['x'] - p.XC, r['y'] - p.YC) / 1000)
print(f"{'#':>2} {'sítio':16} {'rumo':>4} {'nota':>6} {'TOPVol mil m³':>13} {'RUI ha':>6} {'DIS km':>6} {'ACE km':>6} {'URB km':>6} {'ΔH m':>5} {'desloc km':>9}")
for i, r in enumerate(rank, 1):
    print(f"{i:2d} {r['nome']:16} {r['az']:4d} {r['nota']:.4f} {r['TOPVol'] / 1e3:13.0f} {r['RUI']:6.1f} {r['DIS']:6.1f} {r['ACE']:6.1f} "
          f"{r['dURB'] / 1e3:6.1f} {r['TOPAlt']:5.0f} {r['desloc_km']:9.1f}  ({r['lat']:.4f}, {r['lon']:.4f})")

# sensibilidade: vencedor em função de cada peso
sens = {}
for c in CRIT:
    xs = np.linspace(0, 1, 101); venc = []
    for x in xs:
        resto = 1 - PESOS[c]
        w = {k: (x if k == c else (PESOS[k] / resto * (1 - x) if resto > 0 else 0)) for k in CRIT}
        _, s = notas(lista, w)
        venc.append(lista[int(np.argmax(s))]['nome'])
    sens[c] = venc
    trocas = [(round(float(xs[i]) * 100), venc[i - 1], venc[i]) for i in range(1, len(xs)) if venc[i] != venc[i - 1]]
    print(f'sensibilidade {c}: vencedor no peso atual = {venc[int(round(PESOS[c] * 100))]}; trocas: {trocas}')

print('eliminados por URB (< 2 km da mancha urbana):')
for r in elim + [atual]:
    print(f"   {r['nome']:16} {r['az']:4d} {'':6} {r['TOPVol'] / 1e3:13.0f} {r['RUI']:6.1f} {r['DIS']:6.1f} {r['ACE']:6.1f} "
          f"{r['dURB'] / 1e3:6.1f} {r['TOPAlt']:5.0f} {r['desloc_km']:9.1f}  ({r['lat']:.4f}, {r['lon']:.4f})")
json.dump(dict(pesos=PESOS, candidatos=rank, eliminados_urb=elim + [atual], sensibilidade=sens),
          open('dados/mesa_ranking.json', 'w', encoding='utf-8'), indent=1)


def salva(fig, nome):
    fig.savefig(f'figuras/{nome}', dpi=160, bbox_inches='tight'); plt.close(fig); print('ok figuras/' + nome)


# 12. azimute: o que cada rumo permite --------------------------------------------------------------
az = sorted(int(k) for k in d['por_az'])
pa = [d['por_az'][str(a)] for a in az]
fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 6.4), sharex=True, gridspec_kw=dict(height_ratios=[1, 1.15]))
pre_n = [q['pre'] for q in pa]; ok_n = [q['obs_ok'] for q in pa]; urb_n = [q['urb_ok'] for q in pa]
a1.bar(az, pre_n, width=7, color=CINZA, alpha=0.45, label='passam relevo, várzea, ambiente, infraestrutura')
a1.bar(az, ok_n, width=7, color=NAVY, label='… e também as superfícies de proteção (OBS)')
a1.bar(az, urb_n, width=7, color=OURO, label='… e ficam a ≥ 2 km da mancha urbana (URB)')
a1.set_ylabel('posições viáveis'); a1.legend(frameon=False, fontsize=9, loc='upper right')
a1.set_title('Só os rumos de 20° a 80°, no eixo do vale, passam nas superfícies de proteção; o vento não restringe nenhum', loc='left', fontsize=12)
tv = [q['topvol_min_viavel'] / 1e3 if q['topvol_min_viavel'] else np.nan for q in pa]
tu = [q['topvol_min_viavel_urb'] / 1e3 if q['topvol_min_viavel_urb'] else np.nan for q in pa]
a2.plot(az, tv, 'o-', color=NAVY, label='melhor posição viável')
a2.plot(az, tu, 's-', color=OURO, label='melhor posição viável a ≥ 2 km da cidade')
a2.axhline(atual['TOPVol'] / 1e3, color=CINZA, ls='--')
a2.text(100, atual['TOPVol'] / 1e3 + 25, 'sítio da prévia (060°)', va='bottom', color=MUTED, fontsize=9)
a2.set_ylim(0, atual['TOPVol'] / 1e3 * 1.18)
a2.set_ylabel('TOPVol (mil m³)'); a2.set_xlabel('Rumo da PPD (°)'); a2.legend(frameon=False, fontsize=9, loc='lower right')
met = [d['MET'][str(a)]['u10'] * 100 for a in az]
a2.text(95, atual['TOPVol'] / 1e3 * 0.62, f'Vento (ERA5, través ≤ 10 kt): utilização de {min(met):.1f}% a {max(met):.1f}%\nem todos os rumos — não diferencia',
        fontsize=9, color=MUTED, va='bottom')
a2.set_xticks(az)
salva(fig, '12_mesa_azimute.png')

# 13. candidatos sobre a imagem -------------------------------------------------------------------
todos = rank + [atual]
xs_ = [r['x'] for r in todos]; ys_ = [r['y'] for r in todos]
cx, cy = (min(xs_) + max(xs_)) / 2, (min(ys_) + max(ys_)) / 2
h = max(max(xs_) - min(xs_), max(ys_) - min(ys_)) / 2 + 3500
img = imagem_utm(cx - h, cy - h, cx + h, cy + h, res=h / 700, z=14)
fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(img, extent=[cx - h, cx + h, cy - h, cy + h])
for i, r in enumerate(todos):
    u = np.array([np.sin(np.radians(r['az'])), np.cos(np.radians(r['az']))]); v = np.array([u[1], -u[0]])
    cor = OURO if r['nome'] == rank[0]['nome'] else ('white' if r['nome'].startswith('Prévia') else '#7FA2FF')
    cs = [(-1010, -150), (1010, -150), (1010, 150), (-1010, 150), (-1010, -150)]
    P_ = np.array([[r['x'], r['y']] + s * u + t * v for s, t in cs])
    ax.plot(P_[:, 0], P_[:, 1], color=cor, lw=2.2 if i == 0 else 1.4, ls='-' if not r['nome'].startswith('Prévia') else '--')
    rot = r['nome'] if r['nome'].startswith('Prévia') else f"{r['nome']} ({i + 1}º)"
    if i == 0 or r['nome'].startswith('Prévia'):
        ax.text(r['x'] - 1500 * u[0], r['y'] - 1500 * u[1], rot, color=cor, fontsize=10, ha='center', va='center',
                bbox=dict(facecolor='black', alpha=0.45, lw=0, pad=2))
ax.set_xlim(cx - h, cx + h); ax.set_ylim(cy - h, cy + h); ax.set_xticks([]); ax.set_yticks([])
ax.set_title('Candidatos MESA a ≥ 2 km da cidade (azul; ouro = 1º lugar) e a faixa da prévia (tracejado)',
             loc='left', fontsize=11)
salva(fig, '13_mesa_candidatos.png')

# 14. sensibilidade -------------------------------------------------------------------------------
nomes = [r['nome'] for r in rank]
fig, ax = plt.subplots(figsize=(10, 3.6))
for j, c in enumerate(['TOPVol', 'RUI', 'DIS', 'ACE']):
    venc = sens[c]
    for k in range(101):
        ax.add_patch(plt.Rectangle((k - 0.5, j - 0.35), 1, 0.7, color=OURO if venc[k] == rank[0]['nome'] else CINZA, lw=0))
    ax.plot(PESOS[c] * 100, j, 'v', color=NAVY, ms=9)
ax.set_yticks(range(4)); ax.set_yticklabels(['TOPVol', 'RUI', 'DIS', 'ACE']); ax.set_xlim(-1, 101); ax.set_ylim(-0.6, 3.6)
ax.set_xlabel('peso do critério (%) — os demais reescalados na mesma proporção')
ax.set_title(f'Sensibilidade: ouro = {rank[0]["nome"]} continua em 1º; triângulo = peso adotado', loc='left', fontsize=12)
salva(fig, '14_mesa_sensibilidade.png')
