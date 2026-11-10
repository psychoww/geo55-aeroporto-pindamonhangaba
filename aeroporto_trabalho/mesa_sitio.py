"""Escolha de posição e azimute da PPD pelo método MESA (Manual de Apoio à Prospecção de Sítios Aeroportuários
Regionais, SAC/MInfra + ITA, 2021), na vizinhança do sítio da prévia (oeste de Pindamonhangaba).

Combinações testadas: centros numa grade de PASSO m até RAIO m do centro atual × rumos de 0° a 170° (10° em 10°).
Geometria (manual, I-2.2, código 3/4 IFR-NP): área física = PPD + 600 m × 500 m; curva de 75 dB e 65 dB do PBZR
(RBAC 161, Tabela C-1, classe 4): 75 dB L1 = 550, R1 = 160; 65 dB L2 = 700, R2 = 500 (a partir das cabeceiras).

Critérios eliminatórios (II-2 e III-2):
  ESP   ≥ 10 km de SBSJ e SBTA (proxy da influência de aeroportos de mesmo porte)
  MET   utilização ≥ 95% com vento de través ≤ 10 kt ("sempre que possível 10 kt", I-2.1.3)
  AMB   água/área úmida ≤ 1% e árvores ≤ 20% da área física (ESA WorldCover 2021)
  ALAG  várzea (área propensa a alagamento, plano de informação da Tabela II-4): no máximo 5% da área física a menos
        de 8 m acima do fundo do vale (mínimo do MDE num raio de 3 km)
  INF   área física sem rodovia (motorway/trunk/primary/secondary), ferrovia ou linha de transmissão (OSM), folga de 30 m
  TOPAlt  ΔH na área física ≤ X_TOPALT
  OBS   sem penetração > 5 m em aproximação/decolagem e transição fora do PPSit, exceto em pixels de árvore (removíveis)
  URB   ≥ 2 km da mancha urbana — o manual permite flexibilizar quando não há área viável (III-1.1); aqui é medido
        e usado como critério flexível (ver relatório)
Critérios classificatórios (V): TOPVol (pseudocódigo do manual), RUI (proxy: ha construídos na curva de 65 dB),
DIS (km até o centro de Pindamonhangaba), ACE (km até rodovia pavimentada), GEO e DIP sem dado (iguais para todos).
Pesos: vetor final do exemplo do manual (Tabela V-3). Normalização: (1/x)/Σ(1/x) (menor é melhor), como nas Tabelas V-6/V-7.

Saída: dados/mesa.json. Uso: python mesa_sitio.py
"""
import json
import numpy as np
from scipy.ndimage import uniform_filter, distance_transform_edt, map_coordinates
from dem import carrega_worldcover, geo2utm, utm2geo
import ols
import projeto as p

RAIO, PASSO = 6000.0, 200.0
AZS = list(range(0, 180, 10))
PPD = 1900.0
L_FIS, W_FIS = PPD + 600, 500.0
L1, R1, L2, R2 = 550.0, 160.0, 700.0, 500.0
X_TOPALT = 40.0
CGD = ('Pindamonhangaba (centro)', -45.4617, -22.9244)
AEROPORTOS = [(-45.8711, -23.2292), (-45.5158, -23.0389)]
PESOS = dict(GEO=0.280, TOPVol=0.333, RUI=0.079, DIS=0.127, ACE=0.125, DIP=0.056)

U0 = np.array([p.XC, p.YC])

# ---------------------------------------------------------------- rasters em UTM (10 m) no domínio
M = RAIO + 6000
gx0, gy0, R10 = p.XC - M, p.YC - M, 10.0
n10 = int(2 * M / R10)
xs = gx0 + (np.arange(n10) + 0.5) * R10; ys = gy0 + (np.arange(n10) + 0.5) * R10
lo_min, la_min = utm2geo.transform(gx0 - 2000, gy0 - 2000); lo_max, la_max = utm2geo.transform(gx0 + 2 * M + 2000, gy0 + 2 * M + 2000)
wc = carrega_worldcover(lo_min, lo_max, la_min, la_max)
CL = np.empty((n10, n10), np.uint8)
for i in range(n10):
    lo, la = utm2geo.transform(xs, np.full(n10, ys[i]))
    CL[i] = wc.nearest(lo, la)
BUILT = (CL == 50).astype(np.float32)
# mancha urbana: ≥ 20% construído num raio de ~250 m
dens = uniform_filter(BUILT, size=51, mode='constant')
MANCHA = dens >= 0.20
DIST_MANCHA = distance_transform_edt(~MANCHA) * R10


def amostra10(arr, x, y, order=0):
    return map_coordinates(arr, [(y - gy0) / R10 - 0.5, (x - gx0) / R10 - 0.5], order=order, mode='nearest')


# infraestrutura OSM rasterizada (10 m) para INF e ACE
osm = json.load(open('dados/osm/infra.json', encoding='utf-8'))['elements']
INF = np.zeros((n10, n10), bool); PAV = np.zeros((n10, n10), bool)
for e in osm:
    tg = e.get('tags', {}); g = e.get('geometry') or []
    if len(g) < 2:
        continue
    hw = tg.get('highway', '')
    eh_inf = hw in ('motorway', 'trunk', 'primary', 'secondary', 'motorway_link', 'trunk_link', 'primary_link') \
        or tg.get('railway') == 'rail' or tg.get('power') == 'line'
    eh_pav = hw in ('motorway', 'trunk', 'primary', 'secondary', 'motorway_link', 'trunk_link', 'primary_link') \
        or tg.get('surface') in ('asphalt', 'paved', 'concrete')
    lon = np.array([q['lon'] for q in g]); lat = np.array([q['lat'] for q in g])
    x, y = geo2utm.transform(lon, lat)
    for k in range(len(x) - 1):
        n = int(np.hypot(x[k + 1] - x[k], y[k + 1] - y[k]) / 5) + 2
        px = np.linspace(x[k], x[k + 1], n); py = np.linspace(y[k], y[k + 1], n)
        j = ((px - gx0) / R10).astype(int); i = ((py - gy0) / R10).astype(int)
        ok = (i >= 0) & (i < n10) & (j >= 0) & (j < n10)
        if eh_inf:
            INF[i[ok], j[ok]] = True
        if eh_pav:
            PAV[i[ok], j[ok]] = True
DIST_INF = distance_transform_edt(~INF) * R10
DIST_PAV = distance_transform_edt(~PAV) * R10

# várzea (área propensa a alagamento, Tabela II-4): altura sobre o fundo do vale num raio de 3 km < HV_MIN
from scipy.ndimage import minimum_filter
HV = ols.Z - minimum_filter(ols.Z, size=int(6000 / ols.P) + 1, mode='nearest')
HV_MIN = 8.0

# ---------------------------------------------------------------- vento (MET)
d = json.load(open('dados/vento_era5.json'))
vv = np.array(d['hourly']['wind_speed_10m'], float); aa = np.array(d['hourly']['wind_direction_10m'], float)
m = ~np.isnan(vv) & ~np.isnan(aa); vv, aa = vv[m], aa[m]


def utilizacao(az, lim):
    trav = vv * np.abs(np.sin(np.radians(aa - az)))
    return float((trav <= lim).mean())


MET = {az: dict(u10=utilizacao(az, 10), u13=utilizacao(az, 13), u20=utilizacao(az, 20)) for az in AZS}

# ---------------------------------------------------------------- grades locais (s ao longo do eixo, t transversal)
def grade(L, W, passo):
    s = np.arange(-L / 2, L / 2 + 0.1, passo); t = np.arange(-W / 2, W / 2 + 0.1, passo)
    S, T = np.meshgrid(s, t); return S.ravel(), T.ravel()


Sf, Tf = grade(2020, 300, 30)                      # faixa de pista (TOPVol)
Sa, Ta = grade(L_FIS, W_FIS, 50)                   # área física (TOPAlt, AMB, INF, URB)
Sr, Tr = grade(PPD + 2 * (L2 + R2) + 100, 2 * R2 + 100, 20)
cab = PPD / 2
sx = np.maximum(np.abs(Sr) - cab - L2, 0)
in65 = (np.hypot(sx, Tr) <= R2) & (np.abs(Sr) <= cab + L2 + R2)
Sr, Tr = Sr[in65], Tr[in65]                        # curva de 65 dB (RUI)


def xy(cx, cy, az, S, T):
    u = np.array([np.sin(np.radians(az)), np.cos(np.radians(az))]); v = np.array([u[1], -u[0]])
    return cx + S * u[0] + T * v[0], cy + S * u[1] + T * v[1]


# centros
gx = np.arange(-RAIO, RAIO + 0.1, PASSO)
GX, GY = np.meshgrid(gx, gx)
dentro = np.hypot(GX, GY) <= RAIO
CX = p.XC + GX[dentro]; CY = p.YC + GY[dentro]
esp = np.ones(CX.size, bool)
for lo, la in AEROPORTOS:
    ax_, ay_ = geo2utm.transform(lo, la)
    esp &= np.hypot(CX - ax_, CY - ay_) >= 10000
print('centros:', CX.size, ' ESP ok:', esp.sum())

cgx, cgy = geo2utm.transform(CGD[1], CGD[2])
reg = []
for az in AZS:
    # TOPVol e TOPAlt (MDE de 30 m)
    X, Y = xy(CX[:, None], CY[:, None], az, Sf[None], Tf[None])
    H = ols.amostra(X.ravel(), Y.ravel()).reshape(X.shape)
    hmed = H.mean(1, keepdims=True)
    topvol = (np.clip(hmed - H, 0, None) * 30 * 30).sum(1)
    X, Y = xy(CX[:, None], CY[:, None], az, Sa[None], Ta[None])
    Ha = ols.amostra(X.ravel(), Y.ravel()).reshape(X.shape)
    topalt = Ha.max(1) - Ha.min(1)
    ca = amostra10(CL, X.ravel(), Y.ravel()).reshape(X.shape)
    agua = np.isin(ca, (80, 90)).mean(1); arv = (ca == 10).mean(1)
    dinf = amostra10(DIST_INF, X.ravel(), Y.ravel()).reshape(X.shape).min(1)
    durb = amostra10(DIST_MANCHA, X.ravel(), Y.ravel()).reshape(X.shape).min(1)
    hv = map_coordinates(HV, [(Y.ravel() - ols.Y0) / ols.P, (X.ravel() - ols.X0) / ols.P], order=1, mode='nearest').reshape(X.shape)
    hv_baixo = (hv < HV_MIN).mean(1)
    X, Y = xy(CX[:, None], CY[:, None], az, Sr[None], Tr[None])
    rui = amostra10(BUILT, X.ravel(), Y.ravel()).reshape(X.shape).sum(1) * 20 * 20 / 1e4
    ace = amostra10(DIST_PAV, CX, CY, order=1) / 1000
    dis = np.hypot(CX - cgx, CY - cgy) / 1000
    for k in range(CX.size):
        reg.append(dict(x=float(CX[k]), y=float(CY[k]), az=az, ESP=bool(esp[k]), TOPVol=float(topvol[k]),
                        TOPAlt=float(topalt[k]), agua=float(agua[k]), arv=float(arv[k]), dINF=float(dinf[k]),
                        varzea=float(hv_baixo[k]), hv_min=float(hv[k].min()),
                        dURB=float(durb[k]), RUI=float(rui[k]), ACE=float(ace[k]), DIS=float(dis[k])))
    print(f'az {az:3d}: ok')

for r in reg:
    r['MET'] = MET[r['az']]['u10'] >= 0.95
    r['AMB'] = r['agua'] <= 0.01 and r['arv'] <= 0.20
    r['ALAG'] = r['varzea'] <= 0.05
    r['INF'] = r['dINF'] >= 30
    r['TOPAlt_ok'] = r['TOPAlt'] <= X_TOPALT
pre = [r for r in reg if r['ESP'] and r['MET'] and r['AMB'] and r['ALAG'] and r['INF'] and r['TOPAlt_ok']]
print('passam ESP, MET, AMB, ALAG, INF, TOPAlt:', len(pre), 'de', len(reg))
for nome in ('ESP', 'MET', 'AMB', 'ALAG', 'INF', 'TOPAlt_ok'):
    print(f'  reprovadas por {nome}:', sum(not r[nome] for r in reg))


# OBS: só nas combinações que passaram (aproximação/decolagem e transição; horizontal interna e cônica documentadas)
def obs(cx, cy, az, passo=120.0):
    s = np.arange(-16000, 16000.1, passo); t = np.arange(-6000, 6000.1, passo)
    S, T = np.meshgrid(s, t)
    X, Y = xy(cx, cy, az, S, T)
    z = ols.amostra(X.ravel(), Y.ravel()).reshape(S.shape)
    mf = (np.abs(S) <= 1010) & (np.abs(T) <= 150)
    ze = z[mf].mean()
    h = 1010.0
    ds = np.maximum(np.abs(S) - h, 0); at = np.abs(T)
    apr = (ds > 0) & (at <= 150 + 0.15 * ds) & (ds <= 15000)
    za = np.where(ds <= 3000, 0.02 * ds, np.where(ds <= 6600, 60 + 0.025 * (ds - 3000), 150.0))
    tra = (ds == 0) & (at > 150) & (0.143 * (at - 150) <= 45)
    sup_crit = np.where(apr, ze + za, np.where(tra, ze + 0.143 * (at - 150), np.inf))
    ppsit = (np.abs(S) <= PPD / 2 + L1 + R1) & (at <= 270)
    cls = amostra10(CL, X.ravel(), Y.ravel()).reshape(S.shape)
    pen = z - sup_crit
    crit = (pen > 5) & ~ppsit & (cls != 10)
    sup_all = ols.superficie(S, T, ze)
    pen_all = np.where(~mf & np.isfinite(sup_all), z - sup_all, -np.inf)
    return dict(OBS=not crit.any(), pen_crit_max=float(np.max(np.where(~ppsit & (cls != 10), pen, -np.inf))),
                area_crit_ha=float(crit.sum() * passo ** 2 / 1e4), pen_hz_max=float(pen_all.max()),
                area_hz_ha=float((pen_all > 5).sum() * passo ** 2 / 1e4))


for k, r in enumerate(pre):
    r.update(obs(r['x'], r['y'], r['az']))
    if k % 500 == 0:
        print('OBS', k, '/', len(pre))
viav = [r for r in pre if r['OBS']]
print('viáveis (sem URB):', len(viav), ' com URB ≥ 2 km:', sum(r['dURB'] >= 2000 for r in viav))

# combinação atual (sítio da prévia), para comparação
atual = min(reg, key=lambda r: (r['az'] != 60, np.hypot(r['x'] - p.XC, r['y'] - p.YC)))
atual = dict(atual); atual.update(obs(atual['x'], atual['y'], atual['az']))

por_az = {}
for az in AZS:
    ra = [r for r in reg if r['az'] == az]; pa = [r for r in pre if r['az'] == az]; va = [r for r in viav if r['az'] == az]
    por_az[str(az)] = dict(total=len(ra), **{f'ok_{n}': sum(r[n] for r in ra) for n in ('ESP', 'AMB', 'ALAG', 'INF', 'TOPAlt_ok')},
                           pre=len(pa), obs_ok=len(va), urb_ok=sum(r['dURB'] >= 2000 for r in va),
                           topvol_min_viavel=min((r['TOPVol'] for r in va), default=None),
                           topvol_min_viavel_urb=min((r['TOPVol'] for r in va if r['dURB'] >= 2000), default=None),
                           topvol_min_esp=min((r['TOPVol'] for r in ra if r['ESP']), default=None))
json.dump(dict(parametros=dict(RAIO=RAIO, PASSO=PASSO, L_FIS=L_FIS, W_FIS=W_FIS, X_TOPALT=X_TOPALT, CGD=CGD, PESOS=PESOS,
                               L1=L1, R1=R1, L2=L2, R2=R2, HV_MIN=HV_MIN),
               MET={str(k): v for k, v in MET.items()}, por_az=por_az, atual=atual, viaveis=viav,
               resumo=dict(combinacoes=len(reg), pre=len(pre), viaveis=len(viav))),
          open('dados/mesa.json', 'w', encoding='utf-8'), indent=0)
print('ok dados/mesa.json')
