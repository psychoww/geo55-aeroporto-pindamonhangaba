"""Motor do projeto da PPD: terreno, alinhamento, seção-tipo, seções transversais e volumes (áreas médias).

Convenções
- Coordenadas UTM 23S (SIRGAS 2000, EPSG:31983). Eixo da PPD no rumo 060° (cabeceiras 06/24).
- Alinhamento = eixo da faixa de pista: estaca 0 (P0) na extremidade SW da faixa, PF a 2020 m (estaca 101).
  Cabeceira 06 no km 0+060 (estaca 3) e cabeceira 24 no km 1+960 (estaca 98).
- Seção-tipo (meia seção, simétrica), superfície acabada:
    0 a 22,5 m  PPD, -1,5% a partir do eixo; pavimento 1,10 m
    22,5 a 30 m acostamento, -2,5%; pavimento 0,50 m
    30 a 150 m  faixa de pista nivelada, -2,5%; sem pavimento
    > 150 m     taludes: corte 1V:1,5H, aterro 1V:2H, até o terreno natural.
- Terraplenagem (aula 7): seções no greide de terraplenagem (= acabado - pavimento); limpeza de 0,15 m em todo o
  footprint, que não entra na compensação; aterro sobre o terreno já limpo; Fh = 1,25 no aterro corrigido
  (adotado para o solo do sítio; a aula usou 1,1 só no exercício).
"""
import json
import os
import numpy as np
from scipy.interpolate import LinearNDInterpolator
from dem import carrega_dem, geo2utm, utm2geo

AQUI = os.path.dirname(os.path.abspath(__file__))
LAT_C, LON_C, RUMO = -22.9300, -45.4993, 60.0
# Teste de outro sítio sem mexer no da prévia: GEO55_SITIO="lat,lon,rumo" (usa cache de terreno próprio).
_SITIO = os.environ.get('GEO55_SITIO')
if _SITIO:
    LAT_C, LON_C, RUMO = (float(v) for v in _SITIO.split(','))
COMP = 2020.0
H_PPD, H_ACOST = 1.10, 0.50
B_PPD, B_ACOST, B_FAIXA = 22.5, 30.0, 150.0
I_PPD, I_FAIXA = 0.015, 0.025
TALUDE_CORTE, TALUDE_ATERRO = 1.5, 2.0      # H:V
LIMPEZA = 0.15
FH = 1.25   # adotado (09/11): latossolo vermelho-amarelo poroso sobre o Grupo Taubaté; ver PROGRESSO.md
R_VERT = 30000.0   # raio mínimo de curva vertical (Anexo 14 / RBAC 154, código 4)

XC, YC = geo2utm.transform(LON_C, LAT_C)
U = np.array([np.sin(np.radians(RUMO)), np.cos(np.radians(RUMO))])
V = np.array([U[1], -U[0]])   # à direita de quem anda no sentido do estaqueamento (SE)
P0 = np.array([XC, YC]) - COMP / 2 * U
PF = np.array([XC, YC]) + COMP / 2 * U


def xy(est, off=0.0):
    """Coordenadas UTM de um ponto do eixo (est em m) com afastamento off (m, + à direita)."""
    est = np.asarray(est, float); off = np.asarray(off, float)
    return P0[0] + est * U[0] + off * V[0], P0[1] + est * U[1] + off * V[1]


# ---------------------------------------------------------------- terreno
def pontos_terreno(s_lim=(-1800, 1800), t_lim=(-1000, 1000)):
    """Nós do MDE (grade de 1") convertidos para UTM, dentro do retângulo local (s ao longo do eixo, t transversal)."""
    cache = os.path.join(AQUI, 'dados', 'pontos_terreno.npy' if not _SITIO else
                         'pontos_terreno_' + _SITIO.replace(',', '_').replace('-', 'm') + '.npy')
    if os.path.exists(cache):          # versionado no repositório: dispensa baixar o MDE
        return np.load(cache)
    dem = carrega_dem()
    lons, lats = [], []
    cs = [np.array([XC, YC]) + a * U + b * V for a in s_lim for b in t_lim]
    lo_c, la_c = utm2geo.transform([c[0] for c in cs], [c[1] for c in cs])
    j0 = int(np.floor((min(lo_c) - dem.lon0) / dem.dlon)) - 2; j1 = int(np.ceil((max(lo_c) - dem.lon0) / dem.dlon)) + 2
    i0 = int(np.floor((dem.lat0 - max(la_c)) / dem.dlat)) - 2; i1 = int(np.ceil((dem.lat0 - min(la_c)) / dem.dlat)) + 2
    J, I = np.meshgrid(np.arange(j0, j1), np.arange(i0, i1))
    lon = dem.lon0 + J * dem.dlon; lat = dem.lat0 - I * dem.dlat
    z = dem.a[I, J]
    x, y = geo2utm.transform(lon, lat)
    s = (x - XC) * U[0] + (y - YC) * U[1]; t = (x - XC) * V[0] + (y - YC) * V[1]
    m = (s >= s_lim[0]) & (s <= s_lim[1]) & (t >= t_lim[0]) & (t <= t_lim[1])
    P = np.column_stack([x[m], y[m], z[m]])
    np.save(cache, P)
    return P


_TER = None


def terreno():
    global _TER
    if _TER is None:
        P = pontos_terreno()
        _TER = LinearNDInterpolator(P[:, :2], P[:, 2])
    return _TER


def cota_terreno(est, off=0.0):
    x, y = xy(est, off)
    return terreno()(x, y)


# ---------------------------------------------------------------- greide
def greide(pvis, est):
    """Greide (superfície acabada no eixo) com curvas verticais parabólicas simétricas.
    pvis: lista de (estaca_m, cota, L_curva) — a primeira e a última sem curva."""
    est = np.asarray(est, float)
    e = np.array([p[0] for p in pvis]); z = np.array([p[1] for p in pvis])
    zt = np.interp(est, e, z)
    g = np.diff(z) / np.diff(e)
    for k in range(1, len(pvis) - 1):
        L = pvis[k][2]
        if L <= 0:
            continue
        a = (g[k] - g[k - 1]) / (2 * L)
        x = est - (e[k] - L / 2)
        m = (x > 0) & (x < L)
        zt = np.where(m, (z[k] - g[k - 1] * L / 2) + g[k - 1] * x + a * x ** 2, zt)
    return zt


def curvas(pvis):
    """PCV/PTV de cada curva vertical."""
    out = []
    e = [p[0] for p in pvis]; z = [p[1] for p in pvis]
    for k in range(1, len(pvis) - 1):
        L = pvis[k][2]
        g1 = (z[k] - z[k - 1]) / (e[k] - e[k - 1]); g2 = (z[k + 1] - z[k]) / (e[k + 1] - e[k])
        if L > 0:
            out.append(dict(n=k, piv=e[k], cota_piv=z[k], L=L, g1=g1, g2=g2, pcv=e[k] - L / 2, ptv=e[k] + L / 2))
    return out


# ---------------------------------------------------------------- seção
OFF = np.arange(-450.0, 450.01, 0.5)


def secao_acabada(zg, off):
    a = np.abs(off)
    return zg - I_PPD * np.minimum(a, B_PPD) - I_FAIXA * np.clip(a - B_PPD, 0, None)


def secao_terraplenagem(zg, off):
    """Plataforma de terraplenagem (topo do subleito) até |off| <= 150 m."""
    a = np.abs(off)
    pav = np.where(a <= B_PPD, H_PPD, np.where(a <= B_ACOST, H_ACOST, 0.0))
    return secao_acabada(zg, off) - pav


def secao(est, zg, eg=None):
    """Seção transversal na estaca est (m) com greide zg no eixo.
    Retorna dict com áreas de corte/aterro (m²), largura de limpeza, offsets de offset (daylight) e as linhas."""
    if eg is None:
        eg = cota_terreno(np.full(OFF.size, est), OFF)
    d = secao_terraplenagem(zg, OFF)
    lados = {}
    for lado, sinal in (('E', -1), ('D', 1)):
        m = sinal * OFF >= B_FAIXA
        idx = np.where(m)[0]
        idx = idx[np.argsort(np.abs(OFF[idx]))]        # do eixo para fora
        o = np.abs(OFF[idx]); ge = eg[idx]
        z150 = secao_terraplenagem(zg, np.array([B_FAIXA]))[0]
        k150 = np.argmin(np.abs(o - B_FAIXA))
        if ge[k150] >= z150:   # corte
            dt = z150 + (o - B_FAIXA) / TALUDE_CORTE
            k = np.argmax(dt >= ge) if np.any(dt >= ge) else len(o) - 1
            tipo = 'corte'
        else:
            dt = z150 - (o - B_FAIXA) / TALUDE_ATERRO
            k = np.argmax(dt <= ge) if np.any(dt <= ge) else len(o) - 1
            tipo = 'aterro'
        # interpolação linear do ponto de offset
        if k > 0:
            f1 = dt[k - 1] - ge[k - 1]; f2 = dt[k] - ge[k]
            frac = f1 / (f1 - f2) if f1 != f2 else 0.0
            od = o[k - 1] + frac * (o[k] - o[k - 1])
        else:
            od = o[k]
        dd = np.where(o <= od, dt, np.nan)
        d[idx] = np.where(np.isnan(dd), ge, dd)
        lados[lado] = (od, tipo)
    oe, od = lados['E'][0], lados['D'][0]
    dentro = (OFF >= -oe) & (OFF <= od)
    base = eg - LIMPEZA
    diff = np.where(dentro, base - d, 0.0)
    h = OFF[1] - OFF[0]
    ac = np.trapezoid(np.clip(diff, 0, None), dx=h)
    aa = np.trapezoid(np.clip(-diff, 0, None), dx=h)
    return dict(est=float(est), zg=float(zg), area_corte=float(ac), area_aterro=float(aa), largura_limpeza=float(oe + od),
                off_esq=float(oe), off_dir=float(od), tipo_esq=lados['E'][1], tipo_dir=lados['D'][1],
                eg=eg, proj=np.where(dentro, d, np.nan), eg_eixo=float(np.interp(0, OFF, eg)))


# ---------------------------------------------------------------- volumes
_EG_CACHE = {}


def eg_secao(est):
    k = round(float(est), 3)
    if k not in _EG_CACHE:
        _EG_CACHE[k] = cota_terreno(np.full(OFF.size, est), OFF)
    return _EG_CACHE[k]


def estacas_memorial(pvis):
    """Estacas inteiras (20 m) + pontos notáveis: P0, cabeceiras, PCV/PTV, PF."""
    pts = {float(e): ('P0' if e == 0 else ('PF' if e == COMP else '')) for e in np.arange(0, COMP + 0.1, 20.0)}
    pts[60.0] = 'CAB 06'; pts[COMP - 60.0] = 'CAB 24'
    for c in curvas(pvis):
        pts[round(c['pcv'], 3)] = f"PCV{c['n']}"; pts[round(c['ptv'], 3)] = f"PTV{c['n']}"
    return sorted(pts.items())


def volumes(pvis, ests=None):
    if ests is None:
        ests = [e for e, _ in estacas_memorial(pvis)]
    ests = np.asarray(ests, float)
    zg = greide(pvis, ests)
    S = [secao(e, z, eg_secao(e)) for e, z in zip(ests, zg)]
    ac = np.array([s['area_corte'] for s in S]); aa = np.array([s['area_aterro'] for s in S])
    lw = np.array([s['largura_limpeza'] for s in S])
    dist = np.diff(ests)
    vc = dist * (ac[1:] + ac[:-1]) / 2; va = dist * (aa[1:] + aa[:-1]) / 2
    vl = dist * LIMPEZA * (lw[1:] + lw[:-1]) / 2
    return dict(ests=ests, zg=zg, secoes=S, ac=ac, aa=aa, vc=vc, va=va, vl=vl,
                Vc=float(vc.sum()), Va=float(va.sum()), Vl=float(vl.sum()))


def estaca_txt(e):
    n = int(e // 20); r = e - 20 * n
    return f'{n} + {r:05.2f}'.replace('.', ',')
