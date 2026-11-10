"""Custo comparado dos sítios: terraplenagem (SICRO) + desapropriação (terra + construções atingidas).

Preços (consultados em 10/11/2026; ver PROGRESSO.md):
  SICRO 5501712 (SP, ref. 2026-07): escavação, carga e transporte de 1ª categoria, DMT 200–400 m, motoscraper: R$ 14,05/m³
  SICRO 5502978 (SP, ref. 2026-07): compactação de aterros a 100% do Proctor normal: R$ 6,38/m³
  CUB/SP R1-N (Sinduscon-SP, set/2026, sem desoneração): R$ 2.690,33/m²
  Terra rural em Pindamonhangaba: anúncios de 2025 de áreas grandes, R$ 59–67 mil/ha → base R$ 65 mil/ha, faixa 40–120 mil
  (sem tabela oficial municipal acessível: o IEA publica por região e a planilha VTN da Receita não estava disponível).
Hipóteses: construções = área construída do ESA WorldCover × taxa de ocupação (base 40%, faixa 25–60%) × CUB; a terra sob as
construções entra pelo valor rural (limite inferior para lotes urbanos). Volumes do motor Python (mesma base para todos).
Áreas desapropriadas: (A) sítio do enunciado 3000 × 1500 m, deslocado para pegar o mínimo de construções com a faixa dentro;
(B) PPSit externo do manual MESA (curva de 75 dB): (PPD + 1420) × 540 m, centrado no eixo.
Saída: dados/custo_sitios.json. Uso: python custo_sitios.py
"""
import json
import numpy as np
from dem import carrega_worldcover, geo2utm, utm2geo

P_ESC, P_COMP, CUB = 14.05, 6.38, 2690.33
VTN, VTN_FAIXA = 65000.0, (40000.0, 120000.0)
OCUP, OCUP_FAIXA = 0.40, (0.25, 0.60)
SITIOS = {
    'Prévia (atual)': dict(lat=-22.9300, lon=-45.4993, az=60, greide='dados/greide.json'),
    'C1': dict(lat=-22.8885, lon=-45.4874, az=60, greide='tmp/mesa/greide_C1.json'),
    'C2': dict(lat=-22.8885, lon=-45.4933, az=60, greide='tmp/mesa/greide_C2.json'),
}
wc = carrega_worldcover(-45.60, -45.38, -23.02, -22.82)


def construido_ha(x, y, az, L, W, ds=0.0, dt=0.0, passo=10.0):
    u = np.array([np.sin(np.radians(az)), np.cos(np.radians(az))]); v = np.array([u[1], -u[0]])
    s = np.arange(-L / 2, L / 2 + 0.1, passo) + ds; t = np.arange(-W / 2, W / 2 + 0.1, passo) + dt
    S, T = [a.ravel() for a in np.meshgrid(s, t)]
    lo, la = utm2geo.transform(x + S * u[0] + T * v[0], y + S * u[1] + T * v[1])
    return float((wc.nearest(lo, la) == 50).sum() * passo ** 2 / 1e4)


def melhor_posicao(x, y, az):
    """Sítio 3000 × 1500 deslocado (faixa 2020 × 300 sempre dentro) para o mínimo de área construída."""
    melhor = None
    for ds in range(-490, 491, 70):
        for dt in range(-600, 601, 75):
            b = construido_ha(x, y, az, 3000, 1500, ds, dt, passo=20.0)
            if melhor is None or b < melhor[0]:
                melhor = (b, ds, dt)
    b = construido_ha(x, y, az, 3000, 1500, melhor[1], melhor[2])   # refina com passo de 10 m
    return b, melhor[1], melhor[2]


def custo_desap(area_ha, constr_ha, vtn=VTN, ocup=OCUP):
    terra = area_ha * vtn
    benf = constr_ha * 1e4 * ocup * CUB
    return terra, benf


res = {}
for nome, s in SITIOS.items():
    g = json.load(open(s['greide'], encoding='utf-8'))
    vc, va = g['Vc'], g['Va']
    terrapl = vc * P_ESC + va * P_COMP
    x, y = geo2utm.transform(s['lon'], s['lat'])
    bA, ds, dt = melhor_posicao(x, y, s['az'])
    bA0 = construido_ha(x, y, s['az'], 3000, 1500)
    bB = construido_ha(x, y, s['az'], 1900 + 1420, 540)
    out = dict(Vc=vc, Va=va, terraplenagem=terrapl, constr_sitio_centrado_ha=bA0, constr_A_ha=bA, desloc_A=(ds, dt), constr_B_ha=bB)
    for k, area, b in (('A', 450.0, bA), ('B', (1900 + 1420) * 540 / 1e4, bB)):
        terra, benf = custo_desap(area, b)
        out[k] = dict(area_ha=area, terra=terra, benfeitorias=benf, desapropriacao=terra + benf, total=terrapl + terra + benf)
        lo = sum(custo_desap(area, b, VTN_FAIXA[0], OCUP_FAIXA[0])) + terrapl
        hi = sum(custo_desap(area, b, VTN_FAIXA[1], OCUP_FAIXA[1])) + terrapl
        out[k]['total_faixa'] = (lo, hi)
    res[nome] = out

mi = lambda v: f'{v / 1e6:7.1f}'
print(f"{'sítio':16} {'corte m³':>10} {'aterro m³':>10} {'terrapl.':>8} | {'constr. ha (A/B)':>16} | {'desap A':>7} {'total A':>7} {'faixa A':>15} | {'desap B':>7} {'total B':>7}   (R$ milhões)")
for nome, o in res.items():
    A, B = o['A'], o['B']
    print(f"{nome:16} {o['Vc']:10,.0f} {o['Va']:10,.0f} {mi(o['terraplenagem'])} | {o['constr_A_ha']:6.2f} / {o['constr_B_ha']:6.2f}   | "
          f"{mi(A['desapropriacao'])} {mi(A['total'])} {mi(A['total_faixa'][0])}–{mi(A['total_faixa'][1]).strip()} | {mi(B['desapropriacao'])} {mi(B['total'])}")
    print(f"{'':16} sítio centrado: {o['constr_sitio_centrado_ha']:.2f} ha construídos; melhor deslocamento (ao longo, transversal) = {o['desloc_A']} m")
json.dump(dict(precos=dict(P_ESC=P_ESC, P_COMP=P_COMP, CUB=CUB, VTN=VTN, VTN_FAIXA=VTN_FAIXA, OCUP=OCUP, OCUP_FAIXA=OCUP_FAIXA),
               sitios=res), open('dados/custo_sitios.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('ok dados/custo_sitios.json')
