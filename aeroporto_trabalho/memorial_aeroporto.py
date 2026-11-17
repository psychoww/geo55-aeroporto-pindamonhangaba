"""Memorial descritivo e de cálculo do aeroporto (sítio C1, PPD 06/24) em PDF.
Fontes: dados/memorial.json (estacas, cotas), dados/areas_civil3d.json (áreas do Civil 3D), civil3d/relatorio_volume_corredor.csv,
dados/distribuicao.json, figuras/. Uso: PYTHONUTF8=1 python memorial_aeroporto.py [../Memorial_final_aeroporto_PPD.pdf]"""
import json
import os
import sys
import numpy as np
import matplotlib
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import projeto as p

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, '..', 'Memorial_final_aeroporto_PPD.pdf')
fd = os.path.join(os.path.dirname(matplotlib.__file__), 'mpl-data', 'fonts', 'ttf')
pdfmetrics.registerFont(TTFont('DV', os.path.join(fd, 'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DVB', os.path.join(fd, 'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFont(TTFont('DVI', os.path.join(fd, 'DejaVuSans-Oblique.ttf')))
pdfmetrics.registerFontFamily('DV', normal='DV', bold='DVB', italic='DVI', boldItalic='DVB')

NAVY = colors.HexColor('#33335B'); ARD = colors.HexColor('#273348'); CINZA = colors.HexColor('#6E6E80')
BAND = colors.HexColor('#F4F1EA'); DEST = colors.HexColor('#E6E4EE'); LAV = colors.HexColor('#9F9DB6')
st = {
    'h1': ParagraphStyle('h1', fontName='DVB', fontSize=14, leading=18, textColor=NAVY, spaceBefore=6, spaceAfter=8),
    'h2': ParagraphStyle('h2', fontName='DVB', fontSize=10.5, leading=14, textColor=NAVY, spaceBefore=8, spaceAfter=4),
    'p': ParagraphStyle('p', fontName='DV', fontSize=9, leading=13, alignment=TA_JUSTIFY, spaceAfter=5, textColor=ARD),
    'nota': ParagraphStyle('nota', fontName='DV', fontSize=7.5, leading=10, textColor=CINZA, spaceAfter=4),
    'cel': ParagraphStyle('cel', fontName='DV', fontSize=7.6, leading=9.6),
    'celp': ParagraphStyle('celp', fontName='DV', fontSize=6.6, leading=8.0),
    'celb': ParagraphStyle('celb', fontName='DVB', fontSize=7.6, leading=9.6, textColor=colors.white),
    'celbp': ParagraphStyle('celbp', fontName='DVB', fontSize=6.6, leading=8.0, textColor=colors.white),
    'dest': ParagraphStyle('dest', fontName='DVB', fontSize=9, leading=13, textColor=NAVY, backColor=DEST, borderPadding=6,
                           leftIndent=4, rightIndent=4, spaceBefore=6, spaceAfter=10),
    'form': ParagraphStyle('form', fontName='DV', fontSize=10, leading=15, textColor=NAVY, leftIndent=20, spaceAfter=3),
}
FIG = os.path.join(AQUI, 'figuras')
GRUPO = 'Pedro Feitosa Guttemberg · Guilherme Rodrigues · Gilberto Patri'

# ------------------------------------------------------------------ dados
M = json.load(open(os.path.join(AQUI, 'dados', 'memorial.json'), encoding='utf-8'))
C3 = json.load(open(os.path.join(AQUI, 'dados', 'areas_civil3d.json'), encoding='utf-8'))['por_estaca']
DI = json.load(open(os.path.join(AQUI, 'dados', 'distribuicao.json'), encoding='utf-8'))
REL = np.genfromtxt(os.path.join(AQUI, 'civil3d', 'relatorio_volume_corredor.csv'), delimiter=';', skip_header=1)
PV = M['pvis']; CV = p.curvas(PV); LIN = M['linhas']; FH = p.FH
EST = np.array([l['est_m'] for l in LIN])
AC = np.array([C3[str(float(e))]['ac'] for e in EST]); AA = np.array([C3[str(float(e))]['aa'] for e in EST])
D = np.r_[0, np.diff(EST)]
VC = np.r_[0, D[1:] * (AC[1:] + AC[:-1]) / 2]; VA = np.r_[0, D[1:] * (AA[1:] + AA[:-1]) / 2]
VAC = FH * VA; CL = np.minimum(VC, VAC); ORD = np.cumsum(VC - VAC)
Vc, Va = VC.sum(), VA.sum(); Vac = FH * Va; CLT = CL.sum()
LIMP = 92401.0
dr = np.diff(REL[:, 0]); RVc = (dr * (REL[1:, 1] + REL[:-1, 1]) / 2).sum(); RVa = (dr * (REL[1:, 2] + REL[:-1, 2]) / 2).sum()
RVc, RVa = 435036.85, 442740.25 / FH   # acumulados do Relatório de volume (o Civil 3D arredonda as áreas a 0,01 m²)
NS = json.load(open(os.path.join(AQUI, 'dados', 'nota_servico.json'), encoding='utf-8'))
assert abs(Vc - 435439.6) < 5 and abs(Va - 344978.5) < 5, (Vc, Va)


def f(v, d=2):
    return f'{v:,.{d}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def P(t, k='p'):
    return Paragraph(t, st[k])


def tab(linhas, larg, dest_rows=(), peq=False, alinhar_dir=True):
    c, cb = ('celp', 'celbp') if peq else ('cel', 'celb')
    dados = [[Paragraph(str(x), st[cb] if i == 0 else st[c]) for x in row] for i, row in enumerate(linhas)]
    t = Table(dados, colWidths=[w * cm for w in larg], repeatRows=1)
    sty = [('BACKGROUND', (0, 0), (-1, 0), NAVY), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
           ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.HexColor('#D5D1C6')),
           ('TOPPADDING', (0, 0), (-1, -1), 1.6 if peq else 2.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 1.6 if peq else 2.5)]
    for i in range(1, len(linhas)):
        if i % 2 == 0:
            sty.append(('BACKGROUND', (0, i), (-1, i), BAND))
    for i in dest_rows:
        sty.append(('BACKGROUND', (0, i), (-1, i), DEST))
    t.setStyle(TableStyle(sty))
    return t


def img(nome, w):
    from reportlab.lib.utils import ImageReader
    fp = os.path.join(FIG, nome); iw, ih = ImageReader(fp).getSize()
    return Image(fp, width=w * cm, height=w * cm * ih / iw)


def fig(nome, w, leg):
    return KeepTogether([img(nome, w), P(leg, 'nota')])


def rodape(canvas, doc):
    canvas.saveState(); canvas.setFont('DV', 7); canvas.setFillColor(CINZA)
    canvas.drawString(2 * cm, 1.2 * cm, 'GEO-55 · Aeroporto em Pindamonhangaba (sítio C1, PPD 06/24) · memorial descritivo e de cálculo · 17/11/2026')
    canvas.drawRightString(19 * cm, 1.2 * cm, str(doc.page))
    canvas.setStrokeColor(LAV); canvas.setLineWidth(1.2); canvas.line(2 * cm, 28.1 * cm, 19 * cm, 28.1 * cm)
    canvas.restoreState()


def main():
    doc = BaseDocTemplate(SAIDA, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm, bottomMargin=2 * cm,
                          title='Memorial descritivo e de cálculo - Aeroporto em Pindamonhangaba (PPD 06/24)', author=GRUPO)
    doc.addPageTemplates([PageTemplate(id='p', frames=[Frame(2 * cm, 1.8 * cm, 17 * cm, 26 * cm, id='f')], onPage=rodape)])
    S = []
    g = [(PV[k + 1][1] - PV[k][1]) / (PV[k + 1][0] - PV[k][0]) for k in range(len(PV) - 1)]
    # ------------------------------------------------ capa
    S += [Spacer(1, 2.5 * cm), P('ITA · Divisão de Engenharia Civil · GEO-55 Projeto e Construção de Pistas · Exame do 2º bimestre de 2026', 'nota'),
          Paragraph('Aeroporto em Pindamonhangaba-SP', ParagraphStyle('t', fontName='DVB', fontSize=26, leading=32, textColor=NAVY, spaceAfter=10)),
          Paragraph('Memorial descritivo e de cálculo do projeto geométrico e de terraplenagem da pista de pouso e decolagem 06/24 no sítio C1',
                    ParagraphStyle('s', fontName='DV', fontSize=13, leading=18, textColor=ARD, spaceAfter=24)),
          P(f'<b>Grupo:</b> {GRUPO}'),
          P('<b>Data:</b> 17 de novembro de 2026 (apresentação final) · <b>Software:</b> Autodesk Civil 3D 2027, Python e MATLAB'), Spacer(1, 0.6 * cm),
          tab([['PPD', 'Faixa de pista', 'Corte', f'Aterro × {f(FH)}', 'Saldo'],
               ['1900 × 45 m, rumo 060°', '2020 × 300 m', f'{f(Vc, 0)} m³', f'{f(Vac, 0)} m³', f'{f(Vc - Vac, 0)} m³']], [3.6, 3.0, 3.4, 3.6, 3.4]),
          Spacer(1, 0.6 * cm), img('15_capa_sitio.png', 15),
          P('Imagem do sítio C1 com a faixa de pista. Estudo acadêmico: o terreno é o modelo Copernicus GLO-30 (radar TanDEM-X, 2011–2015), '
            'sem levantamento topográfico nem sondagens.', 'nota'),
          P('<b>Arquivos que acompanham este memorial:</b> Aeroporto_PPD_Civil3D.dwg (superfícies, eixo, perfis, 104 seções, montagem e corredor), '
            'Memorial_terraplenagem_PPD.xlsx (planilha com fórmulas: Premissas, Greide, Memorial, Cálculo à mão, Conferência, Distribuição, Equipamentos, Corredor), '
            'Pranchas_aeroporto_PPD.pdf (5 folhas A3) e a apresentação.', 'nota'),
          PageBreak()]
    # ------------------------------------------------ 1 enunciado
    S += [P('1. Objeto e requisitos', 'h1'),
          P('O trabalho pede o projeto geométrico e de terraplenagem de um novo aeroporto no Civil 3D, em três etapas: (1) escolha e justificativa do sítio; '
            '(2) imagem georreferenciada, modelo do terreno, alinhamentos horizontal e vertical da PPD e seção-tipo; (3) terraplenagem: quantitativos, '
            'seções transversais e volumes pelo método das áreas médias, com o trecho entre duas estacas consecutivas calculado à mão.'),
          tab([['Requisito', 'Valor', 'Fonte'],
               ['Pista de pouso e decolagem (PPD)', '1900 × 45 m (a figura vale; o "2300 m" do texto é erro)', 'Enunciado; professora em 03/11'],
               ['Faixa de pista', '2020 × 300 m (60 m além de cada cabeceira), nivelada inteira', 'Enunciado; prévia de 10/11'],
               ['Acostamentos', '7,5 m de cada lado', 'Enunciado'],
               ['Declividade transversal', 'PPD 1,5% a partir do eixo; faixa 2,5%', 'Enunciado'],
               ['Declividade longitudinal', 'máx. 1,5%; efetiva máx. 1,0%; mudança máx. 1,5%', 'Enunciado'],
               ['Pavimento', '1,10 m na PPD; 0,50 m nos acostamentos (considerado no volume)', 'Enunciado; aula 7'],
               ['Sítio aeroportuário', 'área de 3000 × 1500 m', 'Enunciado'],
               ['Limpeza', '0,15 m de camada vegetal em toda a área; aterro nunca sobre ela', 'Aula 7'],
               ['Taludes', 'corte 1V:1,5H; aterro 1V:2H', 'Adotado; mantido na prévia'],
               ['Estaqueamento', '20 m', 'Mantido na versão final']], [4.6, 7.9, 4.5]),
          Spacer(1, 0.3 * cm)]
    # ------------------------------------------------ 2 sítio
    S += [P('2. Etapa 1: escolha do sítio pelo método MESA', 'h1'),
          P('Depois da prévia, a escolha foi refeita pelo método MESA do <i>Manual de Apoio à Prospecção de Sítios Aeroportuários Regionais</i> '
            '(SAC/MInfra e ITA, 2021). Critérios eliminatórios tiram áreas e combinações de rumo; os candidatos restantes recebem nota pelos classificatórios, '
            'agregados com os pesos do exemplo do manual (AHP).'),
          tab([['Critério', 'Como foi aplicado'],
               ['Vento (MET)', 'ERA5, setores de 10°; utilização ≥ 95% com 10 kt de través: 99,9–100% em todos os rumos (não restringe)'],
               ['Obstáculos (OBS)', 'aproximação, decolagem e transição livres: só rumos de 20° a 80° (eixo do vale)'],
               ['Cidade (URB)', 'buffer de 2 km da mancha urbana (flexível só se não houver área viável; havia)'],
               ['Relevo (TOPAlt)', 'ΔH na área física ≤ 40 m (terreno ondulado; o manual usa 20 m para plano)'],
               ['Várzea (ALAG)', '≤ 5% da área física a menos de 8 m do fundo do vale'],
               ['Classificatórios', 'GEO 28,0%, TOPVol 33,3%, RUI 7,9%, DIS 12,7%, ACE 12,5%, DIP 5,6%; normalização 1/x ÷ Σ(1/x)']], [3.6, 13.4]),
          Spacer(1, 0.2 * cm),
          P('Foram avaliados 2821 centros (malha de 200 m num raio de 6 km) × 18 rumos. Sobraram 379 combinações viáveis, 35 delas a ≥ 2 km da cidade. '
            '<b>C1 (−22,8885; −45,4874), rumo 060°</b>, ficou em 1º com nota 0,312 (C2: 0,259): proxy de volume 369 mil m³ (prévia 1,15 milhão), '
            '8,4 ha construídos na curva de 65 dB, 3,4 km da mancha urbana, 0,5 km da rodovia, ΔH = 15 m. C1 só perde com peso de RUI > 31% ou de TOPVol < 8%.'),
          fig('13_mesa_candidatos.png', 15, 'Candidatos viáveis do MESA e o ranking (C1 em 1º).'),
          P('<b>Pontos fracos documentados.</b> Os morros ao norte (pé da Mantiqueira) passam acima da superfície horizontal interna (até 144 m, 675 ha) '
            'e da cônica (até 255 m, 1422 ha); a aproximação tem 3,9 m em 3 ha (árvores perto das pontas), dentro do que o manual aceita. '
            'Pelo manual, essas superfícies "devem ser documentadas" e pediriam estudo aeronáutico. Uma pista particular asfaltada (~1,4 km, rumo ~020°, '
            'Fazenda Santa Helena) cruza a ponta SW da faixa e seria desativada e desapropriada; há chácaras na faixa (~1 ha construído). '
            'O aeródromo SDPD (pista de terra de ~1110 m, 7 km a leste) é menor que a PPD e seria substituído.'),
          fig('16_ols_planta.png', 14, 'Superfícies de proteção (Anexo 14 / RBAC 154) em planta: obstáculos ao norte furam a horizontal interna e a cônica.'),
          P('<b>Custo comparado</b> (R$ milhões, 2026): terraplenagem pelo SICRO (escavação e transporte com moto-scraper, 5501712 e, para a onda de 745 m de C1, '
            '5501714; compactação 5502978): prévia 23,5; C1 8,7. Com desapropriação (terra a R$ 65 mil/ha; construções pelo CUB/SP R1-N, 40% ocupado): '
            'sítio de 3000 × 1500 m deslocado para o mínimo de casas, prévia 57,9 e C1 80,6; curva de 75 dB do manual (179 ha), prévia 78,1 e C1 53,7. '
            'O custo não separa os sítios: depende da área desapropriada.'),
          PageBreak()]
    # ------------------------------------------------ 3 etapa 2
    S += [P('3. Etapa 2: modelo, alinhamentos e seção-tipo', 'h1'),
          P('<b>Dados.</b> Terreno: Copernicus GLO-30 (grade de 30 m, precisão vertical < 4 m em 90% dos pontos), 8219 pontos exportados para o Civil 3D '
            '(superfície TN; TN_limpo 0,15 m abaixo). Imagem: mosaico georreferenciado de 4,1 × 3,5 km (1 m/pixel), SIRGAS 2000 / UTM 23S.'),
          P(f'<b>Alinhamento horizontal.</b> A PPD é reta. O eixo "EIXO PPD 06-24" tem 2020 m no rumo 060°: P0 (estaca 0) na extremidade SW da faixa, '
            f'E {f(p.P0[0], 1)} / N {f(p.P0[1], 1)}; PF (estaca 101) em E {f(p.PF[0], 1)} / N {f(p.PF[1], 1)}. Cabeceira 06 na estaca 3 e 24 na estaca 98.'),
          P('<b>Alinhamento vertical.</b> O greide foi otimizado (5 PIVs) para que o corte cubra o aterro corrigido pelo Fh, e as cotas foram arredondadas '
            'ao centímetro e baixadas 1 cm, para não faltar terra com as áreas do Civil 3D.')]
    linhas = [['PIV', 'Estaca', 'Cota (m)', 'Curva L (m)', 'Rampa seguinte', 'R (m)']]
    for k, (e, z, L) in enumerate(PV):
        R = ''
        if 0 < k < len(PV) - 1:
            R = f(L / abs(g[k] - g[k - 1]), 0)
        linhas.append([f'PIV{k}', f'{e / 20:.0f}', f(z), f(L, 0) if L else '—', f'{100 * g[k]:+.3f}%'.replace('.', ',') if k < len(g) else '—', R or '—'])
    S += [tab(linhas, [2.0, 2.0, 2.6, 2.6, 3.4, 2.6]), Spacer(1, 0.2 * cm),
          P(f'Verificações: rampa máxima {f(100 * max(map(abs, g)), 2)}% (limite 1,5%); declividade efetiva '
            f'{f(100 * abs(PV[-1][1] - PV[0][1]) / p.COMP, 2)}% (limite 1,0%); mudança máxima de declividade '
            f'{f(100 * max(abs(g[k] - g[k - 1]) for k in range(1, len(g))), 2)}% (limite 1,5%); raios ≥ 30.000 m (código 4).'),
          fig('05_perfil.png', 16, 'Perfil longitudinal: terreno no eixo e greide acabado.'),
          P('<b>Seção-tipo</b> (simétrica, superfície acabada): PPD de 0 a 22,5 m a −1,5%, pavimento 1,10 m; acostamento de 22,5 a 30 m a −2,5%, '
            'pavimento 0,50 m; faixa de 30 a 150 m a −2,5%, sem pavimento; taludes 1V:1,5H no corte e 1V:2H no aterro até o terreno limpo. '
            'A terraplenagem é medida no topo do subleito (acabado − pavimento).'),
          fig('04_secao_tipo.png', 16, 'Seção-tipo (meia seção).'),
          PageBreak()]
    # ------------------------------------------------ 4 etapa 3
    S += [P('4. Etapa 3: terraplenagem', 'h1'),
          P('<b>Premissas.</b> Limpeza de 0,15 m em toda a largura entre os pés de talude, que vai para bota-fora ou estoque e não entra na compensação; '
            f'as áreas são medidas a partir do TN limpo, então o aterro nunca fica sobre a camada vegetal. Fh = {f(FH)} (adotado, sem ensaios): o aterro corrigido é Fh × aterro.'),
          P('<b>Geologia e o Fh.</b> Pelo mapa geológico do SGB na escala 1:100.000 (folha Pindamonhangaba, SF.23-Y-B-VI, 2020), consultado ao longo do eixo, '
            'a faixa fica sobre a <b>Formação Tremembé</b> (Grupo Taubaté: argilitos verdes, folhelhos e margas de origem lacustre) da estaca 0 à 65 e sobre '
            '<b>depósito aluvionar</b> (cascalho, areia e lama inconsolidada) da estaca 70 ao fim. Os cortes são rasos (até cerca de 5 m), no solo de alteração '
            'argiloso, de 1ª categoria. O Fh = 1,25 é adotado: o balanço fecha exatamente com Fh = 1,26, e cada 0,05 de Fh muda o saldo em cerca de 17 mil m³ '
            '(tabela). Num projeto real, o Fh viria de ensaios (densidade in situ nos cortes e Proctor), os argilitos seriam ensaiados quanto à expansão e o '
            'aterro sobre o aluvião, que coincide com o maior aterro (estacas 70 a 87), pediria sondagem por causa de recalques.'),
          tab([['Fh', '1,15', '1,20', '1,25 (adotado)', '1,30', '1,35'],
               ['Saldo (m³)'] + [f(Vc - x * Va, 0) for x in (1.15, 1.20, 1.25, 1.30, 1.35)],
               ['% do corte'] + [f'{f(100 * (Vc - x * Va) / Vc, 1)}%' for x in (1.15, 1.20, 1.25, 1.30, 1.35)]], [3.0, 2.8, 2.8, 2.8, 2.8, 2.8]),
          Spacer(1, 0.2 * cm),
          P('<b>Seções.</b> 104 linhas de amostragem no Civil 3D (grupo "SL - PPD"): as 102 estacas inteiras e os PCV3/PTV3 (1490 e 1550 m). '
            'Em cada uma, as seções do TN limpo e da plataforma de terraplenagem foram lidas a cada 0,25 m; as áreas de corte e aterro saem dessas linhas.'),
          P('<b>Método das áreas médias.</b>'),
          P('V = (A<sub>1</sub> + A<sub>2</sub>) / 2 × d', 'form'),
          P('Aterro corrigido = Fh × V<sub>aterro</sub>; compensação lateral = menor(V<sub>corte</sub>; Fh·V<sub>aterro</sub>) no trecho; '
            'ordenada de Brückner = Σ (V<sub>corte</sub> − Fh·V<sub>aterro</sub>).', 'form'),
          P('<b>Trecho calculado à mão: estacas 52 → 53</b> (o par de seções mistas com as maiores áreas de corte e aterro ao mesmo tempo). '
            'Dados: corte 286,27 e 231,39 m²; aterro 252,72 e 271,10 m²; d = 20 m. A conta foi feita à mão, em sala, na apresentação; '
            'a planilha (aba "Cálculo à mão") e a tabela abaixo trazem o valor para conferência.'),
          fig('06_secoes.png', 16, 'Seções transversais típicas (terreno limpo, plataforma e taludes).'),
          PageBreak(),
          P('4.1 Memorial de volumes', 'h2'),
          P(f'Áreas do Civil 3D; d em m; volumes em m³. Fh = {f(FH)}. A linha do trecho calculado à mão (52 → 53) está destacada.', 'nota')]
    cab = ['Ponto', 'Estaca', 'Área corte (m²)', 'Área aterro (m²)', 'd', 'V corte', 'V aterro', 'Aterro corr.', 'Comp. lateral', 'Ordenada']
    linhas = [cab]; dest = []
    for i, l in enumerate(LIN):
        linhas.append([l['ponto'] or '', l['estaca'], f(AC[i]), f(AA[i]), f(D[i], 0) if i else '',
                       f(VC[i], 0) if i else '', f(VA[i], 0) if i else '', f(VAC[i], 0) if i else '', f(CL[i], 0) if i else '', f(ORD[i], 0)])
        if l['estaca'].startswith('53 +'):
            dest.append(len(linhas) - 1)
    linhas.append(['<b>Total</b>', '', '', '', '', f'<b>{f(Vc, 0)}</b>', f'<b>{f(Va, 0)}</b>', f'<b>{f(Vac, 0)}</b>', f'<b>{f(CLT, 0)}</b>',
                   f'<b>{f(ORD[-1], 0)}</b>'])
    S += [tab(linhas, [1.4, 1.9, 1.75, 1.75, 0.9, 1.6, 1.6, 1.7, 1.7, 1.7], dest_rows=dest, peq=True), Spacer(1, 0.3 * cm),
          P('4.2 Resumo', 'h2'),
          tab([['Quantidade', 'Volume (m³)'],
               ['Corte', f(Vc, 0)], ['Aterro', f(Va, 0)], [f'Aterro corrigido (× {f(FH)})', f(Vac, 0)],
               ['Saldo (corte − aterro corrigido): bota-fora', f(Vc - Vac, 0)],
               ['Compensação lateral (dentro de cada trecho)', f(CLT, 0)],
               ['Transporte ao longo do eixo (corte − compensação lateral)', f(Vc - CLT, 0)],
               ['Limpeza (0,15 m), bota-fora ou estoque para os taludes', f(LIMP, 0)]], [11, 6], dest_rows=(4,)),
          P(f'O saldo de {f(Vc - Vac, 0)} m³ é {f(100 * (Vc - Vac) / Vc, 1)}% do corte: vem do arredondamento das cotas do greide ao centímetro, '
            '1 cm abaixo do ótimo.'),
          PageBreak()]
    # ------------------------------------------------ 5 Brückner e distribuição
    S += [P('5. Diagrama de Brückner e distribuição', 'h1'),
          fig('07_brueckner.png', 16, f'Áreas por seção e diagrama de Brückner (Fh = {f(FH)}); a ordenada final é o saldo de {f(ORD[-1], 0)} m³.'),
          P('A distribuição usou o programa da aula 8 (diagrama de massas com linhas de compensação entre cruzamentos, MATLAB). '
            'O ótimo com bota-fora e empréstimo a 150 m (7 LCs, momento de transporte de 3,37 × 10⁶ m³·dam) mandaria 63 mil m³ para bota-fora e traria '
            '59 mil de empréstimo, porque o modelo cobra só o transporte. Contando a escavação do empréstimo pelos preços do exercício 6, o ótimo passa a ser '
            '<b>compensar tudo com 2 LCs</b>: momento de transporte de 6,61 × 10⁶ m³·dam e só 4,2 mil m³ de bota-fora. A onda principal leva 79 mil m³ '
            'por 745 m em média.'),
          fig('11_distribuicao.png', 15, 'Diagrama de massas com as duas soluções: compensar tudo (adotada) e o ótimo com bota-fora e empréstimo.'),
          P('<b>Execução, em resumo (aula 9).</b> Limpeza com trator de esteira de lâmina reta; a onda principal (79 mil m³, DMT de 745 m) com moto-scraper '
            'empurrado (SICRO 5501714); as ondas curtas e a compensação lateral com trator de lâmina; regularização com motoniveladora; compactação do aterro '
            'com rolo pé-de-carneiro (solo argiloso) e selagem do topo do subleito com rolo pneumático.'),
          PageBreak()]
    # ------------------------------------------------ 6 corredor
    S += [P('6. Verificação no Civil 3D: corredor com a seção-tipo', 'h1'),
          P('A seção-tipo foi montada como montagem ("PPD 06-24"): pista básica de 22,5 m (−1,5%, profundidade 1,10 m), acostamento básico de 7,5 m '
            '(−2,5%, 0,50 m), link de 120 m a −2,5% e talude 1V:1,5H / 1V:2H até o TN limpo. O corredor ("Corredor PPD") corre a montagem pelo eixo e pelo '
            'greide acabado, a cada 20 m e nos pontos de geometria vertical, e gera as superfícies Top e Datum. O Calcular materiais compara o TN limpo '
            'com a Datum (topo do subleito) nas mesmas 104 linhas de amostragem, com fator de aterro 1,25.'),
          fig('17_c3d_corredor.png', 15, 'Corredor em planta no Civil 3D: linhas de amostragem a cada 20 m e taludes (verde) nas bordas da faixa.'),
          tab([['m³', 'Corredor (Relatório de volume)', 'Memorial', 'Diferença'],
               ['Corte', f(RVc, 0), f(Vc, 0), f'{f(100 * (RVc / Vc - 1), 1)}%'],
               ['Aterro', f(RVa, 0), f(Va, 0), f'{f(100 * (RVa / Va - 1), 1)}%'],
               [f'Aterro corrigido (× {f(FH)})', f(FH * RVa, 0), f(Vac, 0), f'{f(100 * (RVa / Va - 1), 1)}%'],
               ['Saldo', f(RVc - FH * RVa, 0), f(Vc - Vac, 0), f'{f(100 * (RVc - FH * RVa) / RVc, 1)}% do corte']], [5, 4.4, 3.8, 3.8]),
          Spacer(1, 0.2 * cm),
          P('O corte confere com o memorial. O aterro do corredor é 2,7% maior por dois motivos: nas estacas extremas (0 e 101) a seção do corredor é '
            'completa, enquanto a do memorial parou na borda da superfície de projeto; e a superfície Datum, triangulada, suaviza o degrau do pavimento '
            '(1,10 m na pista, 0,50 m no acostamento, zero na faixa). O saldo de −1,8% do corte cabe na precisão do modelo de terreno; para zerá-lo bastaria '
            'baixar o greide cerca de 6 mm (cada milímetro muda o saldo em cerca de 1,4 mil m³). O memorial continua sendo a base do Brückner e da distribuição.'),
          PageBreak(), P('7. Nota de serviço de terraplenagem', 'h1'),
          P('Para cada estaca: cota do terreno natural no eixo, greide acabado e de terraplenagem (topo do subleito), altura no eixo a partir do terreno limpo '
            '(+ corte, − aterro) e, de cada lado, o afastamento do pé de talude (offset) a partir do eixo, se é corte (C) ou aterro (A), e a cota do terreno nesse ponto. '
            'É o que a topografia usa para locar a obra. Arquivo completo: aeroporto_trabalho/Tabelas/nota_servico.csv.', 'nota')]
    cab = ['Estaca', 'Ponto', 'Cota TN (m)', 'Greide acab. (m)', 'Greide terr. (m)', 'h eixo (m)', 'Offset esq. (m)', 'Cota pé esq.', 'Offset dir. (m)', 'Cota pé dir.']
    linhas = [cab]; dest = []
    for r in NS:
        linhas.append([r['estaca'], r['ponto'] or '', f(r['cota_tn']), f(r['greide']), f(r['terrapl']), f'{r["h_eixo"]:+.2f}'.replace('.', ','),
                       f"{f(r['off_esq'])} {'C' if r['tipo_esq'] == 'corte' else 'A'}", f(r['cota_pe_esq']),
                       f"{f(r['off_dir'])} {'C' if r['tipo_dir'] == 'corte' else 'A'}", f(r['cota_pe_dir'])])
        if r['estaca'].startswith(('52 +', '53 +')):
            dest.append(len(linhas) - 1)
    S += [tab(linhas, [1.9, 1.3, 1.6, 1.7, 1.7, 1.4, 1.9, 1.7, 1.9, 1.7], dest_rows=dest, peq=True),
          P('8. Referências', 'h1'),
          P('Notas de aula de GEO-55 (aulas 7, 8 e 9, 2026). · SAC/MInfra; ITA. <i>Manual de Apoio à Prospecção de Sítios Aeroportuários Regionais</i>, 2021. · '
            'ANAC. RBAC 154 (projeto de aeródromos) e RBAC 161 (planos de zoneamento de ruído). · ICAO. Anexo 14, vol. I. · DNIT. SICRO, SP, jul/2026. · '
            'Sinduscon-SP. CUB R1-N, set/2026. · Copernicus DEM GLO-30. · ESA WorldCover 2021. · ERA5 (ECMWF). · OpenStreetMap. · '
            'SGB/CPRM. Carta geológica 1:100.000, folha Pindamonhangaba (SF.23-Y-B-VI), 2020, e Mapa geológico e de recursos minerais da Bacia de Taubaté, 2021 '
            '(serviço GeoSGB, litoestratigrafia 1:100.000, consultado em 16/11/2026).', 'nota')]
    doc.build(S)
    print('memorial:', os.path.abspath(SAIDA))


if __name__ == '__main__':
    main()
