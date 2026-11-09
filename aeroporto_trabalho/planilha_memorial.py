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
    ('Fh', 'Fator de homogeneização (aterro corrigido = Fh × aterro)', p.FH, '0.00', 'Aula 7 (13/10): exercício da aula usou Fh = 1,1'),
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
cel(wm, 'A2', 'Áreas de corte e aterro extraídas das 106 seções do Civil 3D (linhas de amostragem "SL - PPD", superfícies TN_limpo e TERRAPLENAGEM). Áreas já descontam a limpeza de 0,15 m (medidas a partir do TN limpo); pavimento desconsiderado (seção no greide de terraplenagem). Fh e limpeza na aba Premissas.', Font(name=F, italic=True, size=9))
cols = ['Ponto', 'Estaca', 'Dist. acum. (m)', 'Cota TN eixo (m)', 'Cota greide (m)', 'Cota terrapl. eixo (m)',
        'Área corte (m²)', 'Área aterro (m²)', 'Á. média corte (m²)', 'Á. média aterro (m²)', 'Dist. (m)',
        'Vol. corte (m³)', 'Vol. aterro (m³)', 'Aterro corrigido Fh×A (m³)', 'Vol. acum. corte (m³)', 'Vol. acum. aterro corr. (m³)',
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
    cel(wm, f'R{r}', round(c3['dl_dir'] - c3['dl_esq'], 2), AZUL, '0.00')
    if i == 0:
        cel(wm, f'O{r}', 0, fmt='#,##0'); cel(wm, f'P{r}', 0, fmt='#,##0'); cel(wm, f'Q{r}', 0, fmt='#,##0')
        continue
    cel(wm, f'I{r}', f'=(G{r-1}+G{r})/2', fmt='#,##0.00'); cel(wm, f'J{r}', f'=(H{r-1}+H{r})/2', fmt='#,##0.00')
    cel(wm, f'K{r}', f'=C{r}-C{r-1}', fmt='0.00')
    cel(wm, f'L{r}', f'=I{r}*K{r}', fmt='#,##0'); cel(wm, f'M{r}', f'=J{r}*K{r}', fmt='#,##0')
    cel(wm, f'N{r}', f'={FH}*M{r}', fmt='#,##0')
    cel(wm, f'O{r}', f'=O{r-1}+L{r}', fmt='#,##0'); cel(wm, f'P{r}', f'=P{r-1}+N{r}', fmt='#,##0')
    cel(wm, f'Q{r}', f'=Q{r-1}+L{r}-N{r}', fmt='#,##0')
    cel(wm, f'S{r}', f'={HL}*K{r}*(R{r-1}+R{r})/2', fmt='#,##0')
rl = r0 + len(lin) - 1
rt = rl + 2
cel(wm, f'A{rt}', 'TOTAIS', NEG)
for c, f in (('L', 'SUM'), ('M', 'SUM'), ('N', 'SUM'), ('S', 'SUM')):
    cel(wm, f'{c}{rt}', f'={f}({c}{r0+1}:{c}{rl})', NEG, '#,##0')
cel(wm, f'A{rt+1}', 'Saldo (corte − aterro corrigido) = ordenada final de Brückner (m³)', NEG); cel(wm, f'L{rt+1}', f'=L{rt}-N{rt}', NEG, '#,##0')
cel(wm, f'A{rt+2}', 'Volume total movimentado (corte + limpeza) (m³)', NEG); cel(wm, f'L{rt+2}', f'=L{rt}+S{rt}', NEG, '#,##0')
wm.freeze_panes = 'C5'
for k, w in enumerate([9, 11, 10, 10, 10, 10, 10, 10, 10, 10, 7, 11, 11, 12, 12, 12, 12, 9, 10], 1):
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
xs = Reference(wm, min_col=3, min_row=r0, max_row=rl); ys = Reference(wm, min_col=17, min_row=r0, max_row=rl)
s = Series(ys, xs, title='Ordenada de Brückner'); s.marker.symbol = 'none'; ch.series.append(s)
ch.height = 9; ch.width = 22
wm.add_chart(ch, f'U5')

# ------------------------------------------------------------------ Cálculo à mão
wh = wb.create_sheet('Cálculo à mão')
# par escolhido: duas estacas inteiras consecutivas com corte e aterro (seções mistas)
par = None
for i in range(1, len(lin)):
    a, b = lin[i - 1], lin[i]
    if b['est_m'] - a['est_m'] == 20 and min(C3[str(round(a['est_m'], 3))]['ac'], C3[str(round(a['est_m'], 3))]['aa'],
                                             C3[str(round(b['est_m'], 3))]['ac'], C3[str(round(b['est_m'], 3))]['aa']) > 300:
        par = i; break
a, b = lin[par - 1], lin[par]
ca, cb = C3[str(round(a['est_m'], 3))], C3[str(round(b['est_m'], 3))]
ra, rb = r0 + par - 1, r0 + par
cel(wh, 'A1', f'Volume entre as estacas {a["estaca"]} e {b["estaca"]} pelo método das áreas médias (feito à mão)', TIT)
cel(wh, 'A2', 'Regra da aula de 20/10: o volume entre duas estacas consecutivas é calculado à mão; o restante pode ser automatizado. Par escolhido: duas seções mistas (corte e aterro), para mostrar também o aterro corrigido.', Font(name=F, italic=True, size=9))
def br(v, d=2):
    return f'{v:,.{d}f}'.replace(',', ' ').replace('.', ',')


txt = [
    ('Dados (áreas das seções do Civil 3D)', ''),
    (f'Estaca {a["estaca"]}:  A_corte,1 = {br(ca["ac"])} m²   A_aterro,1 = {br(ca["aa"])} m²', ''),
    (f'Estaca {b["estaca"]}:  A_corte,2 = {br(cb["ac"])} m²   A_aterro,2 = {br(cb["aa"])} m²', ''),
    ('Distância entre as seções:  d = 20,00 m', ''),
    ('', ''),
    ('Fórmula:  V = (A₁ + A₂) / 2 × d', ''),
    (f'Corte:   Vc = ({br(ca["ac"])} + {br(cb["ac"])}) / 2 × 20 = {br((ca["ac"] + cb["ac"]) / 2)} × 20 = {br((ca["ac"] + cb["ac"]) * 10)} m³', ''),
    (f'Aterro:  Va = ({br(ca["aa"])} + {br(cb["aa"])}) / 2 × 20 = {br((ca["aa"] + cb["aa"]) / 2)} × 20 = {br((ca["aa"] + cb["aa"]) * 10)} m³', ''),
    (f'Aterro corrigido:  Fh × Va = 1,1 × {br((ca["aa"] + cb["aa"]) * 10)} = {br(1.1 * (ca["aa"] + cb["aa"]) * 10)} m³', ''),
    (f'Contribuição à ordenada de Brückner:  Vc − Fh·Va = {br((ca["ac"] + cb["ac"]) * 10 - 1.1 * (ca["aa"] + cb["aa"]) * 10)} m³', ''),
]
for i, (t, _) in enumerate(txt, 4):
    cel(wh, f'A{i}', t, NEG if i in (4, 9) else PRETO)
cel(wh, 'A16', 'Conferência com o Memorial (fórmulas):', NEG)
cel(wh, 'A17', 'Vol. corte no Memorial (m³)'); cel(wh, 'D17', f'=Memorial!L{rb}', VERDE, '#,##0.00')
cel(wh, 'A18', 'Vol. aterro no Memorial (m³)'); cel(wh, 'D18', f'=Memorial!M{rb}', VERDE, '#,##0.00')
cel(wh, 'A19', 'Aterro corrigido no Memorial (m³)'); cel(wh, 'D19', f'=Memorial!N{rb}', VERDE, '#,##0.00')
cel(wh, 'A20', 'Conta à mão — corte (m³)'); cel(wh, 'D20', round((ca['ac'] + cb['ac']) * 10, 2), AZUL, '#,##0.00')
cel(wh, 'A21', 'Conta à mão — aterro (m³)'); cel(wh, 'D21', round((ca['aa'] + cb['aa']) * 10, 2), AZUL, '#,##0.00')
cel(wh, 'A22', 'Confere?'); cel(wh, 'D22', '=IF(AND(ABS(D17-D20)<0.1,ABS(D18-D21)<0.1),"OK","VERIFICAR")', NEG)
wh.column_dimensions['A'].width = 34; wh.column_dimensions['D'].width = 14

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

wb.save(SAIDA)
print('salvo', SAIDA, 'par à mão:', a['estaca'], '→', b['estaca'], 'linhas', rb)
