"""Nota de serviço de terraplenagem (aula 7): por estaca, cotas do terreno e do greide no eixo, altura de corte/aterro
no eixo e afastamentos/cotas dos pés de talude (offsets) dos dois lados, com o tipo (corte C ou aterro A).
Como no modelo da aula 7 (slide 21), traz também os pontos notáveis da plataforma (bordas da pista ±22,5 m, do acostamento
±30 m e da faixa ±150 m): cota do terreno, cota de projeto (topo do subleito) e h; e os volumes de corte e aterro da estaca.
Nas bordas ±22,5 e ±30 a cota de projeto é a do subleito sob o pavimento (o degrau fica logo fora; prancha 03).
Geometria do motor do projeto (mesmo terreno e seção-tipo do Civil 3D). Saída: dados/nota_servico.json e Tabelas/nota_servico.csv.
Uso: PYTHONUTF8=1 python nota_servico.py"""
import csv
import json
import os
import numpy as np
import projeto as p

AQUI = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(AQUI, 'dados', 'memorial.json'), encoding='utf-8'))
PONTOS = [-p.B_FAIXA, -p.B_ACOST, -p.B_PPD, 0.0, p.B_PPD, p.B_ACOST, p.B_FAIXA]
out = []
for l in M['linhas']:
    e = l['est_m']; zg = float(p.greide(M['pvis'], e))
    s = p.secao(e, zg, p.eg_secao(e))
    proj = p.secao_terraplenagem(zg, np.array(PONTOS))
    zt = float(proj[3])
    def cota(off):
        return float(np.interp(off, p.OFF, s['eg']))
    pts = []
    for off, zp in zip(PONTOS, proj):
        tn = s['eg_eixo'] if off == 0 else cota(off)
        pts.append(dict(off=off, tn=tn, proj=float(zp), h=float(tn - p.LIMPEZA - zp)))
    out.append(dict(estaca=l['estaca'], ponto=l['ponto'], est_m=e, cota_tn=s['eg_eixo'], greide=zg, terrapl=zt,
                    h_eixo=float(s['eg_eixo'] - p.LIMPEZA - zt),
                    off_esq=s['off_esq'], tipo_esq=s['tipo_esq'], cota_pe_esq=cota(-s['off_esq']),
                    off_dir=s['off_dir'], tipo_dir=s['tipo_dir'], cota_pe_dir=cota(s['off_dir']),
                    pontos=pts, vol_c=l['vol_c'], vol_a=l['vol_a']))
json.dump(out, open(os.path.join(AQUI, 'dados', 'nota_servico.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)


def br(v, d=3):
    return f'{v:.{d}f}'.replace('.', ',')


def nome(off):
    return 'eixo' if off == 0 else f"{'+' if off > 0 else '−'}{br(abs(off), 1)}"


os.makedirs(os.path.join(AQUI, 'Tabelas'), exist_ok=True)
with open(os.path.join(AQUI, 'Tabelas', 'nota_servico.csv'), 'w', newline='', encoding='utf-8-sig') as fh:
    w = csv.writer(fh, delimiter=';')
    cab = ['estaca', 'ponto', 'cota TN eixo (m)', 'greide acabado (m)', 'greide terraplenagem (m)', 'h eixo (+corte/-aterro) (m)',
           'offset esq. (m)', 'tipo esq.', 'cota pé esq. (m)', 'offset dir. (m)', 'tipo dir.', 'cota pé dir. (m)']
    for off in PONTOS:
        if off != 0:
            cab += [f'{nome(off)} cota TN (m)', f'{nome(off)} cota projeto (m)', f'{nome(off)} h (m)']
    cab += ['volume corte (m³)', 'volume aterro geom. (m³)']
    w.writerow(cab)
    for r in out:
        lin = [r['estaca'], r['ponto'], *(br(r[k]) for k in ('cota_tn', 'greide', 'terrapl', 'h_eixo', 'off_esq')),
               r['tipo_esq'], br(r['cota_pe_esq']), br(r['off_dir']), r['tipo_dir'], br(r['cota_pe_dir'])]
        for q in r['pontos']:
            if q['off'] != 0:
                lin += [br(q['tn']), br(q['proj']), br(q['h'])]
        lin += [br(r['vol_c'] or 0, 1), br(r['vol_a'] or 0, 1)]
        w.writerow(lin)
r = out[52]
print('nota de serviço:', len(out), 'estacas; ex. 52:', r['estaca'], 'h nos pontos', [round(q['h'], 2) for q in r['pontos']],
      'Δ projeto', [round(q['proj'] - r['terrapl'], 3) for q in r['pontos']], 'Vc', round(r['vol_c']), 'Va', round(r['vol_a']))
