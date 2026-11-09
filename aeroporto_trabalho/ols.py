"""Verificação das superfícies limitadoras de obstáculos (OLS, Anexo 14 / RBAC 154, código 4, precisão CAT I)
contra o MDE (Copernicus é DSM: inclui árvores e edificações, que também são obstáculos).

Superfícies (referência: elevação do aeródromo = cota média da faixa):
  - aproximação: borda interna de 300 m a 60 m da cabeceira, divergência 15%, 2% nos primeiros 3000 m,
    2,5% nos 3600 m seguintes, horizontal até 15000 m;
  - transição: 14,3% a partir das bordas da faixa (150 m do eixo) até a horizontal interna;
  - horizontal interna: +45 m, raio de 4000 m a partir das extremidades da faixa;
  - cônica: 5% a partir da horizontal interna, até +100 m acima dela (2000 m de largura).
"""
import numpy as np
from scipy.ndimage import map_coordinates

D = np.load('dados/grade_utm30.npz')
Z, X0, Y0, P = D['Z'], float(D['x0']), float(D['y0']), float(D['passo'])


def amostra(px, py):
    return map_coordinates(Z, [(py - Y0) / P, (px - X0) / P], order=1, mode='nearest')


def superficie(s, t, ze, comp_faixa=2020.0):
    """Cota da OLS (a menor entre as superfícies que cobrem o ponto) em coordenadas locais s, t."""
    h = comp_faixa / 2
    ds = np.maximum(np.abs(s) - h, 0.0)          # distância além da extremidade da faixa
    at = np.abs(t)
    inf = np.full(s.shape, np.inf)
    # aproximação (em cada sentido): borda interna na extremidade da faixa (60 m além da cabeceira)
    dentro = (ds > 0) & (at <= 150 + 0.15 * ds) & (ds <= 15000)
    za = np.where(ds <= 3000, 0.02 * ds, np.where(ds <= 6600, 60 + 0.025 * (ds - 3000), 150.0))
    inf = np.where(dentro, np.minimum(inf, ze + za), inf)
    # distância "estádio" até a faixa (para horizontal interna e cônica)
    dist = np.hypot(ds, np.maximum(at - 150, 0))
    zh = np.where(dist <= 4000, ze + 45, np.where(dist <= 6000, ze + 45 + 0.05 * (dist - 4000), np.inf))
    # transição: a partir da borda lateral da faixa (e da borda da aproximação), 14,3%
    zt = np.where((ds == 0) & (at > 150), ze + 0.143 * (at - 150), np.inf)
    sup = np.minimum(np.minimum(inf, zh), zt)
    sup = np.where((ds == 0) & (at <= 150), ze, sup)  # dentro da faixa: a própria faixa
    return sup


def verifica(cx, cy, az, ze=None, passo=90.0):
    u = np.array([np.sin(np.radians(az)), np.cos(np.radians(az))]); v = np.array([u[1], -u[0]])
    s = np.arange(-16000, 16000.1, passo); t = np.arange(-6000, 6000.1, passo)
    S, T = np.meshgrid(s, t)
    X = cx + S * u[0] + T * v[0]; Y = cy + S * u[1] + T * v[1]
    z = amostra(X.ravel(), Y.ravel()).reshape(S.shape)
    if ze is None:
        m = (np.abs(S) <= 1010) & (np.abs(T) <= 150)
        ze = z[m].mean()
    sup = superficie(S, T, ze)
    fora_faixa = ~((np.abs(S) <= 1010) & (np.abs(T) <= 150))
    pen = np.where(fora_faixa & np.isfinite(sup), z - sup, -np.inf)
    k = np.unravel_index(np.argmax(pen), pen.shape)
    area = (pen > 0).sum() * passo ** 2 / 1e4  # ha
    return dict(ze=float(ze), pen_max=float(pen[k]), s_pen=float(S[k]), t_pen=float(T[k]), area_pen_ha=float(area))


if __name__ == '__main__':
    import json
    c = json.load(open('dados/candidatos.json'))
    for k, d in enumerate(c):
        linhas = []
        for az in range(0, 180, 10):
            r = verifica(d['x'], d['y'], az)
            linhas.append((az, r['pen_max'], r['area_pen_ha']))
        best = sorted(linhas, key=lambda l: (l[2], l[1]))[:4]
        r0 = verifica(d['x'], d['y'], d['az'])
        print(f"#{k:2d} az_terra {d['az']:3.0f}: pen {r0['pen_max']:6.1f} m em (s={r0['s_pen']:.0f}, t={r0['t_pen']:.0f}), área {r0['area_pen_ha']:7.1f} ha | melhores az: "
              + '; '.join(f'{a}°: {p:.0f} m/{ar:.0f} ha' for a, p, ar in best))
