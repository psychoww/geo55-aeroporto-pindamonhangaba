"""Gera explicacao/index.html (artefato explicativo) a partir de modelo.html e dos resultados do projeto.
Uso (na pasta aeroporto_trabalho): python explicacao/gerar.py"""
import json
import os
import shutil
import numpy as np
import projeto as p

AQUI = os.path.dirname(os.path.abspath(__file__))
M = json.load(open('dados/memorial.json'))
C3 = json.load(open('dados/areas_civil3d.json'))
R = json.load(open('dados/distribuicao.json', encoding='utf-8'))


def br(v, d=0):
    return f'{v:,.{d}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def lista(v):
    return v if isinstance(v, list) else ([] if v is None else [v])


def lcs(S):
    return S if (S and isinstance(S[0], list)) else ([S] if S else [])


lin = M['linhas']
est = np.array([l['est_m'] for l in lin])
ac = np.array([round(C3['por_estaca'][str(round(x, 3))]['ac'], 2) for x in est])
aa = np.array([round(C3['por_estaca'][str(round(x, 3))]['aa'], 2) for x in est])
d = np.diff(est)
vc = d * (ac[1:] + ac[:-1]) / 2; va = d * (aa[1:] + aa[:-1]) / 2
Vc, Va = vc.sum(), va.sum(); VaC = p.FH * Va
CL = np.minimum(vc, p.FH * va).sum()
T = dict(M['totais'])
# limpeza como na planilha: largura entre pés de talude (Civil 3D) arredondada a 0,01 m
lw = np.array([round(C3['por_estaca'][str(round(x, 3))]['dl_dir'] - C3['por_estaca'][str(round(x, 3))]['dl_esq'], 2) for x in est])
T['Vl'] = float((p.LIMPEZA * d * (lw[1:] + lw[:-1]) / 2).sum())

pv = M['pvis']
e = np.array([x[0] for x in pv]); z = np.array([x[1] for x in pv]); g = np.diff(z) / np.diff(e)
piv = ''
for k, (ee, zz, L) in enumerate(pv):
    rampa = f'{g[k] * 100:+.3f}%'.replace('.', ',') if k < len(pv) - 1 else '—'
    piv += f'<tr><td>{k}</td><td class="n">{br(ee)}</td><td class="n">{br(zz, 3)}</td><td class="n">{br(L) if L else "—"}</td><td class="n">{rampa}</td></tr>\n    '
zr = p.greide([tuple(x) for x in pv], np.arange(60, 1960.1, 1.0))
efet = (zr.max() - zr.min()) / 1900 * 100

# par sugerido para a conta à mão (mesma regra da planilha)
par = next(i for i in range(1, len(lin)) if est[i] - est[i - 1] == 20 and min(ac[i - 1], aa[i - 1], ac[i], aa[i]) > 300)
par_lin = ''.join(f'<tr><td>{lin[i]["estaca"]}</td><td class="n">{br(ac[i], 2)}</td><td class="n">{br(aa[i], 2)}</td></tr>' for i in (par - 1, par))

nomes = {'eco_aula': 'Adotada: 1 LC do P0 ao PF (compensa tudo)', 'lc_unica': 'LC única entre cruzamentos (busca de LC única)',
         'ate_2_lcs': 'Até 2 LCs', 'ate_3_lcs': 'Até 3 LCs', 'livre': 'LCs livres: ótimo do modelo da aula (6 LCs)'}
cen = ''
for k in ['eco_aula', 'lc_unica', 'ate_2_lcs', 'ate_3_lcs', 'livre']:
    c = R['cenarios'][k]
    cls = ' class="rec"' if k == 'eco_aula' else ''
    cen += (f'<tr{cls}><td>{nomes[k]}</td><td class="n">{len(lcs(c["S"]))}</td><td class="n">{br(c["MT"] / 1e6, 2)}</td>'
            f'<td class="n">{br(c["Vbf"])}</td><td class="n">{br(c["Vemp"])}</td></tr>\n    ')
rec = R['cenarios']['eco_aula']
ondas = ''
for i, w in enumerate([w for w in lista(rec['ondas']) if w['V'] >= 1000], 1):
    sent = '→ sentido do estaqueamento' if w['sinal'] > 0 else '← sentido contrário'
    ondas += (f'<tr><td>{i}</td><td class="n">{br(w["ini"])}</td><td class="n">{br(w["fim"])}</td><td>{sent}</td>'
              f'<td class="n">{br(w["V"])}</td><td class="n">{br(w["DMT"])}</td></tr>\n    ')
liv = R['cenarios']['livre']

dif_c = (Vc / T['Vc'] - 1) * 100; dif_a = (Va / T['Va'] - 1) * 100
fh = f'{p.FH:.2f}'.replace('.', ',')
tok = {
    'FH': fh, 'VC': br(Vc), 'VA': br(Va), 'VACORR': br(VaC), 'SALDO': ('+' if Vc - VaC >= 0 else '') + br(Vc - VaC), 'VL': br(T['Vl']),
    'CL': br(CL), 'CLONG': br(Vc - CL), 'ALONG': br(VaC - CL), 'NSEC': str(len(lin)),
    'DIFC': f'{dif_c:+.2f}%'.replace('.', ','), 'DIFA': f'{dif_a:+.2f}%'.replace('.', ','),
    'PIVS': piv, 'EFETIVA': f'{efet:.2f}%'.replace('.', ','), 'DIMAX': f'{np.abs(np.diff(g)).max() * 100:.3f}%'.replace('.', ','),
    'PAR_A': lin[par - 1]['estaca'], 'PAR_B': lin[par]['estaca'], 'PAR_LINHAS': par_lin,
    'CENARIOS': cen, 'BF_LIVRE': br(liv['Vbf']), 'EMP_LIVRE': br(liv['Vemp']), 'BF_REC': br(rec['Vbf']), 'ONDAS': ondas,
}
s = open(os.path.join(AQUI, 'modelo.html'), encoding='utf-8').read()
for k, v in tok.items():
    s = s.replace(f'%%{k}%%', v)
assert '%%' not in s, s[s.index('%%') - 40:s.index('%%') + 40]
open(os.path.join(AQUI, 'index.html'), 'w', encoding='utf-8').write(s)
os.makedirs(os.path.join(AQUI, 'img'), exist_ok=True)
for f in ('06_secoes.png', '11_distribuicao.png'):
    shutil.copy(os.path.join('figuras', f), os.path.join(AQUI, 'img', f))
print('ok explicacao/index.html', {k: v for k, v in tok.items() if len(v) < 30})
