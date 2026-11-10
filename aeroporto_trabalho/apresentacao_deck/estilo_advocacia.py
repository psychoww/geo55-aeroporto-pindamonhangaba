"""Aplica aos slides a identidade visual do modelo "Apresentação Advocacia Básico Azul e Bege" (../../Apresentação
Advocacia Básico Azul e Bege.pptx), no lugar da identidade ITA da prévia.

Do modelo (cores lidas do XML; fonte Anaphora é paga/embutida, trocada por Spectral do Google Fonts):
  índigo #33335B (blocos de título, texto), marfim #FFFBF5 (fundo), ardósia #273348 (texto corrido), cinza #9B9B9B
  (linhas finas), lavanda = índigo a ~53% sobre o marfim (#9F9DB6: barras e molduras deslocadas), azuis-petróleo
  #147699 / #006A78 / #88C0E6 (números de etapa); títulos em caixa alta dentro de um bloco índigo, com uma linha
  cinza saindo dele; pequeno bloco índigo no rodapé; fotos em preto e branco.

Lê os slides originais de slides_ita/ (cópia feita na primeira execução) e escreve em project/slides/.
Uso: python estilo_advocacia.py
"""
import os
import re
import shutil
import sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from montar_pasta_apresentacao import BLOBS, FIG  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(AQUI, 'slides_ita')
DEST = os.path.join(AQUI, 'project', 'slides')
if not os.path.isdir(ORIG):
    shutil.copytree(DEST, ORIG)

IND, MARF, ARD, CINZA, LAV, TINTA = '#33335B', '#FFFBF5', '#273348', '#9B9B9B', '#9F9DB6', '#F1EBDF'
FONTE = "'Spectral', Georgia, serif"
ESCUROS = {'etapa1', 'etapa2', 'etapa3', 'proximos'}          # continuam escuros (índigo)
CLAREAR = {'civil3d', 'c3dsecoes'}                            # eram escuros; passam a marfim
LOGO = '/_blob/3603ec8169e4121cda33e4e85919be84'
SITIO = '/_blob/434ea1a0958da3d424b5d0fc7cf23f86'   # figuras/15_capa_sitio.png (sem eixos)

MAPA = {  # cores ITA → modelo (depois de tratar fundos de seção e de cartões)
    '#13306B': IND, '#0B1F4A': '#26264A', '#F8F6EF': MARF, '#EEF0F4': TINTA, '#E0C25A': '#C8C5DA',
    '#8A6A04': IND, '#D6DCEB': '#DCD9E8', '#3F4654': ARD, '#5B6270': '#6E6E80', '#1E1E1E': ARD,
    '#C99A06': CINZA, '#1F4FD8': '#147699',
}
NUM_CORES = [('#147699', MARF), (ARD, MARF), ('#88C0E6', IND), ('#006A78', MARF)]


def cabecalho(m, escuro):
    kicker, h2style, titulo = m.group(3), m.group(4), m.group(5)
    sz = int(re.search(r'font-size:(\d+)px', h2style).group(1))
    sz = {96: 80, 64: 54, 56: 48}.get(sz, sz)
    if escuro:
        bg, fg, linha, cor = MARF, IND, '#8F8CA8', MARF
    else:
        bg, fg, linha, cor = IND, MARF, CINZA, IND
    return (f'<div style="display:flex;align-items:center">'
            f'<p style="font-size:30px;letter-spacing:4px;text-transform:uppercase;color:{fg};background:{bg};'
            f'padding:12px 32px 8px 32px;white-space:nowrap;font-weight:500">{kicker}</p>'
            f'<div style="flex:1;height:2px;background:{linha}"></div></div>\n'
            f'<h2 style="font-family:{FONTE};font-size:{sz}px;font-weight:500;line-height:1.12;color:{cor}">{titulo}</h2>')


def decoracao(escuro):
    barra = '#6B6990' if escuro else LAV
    aba = LAV if escuro else IND
    return (f'<div style="position:absolute;left:0px;top:330px;width:40px;height:420px;background:{barra}"></div>\n'
            f'<div style="position:absolute;left:1592px;top:1016px;width:200px;height:64px;background:{aba}"></div>\n')


def estiliza(nome, s):
    escuro = nome in ESCUROS
    if nome in CLAREAR:
        s = s.replace('background:#13306B;color:#F8F6EF', f'background:{MARF};color:{IND}', 1)
        for a, b in (('#F8F6EF', IND), ('#D6DCEB', ARD), ('#E0C25A', IND)):
            s = re.sub(a, b, s, flags=re.I)
    # fundo da seção: conteúdo sempre marfim; escuros em índigo
    s = re.sub(r'(<section[^>]*style="background:)#(?:EEF0F4|F8F6EF)', r'\g<1>' + MARF, s, count=1)
    # cartões: tinta bege, sem faixa colorida no topo
    s = re.sub(r';border-(?:top|left):6px solid #[0-9A-Fa-f]{6}', '', s)
    s = re.sub(r'(<div style="[^"]*background:)#(?:F8F6EF|EEF0F4)', r'\g<1>' + TINTA, s)
    # cabeçalho: rótulo → bloco índigo + linha; título serifado
    s = re.sub(r'<p style="font-size:(\d+)px;color:#(8A6A04|E0C25A);letter-spacing:\dpx;text-transform:uppercase;font-weight:600">(.*?)</p>\s*'
               r'<h2 style="([^"]*)">(.*?)</h2>', lambda m: cabecalho(m, escuro), s, count=1, flags=re.S)
    # números das etapas (slide método): quadrados coloridos, como no modelo
    k = iter(range(10))
    def num(m):
        bg, fg = NUM_CORES[next(k) % 4]
        return (f'<p style="font-family:{FONTE};font-size:56px;font-weight:500;color:{fg};background:{bg};'
                f'padding:0px 26px;align-self:flex-start">{m.group(1)}</p>')
    s = re.sub(r"<p style=\"font-family:'Caladea', Cambria, Georgia, serif;font-size:64px;font-weight:700;color:#13306B\">(\d)</p>", num, s)
    # fontes
    s = s.replace("'Caladea', Cambria, Georgia, serif", FONTE).replace("'Barlow', Arial, sans-serif", FONTE)
    s = s.replace('font-weight:700', 'font-weight:600')
    # rodapé: mais curto, para caber o bloco índigo
    s = re.sub(r'(<p style="position:absolute;left:128px;bottom:56px;font-size:24px;color:#[0-9A-Fa-f]{6};width:)1664px', r'\g<1>1420px', s)
    # ajustes de espaço (Spectral é mais larga que a Caladea)
    if nome == 'distribuicao':
        s = s.replace('width:1024px;height:560px', 'width:1024px;height:470px')
        s = s.replace('; DMTs das ondas de 42 a 248 m</p>', '</p>')
    # figuras em fluxo: caixa na proporção real do arquivo (a moldura acompanha o desenho) + moldura lavanda deslocada
    def moldura(m):
        attrs, st = m.group(1), m.group(2)
        src = re.search(r'src="/_blob/([0-9a-f]{32})"', attrs)
        w = re.search(r'width:(\d+)px', st); h = re.search(r'height:(\d+)px', st)
        if src and w and h and src.group(1) in BLOBS and 'object-fit:contain' in st:
            iw, ih = Image.open(os.path.join(FIG, BLOBS[src.group(1)])).size
            W, H = int(w.group(1)), int(h.group(1))
            k = min(W / iw, H / ih)
            st = st.replace(f'width:{W}px', f'width:{round(iw * k)}px').replace(f'height:{H}px', f'height:{round(ih * k)}px')
        return f'<img {attrs}style="{st};box-shadow:28px 28px 0 #B9B6CB"'
    s = re.sub(r'<img ([^>]*?)style="(?![^"]*position:absolute)([^"]*)"', moldura, s)
    # cores
    for a, b in MAPA.items():
        s = re.sub(a, b, s, flags=re.I)
    # elementos fixos do modelo, antes do primeiro filho (pintam por baixo)
    s = re.sub(r'(<section[^>]*>\n?)', lambda m: m.group(1) + decoracao(escuro), s, count=1)
    return s


CAPA = f"""<section id="cover" data-transition="fade" style="background:{MARF};color:{IND};font-family:{FONTE};padding:128px;display:flex;flex-direction:column">
<div style="position:absolute;left:0px;top:206px;width:1920px;height:2px;background:{CINZA}"></div>
<div style="position:absolute;left:0px;top:842px;width:1920px;height:2px;background:{CINZA}"></div>
<div style="position:absolute;left:0px;top:300px;width:56px;height:460px;background:{LAV}"></div>
<div style="position:absolute;left:1836px;top:0px;width:84px;height:842px;background:{LAV}"></div>
<img src="{SITIO}" alt="Imagem de satélite do sítio C1, em preto e branco, com a faixa de pista desenhada" style="position:absolute;left:820px;top:262px;width:960px;height:524px;object-fit:cover;filter:grayscale(1) contrast(1.08)">
<img src="{LOGO}" alt="Brasão do ITA" style="position:absolute;left:128px;top:64px;width:280px;height:108px;object-fit:contain">
<p style="position:absolute;left:236px;top:398px;width:900px;font-size:36px;letter-spacing:5px;text-transform:uppercase;color:{IND}">Novo aeroporto em</p>
<p style="position:absolute;left:206px;top:456px;font-size:112px;line-height:1.05;letter-spacing:3px;text-transform:uppercase;color:{MARF};background:{IND};padding:14px 36px 4px 30px;white-space:nowrap">Pindamonhangaba</p>
<p style="position:absolute;left:236px;top:640px;width:560px;font-size:32px;line-height:1.35;color:{ARD}">PPD 06/24 de 1900 × 45 m: sítio, modelo no Civil 3D e terraplenagem</p>
<p style="position:absolute;left:236px;top:884px;width:1500px;font-size:30px;color:{IND}">Pedro Feitosa Guttemberg  |  Guilherme Rodrigues  |  Gilberto Patri</p>
<p style="position:absolute;left:236px;top:940px;width:1300px;font-size:24px;letter-spacing:1px;color:#6E6E80">ITA · GEO-55 Projeto e Construção de Pistas · Profa. Cláudia Azevedo Pereira · novembro de 2026</p>
<div style="position:absolute;left:1592px;top:1016px;width:200px;height:64px;background:{IND}"></div>
<aside>{{NOTAS}}</aside>
</section>
"""

for arq in sorted(os.listdir(ORIG)):
    if not arq.endswith('.html'):
        continue
    nome = arq[:-5]
    s = open(os.path.join(ORIG, arq), encoding='utf-8').read()
    if nome == 'cover':
        notas = re.search(r'<aside>(.*?)</aside>', s, flags=re.S).group(1)
        s = CAPA.replace('{NOTAS}', notas)
    else:
        s = estiliza(nome, s)
    open(os.path.join(DEST, arq), 'w', encoding='utf-8').write(s)
    print('ok', arq)
