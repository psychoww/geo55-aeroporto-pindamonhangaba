"""Reescreve as fontes dos slides (slides_ita/, identidade ITA) para o sítio C1 da análise MESA e cria os slides do
método MESA. Depois rodar estilo_advocacia.py (identidade do modelo) e publicar. Números: PROGRESSO.md, 10/11 (noite).
Uso: python atualiza_slides_c1.py   (idempotente: reescreve os arquivos inteiros)"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
SL = os.path.join(AQUI, 'slides_ita')
LOGO = '/_blob/3603ec8169e4121cda33e4e85919be84'
B = dict(sitio='/_blob/efaec2d21633e42566f7a94f2c3f6177', regiao='/_blob/8f6952626c2493b4333f8392a7a544cb',
         ols='/_blob/1d36e032eb1f1a0e8ce6c5793bb945b4', secaotipo='/_blob/4c7d12b7bfd0f68817bf1a501b6060cf',
         perfil='/_blob/00df1846f0bcc7fc51dfe5062b9f967e', secoes='/_blob/257256a304c7d7d6063a341983edb7fc',
         brueckner='/_blob/cf7ed4b7afe4fb6bfe1f1303883343cb', c3dplanta='/_blob/dbd07c5acbffd6220d2d47391dc62be1',
         c3dsecoes='/_blob/26d9acfb76afab6939fe343642588c72', distrib='/_blob/dd9871873101561747a9fa2bed128030',
         azimute='/_blob/8189575aa20fe5246d24a3536d08dbe5', candidatos='/_blob/8fc205f9b22bc145a5377ee86547844b',
         sensib='/_blob/fbd8f3f6cf2cea955bd0967feea2c634', capa='/_blob/434ea1a0958da3d424b5d0fc7cf23f86',
         olsplanta='/_blob/cefe0c2fa8d554cdfeba0f3d5b8113e9', vento='/_blob/b56fd80fa68925c9bbc60c040ccd484d')

CLARO = "background:#F8F6EF;color:#13306B;font-family:'Barlow', Arial, sans-serif;padding:128px 128px 160px"
ESC = "background:#13306B;color:#F8F6EF;font-family:'Barlow', Arial, sans-serif;padding:128px 128px 160px"
H2 = "font-family:'Caladea', Cambria, Georgia, serif;font-size:{}px;font-weight:700;{}color:#13306B;border-bottom:4px solid #C99A06;padding:0 0 16px 0"
TXT = 'font-size:26px;line-height:1.4;color:#3F4654'
CARD = 'flex:1;display:flex;flex-direction:column;gap:8px;background:#EEF0F4;padding:24px 28px;border-top:6px solid #C99A06'
NUM = "font-family:'Caladea', Cambria, Georgia, serif;font-size:{}px;font-weight:700;color:#13306B"


def logo(top=40):
    return f'<img src="{LOGO}" alt="" style="position:absolute;left:1612px;top:{top}px;width:180px;height:69px;object-fit:contain">'


def cab(kicker, titulo, sz=64, lh=''):
    return (f'<p style="font-size:24px;color:#8A6A04;letter-spacing:3px;text-transform:uppercase;font-weight:600">{kicker}</p>\n'
            f'<h2 style="{H2.format(sz, lh)}">{titulo}</h2>')


def rodape(t):
    return f'<p style="position:absolute;left:128px;bottom:56px;font-size:24px;color:#5B6270;width:1664px">ITA · Engenharia Civil-Aeronáutica · GEO-55 · {t}</p>'


def tabela(cab_, linhas, larg, fs=26, w=None):
    th = ''.join(f'<th style="width:{l}%;color:#F8F6EF">{c}</th>' for c, l in zip(cab_, larg))
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in l) + '</tr>\n' for l in linhas)
    ws = f';width:{w}px' if w else ''
    return f'<table style="font-size:{fs}px;color:#1E1E1E{ws}">\n<tr style="background:#13306B">{th}</tr>\n{tr}</table>'


def card(rot, val, fs=48):
    return f'<div style="{CARD}"><p style="font-size:24px;color:#3F4654">{rot}</p><p style="{NUM.format(fs)}">{val}</p></div>'


S = {}
S['mesa_criterios'] = f"""<section id="mesa_criterios" data-transition="fade" style="{CLARO};display:flex;flex-direction:column;gap:24px">
{logo()}
{cab('Etapa 1 · método MESA (SAC/ITA, 2021)', 'Critérios: primeiro eliminam, depois pontuam')}
<div style="display:grid;grid-template-columns:1fr 1fr;gap:40px">
{tabela(['Eliminatório', 'Limite usado'], [['ESP · espaço aéreo', '≥ 10 km de SBSJ e SBTA'], ['MET · vento', 'utilização ≥ 95% com través ≤ 10 kt'], ['AMB · ambiente', 'água ≤ 1%; árvores ≤ 20%'], ['Várzea (alagamento)', '≤ 5% da área a &lt; 8 m do fundo'], ['INF · infraestrutura', 'sem rodovia, ferrovia ou LT'], ['TOPAlt · relevo', 'ΔH ≤ 40 m na área física'], ['OBS · obstáculos', 'aproximação e transição livres'], ['URB · cidade', '≥ 2 km da mancha urbana']], [48, 52], fs=24)}
{tabela(['Classificatório', 'Medida', 'Peso'], [['TOPVol', 'volume de aterro (m³)', '33%'], ['GEO', 'CBR de campo', '28% (igual)'], ['DIS', 'km ao centro da cidade', '13%'], ['ACE', 'km à rodovia', '13%'], ['RUI', 'ha construídos em 65 dB', '8%'], ['DIP', 'km à rede elétrica', '6% (igual)']], [30, 46, 24], fs=24)}
</div>
<p style="{TXT}">50 778 combinações testadas: centros a cada 200 m num raio de 6 km × 18 rumos. Nota = Σ peso × (1/x)/Σ(1/x), como nas tabelas V-6 a V-8 do manual; GEO e DIP sem dado entram iguais para todos.</p>
{rodape('Manual de Apoio à Prospecção de Sítios Aeroportuários Regionais (SAC/MInfra + ITA, 2021); pesos do exemplo do manual')}
<aside>O manual do professor Cláudio Jorge, feito pela SAC com o ITA, separa critérios eliminatórios, que tiram áreas do mapa, de classificatórios, que dão nota aos sítios que sobram. Usamos os eliminatórios do manual com os limites da tabela, mais a várzea, que o manual lista como camada de áreas sujeitas a alagamento. A nota usa os pesos do exemplo do próprio manual, porque não montamos um painel de especialistas, e fizemos a análise de sensibilidade que o manual recomenda.</aside>
</section>
"""
S['mesa_azimute'] = f"""<section id="mesa_azimute" data-transition="fade" style="{CLARO};display:flex;flex-direction:column;gap:24px">
{logo()}
{cab('Etapa 1 · MESA · rumo da pista', 'O rumo é decidido pelos obstáculos, não pelo vento')}
<img src="{B['azimute']}" alt="Por rumo: posições viáveis e menor volume; só os rumos de 20° a 80° passam nas superfícies de proteção; 50° e 60° dão o menor volume" style="width:1180px;height:520px;object-fit:contain">
<p style="{TXT}">Vento: utilização de 99,9% a 100% em qualquer rumo, mesmo com 10 kt. Fora de 20°–80°, sempre há morro na aproximação ou na transição. Os rumos 50°–60° dão o menor volume e os únicos sítios a ≥ 2 km da cidade.</p>
{rodape('Vento ERA5 2015–2024; relevo Copernicus GLO-30')}
<aside>Este gráfico responde a pergunta de como o azimute pesa. Em cima, quantas posições passam em cada rumo: as cinzas passam no relevo e no entorno, as azuis também nas superfícies de proteção, as douradas ainda ficam a mais de 2 km da cidade. Embaixo, o menor volume possível em cada rumo. O vento não tira nenhum rumo. Quem limita são os morros, e o melhor rumo continua sendo 060°, o mesmo da prévia.</aside>
</section>
"""
S['mesa_ranking'] = f"""<section id="mesa_ranking" data-transition="fade" style="{CLARO};display:grid;grid-template-columns:760px 1fr;gap:56px;align-items:center">
{logo()}
<img src="{B['candidatos']}" alt="Imagem de satélite com os candidatos C1 a C4 ao norte do rio e a faixa da prévia ao sul, colada à cidade" style="width:760px;height:760px;object-fit:contain">
<div style="display:flex;flex-direction:column;gap:22px">
{cab('Etapa 1 · MESA · ranking', 'C1, 4,8 km ao norte, em 1º lugar', 48, 'line-height:1.1;')}
{tabela(['Sítio', 'Nota', 'TOPVol mil m³', 'Cidade'], [['<b>C1</b>', '<b>0,31</b>', '<b>369</b>', '<b>3,4 km</b>'], ['C2', '0,26', '574', '3,7 km'], ['C3', '0,22', '1487', '4,3 km'], ['C4', '0,21', '1170', '4,1 km'], ['Prévia', '—', '1154', '0 km (URB)']], [28, 18, 30, 24], fs=24)}
<p style="{TXT}">A prévia é viável no resto, mas está colada à mancha urbana: o manual só flexibiliza esse critério quando não há outra área, e há.</p>
<p style="{TXT}">Sensibilidade: C1 só perde o 1º lugar com peso de RUI acima de 31% ou de TOPVol abaixo de 8%.</p>
</div>
{rodape('Pesos do exemplo do manual; TOPVol = proxy do manual')}
<aside>Ranqueamos só os sítios que passam em todos os eliminatórios, inclusive o de distância à cidade, como manda o manual. Os quatro candidatos ficam ao norte do rio Paraíba. A prévia, ao sul, passa em tudo menos nisso: está colada ao bairro. C1 ganha porque tem o menor volume e fica longe da cidade, e continua em primeiro numa faixa larga de pesos.</aside>
</section>
"""
S['mesa_custo'] = f"""<section id="mesa_custo" data-transition="fade" style="{CLARO};display:flex;flex-direction:column;gap:24px">
{logo()}
{cab('Etapa 1 · custo · terraplenagem + desapropriação', 'O custo não separa os dois sítios: depende da área desapropriada')}
{tabela(['R$ milhões (preços de 2026)', 'Prévia', 'C1'], [['Terraplenagem (SICRO, escavação + compactação)', '23,5', '<b>8,3</b>'], ['A) sítio 3000 × 1500 m (450 ha), deslocado para o mínimo de casas', '57,9', '80,3'], ['B) curva de 75 dB do manual (179 ha)', '78,1', '<b>53,4</b>']], [60, 20, 20], fs=26, w=1664)}
<div style="display:flex;gap:24px">
{card('Terra rural (anúncios em Pindamonhangaba)', 'R$ 65 mil/ha', 40)}
{card('Construção atingida (CUB R1-N, set/2026)', 'R$ 2.690/m²', 40)}
{card('Cada hectare construído (40% ocupado)', '≈ R$ 11 mi', 40)}
</div>
<p style="{TXT}">C1 economiza R$ 15 mi de terra movida, mas o sítio grande pega chácaras e uma pista particular asfaltada. Pela área do manual (B), C1 sai mais barato.</p>
{rodape('SICRO 5501712 e 5502978 (SP, jul/2026); CUB/SP set/2026; terra: anúncios de 2025')}
<aside>A área desapropriada é praticamente a mesma em qualquer sítio, então o que muda é o preço da terra e quantas construções são atingidas. Cada hectare construído pesa cerca de 11 milhões. Pelo sítio retangular do enunciado, a prévia sai mais barata; pela área do manual, que é a curva de ruído de 75 dB, C1 sai mais barato. A terra é o dado mais fraco: não há tabela oficial municipal acessível, usamos anúncios.</aside>
</section>
"""
S['sitio'] = f"""<section id="sitio" data-transition="fade" style="{CLARO};display:grid;grid-template-columns:800px 1fr;gap:56px;align-items:center">
{logo()}
<img src="{B['sitio']}" alt="Imagem de satélite de C1: retângulo amarelo de 3000 × 1500 m, faixa em vermelho e PPD em branco, ao norte do rio Paraíba" style="width:800px;height:792px;object-fit:contain">
<div style="display:flex;flex-direction:column;gap:20px">
{cab('Etapa 1 · sítio escolhido (C1)', 'Ao norte do Paraíba, 4,8 km do centro', 52, 'line-height:1.1;')}
{tabela(['Centro (SIRGAS 2000)', '−22,8885° / −45,4874°'], [['Rumo da PPD', '060° / 240° (06/24)'], ['Cota média da faixa', '540 m'], ['Altura sobre a várzea', '12,5 m'], ['Uso do solo (faixa)', '68% pasto, 20% cultivo, 10% árvores'], ['Distância à cidade', '3,4 km da mancha urbana']], [50, 50], fs=24, w=800)}
<p style="font-size:24px;line-height:1.4;color:#3F4654">A pista particular asfaltada (~1,4 km, rumo 020°) que cruza a ponta SW seria desativada; chácaras na faixa (~1 ha construído) seriam desapropriadas.</p>
</div>
{rodape('Imagem: Esri World Imagery; uso do solo: ESA WorldCover 2021')}
<aside>Amarelo é o sítio de 3000 por 1500 metros, vermelho a faixa de pista, branco a PPD. C1 fica num terreno ondulado e baixo ao norte do rio, a quase cinco quilômetros do centro de Pindamonhangaba. Pontos fracos, ditos com franqueza: há uma pista particular asfaltada que cruza a ponta sudoeste e seria substituída pelo novo aeroporto; há chácaras dentro da faixa; e há arrozais e uma lagoa perto, que atraem aves. Pindamonhangaba já tem o aeródromo SDPD, com pista de cerca de 1100 metros, a 8 km daqui; o novo aeroporto o substituiria.</aside>
</section>
"""
S['ols'] = f"""<section id="ols" data-transition="fade" style="{CLARO};display:flex;flex-direction:column;gap:22px">
{logo()}
{cab('Etapa 1 · obstáculos', 'Aproximações livres; morros ao norte furam a horizontal interna')}
<img src="{B['olsplanta']}" alt="Mapa em planta: terreno acima das superfícies limitadoras concentrado nos morros a 4–6 km ao norte (horizontal interna e cônica); aproximações livres" style="width:1340px;height:470px;object-fit:contain">
<div style="display:flex;gap:24px">
{card('Aproximação (2% e 2,5%, 15 km)', '3,9 m · 3 ha (árvores)', 36)}
{card('Horizontal interna (+45 m, 4 km)', '144 m · 675 ha', 36)}
{card('Cônica (5%)', '255 m · 1422 ha', 36)}
</div>
{rodape('Anexo 14 / RBAC 154, código 4, CAT I; DSM Copernicus GLO-30')}
<aside>Este é o ponto fraco de C1 e precisa ser dito claramente. As aproximações nas duas cabeceiras estão livres: o máximo são 4 metros em 3 hectares, provavelmente árvores. Mas os morros ao pé da Mantiqueira, a 4 a 6 km ao norte, passam acima da horizontal interna, em até 144 metros, e da cônica, em até 255. O manual MESA elimina sítios só por aproximação, decolagem e transição, e manda documentar as demais; o Anexo 14 pede essas superfícies livres, então C1 exigiria estudo aeronáutico e procedimentos de circulação que evitem o lado norte. A prévia não tinha esse problema; trocamos isso pela distância à cidade e pelo volume menor.</aside>
</section>
"""
S['perfil'] = f"""<section id="perfil" data-transition="fade" style="{CLARO};display:flex;flex-direction:column;gap:24px">
{logo()}
{cab('Etapa 2 · alinhamento vertical', 'Greide otimizado: corte = Fh × aterro')}
<img src="{B['perfil']}" alt="Perfil longitudinal de C1 com terreno, greide de 5 PIVs e 3 curvas verticais; rampas −0,282%, +0,210%, −0,154% e 0,000%" style="width:1664px;height:420px;object-fit:contain">
<div style="display:flex;gap:20px">
<div style="flex:1;background:#EEF0F4;padding:20px 24px;border-top:6px solid #C99A06"><p style="font-size:26px;color:#3F4654"><b>Rampa máx.</b> 0,28% (≤ 1,5%)</p></div>
<div style="flex:1;background:#EEF0F4;padding:20px 24px;border-top:6px solid #C99A06"><p style="font-size:26px;color:#3F4654"><b>Efetiva</b> 0,06% (≤ 1,0%)</p></div>
<div style="flex:1;background:#EEF0F4;padding:20px 24px;border-top:6px solid #C99A06"><p style="font-size:26px;color:#3F4654"><b>Δi máx.</b> 0,49% (≤ 1,5%)</p></div>
<div style="flex:1;background:#EEF0F4;padding:20px 24px;border-top:6px solid #C99A06"><p style="font-size:26px;color:#3F4654"><b>PIVs</b> ao centímetro</p></div>
</div>
{rodape('PIVs 542,38 / 540,97 / 542,02 / 541,22 / 541,22 m; raio e 0,8% nos quartos extremos: Anexo 14')}
<aside>O alinhamento horizontal é uma reta de 2020 metros no rumo 060°. O greide tem 5 PIVs, com cotas otimizadas para o menor volume com o corte igual a 1,25 vez o aterro. Depois arredondamos as cotas ao centímetro e as baixamos 1 cm, para que o balanço feche com as áreas do Civil 3D sem faltar terra. O terreno de C1 é baixo e quase plano, por isso as rampas ficaram muito abaixo dos limites.</aside>
</section>
"""
S['volumes'] = f"""<section id="volumes" data-transition="fade" style="{CLARO};display:flex;flex-direction:column;gap:32px">
{logo()}
{cab('Etapa 3 · quantitativos', 'Greide compensado: o corte paga o aterro corrigido')}
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:24px">
{card('Corte', '435.440 m³', 64)}
{card('Aterro (geométrico)', '344.978 m³', 64)}
{card('Aterro corrigido (Fh = 1,25)', '431.223 m³', 64)}
</div>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:24px">
<div style="display:flex;flex-direction:column;gap:8px;padding:8px 24px"><p style="font-size:26px;color:#3F4654">Saldo (sobra de corte)</p><p style="{NUM.format(48)}">+4.216 m³</p></div>
<div style="display:flex;flex-direction:column;gap:8px;padding:8px 24px"><p style="font-size:26px;color:#3F4654">Compensação lateral</p><p style="{NUM.format(48)}">238.422 m³</p></div>
<div style="display:flex;flex-direction:column;gap:8px;padding:8px 24px"><p style="font-size:26px;color:#3F4654">Transporte longitudinal</p><p style="{NUM.format(48)}">197.018 m³</p></div>
<div style="display:flex;flex-direction:column;gap:8px;padding:8px 24px"><p style="font-size:26px;color:#3F4654">Limpeza (15 cm)</p><p style="{NUM.format(48)}">92.401 m³</p></div>
</div>
<p style="{TXT}">Fh = 1,25 para solos argilosos porosos (latossolos e argissolos) sobre os sedimentos terciários da Bacia de Taubaté, que adensam bastante na compactação (faixa usual de 1,2 a 1,3). Corte 65% menor que no sítio da prévia.</p>
{rodape('Método das áreas médias nas 104 seções do Civil 3D; memorial completo em Memorial_terraplenagem_PPD.xlsx')}
<aside>Volumes pelas áreas médias das 104 seções do Civil 3D. O corte cobre o aterro corrigido pelo Fh de 1,25 e sobram 4,2 mil m³, menos de 1% do corte. A compensação lateral resolve 238 mil m³ dentro da própria seção; só 197 mil m³ andam ao longo do eixo. Comparado com a prévia, o corte caiu de 1,23 milhão para 435 mil m³, porque o terreno de C1 é mais plano.</aside>
</section>
"""
S['mao'] = f"""<section id="mao" data-transition="fade" style="background:#EEF0F4;color:#13306B;font-family:'Barlow', Arial, sans-serif;padding:128px 128px 160px;display:flex;flex-direction:column;gap:28px">
{logo()}
{cab('Etapa 3 · cálculo à mão', 'Estacas 52 → 53, pelo método das áreas médias')}
<div style="display:grid;grid-template-columns:620px 1fr;gap:48px">
{tabela(['Estaca', 'Corte (m²)', 'Aterro (m²)'], [['52 + 00,00', '286,27', '252,72'], ['53 + 00,00', '231,39', '271,10'], ['d = 20,00 m', 'Fh = 1,25', '']], [40, 30, 30], fs=28)}
<div style="display:flex;flex-direction:column;gap:18px;background:#F8F6EF;padding:36px;border-left:6px solid #C99A06">
<p style="font-family:'Caladea', Cambria, Georgia, serif;font-size:36px;color:#13306B">V = (A₁ + A₂) / 2 × d</p>
<p style="font-size:28px;color:#3F4654">Vc = (286,27 + 231,39) / 2 × 20 = <b>[ … ] m³</b></p>
<p style="font-size:28px;color:#3F4654">Va = (252,72 + 271,10) / 2 × 20 = <b>[ … ] m³</b></p>
<p style="font-size:28px;color:#3F4654">Fh × Va = 1,25 × Va = <b>[ … ] m³</b></p>
<p style="font-size:28px;color:#3F4654">Compensação lateral = menor(Vc; Fh·Va) = <b>[ … ] m³</b></p>
<p style="font-size:28px;color:#3F4654">Vc − Fh·Va = <b>[ … ] m³</b> na ordenada de Brückner</p>
</div>
</div>
<p style="font-size:26px;color:#3F4654">Conta feita à mão na apresentação; a aba “Cálculo à mão” da planilha confere com o memorial.</p>
{rodape('Regra da aula de 20/10: o trecho entre duas estacas é feito à mão')}
<aside>A regra é fazer à mão o volume entre duas estacas consecutivas pelo método das áreas médias; o Fh, a compensação lateral e a ordenada são extras. O par 52 e 53 é o de seções mistas com as maiores áreas de corte e de aterro ao mesmo tempo. Os resultados ficam em branco aqui: a conta é feita na hora e conferida na aba Cálculo à mão.</aside>
</section>
"""
S['brueckner'] = f"""<section id="brueckner" data-transition="fade" style="{CLARO};display:flex;flex-direction:column;gap:24px">
{logo()}
{cab('Etapa 3 · diagrama de massas', 'Sobe até 1360 m: o corte do início abastece o fim')}
<div style="display:grid;grid-template-columns:1fr 460px;gap:40px;align-items:center">
<img src="{B['brueckner']}" alt="Áreas por seção e diagrama de Brückner de C1 com Fh = 1,25: sobe até +83,6 mil m³ perto de 1360 m, desce a −5,7 mil m³ perto de 1720 m e termina em +4,2 mil m³" style="width:1164px;height:640px;object-fit:contain">
<div style="display:flex;flex-direction:column;gap:20px">
<p style="{TXT}">Máximo de <b>+83,6 mil m³</b> perto da estaca 68 e mínimo de <b>−5,7 mil m³</b> perto da 86.</p>
<p style="{TXT}">Trecho subindo: predomina corte. Trecho descendo: predomina aterro.</p>
<p style="{TXT}">Fecha em +4,2 mil m³ porque o greide é compensado.</p>
</div>
</div>
{rodape('Ordenada = Σ(Vc − Fh·Va), Fh = 1,25')}
<aside>O diagrama sai da última coluna do memorial. Ele sobe quase o tempo todo até perto de 1360 metros: o primeiro terço da pista tem mais corte que aterro, e esse excesso precisa ir para o fim, onde o terreno é mais baixo. Por isso as distâncias de transporte de C1 são maiores que as da prévia, apesar do volume bem menor.</aside>
</section>
"""
S['distribuicao'] = f"""<section id="distribuicao" data-transition="fade" style="{CLARO};display:flex;flex-direction:column;gap:24px">
{logo()}
{cab('Etapa 3 · distribuição de massas', 'Linhas de compensação do programa da aula 8')}
<div style="display:grid;grid-template-columns:1fr 600px;gap:40px;align-items:center">
<img src="{B['distrib']}" alt="Diagrama de massas de C1 com duas soluções: em cima, LCs que compensam tudo (MT 6,61 milhões de m³·dam); embaixo, o ótimo com bota-fora e empréstimo a 150 m (MT 3,37 milhões)" style="width:1024px;height:470px;object-fit:contain">
{tabela(['Solução', 'MT (10⁶ m³·dam)', 'Bota-fora / empréstimo'], [['<b>Compensa tudo (2 LCs)</b>', '<b>6,61</b>', '<b>4,2 mil m³ / 0</b>'], ['Ótimo a 150 m (7 LCs)', '3,37', '63 / 59 mil m³'], ['Ótimo contando a escavação do empréstimo', 'o mesmo de cima', '4,2 mil m³ / 0']], [46, 27, 27], fs=24, w=600)}
</div>
<p style="{TXT}">Adotada: <b>compensar tudo</b>. A onda principal leva 79 mil m³ por 745 m em média; o ótimo a 150 m trocaria isso por 59 mil m³ de empréstimo.</p>
{rodape('Programa diagrama_massas (MATLAB); DMT externa 150 m (aula 8)')}
<aside>Com bota-fora e empréstimo a 150 metros, o mínimo do modelo da aula manda 63 mil m³ para bota-fora e traz 59 mil de empréstimo. Contando a escavação do empréstimo pelos preços do exercício 6, compensar tudo sai mais barato, com duas linhas de compensação: só sobram 4,2 mil m³. A onda principal vai da estaca 9 até a 83, com distância média de 745 metros.</aside>
</section>
"""
S['equipamentos'] = f"""<section id="equipamentos" data-transition="fade" style="background:#EEF0F4;color:#13306B;font-family:'Barlow', Arial, sans-serif;padding:128px 128px 160px;display:flex;flex-direction:column;gap:28px">
{logo()}
{cab('Etapa 3 · execução', 'Equipamentos e por que cada um')}
{tabela(['Serviço', 'Equipamento', 'Por quê (aula 9; faixas do SICRO)'], [['Limpeza (92 mil m³)', 'Trator de esteira, lâmina reta; motoniveladora', 'Lâmina reta: limpeza geral, cava e amontoa'], ['Onda principal (79 mil m³, DMT 745 m)', 'Moto-scraper com trator empurrador', 'Escava, carrega, transporta e espalha; SICRO prevê até 800–1000 m'], ['Ondas curtas (DMT de 72 a 135 m)', 'Trator de lâmina; moto-scraper', 'Distância curta, sem carregar'], ['Compensação lateral (238 mil m³)', 'Trator de lâmina', 'Corte de um lado da seção, aterro do outro'], ['Regularização (1,5% e 2,5%)', 'Motoniveladora', 'Acabamento fino; taludes'], ['Compactação do aterro', 'Rolo pé-de-carneiro', 'Solo argiloso; compacta do fundo para o topo'], ['Topo do subleito', 'Rolo pneumático', 'Sela a superfície; solos finos']], [28, 30, 42], fs=24, w=1664)}
<p style="font-size:24px;color:#3F4654">Eventuais: escarificador (camadas compactas) e rolo vibratório (lentes de areia). Na onda longa, escavadeira + caminhões basculantes é a alternativa se a frota de scrapers for pequena.</p>
{rodape('Aula 9; SICRO 5501712 e 5501714 (motoscraper)')}
<aside>A distribuição de C1 tem uma onda longa: 79 mil m³ andando 745 metros em média. O SICRO tem composições de moto-scraper até 800 a 1000 metros, então ele continua sendo a escolha natural, só que com custo maior por metro cúbico. As ondas curtas e a compensação lateral ficam com o trator de lâmina. A compactação é com pé-de-carneiro, porque o solo é argiloso.</aside>
</section>
"""
S['proximos'] = f"""<section id="proximos" data-transition="fade" style="{ESC};display:flex;flex-direction:column;gap:40px">
{logo()}
<p style="font-size:24px;color:#E0C25A;letter-spacing:3px;text-transform:uppercase;font-weight:600">Fechamento</p>
<h2 style="font-family:'Caladea', Cambria, Georgia, serif;font-size:64px;font-weight:700;color:#F8F6EF;border-bottom:4px solid #C99A06;padding:0 0 16px 0">O que mudou desde a prévia e o que falta</h2>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:56px">
<div style="display:flex;flex-direction:column;gap:20px">
<h3 style="font-size:36px;font-weight:600;color:#E0C25A">Mudou</h3>
<ul style="font-size:28px;line-height:1.5;color:#D6DCEB">
<li>Sítio escolhido pelo método MESA: C1, longe da cidade</li>
<li>Corte de 1,23 milhão para 435 mil m³</li>
<li>Obstáculos ao norte documentados</li>
</ul>
</div>
<div style="display:flex;flex-direction:column;gap:20px">
<h3 style="font-size:36px;font-weight:600;color:#E0C25A">Falta</h3>
<ul style="font-size:28px;line-height:1.5;color:#D6DCEB">
<li>Corredor (assembly) e Compute Materials no Civil 3D</li>
<li>Pranchas e memorial final em PDF</li>
<li>Estudo aeronáutico da horizontal interna</li>
</ul>
</div>
</div>
{rodape('Projeto e Construção de Pistas')}
<aside>Desde a prévia, aplicamos o método MESA do manual da SAC com o ITA e mudamos o sítio para C1, ao norte do rio: longe da cidade e com um terço do volume de terra. O preço disso são os morros ao norte, que passam acima da horizontal interna e da cônica; ficam documentados e pediriam estudo aeronáutico. Faltam o corredor no Civil 3D, as pranchas e o memorial final.</aside>
</section>
"""

for nome, html in S.items():
    open(os.path.join(SL, nome + '.html'), 'w', encoding='utf-8').write(html)
    print('ok', nome)


def troca(nome, pares):
    f = os.path.join(SL, nome + '.html'); s = open(f, encoding='utf-8').read()
    for a, b in pares:
        if a not in s and b in s:
            continue                      # já aplicado (rodada anterior)
        assert a in s, (nome, a[:60]); s = s.replace(a, b)
    open(f, 'w', encoding='utf-8').write(s); print('ok', nome)


troca('requisitos', [('usado: 0,80% / 0,16%', 'usado: 0,28% / 0,06%'), ('usado: 1,20%', 'usado: 0,49%'),
                     ('busca automática (etapa 1)', 'busca e método MESA (etapa 1)'),
                     ('Fh = 1,25 (adotado para o solo do sítio).', 'Fh = 1,25 (adotado para o solo do sítio); greide ao centímetro.')])
troca('etapa1', [('Método da busca e a região (por que o rumo segue o vale)', 'Busca, região e método MESA (critérios, rumo, ranking, custo)')])
troca('metodo', [('Só pela terraplenagem, o sítio cairia na várzea. Com os quatro critérios, sobraram <b>2 locais</b>; um tinha rodovia cortando a faixa.',
                  'A busca levou ao sítio da prévia, ao sul do rio. Depois da prévia, o método MESA refinou posição e rumo: próximos slides.')])
troca('regiao', [('/_blob/992f302661db59a99fd728cc7e959531', B['regiao']),
                 ('O retângulo azul-petróleo é o sítio escolhido, a oeste de Pindamonhangaba.', 'O retângulo azul-petróleo é o sítio escolhido, C1, ao norte de Pindamonhangaba.')])
troca('vento', [('/_blob/b56fd80fa68925c9bbc60c040ccd484d', B['vento'])])
troca('civil3d', [('/_blob/2d2e4649f1870d534c4f6239b1bf5f8f', B['c3dplanta']), ('8220 nós', '8219 nós')])
troca('secaotipo', [('/_blob/522e3ab84522fa153e1de81b071b75e2', B['secaotipo'])])
troca('secoes', [('/_blob/a1772790ed5bb91f7b239d9ea32bd75d', B['secoes']),
                 ('alt="Quatro seções transversais: estacas 29 (459 m² de corte e 279 de aterro) e 30 (410 e 397), mistas; estaca 50 quase só aterro (1065 m²); estaca 85 só corte (1595 m²)"',
                  'alt="Quatro seções transversais de C1: estacas 29, 30, 50 e 85, todas mistas, com corte em azul-petróleo e aterro em lavanda"')])
troca('c3dsecoes', [('/_blob/a28310fa95b57226b11eafeaf2a10abf', B['c3dsecoes']),
                    ('Conferência com um cálculo independente: <b>0,05%</b> de diferença no volume total.', 'Conferência com um cálculo independente: <b>−0,6%</b> no corte e <b>−0,4%</b> no aterro.')])
troca('cover', [('A foto em preto e branco é o sítio escolhido, a oeste de Pindamonhangaba,', 'A foto em preto e branco é o sítio escolhido, C1, ao norte de Pindamonhangaba,')])

d = json.load(open(os.path.join(AQUI, 'project', 'deck.json'), encoding='utf-8'))
ordem = ['cover', 'requisitos', 'etapa1', 'metodo', 'mesa_criterios', 'mesa_azimute', 'mesa_ranking', 'mesa_custo', 'regiao',
         'sitio', 'vento', 'ols', 'etapa2', 'civil3d', 'secaotipo', 'perfil', 'etapa3', 'secoes', 'c3dsecoes', 'volumes', 'mao',
         'brueckner', 'distribuicao', 'equipamentos', 'proximos']
print('ordem nova:', len(ordem), 'slides; faltando arquivo:', [o for o in ordem if not os.path.exists(os.path.join(SL, o + '.html'))])
json.dump(ordem, open(os.path.join(AQUI, 'ordem_c1.json'), 'w'), indent=0)
