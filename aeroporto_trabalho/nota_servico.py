"""Nota de serviço de terraplenagem (aula 7): por estaca, cotas do terreno e do greide no eixo, altura de corte/aterro
no eixo e afastamentos/cotas dos pés de talude (offsets) dos dois lados, com o tipo (corte C ou aterro A).
Geometria do motor do projeto (mesmo terreno e seção-tipo do Civil 3D). Saída: dados/nota_servico.json e Tabelas/nota_servico.csv.
Uso: PYTHONUTF8=1 python nota_servico.py"""
import csv
import json
import os
import numpy as np
import projeto as p

AQUI = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(AQUI, 'dados', 'memorial.json'), encoding='utf-8'))
out = []
for l in M['linhas']:
    e = l['est_m']; zg = float(p.greide(M['pvis'], e))
    s = p.secao(e, zg, p.eg_secao(e))
    zt = p.secao_terraplenagem(zg, np.array([0.0]))[0]
    def cota(off):
        return float(np.interp(off, p.OFF, s['eg']))
    out.append(dict(estaca=l['estaca'], ponto=l['ponto'], est_m=e, cota_tn=s['eg_eixo'], greide=zg, terrapl=float(zt),
                    h_eixo=float(s['eg_eixo'] - p.LIMPEZA - zt),
                    off_esq=s['off_esq'], tipo_esq=s['tipo_esq'], cota_pe_esq=cota(-s['off_esq']),
                    off_dir=s['off_dir'], tipo_dir=s['tipo_dir'], cota_pe_dir=cota(s['off_dir'])))
json.dump(out, open(os.path.join(AQUI, 'dados', 'nota_servico.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
os.makedirs(os.path.join(AQUI, 'Tabelas'), exist_ok=True)
with open(os.path.join(AQUI, 'Tabelas', 'nota_servico.csv'), 'w', newline='', encoding='utf-8-sig') as fh:
    w = csv.writer(fh, delimiter=';')
    w.writerow(['estaca', 'ponto', 'cota TN eixo (m)', 'greide acabado (m)', 'greide terraplenagem (m)', 'h eixo (+corte/-aterro) (m)',
                'offset esq. (m)', 'tipo esq.', 'cota pé esq. (m)', 'offset dir. (m)', 'tipo dir.', 'cota pé dir. (m)'])
    for r in out:
        w.writerow([r['estaca'], r['ponto'], *(f'{r[k]:.3f}'.replace('.', ',') for k in ('cota_tn', 'greide', 'terrapl', 'h_eixo', 'off_esq')),
                    r['tipo_esq'], f"{r['cota_pe_esq']:.3f}".replace('.', ','), f"{r['off_dir']:.3f}".replace('.', ','), r['tipo_dir'],
                    f"{r['cota_pe_dir']:.3f}".replace('.', ',')])
print('nota de serviço:', len(out), 'estacas; ex. 52:', {k: (round(v, 3) if isinstance(v, float) else v) for k, v in out[52].items()})
