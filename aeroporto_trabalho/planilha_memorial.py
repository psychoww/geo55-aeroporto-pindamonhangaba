"""Gera ../Memorial_terraplenagem_PPD.xlsx (fórmulas vivas) a partir de dados/memorial.json e dados/areas_civil3d.json."""
import json
from openpyxl import Workbook
from openpyxl.chart import ScatterChart, Reference, Series
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as L
import projeto as p

M = json.load(open('dados/memorial.json'))
C3 = json.load(open('dados/areas_civil3d.json'))['por_estaca']
SAIDA = '../Memorial_terraplenagem_PPD.xlsx'

F = 'Arial'
AZUL = Font(name=F, color='0000FF', size=10)
PRETO = Font(name=F, size=10)
VERDE = Font(name=F, color='008000', size=10)
NEG = Font(name=F, bold=True, size=10)
TIT = Font(name=F, bold=True, size=13)
CAB = PatternFill('solid', fgColor='D9E1F2')
AMAR = PatternFill('solid', fgColor='FFF2CC')
fino = Side(style='thin', color='999999')
BORDA = Border(left=fino, right=fino, top=fino, bottom=fino)
CENT = Alignment(horizontal='center', vertical='center', wrap_text=True)

wb = Workbook()


def cel(ws, ref, v, font=PRETO, fmt=None, fill=None, al=None):
    c = ws[ref]; c.value = v; c.font = font
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    if al: c.alignment = al
    return c


# ------------------------------------------------------------------ Premissas
ws = wb.active; ws.title = 'Premissas'
cel(ws, 'A1', 'Projeto de terraplenagem da PPD 06/24 — premissas', TIT)
cel(ws, 'A2', 'Azul = dado de entrada; preto = fórmula; verde = vínculo com outra aba. Sítio: oeste de Pindamonhangaba-SP, centro (−22,9300; −45,4993), SIRGAS 2000 / UTM 23S.', Font(name=F, italic=True, size=9))
prem = [
    ('Fh', 'Fator de homogeneização (aterro corrigido = Fh × aterro)', p.FH, '0.00', 'Adotado: latossolo vermelho-amarelo poroso sobre o Grupo Taubaté (γs in situ baixo); faixa usual 1,2–1,3. A aula usou 1,1 só no exercício'),
    ('h_limpeza', 'Limpeza da camada vegetal (m)', p.LIMPEZA, '0.00', 'Aula 7: remover 15 cm em toda a faixa; não entra na compensação'),
    ('h_pav_PPD', 'Espessura do pavimento da PPD (m)', p.H_PPD, '0.00', 'Enunciado do trabalho'),
    ('h_pav_acost', 'Espessura do pavimento dos acostamentos (m)', p.H_ACOST, '0.00', 'Enunciado do trabalho'),
    ('L_PPD', 'Comprimento da PPD (m)', 1900, '0', 'Enunciado (figura); confirmado pela professora em 03/11'),
    ('L_faixa', 'Comprimento da faixa de pista (m)', p.COMP, '0', 'Enunciado: 60 m além de cada cabeceira'),
    ('b_PPD', 'Meia largura da PPD (m)', p.B_PPD, '0.0', 'Enunciado: 45 m'),
    ('b_acost', 'Largura do acostamento (m)', p.B_ACOST - p.B_PPD, '0.0', 'Enunciado'),
    ('b_faixa', 'Meia largura da faixa de pista (m)', p.B_FAIXA, '0.0', 'Enunciado: 22,5 + 127,5 m'),
    ('i_PPD', 'Declividade transversal da PPD', p.I_PPD, '0.0%', 'Enunciado'),
    ('i_faixa', 'Declividade transversal da faixa (e acostamentos)', p.I_FAIXA, '0.0%', 'Enunciado'),
    ('talude_c', 'Talude de corte (H:V)', p.TALUDE_CORTE, '0.0', 'Adotado (solo residual/coluvionar do Vale do Paraíba)'),
    ('talude_a', 'Talude de aterro (H:V)', p.TALUDE_ATERRO, '0.0', 'Adotado'),
    ('i_max', 'Declividade longitudinal máxima', 0.015, '0.0%', 'Enunciado'),
    ('i_ef_max', 'Declividade longitudinal efetiva máxima', 0.010, '0.0%', 'Enunciado'),
    ('di_max', 'Mudança máxima de declividade', 0.015, '0.0%', 'Enunciado'),
    ('R_min', 'Raio mínimo de curva vertical (m)', p.R_VERT, '#,##0', 'Complemento: Anexo 14 OACI / RBAC 154, código 4'),
    ('i_quartos', 'Declividade máx. no 1º e no último quarto da PPD', 0.008, '0.0%', 'Complemento: Anexo 14 OACI, código 4'),
]
for k, h in enumerate(['Símbolo', 'Descrição', 'Valor', 'Fonte'], 1):
    cel(ws, f'{L(k)}4', h, NEG, fill=CAB, al=CENT)
NOMES = {}
for i, (s, d, v, fmt, fonte) in enumerate(prem, 5):
    cel(ws, f'A{i}', s); cel(ws, f'B{i}', d); cel(ws, f'C{i}', v, AZUL, fmt); cel(ws, f'D{i}', fonte, Font(name=F, size=9))
    NOMES[s] = f"Premissas!$C${i}"
ws.column_dimensions['A'].width = 12; ws.column_dimensions['B'].width = 50; ws.column_dimensions['C'].width = 12; ws.column_dimensions['D'].width = 62
FH = NOMES['Fh']; HL = NOMES['h_limpeza']

# ------------------------------------------------------------------ Greide
wg = wb.create_sheet('Greide')
cel(wg, 'A1', 'Greide da PPD (superfície acabada no eixo) — PIVs, rampas e verificações', TIT)
hdr = ['PIV', 'Estaca (m)', 'Cota (m)', 'L curva (m)', 'Rampa seguinte', 'Δi no PIV', 'R = L/|Δi| (m)', 'PCV (m)', 'PTV (m)', 'Cota PCV', 'Cota PTV',
       '|i| ≤ i_max', '|Δi| ≤ Δi_max', 'R ≥ R_min']
for k, h in enumerate(hdr, 1):
    cel(wg, f'{L(k)}3', h, NEG, fill=CAB, al=CENT)
pv = M['pvis']; n = len(pv)
for i, (e, z, Lc) in enumerate(pv):
    r = 4 + i
    cel(wg, f'A{r}', i); cel(wg, f'B{r}', e, AZUL, '#,##0.00'); cel(wg, f'C{r}', round(z, 3), AZUL, '0.000'); cel(wg, f'D{r}', Lc, AZUL, '0')
    if i < n - 1:
        cel(wg, f'E{r}', f'=(C{r+1}-C{r})/(B{r+1}-B{r})', fmt='0.000%')
        cel(wg, f'L{r}', f'=IF(ABS(E{r})<={NOMES["i_max"]},"OK","NÃO")', al=CENT)
    if 0 < i < n - 1:
        cel(wg, f'F{r}', f'=E{r}-E{r-1}', fmt='0.000%')
        cel(wg, f'G{r}', f'=IF(ABS(F{r})>0,D{r}/ABS(F{r}),"")', fmt='#,##0')
        cel(wg, f'H{r}', f'=B{r}-D{r}/2', fmt='#,##0.00'); cel(wg, f'I{r}', f'=B{r}+D{r}/2', fmt='#,##0.00')
        cel(wg, f'J{r}', f'=C{r}-E{r-1}*D{r}/2', fmt='0.000'); cel(wg, f'K{r}', f'=C{r}+E{r}*D{r}/2', fmt='0.000')
        cel(wg, f'M{r}', f'=IF(ABS(F{r})<={NOMES["di_max"]},"OK","NÃO")', al=CENT)
        cel(wg, f'N{r}', f'=IF(G{r}>={NOMES["R_min"]}-1,"OK","NÃO")', al=CENT)
rr = 4 + n + 1
cel(wg, f'A{rr}', 'Declividade efetiva da PPD = (cota máx. − cota mín. no trecho da PPD) / L_PPD', NEG)
# cota máx./mín. no trecho 0+060 a 1+960 vêm do memorial (colunas de cota do greide)
cel(wg, f'A{rr+1}', 'Cota máxima na PPD (m)'); cel(wg, f'A{rr+2}', 'Cota mínima na PPD (m)'); cel(wg, f'A{rr+3}', 'Declividade efetiva'); cel(wg, f'A{rr+4}', 'Verificação (≤ 1,0%)')
cel(wg, f'A{rr+6}', 'Nota: as cotas das curvas verticais (parábola simétrica) estão em cada linha do Memorial (coluna Cota greide), conferidas com o perfil do Civil 3D (diferença < 1 mm).', Font(name=F, italic=True, size=9))
for k, w in enumerate([6, 11, 10, 10, 12, 10, 12, 10, 10, 10, 10, 11, 12, 11], 1):
    wg.column_dimensions[L(k)].width = w
wg.column_dimensions['A'].width = 8

# ------------------------------------------------------------------ Memorial
wm = wb.create_sheet('Memorial')
cel(wm, 'A1', 'Memorial de cálculo de volumes — método das áreas médias (seções do Civil 3D: TN limpo × plataforma de terraplenagem)', TIT)
cel(wm, 'A2', 'Áreas de corte e aterro extraídas das 106 seções do Civil 3D (linhas de amostragem "SL - PPD", superfícies TN_limpo e TERRAPLENAGEM). Áreas já descontam a limpeza de 0,15 m (medidas a partir do TN limpo) e consideram a espessura do pavimento (seção no greide de terraplenagem = acabado − pavimento, aula 7). Compensação lateral = menor valor entre o corte e o aterro corrigido do trecho (não sujeita a transporte longitudinal). Fh e limpeza na aba Premissas.', Font(name=F, italic=True, size=9))
cols = ['Ponto', 'Estaca', 'Dist. acum. (m)', 'Cota TN eixo (m)', 'Cota greide (m)', 'Cota terrapl. eixo (m)',
        'Área corte (m²)', 'Área aterro (m²)', 'Á. média corte (m²)', 'Á. média aterro (m²)', 'Dist. (m)',
        'Vol. corte (m³)', 'Vol. aterro (m³)', 'Aterro corrigido Fh×A (m³)', 'Compensação lateral (m³)', 'Vol. acum. corte (m³)', 'Vol. acum. aterro corr. (m³)',
        'Ordenada de Brückner (m³)', 'Largura limpeza (m)', 'Vol. limpeza (m³)']
for k, h in enumerate(cols, 1):
    cel(wm, f'{L(k)}4', h, NEG, fill=CAB, al=CENT)
wm.row_dimensions[4].height = 45
r0 = 5
lin = M['linhas']
for i, l in enumerate(lin):
    r = r0 + i
    c3 = C3[str(round(l['est_m'], 3))]
    cel(wm, f'A{r}', l['ponto'] or '—', al=CENT); cel(wm, f'B{r}', l['estaca'], al=CENT)
    cel(wm, f'C{r}', l['est_m'], AZUL, '#,##0.00')
    cel(wm, f'D{r}', round(l['cota_tn'], 3), AZUL, '0.000'); cel(wm, f'E{r}', round(l['cota_greide'], 3), AZUL, '0.000')
    cel(wm, f'F{r}', f'=E{r}-{NOMES["h_pav_PPD"]}', fmt='0.000')
    cel(wm, f'G{r}', round(c3['ac'], 2), AZUL, '#,##0.00'); cel(wm, f'H{r}', round(c3['aa'], 2), AZUL, '#,##0.00')
    cel(wm, f'S{r}', round(c3['dl_dir'] - c3['dl_esq'], 2), AZUL, '0.00')
    if i == 0:
        cel(wm, f'P{r}', 0, fmt='#,##0'); cel(wm, f'Q{r}', 0, fmt='#,##0'); cel(wm, f'R{r}', 0, fmt='#,##0')
        continue
    cel(wm, f'I{r}', f'=(G{r-1}+G{r})/2', fmt='#,##0.00'); cel(wm, f'J{r}', f'=(H{r-1}+H{r})/2', fmt='#,##0.00')
    cel(wm, f'K{r}', f'=C{r}-C{r-1}', fmt='0.00')
    cel(wm, f'L{r}', f'=I{r}*K{r}', fmt='#,##0'); cel(wm, f'M{r}', f'=J{r}*K{r}', fmt='#,##0')
    cel(wm, f'N{r}', f'={FH}*M{r}', fmt='#,##0')
    cel(wm, f'O{r}', f'=MIN(L{r},N{r})', fmt='#,##0')
    cel(wm, f'P{r}', f'=P{r-1}+L{r}', fmt='#,##0'); cel(wm, f'Q{r}', f'=Q{r-1}+N{r}', fmt='#,##0')
    cel(wm, f'R{r}', f'=R{r-1}+L{r}-N{r}', fmt='#,##0')
    cel(wm, f'T{r}', f'={HL}*K{r}*(S{r-1}+S{r})/2', fmt='#,##0')
rl = r0 + len(lin) - 1
rt = rl + 2
cel(wm, f'A{rt}', 'TOTAIS', NEG)
for c, f in (('L', 'SUM'), ('M', 'SUM'), ('N', 'SUM'), ('O', 'SUM'), ('T', 'SUM')):
    cel(wm, f'{c}{rt}', f'={f}({c}{r0+1}:{c}{rl})', NEG, '#,##0')
cel(wm, f'A{rt+1}', 'Saldo (corte − aterro corrigido) = ordenada final de Brückner (m³)', NEG); cel(wm, f'L{rt+1}', f'=L{rt}-N{rt}', NEG, '#,##0')
cel(wm, f'A{rt+2}', 'Volume total movimentado (corte + limpeza) (m³)', NEG); cel(wm, f'L{rt+2}', f'=L{rt}+T{rt}', NEG, '#,##0')
cel(wm, f'A{rt+3}', 'Corte sujeito a transporte longitudinal = corte − compensação lateral (m³)', NEG); cel(wm, f'L{rt+3}', f'=L{rt}-O{rt}', NEG, '#,##0')
cel(wm, f'A{rt+4}', 'Aterro corrigido a receber de outros trechos = aterro corr. − compensação lateral (m³)', NEG); cel(wm, f'L{rt+4}', f'=N{rt}-O{rt}', NEG, '#,##0')
wm.freeze_panes = 'C5'
for k, w in enumerate([9, 11, 10, 10, 10, 10, 10, 10, 10, 10, 7, 11, 11, 12, 12, 12, 12, 12, 9, 10], 1):
    wm.column_dimensions[L(k)].width = w
# efetiva no Greide (faixa 0+060 a 1+960 = linhas com C entre 60 e 1960)
rng_c = f"Memorial!$C${r0}:$C${rl}"; rng_e = f"Memorial!$E${r0}:$E${rl}"
cel(wg, f'C{rr+1}', f'=_xlfn.MAXIFS({rng_e},{rng_c},">=60",{rng_c},"<=1960")', VERDE, '0.000')
cel(wg, f'C{rr+2}', f'=_xlfn.MINIFS({rng_e},{rng_c},">=60",{rng_c},"<=1960")', VERDE, '0.000')
cel(wg, f'C{rr+3}', f'=(C{rr+1}-C{rr+2})/{NOMES["L_PPD"]}', fmt='0.000%')
cel(wg, f'C{rr+4}', f'=IF(C{rr+3}<={NOMES["i_ef_max"]},"OK","NÃO")')

# gráfico de Brückner
ch = ScatterChart(); ch.title = 'Diagrama de massas (Brückner)'; ch.style = 13
ch.x_axis.title = 'Distância (m)'; ch.y_axis.title = 'Ordenada (m³)'
xs = Reference(wm, min_col=3, min_row=r0, max_row=rl); ys = Reference(wm, min_col=18, min_row=r0, max_row=rl)
s = Series(ys, xs, title='Ordenada de Brückner'); s.marker.symbol = 'none'; ch.series.append(s)
ch.height = 9; ch.width = 22
wm.add_chart(ch, f'V5')

# ------------------------------------------------------------------ Cálculo à mão
wh = wb.create_sheet('Cálculo à mão')
# par escolhido: duas estacas inteiras consecutivas (d = 20 m), as duas seções mistas, com o maior mínimo entre as quatro
# áreas (corte e aterro de cada seção) — vale para qualquer sítio
def _min4(i):
    x, y = C3[str(round(lin[i - 1]['est_m'], 3))], C3[str(round(lin[i]['est_m'], 3))]
    return min(x['ac'], x['aa'], y['ac'], y['aa'])
par = max((i for i in range(1, len(lin)) if lin[i]['est_m'] - lin[i - 1]['est_m'] == 20), key=_min4)
a, b = lin[par - 1], lin[par]
ca, cb = C3[str(round(a['est_m'], 3))], C3[str(round(b['est_m'], 3))]
ra, rb = r0 + par - 1, r0 + par
cel(wh, 'A1', f'Volume entre as estacas {a["estaca"]} e {b["estaca"]} pelo método das áreas médias — conta à mão', TIT)
cel(wh, 'A2', 'Regra da aula de 20/10: o volume entre duas estacas consecutivas é calculado à mão (a conta fica com o aluno). Par sugerido: duas seções mistas (corte e aterro), para mostrar também o aterro corrigido e a compensação lateral. Preencha os campos amarelos; a coluna F traz o valor do Memorial para conferir.', Font(name=F, italic=True, size=9))
cel(wh, 'A4', 'Dados (áreas das seções do Civil 3D)', NEG)
for k, h in enumerate(['Estaca', 'Área corte (m²)', 'Área aterro (m²)', 'Dist. (m)'], 1):
    cel(wh, f'{L(k)}5', h, NEG, fill=CAB, al=CENT)
cel(wh, 'A6', a['estaca']); cel(wh, 'B6', f'=Memorial!G{ra}', VERDE, '#,##0.00'); cel(wh, 'C6', f'=Memorial!H{ra}', VERDE, '#,##0.00')
cel(wh, 'A7', b['estaca']); cel(wh, 'B7', f'=Memorial!G{rb}', VERDE, '#,##0.00'); cel(wh, 'C7', f'=Memorial!H{rb}', VERDE, '#,##0.00')
cel(wh, 'D7', f'=Memorial!K{rb}', VERDE, '0.00')
cel(wh, 'A8', 'Fh'); cel(wh, 'B8', f'={FH}', VERDE, '0.00')
cel(wh, 'A10', 'Fórmulas:  V = (A₁ + A₂)/2 × d;   aterro corrigido = Fh × Va;   compensação lateral = menor(Vc, Fh·Va);   contribuição à ordenada = Vc − Fh·Va', NEG)
for k, h in enumerate(['Grandeza', '', '', 'Sua conta', '', 'Memorial', 'Confere?'], 1):
    if h: cel(wh, f'{L(k)}12', h, NEG, fill=CAB, al=CENT)
itens = [('Área média de corte (m²)', f'I{rb}', '#,##0.00', 0.01), ('Área média de aterro (m²)', f'J{rb}', '#,##0.00', 0.01),
         ('Volume de corte Vc (m³)', f'L{rb}', '#,##0.00', 0.1), ('Volume de aterro Va (m³)', f'M{rb}', '#,##0.00', 0.1),
         ('Aterro corrigido Fh·Va (m³)', f'N{rb}', '#,##0.00', 0.1), ('Compensação lateral (m³)', f'O{rb}', '#,##0.00', 0.1)]
for j, (nome, ref, fmt, tol) in enumerate(itens, 13):
    cel(wh, f'A{j}', nome); cel(wh, f'D{j}', None, AZUL, fmt, fill=AMAR)
    cel(wh, f'F{j}', f'=Memorial!{ref}', VERDE, fmt)
    cel(wh, f'G{j}', f'=IF(D{j}="","preencher",IF(ABS(D{j}-F{j})<={tol},"OK","VERIFICAR"))', NEG, al=CENT)
j = 13 + len(itens)
cel(wh, f'A{j}', 'Contribuição à ordenada Vc − Fh·Va (m³)'); cel(wh, f'D{j}', None, AZUL, '#,##0.00', fill=AMAR)
cel(wh, f'F{j}', f'=Memorial!L{rb}-Memorial!N{rb}', VERDE, '#,##0.00')
cel(wh, f'G{j}', f'=IF(D{j}="","preencher",IF(ABS(D{j}-F{j})<=0.1,"OK","VERIFICAR"))', NEG, al=CENT)
wh.column_dimensions['A'].width = 38
for c in 'BCDEFG':
    wh.column_dimensions[c].width = 14

# ------------------------------------------------------------------ Conferência
wc = wb.create_sheet('Conferência')
cel(wc, 'A1', 'Conferência: áreas do Civil 3D × motor de cálculo em Python (mesmo terreno, mesma seção-tipo)', TIT)
for k, h in enumerate(['Estaca', 'Dist. acum. (m)', 'Corte C3D (m²)', 'Corte Python (m²)', 'Dif. (m²)', 'Aterro C3D (m²)', 'Aterro Python (m²)', 'Dif. (m²)'], 1):
    cel(wc, f'{L(k)}3', h, NEG, fill=CAB, al=CENT)
for i, l in enumerate(lin):
    r = 4 + i
    cel(wc, f'A{r}', l['estaca']); cel(wc, f'B{r}', f'=Memorial!C{r0+i}', VERDE, '#,##0.00')
    cel(wc, f'C{r}', f'=Memorial!G{r0+i}', VERDE, '#,##0.00'); cel(wc, f'D{r}', round(l['area_c'], 2), AZUL, '#,##0.00'); cel(wc, f'E{r}', f'=C{r}-D{r}', fmt='0.00')
    cel(wc, f'F{r}', f'=Memorial!H{r0+i}', VERDE, '#,##0.00'); cel(wc, f'G{r}', round(l['area_a'], 2), AZUL, '#,##0.00'); cel(wc, f'H{r}', f'=F{r}-G{r}', fmt='0.00')
rc = 4 + len(lin) + 1
cel(wc, f'A{rc}', 'Volume de corte: Civil 3D × Python', NEG); cel(wc, f'C{rc}', f'=Memorial!L{rt}', VERDE, '#,##0'); cel(wc, f'D{rc}', round(M['totais']['Vc']), AZUL, '#,##0'); cel(wc, f'E{rc}', f'=C{rc}/D{rc}-1', fmt='0.00%')
cel(wc, f'A{rc+1}', 'Volume de aterro: Civil 3D × Python', NEG); cel(wc, f'C{rc+1}', f'=Memorial!M{rt}', VERDE, '#,##0'); cel(wc, f'D{rc+1}', round(M['totais']['Va']), AZUL, '#,##0'); cel(wc, f'E{rc+1}', f'=C{rc+1}/D{rc+1}-1', fmt='0.00%')
for k, w in enumerate([12, 11, 12, 12, 9, 12, 12, 9], 1):
    wc.column_dimensions[L(k)].width = w

# ------------------------------------------------------------------ Distribuição (LCs, bota-fora, empréstimo)
import os


def lista(v):
    return v if isinstance(v, list) else ([] if v is None else [v])


def lcs(S):
    return S if (S and isinstance(S[0], list)) else ([S] if S else [])


if os.path.exists('dados/distribuicao.json'):
    R = json.load(open('dados/distribuicao.json', encoding='utf-8'))
    wd = wb.create_sheet('Distribuição')
    cel(wd, 'A1', 'Distribuição de massas: linhas de compensação (LC), bota-fora, empréstimo e momento de transporte', TIT)
    cel(wd, 'A2', f'Programa da aula de 20/10 (diagrama_massas/, MATLAB), funções dm_*.m, sobre as ordenadas do Memorial (Fh = {p.FH:.2f}). '
                  f'Convenção da aula: a LC compensa só entre seus cruzamentos com o diagrama; o resto é externo (bota-fora/empréstimo) a {R["Dext"]:.0f} m (aula 8). '
                  f'MT = Σ V·DMT + V_ext·D_ext, em m³·dam. Variante: o empréstimo também custa a escavação (exercício 6 da lista: R$ 3,20/m³ e R$ 1,60/(m³·km), '
                  f'DMT externa equivalente de {R["DextEco"]:.0f} m).', Font(name=F, italic=True, size=9))
    hd = ['Cenário', 'Nº de LCs', 'MT total (m³·dam)', 'MT interno (m³·dam)', 'MT externo (m³·dam)', 'Bota-fora (m³)', 'Empréstimo (m³)',
          'Volume compensado (m³)', 'DMT média interna (m)']
    for k, h in enumerate(hd, 1):
        cel(wd, f'{L(k)}4', h, NEG, fill=CAB, al=CENT)
    ordem = ['eco_aula', 'lc_unica', 'ate_2_lcs', 'ate_3_lcs', 'livre', 'eco']
    nomes = {'eco_aula': 'Recomendado: 1 LC do P0 ao PF na cota do saldo (compensa tudo; = melhor solução com 1 LC)',
             'eco': f'Variante: empréstimo paga a escavação (DMT externa equivalente {R["DextEco"]:.0f} m), mesma LC'}
    r = 5
    for kk in ordem:
        c = R['cenarios'][kk]
        rec_ = kk == 'eco_aula'
        cel(wd, f'A{r}', nomes.get(kk, c['nome']), NEG if rec_ else PRETO, fill=AMAR if rec_ else None)
        cel(wd, f'B{r}', len(lcs(c['S'])), AZUL, '0')
        for col, campo in zip('CDEFGH', ['MT', 'MTint', 'MText', 'Vbf', 'Vemp', 'Vint']):
            cel(wd, f'{col}{r}', round(c[campo]), AZUL, '#,##0')
        cel(wd, f'I{r}', f'=IF(H{r}>0,D{r}*10/H{r},"")', fmt='#,##0')
        r += 1
    r += 1
    rec = R['cenarios']['eco_aula']
    cel(wd, f'A{r}', 'Ondas da solução recomendada (cada onda = um corte que abastece um aterro)', NEG); r += 1
    for k, h in enumerate(['Onda', 'De (m)', 'Até (m)', 'Sentido', 'V (m³)', 'DMT = MT/V (m)', 'DMT na meia altura (m)', 'MT (m³·dam)'], 1):
        cel(wd, f'{L(k)}{r}', h, NEG, fill=CAB, al=CENT)
    r += 1
    for i, w in enumerate(lista(rec['ondas']), 1):
        cel(wd, f'A{r}', i); cel(wd, f'B{r}', round(w['ini'], 1), AZUL, '#,##0.0'); cel(wd, f'C{r}', round(w['fim'], 1), AZUL, '#,##0.0')
        cel(wd, f'D{r}', '→ sentido do estaqueamento' if w['sinal'] > 0 else '← sentido contrário')
        cel(wd, f'E{r}', round(w['V']), AZUL, '#,##0'); cel(wd, f'F{r}', round(w['DMT']), AZUL, '#,##0')
        cel(wd, f'G{r}', round(w['DMTmeia']), AZUL, '#,##0'); cel(wd, f'H{r}', f'=E{r}*F{r}/10', fmt='#,##0')
        r += 1
    r += 1
    cel(wd, f'A{r}', 'LCs da solução recomendada', NEG); r += 1
    for k, h in enumerate(['LC', 'De (m)', 'Até (m)', 'Cota (m³)'], 1):
        cel(wd, f'{L(k)}{r}', h, NEG, fill=CAB, al=CENT)
    r += 1
    for i, (de, ate, cota) in enumerate(lcs(rec['S']), 1):
        cel(wd, f'A{r}', f'LC{i}'); cel(wd, f'B{r}', round(de, 1), AZUL, '#,##0.0'); cel(wd, f'C{r}', round(ate, 1), AZUL, '#,##0.0'); cel(wd, f'D{r}', round(cota), AZUL, '#,##0')
        r += 1
    for e in lista(rec['ext']):
        cel(wd, f'A{r}', f"{e['tipo']}: {e['V']:,.0f} m³ entre {e['de']:,.0f} e {e['ate']:,.0f} m".replace(',', '.')); r += 1
    cel(wd, f'A{r}', 'A limpeza (camada vegetal de 15 cm) vai toda para bota-fora ou para estoque, para revestir os taludes (ver Memorial).', Font(name=F, italic=True, size=9))
    wd.column_dimensions['A'].width = 62
    for c in 'BCDEFGHI':
        wd.column_dimensions[c].width = 15

# ------------------------------------------------------------------ Equipamentos
we = wb.create_sheet('Equipamentos')
cel(we, 'A1', 'Equipamentos de terraplenagem e razões da escolha (aula 9: máquinas e equipamentos)', TIT)
cel(we, 'A2', 'Solo esperado: latossolo vermelho-amarelo e sedimentos do Grupo Taubaté (argilas, siltes e areias), 1ª categoria (DER-SP: escavável com lâmina e scraper). '
              'As faixas de DMT por equipamento são referência usual de manuais de terraplenagem, não da aula.', Font(name=F, italic=True, size=9))
for k, h in enumerate(['Serviço', 'Quantidade', 'Equipamento', 'Por que este equipamento'], 1):
    cel(we, f'{L(k)}4', h, NEG, fill=CAB, al=CENT)
tot = M['totais']
EQ = [
    ('Limpeza e raspagem da camada vegetal (15 cm)', f'=Memorial!T{rt}',
     'Trator de esteira com lâmina reta; motoniveladora na vegetação rasa',
     'Aula 9: a lâmina reta serve principalmente para limpeza geral, cavando e amontoando material; a motoniveladora também faz capina de vegetação rasa. O sítio é pasto (4% de mata).'),
    ('Carga e remoção da limpeza', 'o mesmo volume', 'Pá carregadeira + caminhões basculantes',
     'Aula 9: a pá carregadeira remove material solto; o basculante comum (4,5 a 6 m³) leva ao bota-fora ou ao estoque para revestir os taludes.'),
    ('Escavação, carga, transporte e espalhamento corte → aterro', f'=Memorial!L{rt}',
     'Moto-scraper, com trator de esteira empurrando na carga',
     'Aula 9: o moto-scraper escava, carrega, transporta e espalha numa única operação. Solo de 1ª categoria, plataforma larga e plana e DMT de algumas centenas de metros: é a faixa em que ele rende mais.'),
    ('Transporte nas ondas mais longas (DMT acima de ~1 km)', 'ver aba Distribuição',
     'Escavadeira de caçamba frontal ou pá carregadeira + caminhões basculantes ou dumpers',
     'Em distâncias longas o ciclo do scraper fica lento; os dumpers (aula 9) têm estrutura reforçada para os esforços da operação em obra.'),
    ('Escarificação localizada', 'eventual', 'Escarificador acoplado ao trator de lâmina',
     'Aula 9: desagrega terrenos compactos. Só se aparecerem camadas cimentadas ou concreções lateríticas.'),
    ('Espalhamento, regularização e acabamento da plataforma (1,5% e 2,5%) e dos taludes', 'cerca de 650 mil m² de plataforma', 'Motoniveladora',
     'Aula 9: acabamento e nivelamento da ordem de meio centímetro e acabamento de taludes: é o que garante as declividades transversais da PPD e da faixa.'),
    ('Compactação do aterro em camadas', f'=Memorial!M{rt}', 'Rolo pé-de-carneiro',
     'Aula 9: as patas compactam do fundo para o topo da camada; indicado para solos coesivos (argilosos), que predominam no sítio; não serve para solo não coesivo.'),
    ('Compactação de lentes arenosas', 'eventual', 'Rolo vibratório liso',
     'Aula 9: adensamento rápido de solos arenosos pela vibração; os sedimentos do Grupo Taubaté têm camadas de areia.'),
    ('Acabamento e selagem do topo do subleito', 'plataforma da PPD e dos acostamentos', 'Rolo pneumático',
     'Aula 9: sela a superfície e compacta solos finos; deixa o subleito pronto para o pavimento.'),
    ('Não usados', '—', 'Drag-line; fresadora; vibroacabadora',
     'A drag-line é para solos moles e saturados (a várzea, que foi descartada). Fresadora e vibroacabadora são serviços de pavimento, fora da terraplenagem.'),
]
for i, linha in enumerate(EQ, 5):
    for k, v in enumerate(linha, 1):
        fmt = '#,##0" m³"' if (k == 2 and str(v).startswith('=')) else None
        cel(we, f'{L(k)}{i}', v, NEG if k == 1 else PRETO, fmt, al=Alignment(wrap_text=True, vertical='top'))
we.column_dimensions['A'].width = 40; we.column_dimensions['B'].width = 22; we.column_dimensions['C'].width = 40; we.column_dimensions['D'].width = 90

wb.save(SAIDA)
print('salvo', SAIDA, 'par à mão:', a['estaca'], '→', b['estaca'], 'linhas', rb)
