"""Monta a pasta ../Apresentacao_aeroporto/ com tudo o que a apresentação usa, para abrir sem internet.

Conteúdo gerado:
  Apresentacao_PPD.html         slides offline (setas/espaço passam, F = tela cheia, N = notas do apresentador)
  Apresentacao_PPD.pdf          os mesmos slides em PDF, 1 slide por página (impresso pelo Edge em modo headless)
  img/                          figuras usadas nos slides (cópias de figuras/)
  Roteiro_aeroporto.pdf, Memorial_terraplenagem_PPD.xlsx, Aeroporto_PPD_Civil3D.dwg   cópias dos arquivos da raiz
  LEIA-ME.md

As fontes dos slides são as de apresentacao_deck/project/ (as mesmas publicadas no artefato). As imagens do artefato
(/_blob/<id>) são trocadas pelas figuras locais: o mapa abaixo foi conferido por sha256 em 10/11/2026.
Rodar de novo depois de mudar slides, figuras, roteiro, memorial ou DWG:
    python montar_pasta_apresentacao.py            (com PDF)
    python montar_pasta_apresentacao.py --sem-pdf
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
DECK = os.path.join(AQUI, 'apresentacao_deck', 'project')
FIG = os.path.join(AQUI, 'figuras')
SAIDA = os.path.join(RAIZ, 'Apresentacao_aeroporto')
URL_DECK = 'https://claude.ai/artifact/8Ugecg9baS44AKMVL9Zja2'

BLOBS = {
    '3603ec8169e4121cda33e4e85919be84': 'ita_logo_transparente.png',
    'e96c1fa6f90719c521a24b1214d85644': '00_sitio.png',
    '53275340257cedb168075f11cd6437e3': '01_regiao.png',
    '7b03b1679f465d3be9e6ab2ae8ef8e68': '02_vento.png',
    '3c88cbb1d037c90498da870af3608910': '03_ols.png',
    '26e1f3b5a0aafbf35bc8abecb78303ae': '04_secao_tipo.png',
    'dfa5b386dc7ba2a04eda7f80298261a9': '05_perfil.png',
    'e3715f69c8bdffe74469d35b90ca7552': '06_secoes.png',
    'adab38c9c5418c81e9f0bd87e78a57ba': '07_brueckner.png',
    '2d2e4649f1870d534c4f6239b1bf5f8f': '08_c3d_planta.png',
    'a28310fa95b57226b11eafeaf2a10abf': '10_c3d_secoes.png',
    'a1446a656ba24ab207c84aebe8df3617': '11_distribuicao.png',
}
COPIAS = ['Roteiro_aeroporto.pdf', 'Memorial_terraplenagem_PPD.xlsx', 'Aeroporto_PPD_Civil3D.dwg']
EDGE = [r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        r'C:\Program Files\Microsoft\Edge\Application\msedge.exe']

CSS = """
*{box-sizing:border-box}
html,body{margin:0;background:#0B1220}
h1,h2,h3,p,ul,ol,table{margin:0}
ul,ol{padding-left:1.2em}
table{border-collapse:collapse}
th,td{padding:10px 16px;text-align:left;vertical-align:top;border-bottom:1px solid rgba(0,0,0,.14)}
th{font-weight:600}
img{display:block}
section{width:1920px;height:1080px;position:relative;overflow:hidden;flex-shrink:0}
section>aside{display:none}
@media screen{
  #palco{position:fixed;inset:0;display:flex;align-items:center;justify-content:center}
  #palco section{position:absolute;left:50%;top:50%;transform-origin:center center}
  #palco section:not(.atual){display:none!important}
  #nota{position:fixed;left:0;right:0;bottom:0;max-height:35vh;overflow:auto;background:#F8F6EF;color:#1C2333;
        font:18px/1.5 Barlow,Arial,sans-serif;padding:14px 24px;border-top:4px solid #C99A06;display:none}
  #nota.ver{display:block}
  #cont{position:fixed;right:14px;bottom:10px;font:14px Barlow,Arial,sans-serif;color:#9BA6BD}
}
@media print{
  @page{size:1920px 1080px;margin:0}
  html,body{background:none}
  #palco{display:block}
  #palco section{page-break-after:always;break-after:page;transform:none!important;position:relative!important;left:0;top:0}
  #nota,#cont{display:none}
}
"""

JS = """
const S=[...document.querySelectorAll('#palco section')];
let i=Math.max(0,Math.min(S.length-1,(parseInt(location.hash.slice(1))||1)-1));
const nota=document.getElementById('nota'), cont=document.getElementById('cont');
function escala(){const k=Math.min(innerWidth/1920,(innerHeight-(nota.classList.contains('ver')?nota.offsetHeight:0))/1080);
  S.forEach(s=>s.style.transform='translate(-50%,-50%) scale('+k+')');}
function mostra(){S.forEach((s,j)=>s.classList.toggle('atual',j===i));
  const a=S[i].querySelector('aside'); nota.textContent=a?a.textContent:'(sem notas)';
  cont.textContent=(i+1)+' / '+S.length; history.replaceState(null,'','#'+(i+1)); escala();}
addEventListener('keydown',e=>{
  if(['ArrowRight','ArrowDown','PageDown',' ','Enter'].includes(e.key)){i=Math.min(S.length-1,i+1);mostra();e.preventDefault();}
  else if(['ArrowLeft','ArrowUp','PageUp','Backspace'].includes(e.key)){i=Math.max(0,i-1);mostra();e.preventDefault();}
  else if(e.key==='Home'){i=0;mostra();} else if(e.key==='End'){i=S.length-1;mostra();}
  else if(e.key==='n'||e.key==='N'){nota.classList.toggle('ver');escala();}
  else if(e.key==='f'||e.key==='F'){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen();}
});
addEventListener('click',e=>{if(e.target.closest('#nota'))return; i=e.clientX<innerWidth/3?Math.max(0,i-1):Math.min(S.length-1,i+1); mostra();});
addEventListener('resize',escala); mostra();
"""


def montar_html(deck):
    usadas = set()

    def troca(m):
        nome = BLOBS.get(m.group(1))
        if not nome:
            sys.exit(f'imagem /_blob/{m.group(1)} sem figura local: atualize BLOBS')
        usadas.add(nome)
        return f'src="img/{nome}"'

    secoes = []
    for sid in deck['order']:
        s = open(os.path.join(DECK, 'slides', f'{sid}.html'), encoding='utf-8').read().strip()
        secoes.append(re.sub(r'src="/_blob/([0-9a-f]{32})"', troca, s))
    hrefs = sorted({f['href'] for f in deck.get('faces', {}).values() if f.get('href')})
    links = ''.join(f'<link rel="stylesheet" href="{html.escape(h)}">' for h in hrefs)
    titulo = html.escape(deck.get('title', 'Apresentação'))
    doc = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
           f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{titulo}</title>{links}'
           f'<style>{CSS}</style></head><body><div id="palco">\n' + '\n'.join(secoes) +
           f'\n</div><div id="nota"></div><div id="cont"></div><script>{JS}</script></body></html>\n')
    return doc, usadas


def imprimir_pdf(html_path, pdf_path):
    edge = next((e for e in EDGE if os.path.exists(e)), None)
    if not edge:
        print('Edge não encontrado: PDF não gerado')
        return False
    perfil = os.path.join(AQUI, 'tmp', 'edge_perfil')
    os.makedirs(perfil, exist_ok=True)
    url = 'file:///' + html_path.replace('\\', '/')
    subprocess.run([edge, '--headless', '--disable-gpu', '--no-pdf-header-footer', f'--user-data-dir={perfil}',
                    '--virtual-time-budget=15000', f'--print-to-pdf={pdf_path}', url],
                   check=False, timeout=180, capture_output=True)
    return os.path.exists(pdf_path)


def main():
    deck = json.load(open(os.path.join(DECK, 'deck.json'), encoding='utf-8'))
    os.makedirs(os.path.join(SAIDA, 'img'), exist_ok=True)
    doc, usadas = montar_html(deck)
    for f in os.listdir(os.path.join(SAIDA, 'img')):
        if f not in usadas:
            os.remove(os.path.join(SAIDA, 'img', f))
    for nome in sorted(usadas):
        shutil.copy2(os.path.join(FIG, nome), os.path.join(SAIDA, 'img', nome))
    html_path = os.path.join(SAIDA, 'Apresentacao_PPD.html')
    open(html_path, 'w', encoding='utf-8').write(doc)
    print('ok', html_path, len(deck['order']), 'slides,', len(usadas), 'imagens')

    for nome in COPIAS:
        try:
            shutil.copy2(os.path.join(RAIZ, nome), os.path.join(SAIDA, nome))
            print('ok', nome)
        except PermissionError:
            print('NÃO COPIADO (arquivo aberto em outro programa; feche e rode de novo):', nome)

    pdf = os.path.join(SAIDA, 'Apresentacao_PPD.pdf')
    if '--sem-pdf' not in sys.argv:
        if os.path.exists(pdf):
            os.remove(pdf)
        print('ok' if imprimir_pdf(html_path, pdf) else 'FALHOU', pdf)

    hoje = datetime.now().strftime('%d/%m/%Y %H:%M')
    leia = f"""# Apresentação do aeroporto (GEO-55, exame do 2º bimestre)

PPD 06/24 em Pindamonhangaba · prévia de 10/11/2026 · entrega final em 17/11/2026.
Pasta montada por `aeroporto_trabalho/montar_pasta_apresentacao.py` em {hoje}. **Não edite aqui:** os originais
ficam em `aeroporto_trabalho/` e na raiz; rode o script de novo para atualizar.

| Arquivo | O que é |
|---|---|
| `Apresentacao_PPD.html` | Os {len(deck['order'])} slides, abrem sem internet (só as fontes Caladea e Barlow vêm do Google Fonts; sem rede, caem em Cambria e Arial). Setas, espaço ou clique passam; **F** = tela cheia; **N** = notas do apresentador; `#7` no fim do endereço abre no slide 7. |
| `Apresentacao_PPD.pdf` | Os mesmos slides em PDF, um por página (sem as notas). |
| `Roteiro_aeroporto.pdf` | Roteiro da fala por etapa e por pessoa, com perguntas prováveis e respostas. |
| `Memorial_terraplenagem_PPD.xlsx` | Memorial de cálculo (áreas, volumes, Fh, compensação lateral, Brückner, conta à mão). |
| `Aeroporto_PPD_Civil3D.dwg` | Modelo do Civil 3D (superfícies, eixo, perfis, 104 seções). |
| `img/` | Figuras usadas nos slides. |

Versão on-line (a mesma, compartilhada por link): {URL_DECK}
"""
    open(os.path.join(SAIDA, 'LEIA-ME.md'), 'w', encoding='utf-8').write(leia)
    print('ok LEIA-ME.md')


if __name__ == '__main__':
    main()
