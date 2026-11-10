"""Roteiro de apresentação da prévia do aeroporto (PDF), a partir dos slides e das notas.
Dividido pelas etapas do enunciado (1, 2 e 3); em cada etapa os três integrantes apresentam uma parte,
e cada parte traz as perguntas prováveis da professora com as respostas. Identidade visual do ITA.
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
from reportlab.platypus import BaseDocTemplate, CondPageBreak, Frame, KeepTogether, PageTemplate, Paragraph, Spacer, Table, TableStyle

AQUI = os.path.dirname(os.path.abspath(__file__))
FD = 'C:/Windows/Fonts'
pdfmetrics.registerFont(TTFont('CB', os.path.join(FD, 'cambriab.ttf')))
pdfmetrics.registerFont(TTFont('BS', os.path.join(FD, 'bahnschrift.ttf')))
pdfmetrics.registerFont(TTFont('SE', os.path.join(FD, 'segoeui.ttf')))
pdfmetrics.registerFont(TTFont('SEB', os.path.join(FD, 'segoeuib.ttf')))
pdfmetrics.registerFontFamily('SE', normal='SE', bold='SEB', italic='SE', boldItalic='SEB')
ID = json.load(open(os.path.join(AQUI, 'comum', 'identidade.json'), encoding='utf-8'))
NAVY = colors.HexColor('#13306B'); OURO = colors.HexColor('#C99A06'); CINZA = colors.HexColor('#5B6270')
PAPEL = colors.HexColor('#FBF1CF'); CLARO = colors.HexColor('#EEF0F4')
LOGO = os.path.join(AQUI, 'figuras', 'ita_logo_transparente.png')  # gerado por logo_transparente.py
GRUPO = 'Pedro Feitosa Guttemberg · Guilherme Rodrigues · Gilberto Patri'
ST = {
    'h1': ParagraphStyle('h1', fontName='CB', fontSize=15, leading=19, textColor=NAVY, spaceBefore=6, spaceAfter=8),
    'et': ParagraphStyle('et', fontName='CB', fontSize=14, leading=18, textColor=colors.white, backColor=NAVY, borderPadding=(6, 6, 6, 6),
                         spaceBefore=14, spaceAfter=10),
    'pe': ParagraphStyle('pe', fontName='CB', fontSize=12, leading=15, textColor=NAVY, spaceBefore=10, spaceAfter=4),
    'h2': ParagraphStyle('h2', fontName='SEB', fontSize=9.6, leading=13, textColor=NAVY, spaceBefore=6, spaceAfter=2),
    'p': ParagraphStyle('p', fontName='SE', fontSize=9.2, leading=13, alignment=TA_JUSTIFY, spaceAfter=5, textColor=colors.HexColor('#1E1E1E')),
    'q': ParagraphStyle('q', fontName='SEB', fontSize=9.2, leading=13, textColor=colors.HexColor('#8A6A04'), spaceBefore=3),
    'r': ParagraphStyle('r', fontName='SE', fontSize=9.2, leading=13, alignment=TA_JUSTIFY, leftIndent=10, spaceAfter=4),
    'pq': ParagraphStyle('pq', fontName='SEB', fontSize=9.6, leading=13, textColor=NAVY, backColor=CLARO, borderPadding=4, spaceBefore=8, spaceAfter=4),
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
SL = {}
for i, sid in enumerate(deck['order'], 1):
    t = open(os.path.join(D, 'slides', f'{sid}.html'), encoding='utf-8').read()
    tit = re.search(r'<h[12][^>]*>(.*?)</h[12]>', t, re.S).group(1)
    tit = html.unescape(re.sub(r'<[^>]+>', '', tit)).strip()
    nota = html.unescape(re.search(r'<aside>(.*?)</aside>', t, re.S).group(1)).strip()
    SL[sid] = (i, tit, nota)
N = len(deck['order'])
FIM = SL['proximos'][0]

# ------------------------------------------------------------------ partes e perguntas
ABERTURA = ('Pedro', ['cover', 'requisitos'], [
    ('Por que a PPD tem 1900 m, se o texto do enunciado diz 2300 m?',
     'A figura do enunciado mostra 1900 m dentro de uma faixa de 2020 m, e a professora confirmou 1900 m em 03/11.'),
    ('As declividades usadas não estão muito abaixo dos limites?',
     'Sim, de propósito: o greide foi otimizado para o menor volume. Rampa máxima 0,80% (limite 1,5%), efetiva 0,16% (limite 1,0%), '
     'mudança máxima 1,20% (limite 1,5%).'),
])

ETAPAS = [
    ('Etapa 1 · Identificação do local do sítio', 'etapa1', [
        ('Pedro', ['etapa1', 'metodo', 'regiao'], [
            ('Por que uma busca automática, e não escolher o local olhando o mapa?',
             'Para que a escolha tenha critérios explícitos e verificáveis. Testamos 25 mil centros (a cada 300 m) em 36 rumos (a cada 5°) '
             'com quatro filtros aplicados em sequência: terraplenagem, distância da várzea, superfícies de proteção e entorno.'),
            ('Onde foi feita a busca? No Vale inteiro? No Estado?',
             'Não. A área foi um retângulo de 59 × 53 km em torno de São José dos Campos, até Pindamonhangaba (lat. −23,36° a −22,89°; '
             'long. −45,96° a −45,39°). Esse recorte foi fixado antes da busca, por ser a região do ITA; a busca escolheu o ponto dentro dele. '
             'Nele havia 35 066 centros a cada 300 m; tirando 10 km em volta de SBSJ e SBTA e a várzea, sobraram 25 062.'),
            ('A várzea é mais plana. Por que não construir lá?',
             'Ela daria a menor terraplenagem, mas é a planície de inundação do Paraíba: argila mole e turfa, lençol raso, arrozais e cavas de areia. '
             'Seria preciso trocar solo, drenar e alteiar a plataforma acima da cheia. O sítio escolhido fica 21 m acima do fundo do vale.'),
            ('Por que o rumo da pista segue o vale?',
             'Porque o vale é estreito entre a Mantiqueira e a Serra do Mar. Uma pista atravessada teria morros furando a horizontal interna (+45 m num raio de 4 km) '
             'e a cônica (5%). Só os rumos de 50° a 70°, no eixo do vale, passaram.'),
            ('Que dados foram usados?',
             'Relevo: Copernicus GLO-30 (modelo de superfície de 30 m, medido pelo radar da missão TanDEM-X entre 2011 e 2015). Uso do solo: ESA WorldCover 2021 (10 m). Vento: reanálise ERA5 (2015–2024). '
             'Imagem: Esri World Imagery.'),
            ('Por que não perto de São José dos Campos?',
             'Perto de SJC os locais planos estão na várzea ou têm morros nas superfícies de proteção, e exigimos 10 km de SBSJ e de SBTA. '
             'Só dois locais passaram em todos os critérios.'),
        ]),
        ('Guilherme', ['sitio'], [
            ('Quais são os pontos fracos do sítio?',
             'As cavas de areia a cerca de 1,5 km ao norte atraem aves e pedem um plano de manejo de fauna; e a borda da cidade fica a cerca de 1 km do cone nordeste '
             '(ruído lateral). Há 4% de mata no sítio.'),
            ('Por que não o outro local que passou nos filtros?',
             'O local B (−22,906; −45,406; rumo 25°) tinha uma rodovia cortando a faixa e uma indústria na cabeceira.'),
            ('O sítio cabe na área de 3000 × 1500 m do enunciado?',
             'Sim: o retângulo amarelo da imagem tem 3000 × 1500 m, alinhado à PPD, e contém a faixa de 2020 × 300 m.'),
            ('O sítio pega parte de um bairro?',
             'Pega a ponta de um bairro no canto sul do retângulo amarelo, perto da cabeceira 06: 10,9 ha construídos, 2,4% do sítio (ESA WorldCover, 10 m). '
             'A faixa de 2020 × 300 m, onde há terraplenagem, não tem nada construído; a construção mais próxima fica a cerca de 160 m da borda, '
             'então greide e volumes não mudam. Num projeto real, esse canto seria desapropriado ou o sítio seria deslocado: '
             '470 m para nordeste e 230 m para noroeste, a faixa continua dentro e sobram só 0,45 ha construídos. '
             'O bairro perto da pista também entraria no estudo de ruído.'),
            ('Que solo se espera no sítio?',
             'Latossolo vermelho-amarelo, profundo e poroso, sobre os sedimentos do Grupo Taubaté (argilas, siltes e areias). É solo de 1ª categoria '
             '(escavável com lâmina e scraper). Esse solo é a base da escolha do Fh = 1,25 na etapa 3.'),
            ('E o acesso?',
             'Pela Via Dutra, a poucos quilômetros, e pela cidade de Pindamonhangaba.'),
        ]),
        ('Gilberto', ['vento', 'ols'], [
            ('O vento não deveria definir o rumo da pista?',
             'Deveria, se restringisse. Com 87 672 horas de ERA5, a cobertura passa de 99,9% em qualquer rumo, até com limite de 10 kt, e o Anexo 14 pede 95%. '
             'Mesmo assim, 060° coincide com o vento predominante de ENE.'),
            ('Como se calcula a cobertura?',
             'Para cada hora, a componente de vento cruzado é V·sen(ângulo entre vento e pista). A cobertura é a porcentagem de horas em que ela fica abaixo do limite '
             '(20 kt para pista de 1500 m ou mais, Anexo 14).'),
            ('O que são as superfícies limitadoras de obstáculos?',
             'Superfícies imaginárias do Anexo 14 / RBAC 154 que nenhum obstáculo pode furar: aproximação (2% e 2,5%), transição (14,3%), horizontal interna '
             '(+45 m num raio de 4 km) e cônica (5%). Usamos código 4, precisão CAT I.'),
            ('Alguma coisa furou as superfícies?',
             'No máximo 2 m em 3 ha, provavelmente árvores: o Copernicus é modelo de superfície, então árvores e prédios aparecem como terreno, o que é conservador.'),
            ('A limitação do ERA5?',
             'É uma reanálise em grade de cerca de 30 km. O ideal seria uma estação local, como o METAR de SBTA.'),
        ]),
    ]),
    ('Etapa 2 · Modelo da área, alinhamentos e seção-tipo', 'etapa2', [
        ('Pedro', ['etapa2', 'civil3d'], [
            ('Como o terreno entrou no Civil 3D?',
             'Os 8220 nós do modelo Copernicus, convertidos para UTM 23S (SIRGAS 2000), foram triangulados e importados como superfície por LandXML. '
             'É a mesma triangulação usada nos cálculos, então o Civil 3D e o memorial trabalham sobre o mesmo terreno.'),
            ('Como a imagem foi georreferenciada?',
             'Mosaico do Esri World Imagery com 1 m de pixel, reprojetado para UTM 23S e inserido com o arquivo de coordenadas (.jgw).'),
            ('Por que o alinhamento horizontal é uma reta só?',
             'Porque a PPD é reta. O eixo tem 2020 m no rumo 060°, com o P0 na extremidade SW da faixa; as cabeceiras ficam nas estacas 3 e 98.'),
            ('O modelo de terreno é confiável?',
             'Para esta fase, sim; para obra, não. O Copernicus tem grade de 30 m, precisão vertical absoluta menor que 4 m (90% dos pontos) e é modelo '
             'de superfície: árvores e construções aparecem como terreno. O sítio tem só 4% de mata, então esse efeito é pequeno. Ele também é um retrato '
             'de 2011 a 2015 (radar TanDEM-X): o que mudou no terreno depois não aparece. Num projeto real, seria trocado por levantamento topográfico '
             '(ou LiDAR) e sondagens.'),
            ('Por que não há corredor (assembly)?',
             'A superfície de projeto foi montada a partir da seção-tipo e importada por LandXML, com a mesma geometria. O corredor e o Compute Materials '
             'estão programados para a entrega de 17/11.'),
        ]),
        ('Guilherme', ['secaotipo'], [
            ('Como o pavimento entra no volume?',
             'Como no slide “Estrutura do pavimento” da aula 7: a espessura do pavimento é considerada. As seções são medidas no greide de terraplenagem, '
             'que é o greide de projeto menos 1,10 m na PPD e menos 0,50 m no acostamento. O volume vai até o topo do subleito.'),
            ('Por que o acostamento a 2,5%?',
             'A figura do enunciado dá 1,5% só nos 22,5 m da pista; daí para fora a faixa é 2,5%, e o acostamento está dentro dessa parte.'),
            ('De onde vêm os taludes?',
             'O enunciado não dá. Adotamos 1V:1,5H no corte e 1V:2H no aterro, valores usuais para solo coesivo. Por isso estão na lista de perguntas à professora.'),
            ('A faixa de 300 m inteira precisa ser nivelada?',
             'Sim. Seguimos a figura do enunciado: 2,5% em toda a largura de 300 m. A nota de serviço da aula 7, que nivela só ±75 m, '
             'é apenas um exemplo de formato e não vale para este projeto.'),
        ]),
        ('Gilberto', ['perfil'], [
            ('Como o greide foi escolhido?',
             'Por otimização: as incógnitas são as cotas de 5 PIVs (0, 500, 1000, 1520 e 2020 m), e o programa minimiza corte + aterro com as restrições do '
             'enunciado e do Anexo 14, exigindo que o corte cubra o aterro corrigido pelo Fh.'),
            ('O que é a declividade efetiva?',
             '(cota máxima − cota mínima ao longo da PPD) / comprimento da PPD. Aqui dá 0,16%, para um limite de 1,0%.'),
            ('De onde vêm o raio de 30 000 m e o limite de 0,8%?',
             'Do Anexo 14, para código 4: raio mínimo de curva vertical de 30 000 m (L = R·|Δi|) e rampa de no máximo 0,8% no primeiro e no último quarto da pista.'),
            ('Por que só 5 PIVs?',
             'Com 7 ou 9 PIVs o volume cai só cerca de 2%, e cada PIV a mais é uma curva vertical a mais. Ficamos com 3 curvas verticais.'),
            ('Quais são as rampas?',
             '−0,432%, +0,067%, +0,395% e −0,800%; o último trecho tem 0,8% porque está no último quarto da PPD.'),
        ]),
    ]),
    ('Etapa 3 · Terraplenagem', 'etapa3', [
        ('Pedro', ['etapa3', 'secoes', 'c3dsecoes'], [
            ('Quantas seções há, e onde?',
             '104: as 102 estacas inteiras (0 a 101) e os PCV/PTV que não caem em estaca inteira (950 e 1050 m). As cabeceiras coincidem com as estacas 3 e 98.'),
            ('As áreas são mesmo do Civil 3D?',
             'Sim. São 104 linhas de amostragem com seções do terreno limpo e da plataforma, lidas a cada 0,25 m. Um cálculo independente dá 0,04% de diferença '
             'no corte e 0,05% no aterro.'),
            ('Como a camada vegetal entra?',
             'Há uma superfície do terreno 15 cm abaixo do natural (TN_limpo). As áreas são medidas a partir dela, então o aterro nunca fica sobre a camada vegetal. '
             'A limpeza, 0,15 m × largura entre os pés de talude, é calculada à parte e não entra na compensação.'),
            ('O que é uma seção mista?',
             'Uma seção com corte e aterro ao mesmo tempo. Com 300 m de largura, a plataforma corta um morro de um lado e aterra um vale do outro.'),
        ]),
        ('Guilherme', ['volumes', 'mao'], [
            ('Por que Fh = 1,25, e não o 1,1 da aula?',
             'O Fh é propriedade do solo: Fh = γs compactado / γs in situ. O 1,1 era dado do exercício. Nosso solo é latossolo poroso, com densidade natural baixa, '
             'que adensa bastante na compactação; a faixa usual fica entre 1,2 e 1,3. Num projeto real ele viria de ensaio in situ (frasco de areia) e Proctor.'),
            ('O que é a compensação lateral?',
             'É o volume que se resolve dentro do próprio trecho: corte de um lado da seção indo para o aterro do outro, sem transporte ao longo do eixo. '
             'Na planilha, é o menor valor entre o corte e o aterro corrigido de cada trecho. Aqui são 534 mil m³; só 693 mil m³ viajam ao longo do eixo.'),
            ('Por que o saldo é +91 m³ e não zero?',
             'O greide foi otimizado nas estacas inteiras e depois baixado 3 mm para que o memorial, com as seções extras, também feche sem déficit. '
             '91 m³ em 1,2 milhão é praticamente zero, e vão para bota-fora.'),
            ('Áreas médias ou prismoide?',
             'O enunciado pede áreas médias: V = (A₁ + A₂)/2 × d. O prismoide usa a área da seção do meio; as áreas médias superestimam um pouco, '
             'principalmente na passagem de corte para aterro.'),
            ('Na tabela da aula o Fh multiplica a área. Muda alguma coisa?',
             'Não. O volume é linear na área, então aplicar o Fh na área de aterro ou no volume de aterro dá o mesmo resultado.'),
            ('O volume não é grande demais?',
             'É grande porque a faixa inteira de 300 m foi nivelada, num terreno ondulado: cerca de 650 mil m² de plataforma, com uns 1,9 m de corte médio.'),
        ]),
        ('Gilberto', ['brueckner', 'distribuicao', 'equipamentos'], [
            ('O diagrama fecha em zero. Então não há transporte?',
             'Há. Fechar em zero só quer dizer que corte e aterro corrigido se equilibram no total. As ondas mostram o transporte ao longo do eixo, com DMTs de 42 a 248 m.'),
            ('O que são LC, DMT e momento de transporte?',
             'A LC é a linha horizontal sobre o diagrama; entre dois cruzamentos, corte e aterro se compensam. Acima dela a terra anda no sentido do estaqueamento; '
             'abaixo, no sentido contrário. DMT = área da onda / altura da onda. Momento de transporte = Σ V·DMT + volume externo × 150 m, em m³·dam.'),
            ('Por que vocês não ficaram com o ótimo do programa?',
             'O ótimo com bota-fora e empréstimo a 150 m (12,32 milhões de m³·dam) manda 144 mil m³ para bota-fora e traz 143 mil de empréstimo, porque o modelo '
             'cobra só o transporte. Contando a escavação do empréstimo (exercício 6: R$ 3,20/m³ e R$ 1,60/(m³·km), ou seja, 2 km de transporte por m³), '
             'o ótimo passa a ser a LC única do P0 ao PF, que compensa tudo (14,34 milhões de m³·dam).'),
            ('De onde vem a DMT externa de 150 m?',
             'Da aula 8, para empréstimos e bota-foras eventuais.'),
            ('Por que moto-scraper?',
             'Solo de 1ª categoria, plataforma larga e plana e DMTs de 160 a 250 m: o moto-scraper escava, carrega, transporta e espalha numa operação só (aula 9). '
             'A onda curta, de 42 m, pode ser feita com trator de lâmina.'),
            ('Por que rolo pé-de-carneiro?',
             'Porque o solo é coesivo (argiloso): as patas compactam do fundo para o topo da camada. Ele não serve para solo não coesivo; nas lentes de areia, '
             'rolo vibratório. O topo do subleito é selado com rolo pneumático.'),
        ]),
    ]),
]
FECHAMENTO = ('Pedro', ['proximos'], [])
ASSUNTO = {'etapa1': 'método da busca e a região', 'sitio': 'o sítio escolhido', 'vento': 'vento e superfícies de proteção',
           'etapa2': 'imagem, superfícies e alinhamento horizontal no Civil 3D', 'secaotipo': 'seção-tipo e espessura do pavimento',
           'perfil': 'alinhamento vertical (greide otimizado)', 'etapa3': 'seções transversais no Civil 3D',
           'volumes': 'volumes, Fh, compensação lateral e conta à mão', 'brueckner': 'diagrama de massas, distribuição e equipamentos'}


def rodape(canvas, doc):
    canvas.saveState()
    canvas.setFont('BS', 7.5); canvas.setFillColor(CINZA)
    canvas.drawString(2 * cm, 1.2 * cm, 'ITA · Engenharia Civil-Aeronáutica · GEO-55 · Aeroporto em Pindamonhangaba · roteiro da prévia · 10/11/2026')
    canvas.drawRightString(19 * cm, 1.2 * cm, str(doc.page))
    canvas.setStrokeColor(OURO); canvas.setLineWidth(1.5); canvas.line(2 * cm, 27.6 * cm, 19 * cm, 27.6 * cm)
    canvas.drawImage(LOGO, 15.4 * cm, 27.75 * cm, width=3.6 * cm, height=3.6 * cm * 1032 / 2700, mask='auto')
    canvas.setFont('CB', 9); canvas.setFillColor(NAVY); canvas.drawString(2 * cm, 27.9 * cm, ID['instituicao'])
    canvas.restoreState()


def faixa(ids):
    nums = [SL[s][0] for s in ids]
    return f'{min(nums)}' if len(nums) == 1 else f'{min(nums)} a {max(nums)}'


def parte(quem, ids, perg):
    out = []
    for k, s in enumerate(ids):
        i, tit, nota = SL[s]
        cab = [P(f'{quem} · slides {faixa(ids)}', 'pe')] if k == 0 else []
        out.append(KeepTogether(cab + [P(f'Slide {i} · {tit}', 'h2'), P(nota)]))
    if perg:
        cab = P(f'Perguntas prováveis sobre esta parte ({quem})', 'pq')
        for k, (q, r) in enumerate(perg):
            out.append(KeepTogether(([cab] if k == 0 else []) + [P(q, 'q'), P(r, 'r')]))
    return out


def main(saida):
    doc = BaseDocTemplate(saida, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2.4 * cm, bottomMargin=2 * cm,
                          title='Roteiro - Aeroporto (prévia)', author=GRUPO)
    doc.addPageTemplates([PageTemplate(id='p', frames=[Frame(2 * cm, 1.8 * cm, 17 * cm, 25.4 * cm)], onPage=rodape)])
    S = [P('Roteiro de apresentação · Aeroporto em Pindamonhangaba (prévia)', 'h1'), P(f'<b>Grupo:</b> {GRUPO}'),
         P(f'{N} slides, divididos nas três etapas do enunciado. Em cada etapa os três apresentam uma parte, e cada etapa abre com um slide próprio. '
           'Apresentação: https://claude.ai/artifact/8Ugecg9baS44AKMVL9Zja2 (compartilhada por link).', 'pl')]
    tab = [[Paragraph('Etapa', ST['celb']), Paragraph('Pedro', ST['celb']), Paragraph('Guilherme', ST['celb']), Paragraph('Gilberto', ST['celb'])]]
    tab.append([Paragraph('Abertura', ST['cel']), Paragraph(f'slides {faixa(ABERTURA[1])}', ST['cel']), Paragraph('—', ST['cel']), Paragraph('—', ST['cel'])])
    for nome, _, partes in ETAPAS:
        lin = [Paragraph(nome.split(' · ')[0], ST['cel'])]
        for q, ids, _ in partes:
            assunto = ASSUNTO[ids[0]]
            lin.append(Paragraph(f'<b>slides {faixa(ids)}</b><br/>{assunto}', ST['cel']))
        tab.append(lin)
    tab.append([Paragraph('Fechamento', ST['cel']), Paragraph(f'slide {faixa(FECHAMENTO[1])}', ST['cel']), Paragraph('—', ST['cel']), Paragraph('—', ST['cel'])])
    t = Table(tab, colWidths=[2.4 * cm, 4.87 * cm, 4.87 * cm, 4.86 * cm])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), NAVY), ('LINEBELOW', (0, 0), (-1, -1), 0.4, colors.HexColor('#C9CFDB')),
                           ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4)]))
    S += [Spacer(1, 4), t, Spacer(1, 6)]
    fims = []
    for nome, _, partes in ETAPAS:
        ult = max(SL[s][0] for _, ids, _ in partes for s in ids)
        fims.append(f'{nome.split(" · ")[0]}: termina no slide {ult}')
    S += [P('<b>Se a professora pedir só até uma etapa:</b> ' + '; '.join(fims) + f'. Depois, pule para o slide {FIM} (o que falta e as perguntas à professora).', 'dest'),
          P('<b>Mensagem central:</b> o sítio saiu de uma busca com critérios explícitos (terreno, várzea, superfícies de proteção, entorno e vento). '
            'O modelo está todo no Civil 3D; o greide foi otimizado para o corte pagar o aterro corrigido pelo Fh de 1,25, adotado para o solo do sítio; '
            'e a distribuição de massas foi otimizada com o programa da aula 8. O volume é grande porque a faixa inteira de 300 m foi nivelada: '
            'é a principal pergunta para a professora.', 'dest')]
    S += [P('Abertura', 'et')] + parte(*ABERTURA)
    for nome, _, partes in ETAPAS:
        S += [CondPageBreak(6 * cm), P(nome, 'et')]
        for q, ids, perg in partes:
            S += parte(q, ids, perg)
    S += [P('Fechamento', 'et')] + parte(*FECHAMENTO)
    doc.build(S)
    print('ok', saida, N, 'slides')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, '..', 'Roteiro_aeroporto.pdf'))
