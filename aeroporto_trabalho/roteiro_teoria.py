"""Bagagem teórica do roteiro: por parte (integrante, primeiro slide da parte), os conceitos que sustentam a fala.
Fontes: anotações das aulas 7, 8 e 9 de GEO-55, documento explicativo do projeto (cópia em explicacao/documento_explicativo_backup.md),
Anexo 14 / RBAC 154, manual MESA (SAC/ITA, 2021) e mapa geológico do SGB. Usado por roteiro_aeroporto.py."""

TEORIA = {
    # ------------------------------------------------------------------ abertura
    ('Pedro', 'cover'): [
        ('Elementos de uma pista', 'A <b>PPD</b> (pista de pouso e decolagem) é a parte pavimentada onde a aeronave pousa e decola: aqui 1900 × 45 m. '
         'Os <b>acostamentos</b> (7,5 m de cada lado) protegem contra a erosão pelo jato e dão apoio a uma saída acidental. A <b>faixa de pista</b> '
         '(2020 × 300 m) é a área nivelada e livre de obstáculos em volta da PPD, que reduz o dano se a aeronave sair da pista; por isso ela é '
         'terraplenada inteira. As <b>cabeceiras</b> recebem o número do rumo magnético dividido por 10: rumo 060° vira 06 e o sentido oposto, 240°, vira 24.'),
        ('Declividades: por que há limites', 'A <b>longitudinal</b> máxima (1,5% para código 4) limita a perda de desempenho na decolagem e a '
         'visibilidade ao longo da pista; a <b>efetiva</b> (diferença entre a maior e a menor cota do eixo dividida pelo comprimento, ≤ 1,0%) controla a '
         'subida média; a <b>mudança de declividade</b> (≤ 1,5%) e o raio mínimo das curvas verticais (30 000 m) evitam cristas que escondam '
         'a pista ao piloto. A <b>transversal</b> (1,5% na PPD, 2,5% na faixa) drena a água para fora do eixo.'),
    ],
    # ------------------------------------------------------------------ etapa 1
    ('Pedro', 'etapa1'): [
        ('Critérios eliminatórios e classificatórios', 'O manual MESA separa dois tipos de critério. Os <b>eliminatórios</b> são passa/não passa e '
         'tiram áreas do mapa: espaço aéreo (ESP), vento (MET), ambiente (AMB), infraestrutura (INF), relevo (TOPAlt), obstáculos (OBS), cidade (URB). '
         'Os <b>classificatórios</b> dão nota aos sítios que sobram: volume de terra (TOPVol), geotecnia (GEO), distância à cidade (DIS), acesso (ACE), '
         'ruído sobre edificações (RUI) e rede elétrica (DIP).'),
        ('Como a nota é calculada (AHP)', 'Os pesos vêm do método AHP (Analytic Hierarchy Process): especialistas comparam os critérios dois a dois '
         '("TOPVol é quantas vezes mais importante que DIS?") e os pesos saem do autovetor dessa matriz de comparações. Usamos os pesos do exemplo do manual. '
         'Para critérios do tipo "menor é melhor", cada sítio recebe (1/x) ÷ Σ(1/x); a nota final é a soma dos pesos vezes essas notas. '
         'A <b>análise de sensibilidade</b> varia cada peso e mostra quando o 1º lugar muda: C1 só perde com RUI > 31% ou TOPVol < 8%.'),
        ('Por que 2 km da cidade', 'O ruído aeronáutico é regulado pelo Plano de Zoneamento de Ruído (RBAC 161): curvas de 75 e 65 dB em volta da pista '
         'limitam o uso do solo (residência dentro de 65 dB é incompatível). O MESA usa 2 km da mancha urbana como eliminatório e só o flexibiliza quando '
         'não há outra área viável; havia, e por isso a prévia, colada à cidade, saiu do ranking.'),
        ('Custo: SICRO e CUB', 'O <b>SICRO</b> (DNIT) dá o preço de cada serviço por composição, com faixas de DMT: escavação, carga e transporte com '
         'moto-scraper sai R$ 14,05/m³ para 200–400 m e R$ 18,14/m³ para distâncias maiores. O <b>CUB</b> (Sinduscon) é o custo do metro quadrado '
         'construído, usado para estimar as benfeitorias desapropriadas.'),
    ],
    ('Guilherme', 'sitio'): [
        ('Várzea e solo mole', 'A planície do Paraíba é plana, mas inunda e tem argila mole, turfa e lençol raso: aterro sobre ela recalca por anos '
         '(adensamento) e exige drenagem e reforço. Por isso a várzea virou critério: no máximo 5% da área física a menos de 8 m do fundo do vale. '
         'C1 fica 12,5 m acima.'),
        ('Geologia do sítio (SGB)', 'O mapa do Serviço Geológico do Brasil na escala 1:100.000 (folha Pindamonhangaba) põe a faixa sobre a '
         '<b>Formação Tremembé</b> (Grupo Taubaté, terciário: argilitos verdes, folhelhos e margas de um antigo lago) da estaca 0 à 65 e sobre '
         '<b>depósito aluvionar</b> (cascalho, areia e lama) daí ao fim. Por cima há solo de alteração argiloso. Argilitos do Tremembé podem ter '
         'argila expansiva (esmectita): pedem ensaio do subleito. O aluvião, sob o maior aterro, pede sondagem.'),
        ('Uso do solo e desapropriação', 'O ESA WorldCover classifica cada pixel de 10 m (pasto, cultivo, árvores, construído). A área construída '
         'atingida pesa muito no custo: cerca de R$ 11 milhões por hectare construído (40% de ocupação × CUB).'),
    ],
    ('Gilberto', 'vento'): [
        ('Coeficiente de utilização (vento)', 'É a porcentagem do tempo em que a componente de vento cruzado fica abaixo do limite da aeronave. '
         'A componente cruzada é V·sen(θ), com θ = ângulo entre o vento e o eixo. O Anexo 14 pede pelo menos 95%, com limite de 20 kt para pistas de '
         '1500 m ou mais (13 kt de 1200 a 1500 m; 10 kt abaixo). Em C1 dá 99,9–100% em qualquer rumo, porque o vento é fraco (média de 3 kt).'),
        ('Superfícies limitadoras de obstáculos (OLS)', 'Planos imaginários em volta da pista que o terreno e as construções não podem furar '
         '(Anexo 14 / RBAC 154, código 4, aproximação de precisão CAT I): <b>aproximação</b> (rampas de 2% e 2,5% a partir de 60 m antes da cabeceira), '
         '<b>transição</b> (14,3% para os lados da faixa), <b>horizontal interna</b> (plano 45 m acima da elevação do aeródromo, raio de 4 km) e '
         '<b>cônica</b> (5% a partir da borda da horizontal, até +100 m). Aproximação, decolagem e transição protegem o pouso e a decolagem diretos; '
         'a horizontal e a cônica protegem o circuito de tráfego. Por isso o MESA elimina pelas primeiras e manda documentar as outras.'),
    ],
    # ------------------------------------------------------------------ etapa 2
    ('Pedro', 'etapa2'): [
        ('MDT, MDS e TIN', 'O <b>MDT</b> (modelo digital do terreno) é o chão; o <b>MDS</b> (de superfície) inclui árvores e construções. O Copernicus GLO-30 '
         'é um MDS de radar (TanDEM-X) com grade de 30 m. No Civil 3D, os pontos viram uma <b>TIN</b> (rede irregular de triângulos): a cota em '
         'qualquer ponto é interpolada no plano do triângulo que o contém.'),
        ('Georreferenciamento', 'Coordenadas em SIRGAS 2000, projeção UTM fuso 23S (metros). A imagem entra com um arquivo de mundo (.jgw), que '
         'diz o tamanho do pixel e a coordenada do canto, e cai no lugar certo sobre as superfícies.'),
        ('Estaqueamento', 'O eixo é dividido em estacas de 20 m a partir do P0. A notação "52 + 00,00" é a estaca 52 mais 0,00 m, ou 1040 m do P0. '
         'Pontos notáveis (cabeceiras, PCV, PTV) entram com a parte fracionária, como "74 + 10,00".'),
        ('Por que o eixo é uma reta', 'Pista de pouso não tem curva horizontal: o projeto horizontal se resume à posição e ao rumo, que vieram da etapa 1.'),
    ],
    ('Guilherme', 'secaotipo'): [
        ('Camadas do pavimento e o subleito', 'O pavimento é a estrutura (revestimento, base, sub-base e, às vezes, reforço) apoiada no <b>subleito</b>, '
         'o terreno terraplenado. A terraplenagem entrega o topo do subleito; o pavimento é outro serviço. Por isso o greide de terraplenagem é o greide '
         'acabado menos a espessura do pavimento: 1,10 m na PPD e 0,50 m no acostamento (aula 7, slide 12: a espessura "deve ser considerada").'),
        ('Taludes', 'Inclinação das faces de corte e aterro, dada como V:H. Talude de aterro é mais deitado (1V:2H) porque o material é lançado e '
         'compactado; o de corte (1V:1,5H) se apoia no solo natural. Os valores certos saem da estabilidade (ensaios de resistência); os nossos são '
         'usuais para solo coesivo.'),
    ],
    ('Gilberto', 'perfil'): [
        ('Greide, PIV e curva vertical', 'O greide é o perfil do projeto no eixo. Rampas retas se encontram nos <b>PIVs</b> (pontos de interseção vertical); '
         'cada PIV interno recebe uma <b>parábola</b> de comprimento L, do PCV (PIV − L/2) ao PTV (PIV + L/2). Com rampas i₁ e i₂, a cota a uma distância x '
         'do PCV é z = z<sub>PCV</sub> + i₁·x + (i₂ − i₁)·x²/(2L). O raio é R = L / |i₂ − i₁|; para R ≥ 30 000 m, L ≥ 30 000 × |Δi|.'),
        ('Por que otimizar', 'O greide define o volume de terra. Um otimizador (SLSQP) escolheu as cotas dos 5 PIVs para o menor volume, com as restrições '
         'do Anexo 14 e o corte igual ao aterro × Fh (greide compensado). As cotas foram arredondadas ao centímetro e baixadas 1 cm, porque ninguém executa milímetro.'),
        ('Declividade efetiva', '(cota máxima − cota mínima no eixo da PPD) ÷ comprimento da PPD, com as cotas da curva, não as dos PIVs. Em C1: 0,06%.'),
    ],
    # ------------------------------------------------------------------ etapa 3
    ('Pedro', 'etapa3'): [
        ('Seção transversal e seção mista', 'Em cada estaca, a seção corta o terreno limpo e a plataforma. Onde o terreno está acima, é <b>corte</b>; abaixo, '
         '<b>aterro</b>. Com 300 m de largura, a mesma seção costuma ter os dois: é a <b>seção mista</b>. A área é a integral da diferença entre as duas '
         'linhas, aqui lida a cada 0,25 m.'),
        ('Offset e pé de talude', 'Onde o talude encontra o terreno fica o <b>offset</b> (pé do talude no aterro, crista no corte). A distância do eixo até '
         'ele, dos dois lados, define a largura da obra, a área de limpeza e a desapropriação mínima.'),
        ('Nota de serviço', 'É a tabela que vai para o campo (aula 7): por estaca, as cotas do terreno e do greide, a altura de corte ou aterro no eixo e os '
         'offsets com as cotas. A topografia crava as estacas de offset e a obra trabalha até elas. No formato completo da aula, cada estaca traz os '
         'pontos notáveis da seção (pés de talude, bordas da faixa, do acostamento e da pista, eixo) com distância transversal, cota primitiva, cota de '
         'projeto e espessura (primitiva − projeto), e os volumes de corte e aterro do trecho.'),
        ('Limpeza', 'A camada vegetal (15 cm) é orgânica e compressível: sai antes de tudo, vai para bota-fora ou estoque (revestir taludes) e não entra na '
         'compensação. Por isso as áreas são medidas a partir do terreno limpo.'),
    ],
    ('Guilherme', 'volumes'): [
        ('Áreas médias × prismoide', 'Áreas médias: V = (A₁ + A₂)/2 × d. Prismoide (Torricelli): V = d/6 × (A₁ + 4A<sub>m</sub> + A₂), com A<sub>m</sub> a '
         'área da seção do meio. As áreas médias são exatas quando A<sub>m</sub> é a média de A₁ e A₂; em geral superestimam um pouco, mais na passagem '
         'de corte para aterro (quando uma área tende a zero, o sólido é uma pirâmide, e o certo seria A·d/3, não A·d/2).'),
        ('Fh e empolamento', 'O <b>Fh</b> (fator de homogeneização) = γ<sub>s</sub> compactado no aterro ÷ γ<sub>s</sub> natural no corte: quanto corte '
         'é preciso para 1 m³ de aterro compactado. Por isso o aterro é multiplicado pelo Fh antes de ser comparado com o corte. O <b>empolamento</b> é outra '
         'coisa: compara o corte com o material <b>solto</b> no caminhão e serve para dimensionar o transporte. Exemplo de ordem de grandeza: '
         'γ in situ 1,4 t/m³ e Proctor 1,75 t/m³ dão Fh = 1,25.'),
        ('Compensação lateral', 'No mesmo trecho, o corte de um lado vai para o aterro do outro sem andar ao longo do eixo: é o menor entre o corte e o aterro '
         'corrigido do trecho. Só o excedente entra no diagrama de massas. Aqui: 238 mil m³ resolvidos na própria seção, 197 mil m³ viajam.'),
        ('Corredor no Civil 3D', 'A <b>montagem</b> (assembly) é a seção-tipo feita de peças (subassemblies): pista, acostamento, link, talude. '
         'O <b>corredor</b> a repete ao longo do eixo e do greide e encontra o terreno nos taludes. Cada peça marca suas linhas com <b>códigos</b>: '
         '<i>Top</i> (superfície acabada) e <i>Datum</i> (base, aqui o topo do subleito). O <b>Calcular materiais</b> compara o terreno com a Datum nas '
         'linhas de amostragem e soma pelas áreas médias.'),
    ],
    ('Gilberto', 'brueckner'): [
        ('Propriedades do diagrama de massas', 'Ordenada: O<sub>i</sub> = O<sub>i−1</sub> + (V<sub>corte</sub> − Fh·V<sub>aterro</sub>). '
         'Trecho <b>subindo</b> = predomina corte; <b>descendo</b> = predomina aterro. Máximo = passagem de corte para aterro; mínimo = de aterro para corte. '
         'A ordenada final é o saldo: + vai para bota-fora, − vem de empréstimo.'),
        ('Linha de compensação (LC)', 'Uma horizontal sobre o diagrama. Entre dois cruzamentos com a curva, corte e aterro se compensam (onda). '
         'Onda acima da LC: a terra anda no sentido do estaqueamento; abaixo, no sentido contrário. O que fica fora das LCs é externo (bota-fora ou empréstimo, '
         'a 150 m pela aula 8).'),
        ('DMT e momento de transporte', 'Na onda, o volume V é a altura em relação à LC e o momento M é a área entre a onda e a LC. '
         '<b>DMT = M / V</b> (leitura aproximada: a largura da onda na metade da altura). O momento total é MT = Σ V·DMT + volume externo × 150 m, '
         'em m³·dam (1 dam = 10 m). O programa da aula muda as LCs até o menor MT.'),
        ('Por que não o ótimo do programa', 'O modelo da aula só cobra transporte; com bota-fora e empréstimo a 150 m, ele prefere jogar fora e buscar '
         'terra. Mas o empréstimo precisa de jazida, licença e escavação (o problema de Viracopos, aula 7). Pelos preços do exercício 6 (R$ 3,20/m³ de '
         'escavação; R$ 1,60/(m³·km) de transporte), escavar 1 m³ equivale a transportá-lo 2 km. Com esse custo, compensar tudo fica mais barato.'),
        ('Equipamento pela DMT (em uma frase)', 'Trator de lâmina para distâncias curtas (até ~100 m), moto-scraper para as médias (até ~800–1000 m no SICRO), '
         'escavadeira e caminhão para as longas; pé-de-carneiro compacta solo argiloso de baixo para cima.'),
    ],
}

FORMULAS = [
    ('Áreas médias', 'V = (A₁ + A₂)/2 × d'),
    ('Prismoide', 'V = d/6 × (A₁ + 4A<sub>m</sub> + A₂)'),
    ('Aterro corrigido', 'V<sub>a,corr</sub> = Fh × V<sub>aterro</sub>; Fh = γ<sub>s,compactado</sub>/γ<sub>s,natural</sub>'),
    ('Compensação lateral', 'menor(V<sub>corte</sub>; Fh·V<sub>aterro</sub>) no trecho'),
    ('Ordenada de Brückner', 'O<sub>i</sub> = O<sub>i−1</sub> + V<sub>corte</sub> − Fh·V<sub>aterro</sub>'),
    ('DMT e momento', 'DMT = M/V; MT = Σ V·DMT + V<sub>ext</sub> × 150 m (m³·dam)'),
    ('Curva vertical', 'z = z<sub>PCV</sub> + i₁x + (i₂ − i₁)x²/(2L); R = L/|Δi| ≥ 30 000 m'),
    ('Declividade efetiva', '(z<sub>máx</sub> − z<sub>mín</sub>)/L<sub>PPD</sub> ≤ 1,0%'),
    ('Vento cruzado', 'V<sub>t</sub> = V·sen θ; utilização ≥ 95% (Anexo 14)'),
]

NUMEROS = [
    ('Sítio C1', '−22,8885; −45,4874 · rumo 060° · 4,8 km do centro · 3,4 km da mancha urbana'),
    ('Geometria', 'PPD 1900 × 45 m · faixa 2020 × 300 m · estacas 0 a 101 · cabeceiras nas estacas 3 e 98'),
    ('Greide', 'PIVs 542,38 / 540,97 / 542,02 / 541,22 / 541,22 m · rampa máx. 0,28% · efetiva 0,06% · Δi máx. 0,49%'),
    ('Volumes', 'corte 435.440 · aterro 344.978 · × 1,25 = 431.223 · saldo +4.216 · comp. lateral 238.422 · limpeza 92.401 (m³)'),
    ('Fh', 'adotado 1,25 · fecha exato com 1,26 · ±0,05 muda o saldo em ~17 mil m³'),
    ('Corredor', 'corte 435.037 (−0,1%) · aterro × 1,25 = 442.740 (+2,7%) · saldo −7.703'),
    ('Distribuição', '2 LCs · MT 6,61 × 10⁶ m³·dam · onda principal 79 mil m³ a 745 m · ótimo a 150 m: 3,37 × 10⁶ com 63/59 mil m³ externos'),
    ('Par à mão', 'estacas 52 → 53 · corte 286,27 / 231,39 m² · aterro 252,72 / 271,10 m² · d = 20 m'),
    ('Obstáculos', 'aproximação 3,9 m (árvores) · horizontal interna 144 m · cônica 255 m (morros ao norte)'),
]
