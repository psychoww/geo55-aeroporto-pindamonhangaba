"""Figuras da apresentação (PNG em figuras/). Paleta e fonte em paleta.py (identidade do modelo de advocacia):
corte = petróleo, aterro = lavanda escura, terreno = cinza, projeto = índigo; fundo marfim; fonte Spectral."""
import json
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
import projeto as p
import paleta
from paleta import CORTE, ATERRO, TN, INK, MUTED, VIOL, MARF, ALERTA, BEGE, BEGE_ESC, GRADE, SEQ
import ols
from dem import geo2utm

os.makedirs('figuras', exist_ok=True)
paleta.aplica()
M = json.load(open('dados/memorial.json'))
PV = [tuple(x) for x in M['pvis']]
C3 = json.load(open('dados/areas_civil3d.json'))['por_estaca']


def salva(fig, nome):
    fig.savefig(f'figuras/{nome}', bbox_inches='tight', facecolor=MARF); plt.close(fig); print('ok', nome)


# 1. Relevo regional + filtros da busca --------------------------------------
Z, X0, Y0, P = ols.Z, ols.X0, ols.Y0, ols.P
ls = LightSource(azdeg=315, altdeg=40)
fig, ax = plt.subplots(figsize=(11, 8))
ext = [X0 / 1000, (X0 + Z.shape[1] * P) / 1000, Y0 / 1000, (Y0 + Z.shape[0] * P) / 1000]
rgb = ls.shade(Z, cmap=plt.cm.bone, vert_exag=3, blend_mode='soft', vmin=480, vmax=1500)
ax.imshow(rgb, origin='lower', extent=ext)
for nome, (lo, la) in {'SBSJ': (-45.8711, -23.2292), 'SBTA': (-45.5158, -23.0389)}.items():
    x, y = geo2utm.transform(lo, la)
    ax.add_patch(plt.Circle((x / 1000, y / 1000), 10, fill=False, ls='--', color='white', lw=1.2))
    ax.plot(x / 1000, y / 1000, 'w^', ms=8); ax.annotate(nome + ' (raio 10 km)', (x / 1000, y / 1000), xytext=(6, 6), textcoords='offset points', color='white', fontsize=10, weight='bold')
_vx, _vy = geo2utm.transform(-45.8096, -23.1256)  # melhor ponto da 1ª rodada (só terraplenagem): várzea, descartado
for c, cor, rot in [(dict(x=_vx, y=_vy), ALERTA, '1ª rodada: várzea (descartada)')]:
    ax.plot(c['x'] / 1000, c['y'] / 1000, 'o', mfc='none', mec=cor, mew=2, ms=12)
    ax.annotate(rot, (c['x'] / 1000, c['y'] / 1000), xytext=(8, -14), textcoords='offset points', color='white', fontsize=10)
u = p.U; v = p.V
cs = np.array([np.array([p.XC, p.YC]) + a * u + b * v for a, b in [(-1500, -750), (1500, -750), (1500, 750), (-1500, 750), (-1500, -750)]])
ax.fill(cs[:, 0] / 1000, cs[:, 1] / 1000, color=CORTE, alpha=0.95)
ax.annotate('Sítio escolhido\nPPD 06/24', (p.XC / 1000, p.YC / 1000), xytext=(18, 18), textcoords='offset points', color='white', fontsize=12, weight='bold',
            arrowprops=dict(arrowstyle='-', color='white'))
for nome, (lo, la) in {'São José dos Campos': (-45.887, -23.180), 'Taubaté': (-45.556, -23.026), 'Pindamonhangaba': (-45.462, -22.924),
                       'Caçapava': (-45.708, -23.101), 'Jacareí': (-45.966, -23.305)}.items():
    x, y = geo2utm.transform(lo, la)
    ax.plot(x / 1000, y / 1000, 's', color='white', ms=4); ax.annotate(nome, (x / 1000, y / 1000), xytext=(5, -12), textcoords='offset points', color='white', fontsize=9)
ax.set_xlabel('E (km, UTM 23S)'); ax.set_ylabel('N (km)'); ax.set_title('Vale do Paraíba: relevo (Copernicus GLO-30) e área de busca')
ax.text(0.01, 0.01, 'Mantiqueira ao N e Serra do Mar ao S: só o eixo do vale (rumo 50–70°) deixa as OLS livres',
        transform=ax.transAxes, color='white', fontsize=9, va='bottom')
salva(fig, '01_regiao.png')

# 2. Rosa dos ventos -----------------------------------------------------------
d = json.load(open('dados/vento_era5.json'))
vv = np.array(d['hourly']['wind_speed_10m'], float); aa = np.array(d['hourly']['wind_direction_10m'], float)
m = ~np.isnan(vv); vv, aa = vv[m], aa[m]
fig = plt.figure(figsize=(6.5, 6.5)); ax = fig.add_subplot(projection='polar')
ax.set_theta_zero_location('N'); ax.set_theta_direction(-1)
bins = np.arange(-11.25, 360, 22.5)
cent = np.radians(np.arange(0, 360, 22.5)); larg = np.radians(22.5) * 0.9
base = np.zeros(16)
for (v0, v1), cor, rot in zip([(3, 6), (6, 10), (10, 99)], SEQ, ['3–6 kt', '6–10 kt', '> 10 kt']):
    sel = (vv >= v0) & (vv < v1)
    h, _ = np.histogram(np.mod(aa[sel] + 11.25, 360) - 11.25, bins=bins)
    h = h / vv.size * 100
    ax.bar(cent, h, width=larg, bottom=base, color=cor, edgecolor='white', lw=1, label=rot); base += h
for ang in (60, 240):
    ax.plot([np.radians(ang)] * 2, [0, base.max() * 1.1], color=CORTE, lw=3)
ax.text(np.radians(60), base.max() * 1.18, 'PPD 06/24', color=CORTE, ha='center', weight='bold')
ax.set_title(f'Vento a 10 m — ERA5 2015–2024 ({vv.size:,} h)\ncalmaria (< 3 kt): {(vv < 3).mean():.0%}'.replace(',', '.'), pad=18)
ax.legend(loc='lower left', bbox_to_anchor=(-0.12, -0.12), frameon=False, fontsize=9)
ax.set_yticklabels([f'{t:.0f}%' for t in ax.get_yticks()], fontsize=8, color=MUTED)
salva(fig, '02_vento.png')

# 3. Corte longitudinal das OLS ----------------------------------------------
s = np.arange(-16000, 16001, 30.0)
ze = None
X = p.XC + s * p.U[0]; Y = p.YC + s * p.U[1]
zt = ols.amostra(X, Y)
r = ols.verifica(p.XC, p.YC, p.RUMO, passo=90)
ze = r['ze']
sup = ols.superficie(s, np.zeros_like(s), ze)
fig, ax = plt.subplots(figsize=(12, 4.2))
ax.fill_between(s / 1000, 480, zt, color=BEGE)
ax.plot(s / 1000, zt, color=TN, lw=1, label='Terreno no prolongamento do eixo (DSM)')
ax.plot(s / 1000, sup, color=VIOL, lw=2, label='Superfícies limitadoras (aproximação 2% / 2,5%, faixa)')
ax.axvspan(-1.01, 1.01, ymax=0.42, color=CORTE, alpha=0.35, lw=0); ax.text(0, ze + 30, 'faixa', ha='center', color=MUTED)
ax.set_xlabel('Distância ao centro da pista ao longo do rumo 060° (km)'); ax.set_ylabel('Cota (m)')
ax.set_ylim(480, max(zt.max(), sup[np.isfinite(sup)].max()) + 40)
ax.set_title(f'Obstáculos: nenhuma penetração relevante (máx. {max(r["pen_max"], 0):.0f} m em {r["area_pen_ha"]:.0f} ha, provavelmente árvores)')
ax.legend(frameon=False, loc='upper center', fontsize=9)
ax.text(-15.8, 490, 'SW (cabeceira 06)', color=MUTED, fontsize=9); ax.text(15.8, 490, 'NE (cabeceira 24)', color=MUTED, fontsize=9, ha='right')
salva(fig, '03_ols.png')

# 4. Seção-tipo -----------------------------------------------------------------
def linhas_secao(o, zg=0.0):
    za = p.secao_acabada(zg, np.clip(o, -150, 150)); zt_ = p.secao_terraplenagem(zg, np.clip(o, -150, 150))
    z150 = p.secao_terraplenagem(zg, np.array([150.0]))[0]
    d_, e_ = o > 150, o < -150
    za = np.where(d_, z150 + (o - 150) / p.TALUDE_CORTE, np.where(e_, z150 - (-o - 150) / p.TALUDE_ATERRO, za))
    return za, np.where(d_ | e_, za, zt_)


fig, (a1, a2) = plt.subplots(2, 1, figsize=(13, 7.5), gridspec_kw=dict(height_ratios=[1, 1.1]))
o = np.linspace(-185, 185, 3001); za, zt_ = linhas_secao(o)
a1.plot(o, za, color=INK, lw=1.8)
a1.fill_between(o, za, -12, where=o < -150, color=ATERRO, alpha=0.18, lw=0); a1.fill_between(o, za, 12, where=o > 150, color=CORTE, alpha=0.18, lw=0)
for x_ in (-150, -30, -22.5, 0, 22.5, 30, 150):
    a1.axvline(x_, color=GRADE, lw=0.8, zorder=0)
a1.annotate('', xy=(-150, 1.2), xytext=(150, 1.2), arrowprops=dict(arrowstyle='<->', color=MUTED))
a1.text(-75, 1.6, 'faixa de pista 300 m', ha='center', color=MUTED, fontsize=10)
a1.text(-90, -1.9, '−2,5%', ha='center', fontsize=11, weight='bold'); a1.text(90, -1.9, '−2,5%', ha='center', fontsize=11, weight='bold')
a1.text(0, -3.2, 'PPD 45 m\n−1,5% ←|→ −1,5%', ha='center', fontsize=9)
a1.text(-172, -8, 'aterro\n1V:2H', ha='center', color=ATERRO, fontsize=10, weight='bold')
a1.text(172, 6, 'corte\n1V:1,5H', ha='center', color=CORTE, fontsize=10, weight='bold')
a1.set_ylim(-12, 12); a1.set_xlim(-185, 185); a1.set_ylabel('Cota rel. ao eixo (m)')
a1.set_title('Seção-tipo da faixa de pista (escala vertical exagerada ~8×)')
o = np.linspace(0, 42, 2001); za, zt_ = linhas_secao(o)
a2.fill_between(o, zt_, za, where=o <= 30.01, color=BEGE_ESC, lw=0, label='Pavimento (fora do volume de terraplenagem)')
a2.plot(o, za, color=INK, lw=2, label='Superfície acabada')
a2.plot(o, zt_, color=ATERRO, lw=2, ls='--', label='Plataforma de terraplenagem (topo do subleito)')
for x_, t in [(0, 'eixo'), (22.5, '22,5 m'), (30, '30,0 m')]:
    a2.axvline(x_, color=GRADE, lw=0.8, zorder=0); a2.text(x_, 0.25, t, ha='center', fontsize=9, color=MUTED)
a2.text(11.25, -0.75, 'PPD: −1,5%\npavimento 1,10 m', ha='center', fontsize=10)
a2.text(26.25, -0.95, 'acostamento 7,5 m\n−2,5%  pav. 0,50 m', ha='center', fontsize=9)
a2.text(36, -0.45, 'faixa\n−2,5%', ha='center', fontsize=9)
a2.set_xlim(-0.5, 42); a2.set_ylim(-1.9, 0.5); a2.set_xlabel('Afastamento do eixo (m)'); a2.set_ylabel('Cota rel. ao eixo (m)')
a2.set_title('Detalhe: PPD e acostamento (o volume é medido na plataforma de terraplenagem)')
a2.legend(frameon=False, loc='lower right', fontsize=9)
plt.tight_layout()
salva(fig, '04_secao_tipo.png')

# 5. Perfil longitudinal -------------------------------------------------------
e = np.arange(0, p.COMP + 0.1, 2.0)
fig, ax = plt.subplots(figsize=(13, 4.8))
zte = p.cota_terreno(e, 0 * e); zge = p.greide(PV, e)
ax.fill_between(e, zte, zge, where=zte >= zge, color=CORTE, alpha=0.25, lw=0, label='Corte (no eixo)')
ax.fill_between(e, zte, zge, where=zte < zge, color=ATERRO, alpha=0.25, lw=0, label='Aterro (no eixo)')
ax.plot(e, zte, color=TN, lw=1.4, label='Terreno natural no eixo')
ax.plot(e, zge, color=INK, lw=2, label='Greide (superfície acabada)')
for c in M['curvas']:
    for xx, t in [(c['pcv'], f"PCV{c['n']}"), (c['ptv'], f"PTV{c['n']}")]:
        ax.plot(xx, p.greide(PV, [xx])[0], 'o', color=INK, ms=4)
        ax.annotate(t, (xx, p.greide(PV, [xx])[0]), xytext=(0, 9), textcoords='offset points', ha='center', fontsize=8, color=MUTED)
ex = [q[0] for q in PV]; zz = [q[1] for q in PV]
ax.plot(ex, zz, ':', color=MUTED, lw=1)
for k in range(len(PV) - 1):
    g = (zz[k + 1] - zz[k]) / (ex[k + 1] - ex[k]) * 100
    ax.text((ex[k] + ex[k + 1]) / 2, max(zz[k], zz[k + 1]) + 1.6, f'{g:+.3f}%'.replace('.', ','), ha='center', fontsize=10, weight='bold')
for xx, t in [(60, 'CAB 06'), (1960, 'CAB 24')]:
    ax.axvline(xx, color=CORTE, lw=1.5); ax.text(xx, 548.6, t, rotation=90, va='bottom', ha='right', fontsize=9, color=MUTED)
ax.set_xlim(0, p.COMP); ax.set_ylim(547, 568)
ax.set_xlabel('Distância (m) — estaca 0 (P0) a 101 (PF)'); ax.set_ylabel('Cota (m)')
ax.set_title('Perfil longitudinal: 3 curvas verticais (R ≥ 30 000 m), rampa máx. 0,80%, declividade efetiva 0,16%')
ax.legend(frameon=False, ncol=4, fontsize=9, loc='upper center', bbox_to_anchor=(0.5, -0.16))
salva(fig, '05_perfil.png')

# 6. Seções transversais (4 exemplos) ------------------------------------------
lin = M['linhas']
alvo = [580.0, 600.0, 1000.0, 1700.0]
fig, axs = plt.subplots(2, 2, figsize=(13, 6.5), sharex=True)
for ax, est in zip(axs.ravel(), alvo):
    zg = float(p.greide(PV, [est])[0])
    sct = p.secao(est, zg, p.eg_secao(est))
    o = p.OFF; eg = sct['eg'] - p.LIMPEZA; pr = sct['proj']
    mm = ~np.isnan(pr)
    ax.fill_between(o[mm], eg[mm], pr[mm], where=eg[mm] >= pr[mm], color=CORTE, alpha=0.55, lw=0, interpolate=True)
    ax.fill_between(o[mm], eg[mm], pr[mm], where=eg[mm] < pr[mm], color=ATERRO, alpha=0.55, lw=0, interpolate=True)
    ax.plot(o, sct['eg'], color=TN, lw=1.2); ax.plot(o[mm], pr[mm], color=INK, lw=1.4)
    c3 = C3[str(round(est, 3))]
    nm = [l for l in lin if abs(l['est_m'] - est) < 1e-6][0]
    ax.set_title(f"Estaca {nm['estaca']} {('(' + nm['ponto'] + ')') if nm['ponto'] else ''} — corte {c3['ac']:,.0f} m²; aterro {c3['aa']:,.0f} m²".replace(',', '.').replace(' + 00.00', ' + 00,00'), fontsize=11)
    ax.set_xlim(-200, 200)
    ax.set_ylabel('Cota (m)')
for ax in axs[1]: ax.set_xlabel('Afastamento do eixo (m)')
fig.suptitle('Seções transversais (áreas do Civil 3D; terreno já sem os 15 cm de limpeza)', weight='bold')
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
fig.legend(handles=[Patch(color=CORTE, alpha=0.55, label='Corte'), Patch(color=ATERRO, alpha=0.55, label='Aterro'),
                    Line2D([], [], color=TN, label='Terreno natural'), Line2D([], [], color=INK, label='Plataforma de terraplenagem')],
           loc='lower center', ncol=4, frameon=False, bbox_to_anchor=(0.5, -0.03))
plt.tight_layout(rect=(0, 0.03, 1, 1))
salva(fig, '06_secoes.png')

# 7. Áreas por estaca + Brückner ------------------------------------------------
est = np.array([l['est_m'] for l in lin])
ac = np.array([C3[str(round(x, 3))]['ac'] for x in est]); aa_ = np.array([C3[str(round(x, 3))]['aa'] for x in est])
vc = np.diff(est) * (ac[1:] + ac[:-1]) / 2; va = np.diff(est) * (aa_[1:] + aa_[:-1]) / 2
ordn = np.concatenate([[0], np.cumsum(vc - p.FH * va)])
fig, (a1, a2) = plt.subplots(2, 1, figsize=(13, 7), sharex=True, gridspec_kw=dict(height_ratios=[1, 1.3]))
a1.bar(est, ac, width=14, color=CORTE, label='Área de corte'); a1.bar(est, -aa_, width=14, color=ATERRO, label='Área de aterro')
a1.axhline(0, color=MUTED, lw=0.8); a1.set_ylabel('Área (m²)'); a1.legend(frameon=False, ncol=2, loc='upper right', fontsize=9)
a1.set_yticks(a1.get_yticks()); a1.set_yticklabels([f'{abs(t):.0f}' for t in a1.get_yticks()])
a1.set_title('Áreas por seção (corte acima, aterro abaixo do zero)')
a2.plot(est, ordn / 1000, color=INK, lw=2)
a2.axhline(0, color=MUTED, lw=0.8, ls='--')
a2.set_ylabel('Ordenada (×10³ m³)'); a2.set_xlabel('Distância (m)')
a2.set_title(f'Diagrama de massas (Brückner), Fh = {p.FH:.2f}'.replace('.', ',') + ' — ordenada final ' + f'{ordn[-1]:+,.0f}'.replace(',', '.') + ' m³ (greide compensado)')
k = np.argmax(ordn); j = np.argmin(ordn)
for kk in (k, j):
    a2.annotate(f'{ordn[kk] / 1000:,.1f}'.replace('.', ','), (est[kk], ordn[kk] / 1000), xytext=(0, 8 if kk == k else -14), textcoords='offset points', ha='center', fontsize=10)
salva(fig, '07_brueckner.png')
print('ordenada máx/mín:', ordn.max(), ordn.min())
