"""Paleta e fonte dos gráficos, iguais às dos slides (identidade do modelo "Advocacia Básico Azul e Bege").

Cores do modelo: índigo #33335B, marfim #FFFBF5, ardósia #273348, cinza #9B9B9B, lavanda #9F9DB6 e os azuis-petróleo
#147699 / #006A78 / #88C0E6. Para os gráficos: corte = petróleo, aterro = lavanda escura (cores e claridades
diferentes), terreno = cinza, linhas de projeto = índigo. Fonte: Spectral (comum/fontes, licença OFL).
"""
import os
import matplotlib
from matplotlib import font_manager

AQUI = os.path.dirname(os.path.abspath(__file__))
for f in ('Spectral-Regular.ttf', 'Spectral-Medium.ttf', 'Spectral-SemiBold.ttf'):
    caminho = os.path.join(AQUI, 'comum', 'fontes', f)
    if os.path.exists(caminho):
        font_manager.fontManager.addfont(caminho)

IND, MARF, ARD, CINZA, LAV = '#33335B', '#FFFBF5', '#273348', '#9B9B9B', '#9F9DB6'
PET, PET_ESC, AZUL_CLARO = '#147699', '#006A78', '#88C0E6'
MUTED = '#6E6E80'
CORTE, ATERRO, TN, INK, VIOL = PET, '#6B6990', CINZA, IND, IND
ALERTA = '#9A3B4A'                 # bota-fora/empréstimo e o que foi descartado (uso pontual)
BEGE, BEGE_ESC, GRADE = '#E6E0D4', '#CFC8BA', '#E8E2D6'
SEQ = ['#C8C5DA', LAV, IND]        # sequência clara → escura (ex.: classes de vento)

RC = {'font.family': ['Spectral', 'Georgia', 'serif'], 'axes.unicode_minus': False, 'font.size': 11,
      'axes.spines.top': False, 'axes.spines.right': False, 'axes.edgecolor': CINZA, 'axes.labelcolor': ARD,
      'xtick.color': ARD, 'ytick.color': ARD, 'text.color': ARD, 'axes.titleweight': 'semibold', 'axes.titlesize': 13,
      'axes.titlecolor': IND, 'figure.facecolor': MARF, 'axes.facecolor': MARF, 'savefig.facecolor': MARF,
      'legend.labelcolor': ARD, 'figure.dpi': 150}


def aplica():
    matplotlib.rcParams.update(RC)
