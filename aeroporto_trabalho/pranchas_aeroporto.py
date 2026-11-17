"""Pranchas A3 do aeroporto (PDF vetorial, imagem de fundo na planta): planta geral, perfil longitudinal,
seções transversais e diagrama de Brückner com o quadro de volumes. Sítio C1, PPD 06/24.
Uso: PYTHONUTF8=1 python pranchas_aeroporto.py [../Pranchas_aeroporto_PPD.pdf]"""
import json
import os
import sys
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle, Polygon, FancyArrow
from matplotlib.tri import Triangulation
import projeto as p

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, '..', 'Pranchas_aeroporto_PPD.pdf')
NAVY = '#33335B'; ARD = '#273348'; CORTE = '#147699'; ATERRO = '#6B6990'; TN = '#8A8A8A'; LAV = '#9F9DB6'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8, 'axes.edgecolor': '#555', 'pdf.fonttype': 42})
GRUPO = 'Pedro Feitosa Guttemberg · Guilherme Rodrigues · Gilberto Patri'
W, H = 16.54, 11.69   # A3 paisagem (pol)
NF = 5

M = json.load(open(os.path.join(AQUI, 'dados', 'memorial.json'), encoding='utf-8'))
C3 = json.load(open(os.path.join(AQUI, 'dados', 'areas_civil3d.json'), encoding='utf-8'))['por_estaca']
PJ = json.load(open(os.path.join(AQUI, 'civil3d', 'projeto.json'), encoding='utf-8'))
PV = M['pvis']; CV = p.curvas(PV)
LIN = M['linhas']
EST = np.array([l['est_m'] for l in LIN])
AC = np.array([C3[str(round(e, 3)) if str(round(e, 3)) in C3 else str(float(e))]['ac'] for e in EST])
AA = np.array([C3[str(round(e, 3)) if str(round(e, 3)) in C3 else str(float(e))]['aa'] for e in EST])
DLE = np.array([C3[str(float(e))]['dl_esq'] for e in EST]); DLD = np.array([C3[str(float(e))]['dl_dir'] for e in EST])
d = np.diff(EST)
VC = np.r_[0, d * (AC[1:] + AC[:-1]) / 2]; VA = np.r_[0, d * (AA[1:] + AA[:-1]) / 2]
ORD = np.cumsum(VC - p.FH * VA)
LIMP = 92401.0   # limpeza (Civil 3D), m³
COR = dict(Vc=435037.0, Va_corr=442740.0)   # corredor (Relatório de volume do Civil 3D, 16/11/2026)


def folha(n, titulo, sub, escala):
    fig = plt.figure(figsize=(W, H))
    fig.add_artist(Rectangle((0.012, 0.015), 0.976, 0.97, fill=False, lw=1.2, ec=NAVY, transform=fig.transFigure))
    x0, y0, w, h = 0.69, 0.015, 0.298, 0.135
    fig.add_artist(Rectangle((x0, y0), w, h, fill=True, fc='white', lw=1.0, ec=NAVY, transform=fig.transFigure, zorder=5))
    for yy in (y0 + 0.095, y0 + 0.058, y0 + 0.028):
        fig.add_artist(plt.Line2D([x0, x0 + w], [yy, yy], lw=0.6, color=NAVY, transform=fig.transFigure, zorder=6))
    kw = dict(color=NAVY, zorder=7)
    fig.text(x0 + 0.006, y0 + 0.118, 'ITA · GEO-55 Projeto e Construção de Pistas · Exame 2026', fontsize=8, **kw)
    fig.text(x0 + 0.006, y0 + 0.101, 'Aeroporto em Pindamonhangaba-SP · sítio C1 · PPD 06/24, 1900 × 45 m', fontsize=8, **kw)
    fig.text(x0 + 0.006, y0 + 0.070, f'{n:02d} · {titulo}', fontsize=12, weight='bold', **kw)
    fig.text(x0 + 0.006, y0 + 0.040, GRUPO, fontsize=7, **kw)
    fig.text(x0 + 0.006, y0 + 0.016, f'Escala: {escala}   ·   folha {n}/{NF}   ·   17/11/2026', fontsize=6.5, **kw)
    fig.text(x0 + 0.006, y0 + 0.004, 'SIRGAS 2000 / UTM 23S; cotas em metros (Copernicus GLO-30)', fontsize=6.5, **kw)
    fig.text(0.025, 0.955, f'{n:02d} · {titulo.upper()}', fontsize=15, weight='bold', color=NAVY)
    fig.text(0.025, 0.93, sub, fontsize=9, color='#333')
    return fig


def contorno(ax, x, y, **kw):
    ax.plot(np.r_[x, x[:1]], np.r_[y, y[:1]], **kw)


with PdfPages(SAIDA) as pdf:
    # ------------------------------------------------------------------ 01 planta geral
    fig = folha(1, 'Planta geral', 'Faixa de pista 2020 × 300 m nivelada, PPD 1900 × 45 m, pés de talude (Civil 3D), estacas a cada 100 m e curvas de nível a cada 1 m.',
                '1:10.000 (A3)')
    ax = fig.add_axes([0.03, 0.06, 0.64, 0.86])
    im = plt.imread(os.path.join(AQUI, 'civil3d', 'imagem_sitio_utm23s.jpg'))
    g = PJ['img']
    cx, cy = PJ['centro']; hx, hy = 1345, 760
    ax.imshow(im, extent=(g['x0'], g['x1'], g['y0'], g['y1']), alpha=0.55, interpolation='bilinear', zorder=0)
    T = np.load(os.path.join(AQUI, 'dados', 'pontos_terreno.npy'))
    m = (np.abs(T[:, 0] - cx) < hx + 200) & (np.abs(T[:, 1] - cy) < hy + 200)
    tri = Triangulation(T[m, 0], T[m, 1])
    tt = tri.triangles; xx, yy = T[m, 0][tt], T[m, 1][tt]
    lado = np.max(np.hypot(xx - np.roll(xx, 1, axis=1), yy - np.roll(yy, 1, axis=1)), axis=1)
    tri.set_mask(lado > 120)   # sem triângulos longos na borda do recorte (eram a linha reta espúria)
    z0, z1 = np.floor(T[m, 2].min()), np.ceil(T[m, 2].max())
    ax.tricontour(tri, T[m, 2], levels=np.arange(z0, z1, 1.0), colors='#4A4A4A', linewidths=0.25, alpha=0.6, zorder=1)
    cs = ax.tricontour(tri, T[m, 2], levels=np.arange(np.ceil(z0 / 5) * 5, z1, 5.0), colors='#222', linewidths=0.6, zorder=1)
    ax.clabel(cs, fmt='%d', fontsize=6, colors='#222')
    # faixa e PPD
    xs, ys = p.xy(np.array([0, p.COMP, p.COMP, 0]), np.array([-150, -150, 150, 150]))
    contorno(ax, xs, ys, color=NAVY, lw=1.2, zorder=3)
    xs, ys = p.xy(np.array([60, 1960, 1960, 60]), np.array([-22.5, -22.5, 22.5, 22.5]))
    ax.fill(xs, ys, color=NAVY, alpha=0.35, lw=0, zorder=3); contorno(ax, xs, ys, color=NAVY, lw=0.8, zorder=3)
    xs, ys = p.xy(np.array([60, 1960, 1960, 60]), np.array([-30, -30, 30, 30]))
    contorno(ax, xs, ys, color=NAVY, lw=0.5, ls='--', zorder=3)
    # pés de talude
    for dl, lab in ((DLE, 'pé de talude'), (DLD, None)):
        xs, ys = p.xy(EST, dl)
        ax.plot(xs, ys, color='#2E8B57', lw=1.0, zorder=3, label=lab)
    # eixo e estacas
    xs, ys = p.xy(np.array([0, p.COMP]), np.zeros(2)); ax.plot(xs, ys, color='#C0392B', lw=0.8, ls='-.', zorder=4, label='eixo (EIXO PPD 06-24)')
    for e in np.arange(0, p.COMP + 1, 100):
        xa, ya = p.xy(np.array([e, e]), np.array([-8, 8])); ax.plot(xa, ya, color='#C0392B', lw=0.8, zorder=4)
        xt, yt = p.xy(e, -175)
        ax.text(xt, yt, f'{int(e // 20)}', fontsize=6, rotation=p.RUMO * 0 + 30, ha='center', va='center', color='#C0392B', zorder=4)
    for e, nome in ((60, 'CAB 06'), (1960, 'CAB 24')):
        xa, ya = p.xy(np.array([e, e]), np.array([-22.5, 22.5])); ax.plot(xa, ya, color='white', lw=2.0, zorder=4)
        xt, yt = p.xy(e, 50); ax.text(xt, yt, nome, fontsize=7, weight='bold', color=NAVY, ha='center', zorder=4, rotation=30,
                                      bbox=dict(fc='white', ec='none', alpha=0.8, pad=1))
    for nm, e in (('P0', 0), ('PF', p.COMP)):
        xt, yt = p.xy(e, 0); ax.plot(xt, yt, 'o', ms=4, color='#C0392B', zorder=5)
        ax.annotate(f'{nm}\nE {xt:,.1f}\nN {yt:,.1f}'.replace(',', ' '), (xt, yt), xytext=(-60 if e == 0 else 15, -40 if e == 0 else 10),
                    textcoords='offset points', fontsize=6.5, color=ARD, bbox=dict(fc='white', ec=NAVY, lw=0.5, pad=2), zorder=6)
    ax.set_xlim(cx - hx, cx + hx); ax.set_ylim(cy - hy, cy + hy); ax.set_aspect('equal')
    ax.ticklabel_format(useOffset=False, style='plain'); ax.tick_params(labelsize=6); ax.grid(color='white', lw=0.3, alpha=0.6)
    ax.legend(loc='lower left', fontsize=7, framealpha=0.9)
    # norte e notas
    ax.annotate('', xy=(cx - hx + 120, cy + hy - 60), xytext=(cx - hx + 120, cy + hy - 220), arrowprops=dict(arrowstyle='-|>', color=NAVY, lw=1.5))
    ax.text(cx - hx + 120, cy + hy - 45, 'N', ha='center', fontsize=11, weight='bold', color=NAVY)
    nt = fig.add_axes([0.69, 0.17, 0.298, 0.75]); nt.axis('off')
    txt = ('ELEMENTOS DO PROJETO\n\n'
           f'Centro do sítio: −22,8885; −45,4874\n'
           f'Rumo do eixo: 060° (cabeceiras 06/24)\n'
           f'Faixa de pista: 2020 × 300 m (estacas 0 a 101)\n'
           f'PPD: 1900 × 45 m, cabeceira 06 na estaca 3\n   e 24 na estaca 98; acostamentos 7,5 m\n\n'
           'SEÇÃO-TIPO\n'
           'PPD ±22,5 m a −1,5%; pavimento 1,10 m\n'
           'Acostamento 7,5 m a −2,5%; pavimento 0,50 m\n'
           'Faixa até ±150 m a −2,5%, sem pavimento\n'
           'Taludes: corte 1V:1,5H; aterro 1V:2H\n\n'
           'TERRAPLENAGEM\n'
           'Limpeza de 0,15 m em toda a área; aterro\n   sobre o terreno limpo\n'
           f'Fh = {p.FH:.2f} (adotado; Tremembé e aluvião)'.replace('.', ',') + '\n'
           'Volumes pelas áreas médias, 104 seções\n   (Civil 3D, linhas "SL - PPD")\n\n'
           'LEGENDA\n'
           'Contorno azul: faixa de pista nivelada\n'
           'Preenchido: PPD; tracejado: acostamentos\n'
           'Verde: pés de talude (offset do Civil 3D)\n'
           'Vermelho: eixo e estacas (número a cada 100 m)\n'
           'Curvas de nível: 1 m (finas) e 5 m (grossas)\n'
           'Imagem: mosaico georreferenciado do sítio')
    nt.text(0.03, 0.98, txt, va='top', fontsize=8.5, color=ARD, linespacing=1.45, family='DejaVu Sans')
    pdf.savefig(fig); plt.close(fig)

    # ------------------------------------------------------------------ 02 perfil longitudinal
    fig = folha(2, 'Perfil longitudinal', 'Terreno natural no eixo, greide acabado (topo do pavimento) e greide de terraplenagem (−1,10 m). Exagero vertical 20×.',
                'H 1:10.000 · V 1:500 (A3)')
    ax = fig.add_axes([0.14, 0.36, 0.83, 0.53])
    e = np.linspace(0, p.COMP, 2021)
    zg = p.greide(PV, e)
    ztn = np.array([l['cota_tn'] for l in LIN])
    ax.plot(EST, ztn, color=TN, lw=1.2, label='terreno natural (eixo)')
    ax.plot(e, zg, color=NAVY, lw=1.6, label='greide acabado')
    ax.plot(e, zg - p.H_PPD, color=NAVY, lw=0.8, ls='--', label='greide de terraplenagem (−1,10 m)')
    zi = np.interp(EST, e, zg - p.H_PPD)
    ax.fill_between(EST, ztn, zi, where=ztn > zi, color=CORTE, alpha=0.35, lw=0, label='corte no eixo')
    ax.fill_between(EST, ztn, zi, where=ztn < zi, color=ATERRO, alpha=0.35, lw=0, label='aterro no eixo')
    ylo, yhi = 534, 546
    for k, (ep, zp, L) in enumerate(PV):
        ax.plot(ep, zp, 'v', color='#C0392B', ms=6)
        txt = f'PIV{k}\nest. {ep / 20:.0f}\n' + f'{zp:.2f}'.replace('.', ',') + ' m' + (f'\nL = {L:.0f} m' if L else '')
        ax.annotate(txt, (ep, zp), xytext=(0, 18), textcoords='offset points', ha='center', fontsize=6.5, color='#C0392B')
    for c in CV:
        for x, nm in ((c['pcv'], f"PCV{c['n']}"), (c['ptv'], f"PTV{c['n']}")):
            ax.axvline(x, color='#C0392B', lw=0.4, ls=':'); ax.text(x, ylo + 0.3, nm, rotation=90, fontsize=6, color='#C0392B', va='bottom', ha='right')
    for k in range(len(PV) - 1):
        xm = (PV[k][0] + PV[k + 1][0]) / 2; gk = (PV[k + 1][1] - PV[k][1]) / (PV[k + 1][0] - PV[k][0])
        ax.text(xm, np.interp(xm, e, zg) - 1.6, f'{100 * gk:+.3f}%'.replace('.', ','), ha='center', fontsize=7.5, color=NAVY, weight='bold')
    for x, nm in ((60, 'CAB 06'), (1960, 'CAB 24')):
        ax.axvline(x, color=NAVY, lw=0.6); ax.text(x, yhi - 0.4, nm, ha='center', va='top', fontsize=7, weight='bold', color=NAVY,
                                                   bbox=dict(fc='white', ec='none', pad=1))
    ax.set_xlim(0, p.COMP); ax.set_ylim(ylo, yhi)
    ax.set_xticks(np.arange(0, p.COMP + 1, 100)); ax.set_xticklabels([f'{int(x // 20)}' for x in np.arange(0, p.COMP + 1, 100)], fontsize=7)
    ax.set_xlabel('estaca (20 m)'); ax.set_ylabel('cota (m)'); ax.grid(color='#E5E5E5', lw=0.4); ax.legend(loc='upper center', ncol=5, fontsize=7)
    # faixa de cotas
    tb = fig.add_axes([0.14, 0.17, 0.83, 0.15]); tb.axis('off'); tb.set_xlim(0, p.COMP); tb.set_ylim(0, 4)
    for r, (nome, vals) in enumerate((('Estaca', [f'{int(x // 20)}' for x in np.arange(0, p.COMP + 1, 100)]),
                                      ('Cota TN (m)', [f'{np.interp(x, EST, ztn):.2f}' for x in np.arange(0, p.COMP + 1, 100)]),
                                      ('Greide acabado (m)', [f'{np.interp(x, e, zg):.2f}' for x in np.arange(0, p.COMP + 1, 100)]),
                                      ('Corte(+)/aterro(−) no eixo (m)', [f'{np.interp(x, EST, ztn) - np.interp(x, e, zg - p.H_PPD):+.2f}' for x in np.arange(0, p.COMP + 1, 100)]))):
        yy = 3.5 - r
        tb.text(-55, yy, nome, ha='right', va='center', fontsize=7, color=NAVY, weight='bold')
        for x, v in zip(np.arange(0, p.COMP + 1, 100), vals):
            tb.text(x, yy, v.replace('.', ','), ha='center', va='center', fontsize=6.5, rotation=0 if r == 0 else 90 if False else 0, color=ARD)
        tb.axhline(yy - 0.5, color='#CCC', lw=0.4)
    fig.text(0.06, 0.155, 'Rampa máx. 0,28% (limite 1,5%); declividade efetiva 0,06% (limite 1,0%); mudança máx. de declividade 0,49% (limite 1,5%); '
                         'curvas verticais com R ≥ 30.000 m (código 4).', fontsize=7.5, color=ARD)
    pdf.savefig(fig); plt.close(fig)

    # ------------------------------------------------------------------ 03 seção-tipo cotada
    fig = folha(3, 'Seção-tipo', 'Seção transversal típica da faixa de pista (simétrica). Em cima, a seção inteira (exagero vertical 20×); embaixo, o detalhe da PPD, '
                'do acostamento e do início da faixa (exagero 5×). Terraplenagem medida no topo do subleito.', 'indicada nos desenhos (A3)')
    zg0 = 0.0
    o = np.linspace(-150, 150, 3001)
    acab = p.secao_acabada(zg0, o); terr = p.secao_terraplenagem(zg0, o)
    z150 = p.secao_terraplenagem(zg0, np.array([150.0]))[0]
    # (a) seção inteira
    ax = fig.add_axes([0.05, 0.56, 0.90, 0.33])
    ax.fill_between(o, terr, acab, where=np.abs(o) <= 30, color='#C9C6D8', lw=0, label='pavimento')
    ax.plot(o, acab, color='#C0392B', lw=1.0, label='superfície acabada')
    ax.plot(o, terr, color=NAVY, lw=1.4, label='plataforma de terraplenagem (topo do subleito)')
    hc, ha = 4.0, 4.0
    ax.plot([-150, -150 - p.TALUDE_CORTE * hc], [z150, z150 + hc], color=CORTE, lw=1.6, label='talude de corte 1V:1,5H')
    ax.plot([150, 150 + p.TALUDE_ATERRO * ha], [z150, z150 - ha], color=ATERRO, lw=1.6, label='talude de aterro 1V:2H')
    ax.axvline(0, color='#888', lw=0.6, ls='-.')
    ax.text(0, 0.7, 'eixo', ha='center', fontsize=8, color='#555')
    for x0, x1, t in ((-150, -30, 'faixa 120,00 m · 2,5%'), (-30, -22.5, ''), (-22.5, 22.5, 'PPD 45,00 m · 1,5% para cada lado'), (22.5, 30, ''), (30, 150, 'faixa 120,00 m · 2,5%')):
        ax.annotate('', xy=(x0, 1.6), xytext=(x1, 1.6), arrowprops=dict(arrowstyle='<->', color=NAVY, lw=0.7))
        if t: ax.text((x0 + x1) / 2, 1.85, t, ha='center', fontsize=8, color=NAVY)
    ax.text(-26.25, 2.3, 'acost.\n7,50', ha='center', fontsize=7, color=NAVY); ax.text(26.25, 2.3, 'acost.\n7,50', ha='center', fontsize=7, color=NAVY)
    ax.annotate('', xy=(-150, 3.6), xytext=(150, 3.6), arrowprops=dict(arrowstyle='<->', color=NAVY, lw=0.9))
    ax.text(0, 3.85, 'faixa de pista nivelada: 300,00 m', ha='center', fontsize=9, weight='bold', color=NAVY)
    ax.text(-158, z150 + 2.4, 'corte\n1V:1,5H', ha='right', fontsize=8, color=CORTE); ax.text(160, z150 - 2.8, 'aterro\n1V:2H', ha='left', fontsize=8, color=ATERRO)
    ax.set_xlim(-175, 175); ax.set_ylim(-8, 4.6); ax.set_xlabel('afastamento do eixo (m)'); ax.set_ylabel('cota relativa ao eixo (m)')
    ax.grid(color='#EEE', lw=0.4); ax.legend(loc='lower center', ncol=3, fontsize=7.5, framealpha=0.95)
    # (b) detalhe
    ax = fig.add_axes([0.05, 0.19, 0.60, 0.31])
    od = np.linspace(-2, 42, 2001)
    a2 = p.secao_acabada(zg0, od); t2 = p.secao_terraplenagem(zg0, od)
    ax.fill_between(od, t2, a2, where=od <= 30, color='#C9C6D8', lw=0)
    ax.plot(od, a2, color='#C0392B', lw=1.2); ax.plot(od, t2, color=NAVY, lw=1.6)
    for x, txt in ((11.25, 'pavimento da PPD\n1,10 m'), (26.25, 'pav. acost.\n0,50 m')):
        ax.text(x, float(np.interp(x, od, (a2 + t2) / 2)), txt, ha='center', va='center', fontsize=8, color=NAVY)
    for x in (0, 22.5, 30):
        ax.axvline(x, color='#AAA', lw=0.5, ls=':')
    ax.text(0.3, 0.25, 'eixo', fontsize=7.5, color='#555'); ax.text(22.7, 0.25, 'borda da PPD', fontsize=7.5, color='#555'); ax.text(30.2, 0.25, 'borda do acostamento', fontsize=7.5, color='#555')
    ax.text(11.25, 0.05, '−1,5%', ha='center', fontsize=9, color='#C0392B', weight='bold'); ax.text(26.25, -0.25, '−2,5%', ha='center', fontsize=9, color='#C0392B', weight='bold')
    ax.text(37, -0.6, '−2,5% (faixa, sem pavimento)', ha='center', fontsize=8, color=NAVY)
    ax.set_xlim(-2, 42); ax.set_ylim(-2.0, 0.6); ax.set_xlabel('afastamento do eixo (m)'); ax.set_ylabel('cota relativa ao eixo (m)'); ax.grid(color='#EEE', lw=0.4)
    nt = fig.add_axes([0.68, 0.19, 0.30, 0.31]); nt.axis('off')
    nt.text(0.02, 0.98, 'NOTAS\n\n'
            '1. Cotas relativas ao greide acabado no eixo.\n'
            '2. Pavimento (estrutura) fora do volume de\n    terraplenagem: os volumes vão até o topo\n    do subleito (aula 7).\n'
            '3. Taludes adotados (o enunciado não os dá):\n    corte 1V:1,5H; aterro 1V:2H, até o\n    terreno limpo (0,15 m de camada vegetal\n    removida em toda a largura).\n'
            '4. Aterro nunca sobre a camada vegetal.\n'
            '5. Declividades: enunciado do trabalho\n    (PPD 1,5%; acostamento e faixa 2,5%).\n'
            '6. Montagem "PPD 06-24" no DWG com as\n    mesmas medidas (corredor de verificação).',
            va='top', fontsize=8.5, color=ARD, linespacing=1.4)
    pdf.savefig(fig); plt.close(fig)

    # ------------------------------------------------------------------ 04 seções transversais
    sel = [100, 300, 520, 700, 900, 1040, 1060, 1200, 1400, 1600, 1720, 1860]
    fig = folha(4, 'Seções transversais', 'Seções-tipo nas estacas indicadas: terreno natural, plataforma de terraplenagem e taludes. Áreas do Civil 3D (memorial). '
                'Exagero vertical 10×.', 'H 1:3.000 · V 1:300 (A3)')
    for i, est in enumerate(sel):
        r, c = divmod(i, 4)
        ax = fig.add_axes([0.04 + c * 0.237, 0.68 - r * 0.225, 0.215, 0.185])
        k = int(np.argmin(np.abs(EST - est)))
        zgi = float(p.greide(PV, est)); s = p.secao(est, zgi, p.eg_secao(est))
        ax.plot(p.OFF, s['eg'], color=TN, lw=0.8)
        ax.plot(p.OFF, s['eg'] - p.LIMPEZA, color=TN, lw=0.4, ls=':')
        ax.plot(p.OFF, s['proj'], color=NAVY, lw=1.0)
        base = s['eg'] - p.LIMPEZA; pr = s['proj']; ok = ~np.isnan(pr)
        ax.fill_between(p.OFF, base, pr, where=ok & (base > pr), color=CORTE, alpha=0.45, lw=0)
        ax.fill_between(p.OFF, base, pr, where=ok & (base < pr), color=ATERRO, alpha=0.45, lw=0)
        ax.plot(p.OFF, p.secao_acabada(zgi, p.OFF) * np.where(np.abs(p.OFF) <= 30, 1, np.nan), color='#C0392B', lw=0.6)
        zc = np.nanmean(pr[np.abs(p.OFF) < 150])
        ax.set_xlim(-185, 185); ax.set_ylim(zc - 10.5, zc + 10.5)
        ax.tick_params(labelsize=5.5); ax.grid(color='#EEE', lw=0.3)
        lab = LIN[k]['estaca'] + (f" ({LIN[k]['ponto']})" if LIN[k]['ponto'] else '')
        ax.set_title(f'Est. {lab} · greide ' + f'{zgi:.2f}'.replace('.', ',') + ' m', fontsize=7.5, color=NAVY, loc='left')
        ax.text(0.99, 0.04, f'Ac = {AC[k]:.1f} m²\nAa = {AA[k]:.1f} m²'.replace('.', ','), transform=ax.transAxes, ha='right', va='bottom',
                fontsize=6.5, color=ARD, bbox=dict(fc='white', ec='#CCC', lw=0.4, pad=1.5))
    fig.text(0.04, 0.205, 'Legenda: cinza = terreno natural (pontilhado: após limpeza de 0,15 m); azul-escuro = plataforma de terraplenagem e taludes; '
                         'vermelho = superfície acabada (pavimento) da PPD e acostamentos;', fontsize=7.5, color=ARD)
    fig.text(0.04, 0.185, 'azul = corte; lilás = aterro. Afastamentos em m (+ à direita, sentido SE).', fontsize=7.5, color=ARD)
    fig.text(0.04, 0.165, 'As 104 seções completas estão no DWG (grupo "SL - PPD", vistas de seção) e as áreas de todas elas na planilha (aba Memorial).',
             fontsize=7.5, color=ARD)
    pdf.savefig(fig); plt.close(fig)

    # ------------------------------------------------------------------ 04 Brückner e quadro de volumes
    fig = folha(5, 'Diagrama de Brückner e volumes', f'Ordenada = Σ(Vc − Fh·Va), Fh = {p.FH:.2f}'.replace('.', ',') + ', áreas médias com as seções do Civil 3D. '
                'Distribuição adotada: compensar tudo com 2 LCs.', 'H 1:10.000 (A3)')
    ax = fig.add_axes([0.06, 0.40, 0.90, 0.48])
    ax.plot(EST, ORD / 1000, color=NAVY, lw=1.5)
    ax.fill_between(EST, 0, ORD / 1000, where=ORD >= 0, color=CORTE, alpha=0.2, lw=0)
    ax.fill_between(EST, 0, ORD / 1000, where=ORD < 0, color=ATERRO, alpha=0.2, lw=0)
    ax.axhline(0, color='#555', lw=0.6)
    ax.set_xlim(0, p.COMP); ax.set_xticks(np.arange(0, p.COMP + 1, 100)); ax.set_xticklabels([f'{int(x // 20)}' for x in np.arange(0, p.COMP + 1, 100)], fontsize=7)
    ax.set_xlabel('estaca (20 m)'); ax.set_ylabel('ordenada de Brückner (mil m³)'); ax.grid(color='#E5E5E5', lw=0.4)
    kmax = int(np.argmax(ORD)); ax.annotate(f'máx. {ORD[kmax] / 1000:.1f} mil m³ (est. {LIN[kmax]["estaca"]})'.replace('.', ',', 1), (EST[kmax], ORD[kmax] / 1000),
                                            xytext=(10, 8), textcoords='offset points', fontsize=7.5, color=NAVY)
    ax.annotate(f'final {ORD[-1]:+,.0f} m³'.replace(',', '.'), (EST[-1], ORD[-1] / 1000), xytext=(-90, 12), textcoords='offset points', fontsize=7.5, color=NAVY)
    Vc, Va = VC.sum(), VA.sum()
    tb = fig.add_axes([0.06, 0.17, 0.60, 0.18]); tb.axis('off')
    linhas = [('Quantidade', 'Memorial (seções da plataforma)', 'Verificação: corredor'),
              ('Corte (m³)', f'{Vc:,.0f}', f"{COR['Vc']:,.0f}"),
              ('Aterro (m³)', f'{Va:,.0f}', f"{COR['Va_corr'] / p.FH:,.0f}"),
              (f'Aterro corrigido × {p.FH:.2f} (m³)'.replace('.', ','), f'{p.FH * Va:,.0f}', f"{COR['Va_corr']:,.0f}"),
              ('Saldo: bota-fora (+) / empréstimo (−) (m³)', f'{Vc - p.FH * Va:+,.0f}', f"{COR['Vc'] - COR['Va_corr']:+,.0f}"),
              ('Limpeza 0,15 m, bota-fora/estoque (m³)', f'{LIMP:,.0f}', '—')]
    t = tb.table(cellText=[[a, b.replace(',', '.'), c.replace(',', '.')] for a, b, c in linhas[1:]], colLabels=linhas[0], loc='upper left',
                 cellLoc='center', colWidths=[0.45, 0.28, 0.27])
    t.auto_set_font_size(False); t.set_fontsize(8.5); t.scale(1, 1.5)
    for (r, c), cell in t.get_celld().items():
        cell.set_edgecolor('#BBB')
        if r == 0:
            cell.set_facecolor(NAVY); cell.set_text_props(color='white', weight='bold')
        if c == 0 and r > 0:
            cell.set_text_props(ha='left'); cell._loc = 'left'
    fig.text(0.06, 0.155, 'Distribuição (programa diagrama_massas, aula 8): 2 LCs, MT = 6,61 × 10⁶ m³·dam; onda principal de 79 mil m³ com DMT de 745 m '
                         '(moto-scraper, SICRO 5501714). Corredor: Relatório de volume do Civil 3D (16/11/2026); o memorial é a base do Brückner.',
             fontsize=7.5, color=ARD)
    pdf.savefig(fig); plt.close(fig)
print('pranchas:', os.path.abspath(SAIDA), f'| Vc {VC.sum():,.0f}  Va {VA.sum():,.0f}  ordenada final {ORD[-1]:+,.0f}')
