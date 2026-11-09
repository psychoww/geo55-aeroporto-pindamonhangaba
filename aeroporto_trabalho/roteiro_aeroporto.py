"""Roteiro de apresentação da prévia do aeroporto (PDF), a partir dos slides e das notas.
Mesmo formato do roteiro do traçado 3 (divisão entre os integrantes + perguntas prováveis), na identidade visual do ITA.
Uso: python roteiro_aeroporto.py ../Roteiro_aeroporto.pdf"""
import html
import json
import os
import re
import sys
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, Image, KeepTogether, PageTemplate, Paragraph, Spacer, Table, TableStyle

AQUI = os.path.dirname(os.path.abspath(__file__))
FD = 'C:/Windows/Fonts'
pdfmetrics.registerFont(TTFont('CB', os.path.join(FD, 'cambriab.ttf')))
pdfmetrics.registerFont(TTFont('BS', os.path.join(FD, 'bahnschrift.ttf')))
pdfmetrics.registerFont(TTFont('SE', os.path.join(FD, 'segoeui.ttf')))
pdfmetrics.registerFont(TTFont('SEB', os.path.join(FD, 'segoeuib.ttf')))
pdfmetrics.registerFontFamily('SE', normal='SE', bold='SEB', italic='SE', boldItalic='SEB')
ID = json.load(open(os.path.join(AQUI, 'comum', 'identidade.json'), encoding='utf-8'))
NAVY = colors.HexColor('#13306B'); OURO = colors.HexColor('#C99A06'); CINZA = colors.HexColor('#5B6270')
PAPEL = colors.HexColor('#FBF1CF')
LOGO = os.path.join(AQUI, 'figuras', 'ita_logo_transparente.png')  # gerado por logo_transparente.py
GRUPO = 'Pedro Feitosa Guttemberg · Guilherme Rodrigues · Gilberto Patri'
ST = {
    'h1': ParagraphStyle('h1', fontName='CB', fontSize=15, leading=19, textColor=NAVY, spaceBefore=6, spaceAfter=8),
    'h2': ParagraphStyle('h2', fontName='CB', fontSize=11, leading=14, textColor=NAVY, spaceBefore=8, spaceAfter=3),
    'p': ParagraphStyle('p', fontName='SE', fontSize=9.2, leading=13, alignment=TA_JUSTIFY, spaceAfter=5, textColor=colors.HexColor('#1E1E1E')),
    'dest': ParagraphStyle('dest', fontName='SEB', fontSize=9.2, leading=13, textColor=NAVY, backColor=PAPEL, borderPadding=6,
                           spaceBefore=6, spaceAfter=10),
    'pl': ParagraphStyle('pl', fontName='SE', fontSize=9.2, leading=13, spaceAfter=5),
    'cel': ParagraphStyle('cel', fontName='SE', fontSize=8.6, leading=11),
    'celb': ParagraphStyle('celb', fontName='SEB', fontSize=8.6, leading=11, textColor=colors.white),
}


def P(t, k='p'):
    return Paragraph(t, ST[k])


D = os.path.join(AQUI, 'apresentacao_deck', 'project')
deck = json.load(open(os.path.join(D, 'deck.json'), encoding='utf-8'))
slides = []
for sid in deck['order']:
    t = open(os.path.join(D, 'slides', f'{sid}.html'), encoding='utf-8').read()
    tit = re.search(r'<h[12][^>]*>(.*?)</h[12]>', t, re.S).group(1)
    tit = html.unescape(re.sub(r'<[^>]+>', '', tit)).strip()
    nota = html.unescape(re.search(r'<aside>(.*?)</aside>', t, re.S).group(1)).strip()
    slides.append((sid, tit, nota))

# divisão: Pedro = enunciado e sítio (1–7); Guilherme = modelo no Civil 3D, seção-tipo, greide, seções (8–12);
# Gilberto = volumes, cálculo à mão, Brückner e próximos passos (13–16)
n = len(slides)
A, B = deck['order'].index('ols') + 1, deck['order'].index('c3dsecoes') + 1
PARTES = [('Pedro', 1, A, 'o enunciado e a escolha do sítio (método, região, sítio, vento e obstáculos)'),
          ('Guilherme', A + 1, B, 'o modelo no Civil 3D, a seção-tipo, o greide e as seções'),
          ('Gilberto', B + 1, n, 'os volumes, o cálculo à mão, o diagrama de massas e os próximos passos')]

PERG = [
    ('Por que Pindamonhangaba, e não perto de São José dos Campos?',
     'Fizemos uma busca automática no Vale do Paraíba, com centros a cada 300 m e rumos a cada 5°. Perto de SJC, os locais planos estão na várzea ou '
     'têm morros nas superfícies de proteção. Também exigimos 10 km de SBSJ e de SBTA. O sítio de Pindamonhangaba foi um dos dois que passaram em todos os critérios.'),
    ('A várzea é mais plana. Por que não construir lá?',
     'Ela daria a menor terraplenagem, mas é a planície de inundação do Paraíba: argila mole e turfa, lençol raso, arrozais e cavas de areia, além da APA do '
     'Banhado perto de SJC. Seria preciso trocar solo, drenar e alteiar a plataforma acima da cheia. O sítio escolhido fica 21 m acima do fundo do vale.'),
    ('O vento não deveria definir o rumo da pista?',
     'Deveria, se restringisse. Com 10 anos de ERA5 (87 672 h), a cobertura passa de 99,9% em qualquer rumo, até com limite de 10 kt, e o Anexo 14 pede 95%. '
     'O rumo 060° ainda coincide com o vento predominante de ENE. Limitação: o ERA5 é uma grade de ~30 km; o ideal é o METAR de SBTA.'),
    ('O que são as superfícies limitadoras de obstáculos?',
     'São superfícies imaginárias do Anexo 14 / RBAC 154 que nenhum obstáculo pode furar: aproximação (2% e 2,5%), transição (14,3%), horizontal interna '
     '(+45 m num raio de 4 km) e cônica (5%). Verificamos todas contra o modelo de superfície; o máximo foi 2 m em 3 ha, provavelmente árvores.'),
    ('O volume de 1,15 milhão de m³ de corte não é grande demais?',
     'É grande porque nivelamos a faixa inteira de 300 m a 2,5%, num terreno ondulado. A plataforma ocupa cerca de 650 mil m², o que dá uns 1,8 m de corte '
     'médio. O Anexo 14 só exige nivelar a parte central da faixa (da ordem de 75 a 105 m de cada lado do eixo); se a professora aceitar, o volume cai bastante. Por isso a pergunta no último slide.'),
    ('O modelo de terreno é confiável?',
     'O Copernicus GLO-30 é um modelo de superfície de 30 m: árvores e construções aparecem como terreno. O sítio tem só 4% de mata, então o efeito é pequeno, '
     'mas num projeto real ele seria trocado por levantamento topográfico (ou LiDAR) e sondagens.'),
    ('Por que o pavimento fica fora do volume?',
     'Foi a regra da aula 7: a terraplenagem vai até o topo do subleito. As seções são medidas no greide de terraplenagem, que é o greide de projeto menos '
     '1,10 m na PPD e menos 0,50 m no acostamento. A limpeza de 15 cm entra à parte e vai para bota-fora.'),
    ('As áreas são mesmo do Civil 3D?',
     'Sim. Criamos 106 linhas de amostragem com seções do TN limpo e da plataforma, e lemos cada seção a cada 0,25 m. Um cálculo independente, com o mesmo terreno '
     'e a mesma seção-tipo, dá 0,06% de diferença no total.'),
    ('Por que não há corredor (assembly) no Civil 3D?',
     'A superfície de projeto foi montada a partir da seção-tipo e importada por LandXML, que dá exatamente a mesma geometria. O corredor com a assembly da '
     'seção-tipo e a tabela de volumes do próprio Civil 3D (Compute Materials) estão programados para a entrega de 17/11.'),
    ('De onde vêm o raio de 30 000 m e o limite de 0,8%?',
     'Do Anexo 14, para pistas de código 4: raio mínimo de curva vertical de 30 000 m e rampa de no máximo 0,8% no primeiro e no último quarto da pista. O enunciado '
     'só dá 1,5% de rampa, 1,0% de declividade efetiva e 1,5% de mudança; usamos o Anexo como complemento.'),
    ('Por que só 5 PIVs no greide?',
     'Testamos 5, 7 e 9 PIVs. Com mais PIVs o volume cai só 2% (2,20 → 2,15 milhões de m³ de corte + aterro), e cada PIV a mais é uma curva vertical a mais. '
     'Ficamos com o mais simples: 3 curvas verticais.'),
    ('O diagrama de massas fecha em zero. Então não há transporte?',
     'Há, e bastante. Fechar em zero só quer dizer que corte e aterro corrigido se equilibram no total. A onda entre 1000 e 1800 m mostra que o morro do meio abastece os aterros vizinhos. '
     'As linhas de compensação, a DMT e o momento de transporte ficam para a entrega final.'),
]


def rodape(canvas, doc):
    canvas.saveState()
    canvas.setFont('BS', 7.5); canvas.setFillColor(CINZA)
    canvas.drawString(2 * cm, 1.2 * cm, 'ITA · Engenharia Civil-Aeronáutica · GEO-55 · Aeroporto em Pindamonhangaba · roteiro da prévia · 10/11/2026')
    canvas.drawRightString(19 * cm, 1.2 * cm, str(doc.page))
    canvas.setStrokeColor(OURO); canvas.setLineWidth(1.5); canvas.line(2 * cm, 27.6 * cm, 19 * cm, 27.6 * cm)
    canvas.drawImage(LOGO, 15.4 * cm, 27.75 * cm, width=3.6 * cm, height=3.6 * cm * 1032 / 2700, mask='auto')
    canvas.setFont('CB', 9); canvas.setFillColor(NAVY); canvas.drawString(2 * cm, 27.9 * cm, ID['instituicao'])
    canvas.restoreState()


def main(saida):
    doc = BaseDocTemplate(saida, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2.4 * cm, bottomMargin=2 * cm,
                          title='Roteiro - Aeroporto (prévia)', author=GRUPO)
    doc.addPageTemplates([PageTemplate(id='p', frames=[Frame(2 * cm, 1.8 * cm, 17 * cm, 25.4 * cm)], onPage=rodape)])
    S = [P('Roteiro de apresentação · Aeroporto em Pindamonhangaba (prévia)', 'h1'), P(f'<b>Grupo:</b> {GRUPO}'),
         P(f'Duração sugerida: 15 a 20 minutos para {n} slides. Apresentação: '
           'https://claude.ai/artifact/8Ugecg9baS44AKMVL9Zja2 (compartilhar pelo menu Share antes de abrir em outro computador).', 'pl')]
    tab = [[Paragraph('Quem', ST['celb']), Paragraph('Slides', ST['celb']), Paragraph('Assunto', ST['celb'])]]
    for q, a, b, assunto in PARTES:
        tab.append([Paragraph(f'<b>{q}</b>', ST['cel']), Paragraph(f'{a} a {b}', ST['cel']), Paragraph(assunto, ST['cel'])])
    t = Table(tab, colWidths=[3 * cm, 2.2 * cm, 11.8 * cm])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), NAVY), ('LINEBELOW', (0, 0), (-1, -1), 0.4, colors.HexColor('#C9CFDB')),
                           ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4)]))
    S += [Spacer(1, 4), t, Spacer(1, 6),
          P('<b>Mensagem central:</b> o sítio saiu de uma busca com critérios explícitos (terreno, várzea, superfícies de proteção, entorno e vento). '
            'O modelo está todo no Civil 3D, e o greide foi otimizado para o corte pagar exatamente o aterro corrigido (Fh = 1,1). '
            'O volume é grande porque a faixa inteira de 300 m foi nivelada: é a principal pergunta para a professora.', 'dest')]
    for i, (sid, tit, nota) in enumerate(slides, 1):
        quem = next(q for q, a, b, _ in PARTES if a <= i <= b)
        S.append(KeepTogether([P(f'Slide {i} · {tit}  <font color="#5B6270">({quem})</font>', 'h2'), P(nota)]))
    S += [Spacer(1, 8), P('Perguntas prováveis e respostas', 'h1')]
    for q, r in PERG:
        S.append(KeepTogether([P(f'<b>{q}</b>'), P(r)]))
    doc.build(S)
    print('ok', saida, n, 'slides')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, '..', 'Roteiro_aeroporto.pdf'))
