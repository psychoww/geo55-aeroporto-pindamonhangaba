"""Superfícies em LandXML 1.2 para o Civil 3D (Surfaces.ImportXML):
  TN            terreno natural (nós do MDE, Delaunay = mesma triangulação do motor de cálculo)
  TN_limpo      TN - 0,15 m (após a limpeza da camada vegetal)
  TERRAPLENAGEM plataforma de terraplenagem (topo do subleito) + taludes, das seções a cada 10 m
  ACABADA       superfície acabada da PPD/acostamentos/faixa (para visualização)
"""
import json
import numpy as np
from scipy.spatial import Delaunay
import projeto as p

g = json.load(open('dados/greide.json'))
PVIS = [tuple(x) for x in g['pvis']]


def xml_surface(nome, desc, P, F):
    out = [f'  <Surface name="{nome}" desc="{desc}">', '   <Definition surfType="TIN">', '    <Pnts>']
    out += [f'     <P id="{k + 1}">{y:.3f} {x:.3f} {z:.3f}</P>' for k, (x, y, z) in enumerate(P)]
    out += ['    </Pnts>', '    <Faces>']
    out += [f'     <F>{a + 1} {b + 1} {c + 1}</F>' for a, b, c in F]
    out += ['    </Faces>', '   </Definition>', '  </Surface>']
    return '\n'.join(out)


def grava(arquivo, superficies):
    cab = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<LandXML xmlns="http://www.landxml.org/schema/LandXML-1.2" version="1.2" date="2026-11-09" time="00:00:00">\n'
           ' <Units><Metric areaUnit="squareMeter" linearUnit="meter" volumeUnit="cubicMeter" temperatureUnit="celsius" pressureUnit="milliBars"/></Units>\n'
           ' <Surfaces>\n')
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(cab + '\n'.join(superficies) + '\n </Surfaces>\n</LandXML>\n')


def malha_secoes(fun_z, passo=10.0):
    """Malha estruturada estação x offset. fun_z(est, zg) -> (offsets, z) com o mesmo número de vértices."""
    ests = sorted(set(np.arange(0, p.COMP + 0.1, passo).tolist()) | {e for e, _ in p.estacas_memorial(PVIS)})
    linhas = []
    for e in ests:
        zg = float(p.greide(PVIS, [e])[0])
        off, z = fun_z(e, zg)
        x, y = p.xy(np.full(len(off), e), off)
        linhas.append(np.column_stack([x, y, z]))
    n = len(linhas[0])
    P = np.vstack(linhas)
    F = []
    for i in range(len(linhas) - 1):
        for j in range(n - 1):
            a, b, c, d = i * n + j, i * n + j + 1, (i + 1) * n + j, (i + 1) * n + j + 1
            if np.hypot(*(P[a, :2] - P[b, :2])) < 1e-3 or np.hypot(*(P[c, :2] - P[d, :2])) < 1e-3:
                continue
            F += [(a, b, d), (a, d, c)]
    return P, np.array(F), ests


OFFS = np.array([0, 22.5, 22.52, 30.0, 30.02, 150.0])


def z_terraplenagem(e, zg):
    s = p.secao(e, zg, p.eg_secao(e))
    ze_d = float(np.interp(s['off_dir'], p.OFF, s['eg']))
    ze_e = float(np.interp(-s['off_esq'], p.OFF, s['eg']))
    od = np.concatenate([OFFS, [s['off_dir']]])
    oe = -np.concatenate([OFFS, [s['off_esq']]])[::-1][:-1]
    off = np.concatenate([oe, od])
    z = p.secao_terraplenagem(zg, off)
    # degraus do pavimento: nos offsets 22,52 e 30,02 já vale a espessura seguinte
    z[0] = ze_e; z[-1] = ze_d
    return off, z


def z_acabada(e, zg):
    off = np.concatenate([-OFFS[::-1][:-1], OFFS])
    off = np.unique(np.concatenate([off, [-150, 150]]))
    return off, p.secao_acabada(zg, off)


if __name__ == '__main__':
    P = p.pontos_terreno()
    tri = Delaunay(P[:, :2])
    surfs = [xml_surface('TN', 'Terreno natural - Copernicus GLO-30 (DSM 1 arcseg), nos do MDE em UTM 23S', P, tri.simplices),
             xml_surface('TN_limpo', 'Terreno apos a limpeza da camada vegetal (TN - 0,15 m)', P - [0, 0, p.LIMPEZA], tri.simplices)]
    Pt, Ft, ests = malha_secoes(z_terraplenagem)
    surfs.append(xml_surface('TERRAPLENAGEM', 'Plataforma de terraplenagem (topo do subleito) e taludes 1V:1,5H / 1V:2H', Pt, Ft))
    Pa, Fa, _ = malha_secoes(z_acabada)
    surfs.append(xml_surface('ACABADA', 'Superficie acabada: PPD 1,5%, acostamentos e faixa 2,5%', Pa, Fa))
    grava('civil3d/superficies.xml', surfs)
    for nome, sx in zip(('TN', 'TN_limpo', 'TERRAPLENAGEM', 'ACABADA'), surfs):
        grava(f'civil3d/sup_{nome}.xml', [sx])   # o ImportXML do COM só lê a primeira superfície do arquivo
    # contorno da terraplenagem (para limitar o volume)
    n = len(Pt) // len(ests)
    contorno = np.vstack([Pt[0::n][:, :2], Pt[n - 1::n][::-1, :2]])
    json.dump(dict(contorno=contorno.tolist(), n_secoes=len(ests)), open('civil3d/contorno_terraplenagem.json', 'w'))
    print('TN', len(P), 'pts', len(tri.simplices), 'faces; TERRAPLENAGEM', len(Pt), 'pts', len(Ft), 'faces; ACABADA', len(Pa), 'pts', len(Fa), 'faces')
