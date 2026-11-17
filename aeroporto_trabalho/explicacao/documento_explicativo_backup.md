

# Aeroporto de Pindamonhangaba: o projeto do começo ao fim

2026-11-10 · Guilherme

O projeto é uma pista de pouso e decolagem (PPD 06/24, de 1900 × 45 m) num terraço a oeste de Pindamonhangaba. O greide foi otimizado para que o corte cubra o aterro: 1.227.480 m³ de corte contra 1.227.389 m³ de aterro corrigido, com sobra de só 91 m³. Este texto conta, na ordem em que foi feito, cada etapa, de onde veio cada número e por que cada escolha foi feita.

## 1. O trabalho e as premissas

O exame do 2º bimestre de GEO-55 (Profa. Cláudia Azevedo Pereira) pede o projeto geométrico e de terraplenagem de um aeroporto novo no Civil 3D, em três etapas. O grupo é Pedro Feitosa Guttemberg, Guilherme Rodrigues e Gilberto Patri. O local é escolhido pelo grupo; o enunciado só pede uma área de 3000 × 1500 m para o sítio.
 | 

Etapa | 

O que o enunciado pede | 

Data
 | 

1 | 

Escolher o local do sítio e justificar | 

20/10 (não apresentada; entrou na prévia)
 | 

2 | 

Imagem georreferenciada e modelo do terreno no Civil 3D; alinhamentos horizontal e vertical; seção-tipo | 

03/11, adiada para a prévia de 10/11
 | 

3 | 

Terraplenagem: seções transversais e volumes pelas áreas médias | 

prévia em 10/11; entrega final em 17/11

As premissas vêm de três fontes: o enunciado, as aulas e decisões adotadas pelo grupo, com justificativa.
 | 

Item | 

Valor | 

Origem
 | 

PPD | 

1900 × 45 m | 

enunciado (figura; o texto dizia 2300 m, e a professora confirmou 1900 m em 03/11)
 | 

Faixa de pista | 

2020 × 300 m, 60 m além de cada cabeceira | 

enunciado
 | 

Declividade transversal | 

PPD 1,5%; da borda da PPD até 150 m do eixo, 2,5% | 

enunciado
 | 

Acostamentos | 

7,5 m de cada lado | 

enunciado
 | 

Declividade longitudinal | 

máxima 1,5%; efetiva máxima 1,0%; mudança máxima 1,5% | 

enunciado
 | 

Pavimento | 

1,10 m na PPD; 0,50 m nos acostamentos | 

enunciado
 | 

Limpeza | 

15 cm de camada vegetal em toda a área; nunca aterrar sobre ela | 

aula 7
 | 

Volumes | 

método das áreas médias | 

enunciado e aula 7
 | 

Curvas verticais | 

raio mínimo de 30 000 m; rampa ≤ 0,8% no primeiro e no último quarto da PPD | 

adotado (Anexo 14 da OACI, código 4)
 | 

Taludes | 

corte 1V:1,5H; aterro 1V:2H | 

adotado (o enunciado não dá)
 | 

Fator de homogeneização | 

Fh = 1,25 | 

adotado (seção 7)
 | 

Bota-fora e empréstimo | 

DMT de 150 m | 

aula 8

A faixa de 300 m é nivelada inteira, como na figura do enunciado. A nota de serviço da aula 7, que nivela só ±75 m, é apenas um exemplo de formato e não vale para este projeto.

## 2. Etapa 1: a escolha do sítio

O sítio fica num terraço a oeste de Pindamonhangaba, com centro em −22,9300; −45,4993 e PPD no rumo 060°/240° (cabeceiras 06 e 24). Ele saiu de uma busca automática com critérios explícitos, e não de uma escolha a olho.

Área de busca. A busca não cobriu o Estado nem o Vale do Paraíba inteiro. O recorte foi fixado antes, em volta de São José dos Campos, por ser a região do ITA:
- 

modelo de terreno: lat. −23,40° a −22,85° e long. −46,00° a −45,35° (67 × 61 km);
- 

centros testados: 4 km para dentro dessa borda, para sobrar terreno em volta na verificação de obstáculos. Isso dá lat. −23,36° a −22,89° e long. −45,96° a −45,39° (59 × 53 km), de São José dos Campos a Pindamonhangaba;
- 

35 066 centros a cada 300 m; tirando 10 km em volta dos aeroportos de São José dos Campos (SBSJ) e Taubaté (SBTA), sobram 28 099; tirando a várzea, 25 062. Cada um foi testado em 36 rumos (de 0° a 175°, de 5 em 5°).

Os critérios entraram em rodadas. Cada rodada mostrou um problema da anterior.
- 

Terraplenagem. Para cada centro e rumo, a busca ajusta um greide reto (rampa ≤ 1%) à faixa de 2020 × 300 m e mede o desvio médio do terreno. Sozinho, esse critério leva todos os melhores locais para a várzea do Paraíba: plana, mas inundável, com argila mole, turfa, lençol raso e arrozais.
- 

Fora da várzea. Passou a exigir que o centro esteja pelo menos 12 m acima do fundo do vale num raio de 3 km.
- 

Superfícies limitadoras de obstáculos (Anexo 14, código 4, precisão CAT I), verificadas contra o modelo de terreno: aproximação a 2% e 2,5%, transição a 14,3%, horizontal interna a +45 m num raio de 4 km e cônica a 5%. Quase todos os rumos têm morros furando a horizontal interna ou a cônica, porque o vale é estreito entre a Mantiqueira e a Serra do Mar. Só os rumos no eixo do vale, de 50° a 70°, passam.
- 

Entorno. No máximo 10% de área urbana nos cones de aproximação de 3 km e a 500 m da faixa (ruído); pouca água num raio de 3 km (risco aviário); no máximo 25% de mata; 10 km de SBSJ e SBTA.

Sobraram dois locais. O B (−22,906; −45,406; rumo 025°) foi descartado porque uma rodovia corta a faixa e há uma indústria na cabeceira. Ficou o A.

Vento. A reanálise ERA5 de 2015 a 2024 (87 672 horas) mostra que o vento não restringe o rumo: a cobertura passa de 99,9% em qualquer direção, e 55% das horas são de calmaria. Mesmo assim, 060° coincide com o vento predominante de ENE.
 | 

Sítio escolhido | 

Valor
 | 

Centro (SIRGAS 2000) | 

−22,9300; −45,4993
 | 

Rumo da PPD | 

060°/240°
 | 

Cota média da faixa | 

cerca de 556 m
 | 

Altura sobre a várzea | 

21 m
 | 

Uso do solo | 

pasto; 4% de mata
 | 

Obstáculos (superfícies de proteção) | 

nenhum relevante

Os pontos fracos ficaram registrados: cavas de areia a cerca de 1,5 km ao norte (aves, mitigável) e a cidade a cerca de 1 km a leste do cone nordeste (ruído lateral).

## 3. Etapa 2: o terreno e o eixo no Civil 3D

O modelo está no arquivo Aeroporto_PPD_Civil3D.dwg, com a imagem georreferenciada, quatro superfícies, o eixo e os perfis. Quase tudo foi feito por scripts que comandam o Civil 3D (COM, pelo PowerShell), e não à mão.
- 

Terreno (superfície TN). Vem do modelo digital Copernicus GLO-30, uma grade de cerca de 30 m. Os nós viraram pontos em UTM 23S (SIRGAS 2000) e foram triangulados. É um modelo de superfície: árvores e construções aparecem como terreno, o que pesa pouco aqui porque o sítio tem só 4% de mata.
- 

Terreno limpo (superfície TN_limpo). É o TN 15 cm abaixo: o terreno depois de tirar a camada vegetal. Todas as áreas de corte e aterro são medidas a partir dele, então o aterro nunca fica sobre a camada vegetal.
- 

Superfícies de projeto (TERRAPLENAGEM e ACABADA). A primeira é a plataforma sob o pavimento; a segunda, a superfície pronta. As duas foram calculadas em Python e importadas por LandXML.
- 

Imagem georreferenciada. Um mosaico Esri World Imagery com pixel de 1 m, inserido no desenho com arquivo de coordenadas (.jgw).
- 

Alinhamento horizontal "EIXO PPD 06-24". Uma reta de 2020 m no eixo da faixa, com estacas a cada 20 m. O P0 fica na ponta sudoeste da faixa e o PF na estaca 101. As cabeceiras ficam em 0+060 (estaca 3) e 1+960 (estaca 98).
- 

Perfis. O perfil do terreno sai da superfície TN. O greide (seção 5) é desenhado com os mesmos PIVs e curvas do cálculo.

O alinhamento horizontal é uma reta única porque pista de pouso não tem curva: a escolha está no rumo, que saiu da busca da etapa 1.

O corredor com assembly da seção-tipo ainda não foi montado, porque a interface COM do Civil 3D não cria assembly. Ele está nas pendências para 17/11 (seção 11).

## 4. Seção-tipo e a espessura do pavimento

A seção é simétrica e cai do eixo para as bordas. Os volumes são medidos até a plataforma de terraplenagem, ou seja, até o topo do subleito, e não até a superfície pronta.
 | 

Trecho (a partir do eixo) | 

Declividade | 

Pavimento
 | 

PPD: 0 a 22,5 m | 

1,5% | 

1,10 m
 | 

Acostamento: 22,5 a 30 m | 

2,5% | 

0,50 m
 | 

Faixa de pista: 30 a 150 m | 

2,5% | 

nenhum
 | 

Taludes, a partir de 150 m até o terreno | 

corte 1V:1,5H; aterro 1V:2H | 

—

O greide de terraplenagem é o greide de projeto menos 1,10 m na PPD e menos 0,50 m no acostamento. Assim, no corte se escava a espessura do pavimento a mais, e no aterro se aterra essa espessura a menos. É o caso "CORRETO" do slide 12 da aula 7 (parte 2): a espessura do pavimento deve ser considerada no cálculo dos volumes. O pavimento em si é outro serviço e não entra no volume de terraplenagem.

Os taludes foram adotados pelo grupo, porque o enunciado não os dá; são valores usuais para solo coesivo. Eles estão entre as perguntas à professora.

## 5. O greide: um problema de otimização

O greide não foi desenhado à mão. Um programa (otimiza_greide.py, método SLSQP) escolheu as cotas de 5 PIVs em posições fixas para dar o menor volume total, corte mais aterro, dentro destas restrições:
- 

rampa de até 1,5% e mudança de rampa (Δi) de até 1,5% (enunciado);
- 

declividade efetiva de até 1,0% (enunciado);
- 

curvas verticais com raio de pelo menos 30 000 m, ou seja, L = R × |Δi|, e rampa de até 0,8% no primeiro e no último quarto da PPD (Anexo 14);
- 

greide compensado: o corte tem de cobrir o aterro multiplicado pelo Fh, sem empréstimo, com sobra de no máximo 1%.

PIV é o Ponto de Interseção Vertical, onde duas rampas se encontram. Cada PIV interno recebe uma curva vertical (parábola) de comprimento L, que vai do PCV (PIV − L/2) ao PTV (PIV + L/2).
 | 

PIV | 

Estaca (m) | 

Cota (m) | 

Curva L (m) | 

PCV → PTV (m) | 

Rampa seguinte
 | 

0 (P0) | 

0 | 

559,083 | 

— | 

— | 

−0,432%
 | 

1 | 

500 | 

556,923 | 

160 | 

420 → 580 | 

+0,067%
 | 

2 | 

1000 | 

557,256 | 

100 | 

950 → 1050 | 

+0,395%
 | 

3 | 

1520 | 

559,310 | 

360 | 

1340 → 1700 | 

−0,800%
 | 

4 (PF) | 

2020 | 

555,310 | 

— | 

— | 

—

Resultado frente aos limites:
- 

maior rampa: 0,80% (limite de 1,5%), no último trecho, preso pelo teto de 0,8% do último quarto;
- 

declividade efetiva: 0,16% (limite de 1,0%). O ponto mais alto da PPD fica perto da cabeceira 06 (cerca de 558,8 m) e o mais baixo na cabeceira 24 (cerca de 555,8 m): cerca de 3,0 m em 1900 m;
- 

maior mudança de rampa: 1,195% (limite de 1,5%), no PIV 3.

A declividade máxima olha cada trecho reto do greide. A efetiva é a média da pista inteira: (cota máxima − cota mínima no eixo da PPD) / 1900 m. A efetiva usa as cotas da curva, e não as dos PIVs: com a curva de 360 m, o greide passa cerca de 0,54 m abaixo do PIV 3.

Detalhes da otimização:
- 

O otimizador trabalha com as estacas inteiras. Depois, o greide foi baixado 3 mm por igual para que o memorial, que tem duas seções extras (950 e 1050 m), também feche sem déficit.
- 

Com 7 ou 9 PIVs, o volume cai só cerca de 2%. O grupo ficou com 5 PIVs e 3 curvas, o perfil mais simples de construir.

## 6. Etapa 3: seções transversais e áreas

As áreas de corte e aterro vêm do Civil 3D, em 104 seções. Um cálculo independente em Python confere o resultado com diferença de −0,04% no corte e +0,05% no aterro.

Onde estão as seções. São 104 linhas de amostragem (grupo "SL - PPD"), com 200 m para cada lado do eixo: as 102 estacas inteiras, de 20 em 20 m, mais duas seções extras em 950 e 1050 m. Essas duas são o PCV e o PTV da curva do PIV 2, que não caem em estaca inteira. Os outros PCV e PTV (420, 580, 1340 e 1700 m) já coincidem com estacas. Cada linha corta as quatro superfícies: TN, TN_limpo, TERRAPLENAGEM e ACABADA.

Como a área é medida. Em cada seção, as cotas do terreno limpo e da plataforma foram lidas a cada 0,25 m. A área é a integral da diferença entre as duas linhas:

Uma seção pode ter corte e aterro ao mesmo tempo (seção mista). Isso é comum aqui, porque a plataforma tem 300 m de largura e o terreno varia de um lado para o outro. A limpeza é calculada à parte: 0,15 m vezes a largura entre os dois pés de talude.

As 104 vistas de seção também estão desenhadas no DWG, com exagero vertical, para as pranchas.

## 7. O fator de homogeneização: por que 1,25

O grupo adotou Fh = 1,25, e não o 1,1 do exercício da aula, porque o Fh é uma propriedade do solo do sítio. O Fh relaciona o mesmo solo em dois estados (aula 7, parte 1, slide 9): 1]]>

Ou seja, para fazer 1 m³ de aterro compactado é preciso escavar Fh m³ de corte. Por isso o aterro é multiplicado pelo Fh antes de ser comparado com o corte.

No sítio, o solo esperado é latossolo vermelho-amarelo, profundo e poroso, sobre os sedimentos do Grupo Taubaté. Um solo poroso tem massa específica natural baixa e ganha bastante densidade na compactação. Em ordem de grandeza, a massa específica in situ fica perto de 1,3 a 1,4 t/m³ e a compactada (Proctor normal) perto de 1,6 a 1,75 t/m³, o que dá Fh entre 1,2 e 1,3. O grupo ficou com 1,25, no meio da faixa. Num projeto real, o Fh sairia de ensaios: frasco de areia nos cortes e Proctor do material do aterro.

Trocar 1,1 por 1,25 mudou o projeto inteiro. Como cada m³ de aterro passou a consumir mais corte, o otimizador baixou o greide de 9 a 30 cm conforme o PIV, o que aumenta o corte e diminui o aterro até a compensação fechar de novo. Depois disso, tudo foi refeito: greide, memorial, superfícies, seções e volumes no Civil 3D, planilha e figuras.

## 8. O memorial de volumes

O corte (1.227.480 m³) cobre o aterro corrigido (1.227.389 m³) e sobram 91 m³. O memorial está na planilha Memorial_terraplenagem_PPD.xlsx, com fórmulas, no formato das aulas 7 e 8. Cada linha é uma seção, e cada linha a partir da segunda fecha o trecho entre ela e a anterior:
 | 

Resultado | 

Volume (m³)
 | 

Corte | 

1.227.480
 | 

Aterro geométrico | 

981.911
 | 

Aterro corrigido (× 1,25) | 

1.227.389
 | 

Saldo (sobra de corte) | 

+91
 | 

Compensação lateral | 

534.083
 | 

Corte que viaja ao longo do eixo | 

693.397
 | 

Limpeza da camada vegetal (15 cm) | 

95.095

Compensação lateral (coluna 10 da tabela da aula 7, parte 2, slide 10) é o volume que se resolve dentro do próprio trecho: o corte de um lado da seção vai para o aterro do outro lado, sem transporte ao longo do eixo. Só o excedente entra no diagrama de massas.

Há uma diferença de forma em relação à tabela da aula: lá, o Fh multiplica a área de aterro, e aqui multiplica o volume. Como o volume é proporcional à área, o resultado é o mesmo.

Limpeza. Os 95.095 m³ de camada vegetal ficam fora da compensação: vão para bota-fora ou para estoque, para revestir os taludes.

Conta à mão. A regra da aula de 20/10 é fazer à mão o volume entre duas estacas seguidas. O par escolhido é o das estacas 10 e 11, d = 20 m: as primeiras duas seções mistas seguidas com mais de 300 m² de corte e de aterro. Essa conta é do Guilherme. A aba "Cálculo à mão" da planilha traz só os dados e os campos em branco, e a coluna "Confere?" compara o resultado com o memorial.
 | 

Estaca | 

Área de corte (m²) | 

Área de aterro (m²)
 | 

10 + 00,00 | 

303,57 | 

522,76
 | 

11 + 00,00 | 

388,35 | 

357,67

## 9. Diagrama de Brückner e distribuição de massas

A solução adotada é uma linha de compensação (LC) única, do P0 ao PF, que compensa tudo: só os 91 m³ de sobra vão para bota-fora, com momento de transporte de 14,34 × 10⁶ m³·dam.

O diagrama. As ordenadas de Brückner são a última coluna do memorial. O diagrama fecha em zero no PF, porque o greide é compensado, mas tem ondas grandes. Ele desce até cerca de −233 mil m³ perto da estaca 54 e sobe até cerca de +166 mil m³ perto da estaca 81. Trecho subindo é trecho com predomínio de corte; trecho descendo, de aterro. Fechar em zero não quer dizer que não há transporte: as ondas mostram terra viajando centenas de metros.

A ferramenta. As ordenadas foram passadas às funções do programa em MATLAB feito para a aula de 20/10 (pasta diagrama_massas/), com as convenções da aula:
- 

uma LC só compensa entre seus cruzamentos com o diagrama; acima dela o material anda no sentido do estaqueamento, abaixo, no sentido contrário;
- 

o que fica fora das LCs é externo: sobra de corte vai para bota-fora, falta de aterro vem de empréstimo, os dois a 150 m;
- 

momento de transporte MT = soma de volume × DMT das ondas, mais o volume externo × 150 m; a DMT de cada onda é a área da onda dividida pela altura;
- 

o programa varre a cota de uma LC única e, por programação dinâmica, combinações de várias LCs com degraus, e fica com o menor MT.
 | 

Cenário | 

LCs | 

MT (10⁶ m³·dam) | 

Bota-fora (m³) | 

Empréstimo (m³)
 | 

Adotado: 1 LC do P0 ao PF | 

1 | 

14,34 | 

91 | 

0
 | 

LC única entre cruzamentos | 

1 | 

15,28 | 

91.916 | 

91.825
 | 

Até 2 LCs | 

2 | 

13,05 | 

90.511 | 

90.420
 | 

Até 3 LCs | 

3 | 

12,36 | 

129.045 | 

128.954
 | 

Ótimo do modelo da aula | 

6 | 

12,32 | 

143.554 | 

143.463

Por que o ótimo do programa não foi adotado. Com bota-fora e empréstimo a só 150 m, o menor MT abre mão de parte da compensação: joga fora 143,6 mil m³ de corte e traz 143,5 mil m³ de empréstimo, porque levar terra 150 m é mais curto que atravessá-la pela obra. Só que esse modelo não cobra a escavação do empréstimo, que exige achar uma jazida, licenciar e escavar. Esse foi o problema de Viracopos contado na aula 7.

Com os preços do exercício 6 da lista (R$ 3,20/m³ de escavação e R$ 1,60/(m³·km) de transporte), escavar 1 m³ custa o mesmo que transportá-lo 2 km. Somando os 150 m do bota-fora e os 150 m do empréstimo, cada m³ que deixa de ser compensado custa o equivalente a 2,3 km de transporte, ou 1150 m por parcela externa. Com essa DMT externa, o ótimo passa a ser a LC única que compensa tudo.

Um detalhe para não confundir: a busca de "LC única" do programa dá 15,28 porque usa a convenção do exercício 2, em que a LC vale só entre o primeiro e o último cruzamento com o diagrama. Como o diagrama começa descendo, a LC na cota do saldo só toca o diagrama no PF, e essa busca a corta. A otimização com degraus acha a mesma LC começando no P0, com um degrau de 91 m³, e ela é a melhor solução com uma LC.
 | 

Onda da solução adotada | 

De (m) | 

Até (m) | 

Sentido | 

Volume (m³) | 

DMT (m)
 | 

1 | 

0 | 

352 | 

contrário ao estaqueamento | 

74.592 | 

162
 | 

2 | 

352 | 

699 | 

do estaqueamento | 

51.110 | 

248
 | 

3 | 

699 | 

1.222 | 

contrário ao estaqueamento | 

232.661 | 

211
 | 

4 | 

1.222 | 

1.603 | 

do estaqueamento | 

146.660 | 

246
 | 

5 | 

1.603 | 

1.670 | 

contrário ao estaqueamento | 

16.317 | 

42
 | 

6 | 

1.670 | 

2.020 | 

do estaqueamento | 

165.830 | 

197

## 10. Equipamentos

O equipamento principal é o moto-scraper, porque as ondas grandes da distribuição têm DMT de 160 a 250 m, em solo de 1ª categoria. Pela classificação do DER-SP, solo de 1ª categoria é escavável com lâmina e scraper. As justificativas vêm da aula 9.
 | 

Serviço | 

Equipamento | 

Por quê
 | 

Limpeza da camada vegetal | 

Trator de esteira com lâmina reta; motoniveladora | 

A lâmina reta faz limpeza geral, cavando e amontoando; a motoniveladora capina vegetação rasa. O sítio é pasto.
 | 

Carga e remoção da limpeza | 

Pá carregadeira e basculantes | 

A pá remove material solto; o basculante comum (4,5 a 6 m³) leva ao bota-fora ou ao estoque.
 | 

Corte para aterro (DMT de 160 a 250 m) | 

Moto-scraper, com trator empurrando na carga | 

Escava, carrega, transporta e espalha numa operação só, em distâncias médias.
 | 

Onda curta perto de 1640 m (DMT de 42 m) | 

Trator de lâmina | 

Empurra o material em distância curta, sem carregar.
 | 

Camadas compactas (eventual) | 

Escarificador no trator | 

Desagrega o terreno antes da escavação.
 | 

Regularização a 1,5% e 2,5% e taludes | 

Motoniveladora | 

Acabamento da ordem de meio centímetro.
 | 

Compactação do aterro | 

Rolo pé-de-carneiro | 

Compacta de baixo para cima; indicado para solo coesivo, que predomina no sítio.
 | 

Lentes de areia (eventual) | 

Rolo vibratório | 

Adensa solos arenosos pela vibração.
 | 

Topo do subleito | 

Rolo pneumático | 

Sela a superfície e compacta solos finos.

Ficaram de fora a drag-line, que serve para solo mole e saturado (a várzea, descartada na etapa 1), e a fresadora e a vibroacabadora, que são do pavimento.

## 11. Ferramentas, arquivos e o que falta

Todo o cálculo é automatizado: mudar uma premissa (largura nivelada, taludes ou Fh) significa rodar a cadeia de scripts de novo, e não refazer à mão.

A cadeia de cálculo, na ordem em que roda (scripts em aeroporto_trabalho/):
- 

otimiza_greide.py: cotas dos PIVs.
- 

memorial.py e landxml.py: memorial em Python e superfícies de projeto em LandXML.
- 

Scripts do Civil 3D (civil3d_aeroporto.ps1, civil3d_secoes.ps1, civil3d_extrai_secoes.ps1, civil3d_vistas_faltantes.ps1): superfícies, eixo, seções e vistas.
- 

areas_civil3d.py: áreas e volumes a partir das cotas lidas no Civil 3D.
- 

distribuicao.py: chama o programa de diagrama de massas no MATLAB.
- 

planilha_memorial.py, figuras.py, roteiro_aeroporto.py e montar_pasta_apresentacao.py: planilha, figuras, roteiro e pasta da apresentação.
 | 

Arquivo | 

O que é
 | 

Aeroporto_PPD_Civil3D.dwg | 

Modelo do Civil 3D: imagem, superfícies, eixo, perfis, 104 seções e vistas
 | 

Memorial_terraplenagem_PPD.xlsx | 

Memorial com fórmulas, Brückner, conferência, cálculo à mão e equipamentos
 | 

Roteiro_aeroporto.pdf | 

Roteiro da fala por etapa e por pessoa, com perguntas prováveis
 | 

Apresentacao_aeroporto/ | 

Slides offline (HTML e PDF) e cópias dos arquivos acima
 | 

Apresentação on-line | 

21 slides em três etapas, compartilhados por link
 | 

Repositório no GitHub | 

Scripts, planilha, DWG e diário do projeto

Decisões já tomadas: PPD de 1900 m (confirmado pela professora); faixa de 300 m toda nivelada; espessura do pavimento considerada nos volumes; Fh = 1,25; distribuição com uma LC que compensa tudo.

Ainda a confirmar com a professora: os taludes 1V:1,5H e 1V:2H e o Fh = 1,25. O que ela disse na prévia de 10/11 ainda não foi registrado.

Pendências para 17/11:
- 

Corredor com o assembly da seção-tipo no Civil 3D (à mão, porque a interface COM não cria assembly)
- 

Volumes pelo Compute Materials do Civil 3D
- 

Pranchas: planta, perfil e seções
- 

Memorial final em PDF
- 

Capturas de tela do Civil 3D refeitas com Fh = 1,25 (as atuais são do modelo com Fh = 1,1)
- 

Conta à mão das estacas 10 e 11 (Guilherme)