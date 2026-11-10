# Trabalho do exame GEO-55 — aeroporto (PPD) no Civil 3D — diário de progresso

Pasta: `D:\documentos\ita\civil\4semestre\geo55\aeroporto_trabalho\`. Os scripts rodam daqui.

## Pedido
- 09/11/2026 (seg): "Quero que vá tocando o projeto". Prévia na **ter 10/11, 13h30** com a etapa 2 + terraplenagem (decisão de 03/11, ver `../anotacoes.md`); entrega final em 17/11.
- Local do sítio: **o Claude escolhe e justifica** (resposta do usuário em 09/11). Região de São José dos Campos.

## Premissas (enunciado `../trabalho segundo bimestre 2026.pdf` + aulas)
- PPD **1900 × 45 m** (Cláudia, 03/11: vale a figura, não os 2300 m do texto). Faixa de pista **2020 × 300 m** (60 m além de cada cabeceira).
- Seção: PPD 1,5% para cada lado a partir do eixo (22,5 m); faixa 2,5% (127,5 m de cada lado). Acostamentos 7,5 m (dentro dos 127,5 m).
- Declividade longitudinal máx. 1,5%; efetiva máx. 1,0%; mudança máx. de declividade 1,5%.
- Pavimento: 1,10 m na PPD e 0,50 m nos acostamentos (aula 7: **desconsiderar a estrutura do pavimento** no volume; registrar a escolha).
- Sítio: área de 3000 × 1500 m.
- Aula 7: remover 15 cm de camada vegetal em toda a faixa; não fazer aterro sobre ela; Fh = 1,1 (exercício da aula); volumes por áreas médias; memorial com ponto, estaca, áreas de corte/aterro, área média, distância, volume, aterro corrigido, acumulado, ordenadas de Brückner.
- Aula 8 (20/10): o volume entre duas estacas consecutivas deve ser **feito à mão** no memorial; o resto pode ser automatizado.

## Fontes de dados
- MDE: Copernicus GLO-30 (DSM, 1"), tiles S24W046 e S23W046 em `dados/`.
- Uso do solo: ESA WorldCover 2021 (10 m), tile S24W048.
- Vento: ERA5 pela API de arquivo do Open-Meteo.
- Imagem: Esri World Imagery (mosaico georreferenciado em UTM 23S).

## Etapa 1 — sítio escolhido (09/11)
- **Sítio A: terraço a oeste de Pindamonhangaba-SP, centro (−22,9300; −45,4993), PPD no rumo 060°/240° (cabeceiras 06/24).** ~556 m de cota, 21 m acima da várzea do Paraíba.
- Busca em 4 rodadas (`busca_sitio.py`, `busca_sitio2.py`, `refina_sitio.py`, `busca_global.py`; `ols.py`, `ver_sitio.py`):
  1. só terraplenagem → todos na **várzea** (arrozais, 530–548 m): descartada (inundável, argila mole/turfa, APA do Banhado). Filtro: ≥ 12–20 m acima do fundo de vale (raio de 3 km).
  2. OLS do Anexo 14 (código 4, precisão CAT I: aproximação 2%/2,5%, transição 14,3%, horizontal interna +45 m/4 km, cônica 5%) contra o DSM → quase todos os locais têm morros furando a horizontal interna/cônica (centenas de metros); só os rumos no eixo do vale (50–70°) passam.
  3. ruído (área urbana nos cones de aproximação de 3 km e a 500 m da faixa ≤ 10%), risco aviário (água a 3 km), mata ≤ 25%, ≥ 10 km de SBSJ e SBTA.
  4. Sobram 2 locais em 25 mil centros × 36 rumos: A (escolhido) e B (−22,906; −45,406; 25°), descartado porque uma rodovia corta a faixa e há indústria na cabeceira.
- Vento (ERA5 2015–2024, 87 672 h): média 3,0 kt, calmaria 55%, predominante ENE (17,5%), máx. 13,5 kt → cobertura ≥ 99,9% para qualquer rumo (limite 20 kt do Anexo 14 para pista ≥ 1500 m; até com 10 kt). O rumo sai do terreno e das OLS; 060° ainda fica alinhado com o vento predominante.
- Contras registrados: cavas de areia a ~1,5 km ao N (aves, mitigável), cidade a ~1 km a leste do cone NE (ruído lateral), 4% de mata no sítio. Copernicus é DSM (árvores aparecem como terreno).
- Figuras: `dados/sitio_a2.png` (5 km), `dados/candidatos.png`.

## Etapas 2 e 3 — modelo e terraplenagem (09/11)
- Motor: `projeto.py` (terreno = nós do MDE em UTM, Delaunay; alinhamento; seção-tipo; seções a cada 0,5 m; áreas médias).
  - Seção (meia): PPD 0–22,5 m a −1,5% (pav. 1,10 m); acostamento 22,5–30 m a −2,5% (pav. 0,50 m); faixa 30–150 m a −2,5%; taludes corte 1V:1,5H, aterro 1V:2H. Seções no greide de terraplenagem; limpeza 0,15 m em todo o footprint; áreas medidas a partir do TN limpo.
  - Alinhamento: P0 na extremidade SW da faixa, PF = 2020 m (estaca 101); cabeceira 06 = estaca 3, cabeceira 24 = estaca 98.
- Greide: `otimiza_greide.py 5` (SLSQP; min Vc+Va com Vc = Fh·Va). PIVs (m; cota; L): 0/559,174; 500/557,055 (L 160); 1000/557,527 (L 100); 1520/559,609 (L 380); 2020/555,609. Rampas −0,424/+0,094/+0,400/−0,800%; efetiva 0,16%; R ≥ 30 000 m; 0,8% no último trecho (quarto da PPD). 7 ou 9 PIVs só reduzem 2%.
- Memorial: `memorial.py` → 106 seções (inteiras + CAB 06/24 + PCV/PTV). Vc = 1 151 744 m³, Va = 1 046 648 m³, Fh·Va = 1 151 313 m³, saldo +431 m³, limpeza 95 023 m³ (áreas do Civil 3D).
- Civil 3D (`../Aeroporto_PPD_Civil3D.dwg`, template Metric NCS):
  - `landxml.py` → superfícies TN, TN_limpo, TERRAPLENAGEM, ACABADA (um LandXML por superfície: o ImportXML do COM só lê a primeira).
  - `civil3d_aeroporto.ps1` (etapas superficies/imagem/alinhamento): imagem Esri 1 m (`civil3d/imagem_sitio_utm23s.jpg` + .jgw), alinhamento "EIXO PPD 06-24", perfis TN e greide (estilos em **LandProfileStyles**; ProfileStyles vem vazio), vista de perfil. Cotas TN e greide = Python (< 1 mm).
  - `civil3d_secoes.ps1`: grupo "SL - PPD" com 106 linhas (±200 m), seções das 4 superfícies. Pegadinhas: `SampledSurface.Sample = $true` e `Section.StaticDynamic = 0` (senão as seções vêm vazias).
  - `civil3d_extrai_secoes.ps1` → `civil3d/secoes_civil3d.csv` (ElevationAt a cada 0,25 m); `areas_civil3d.py`: volumes Civil 3D × Python = −0,06% (corte) / +0,06% (aterro).
  - `civil3d_vistas_secoes.ps1`: vistas de seção (Road Section, exagero 5, banda Offsets Only), grade de 6 colunas abaixo do perfil. `SectionViews.Remove` não apaga a entidade: recriar o grupo de linhas.
  - PowerShell não diferencia maiúsculas: `$sl`/`$sL`, `$e`/`$E` colidiram (já corrigido).
- Planilha: `planilha_memorial.py` → `../Memorial_terraplenagem_PPD.xlsx` (Premissas, Greide com verificações, Memorial com fórmulas e gráfico de Brückner, Cálculo à mão 29→30, Conferência). Recalculada no LibreOffice: 0 erros. (`recalc.py` do skill não roda no Windows; usar `soffice --convert-to xlsx` num diretório temporário.)

## Etapas
- [x] 1. Escolha do sítio (busca automática + conferência na imagem + vento)
- [x] 2. Superfície no Civil 3D, imagem georreferenciada, alinhamento horizontal e vertical, seções
- [x] 3. Seções transversais, volumes por áreas médias, memorial, Brückner (planilha)
- [x] 4. Figuras (`figuras.py` → `figuras/`, paleta e fonte ITA: ouro #C99A06 = corte, azul #1F4FD8 = aterro, Bahnschrift) + apresentação da prévia (16 slides): https://claude.ai/artifact/8Ugecg9baS44AKMVL9Zja2 — fontes em `apresentacao_deck/project/` (root do publish; **nada no disco C**). Identidade visual ITA de `../../geo48/comum/identidade.json` + `ita_logo.png` (Caladea ≈ Cambria, Barlow ≈ Bahnschrift). Capturas do Civil 3D: `captura_civil3d.ps1` (zoom por SendCommand).
- [ ] 5. Pendências para 17/11: corredor (assembly) no Civil 3D feito à mão pelo roteiro; Compute Materials do Civil 3D; pranchas; memorial final em PDF
- [x] 5a. DMT/momento de transporte e bota-fora (09/11 noite, ver abaixo)
- [x] 4b. Grupo (igual ao projeto anterior): Pedro Feitosa Guttemberg · Guilherme Rodrigues · Gilberto Patri (na capa). Roteiro `roteiro_aeroporto.py` → `../Roteiro_aeroporto.pdf` (4 p.): Pedro slides 1–7 (enunciado e sítio), Guilherme 8–12 (Civil 3D, seção-tipo, greide, seções), Gilberto 13–16 (volumes, à mão, Brückner, próximos) + 12 perguntas prováveis.
- [x] 4c. Brasão com fundo transparente: `logo_transparente.py` → `figuras/ita_logo_transparente.png` (2700×1032, só o branco ligado à borda removido, bordas suavizadas). Usado em todos os 16 slides (inclusive os de fundo navy) e no roteiro. O original em geo48/comum não foi alterado.
- [x] 4d. GitHub público: https://github.com/psychoww/geo55-aeroporto-pindamonhangaba — repositório na pasta `geo55/` com `.gitignore` em lista branca (só README, DWG, memorial, roteiro e `aeroporto_trabalho/`; sem aulas, material da professora, `anotacoes.md` nem dados brutos). Commits com o e-mail noreply do GitHub (config local). `baixar_dados.py` recria os dados brutos; `comum/` tem o brasão e a identidade ITA (cópia de geo48).

## 09/11 (noite) — conferência com os PDFs novos e revisão (pedido: "Acrescentei alguns arquivos...")
- PDFs novos na pasta geo55: `aula 7 - projeto de terraplenagem parte 1/2.pdf`, `aula 9 - Maquinas e equipamentos.pdf`, `EXERCÍCIOS SEGUNDO BIMESTRE.pdf`.
- **Pavimento:** o slide 12 da aula 7 (parte 2) diz que a espessura do pavimento "deve ser **considerada**" (CORRETO = medir até o fundo do pavimento). O cálculo já fazia isso; só o texto dizia "desconsiderado". Corrigido em slides, roteiro, planilha, README e comentado em `../aula 7 - anotacoes 13-10.md` (também categorias DER-SP 0,5 m³ e basculante de 4,5–6 m³ da aula 9).
- **Fh = 1,25** (decisão pedida pelo Guilherme: "qual faz mais sentido para Pindamonhangaba?"): latossolo vermelho-amarelo poroso sobre o Grupo Taubaté; faixa usual 1,2–1,3. Pipeline refeito: otimiza_greide 5 → greide baixado 3 mm (memorial com seções extras fechava −879 m³) → memorial → landxml → civil3d_aeroporto (superficies, alinhamento) → civil3d_secoes → civil3d_extrai_secoes (~25 min) → areas_civil3d → planilha → figuras. Backup do greide anterior em `dados/greide_fh110.json` e `dados/memorial_fh110.json`.
  - PIVs (m; cota): 0/559,083; 500/556,923 (L 160); 1000/557,256 (L 100); 1520/559,310 (L 360); 2020/555,310. Rampas −0,432/+0,067/+0,395/−0,800%; efetiva 0,16%; Δi máx 1,195%.
  - 104 seções (PCV/PTV em 420, 580, 1340, 1700 caem em estacas inteiras; extras: 950 e 1050). Civil 3D: Vc 1 227 480; Va 981 911; ×1,25 = 1 227 389; saldo +91; compensação lateral 534 083; limpeza 95 095. Python × Civil 3D: −0,04% / +0,05%.
- **Compensação lateral** (coluna 10 da tabela da aula 7, slide 10): nova coluna O do Memorial = MIN(Vc, Fh·Va) do trecho; colunas seguintes deslocadas (gráfico de Brückner na coluna R).
- **Cálculo à mão fica com o Guilherme** (pedido): aba "Cálculo à mão" virou modelo (estacas 10→11, campos amarelos em branco, coluna Confere?); slide `mao` com os resultados em branco "[ … ]".
- **Distribuição** (`distribuicao.py` + `distribuicao_massas.m`, funções do `../diagrama_massas/`): DMT externa 150 m (aula 8). Ótimo livre: 6 LCs, MT 12,32×10⁶ m³·dam, 144 mil BF / 143 mil EMP. Variante com escavação do empréstimo (exercício 6: R$ 3,20/m³ e R$ 1,60/(m³·km) → DMT externa equivalente 1150 m): 1 LC do P0 ao PF na cota +91, MT 14,34×10⁶, BF 91 m³ — **adotada**. Ondas com DMT de 42 a 248 m. A busca de "LC única" do programa (entre cruzamentos) dá 15,28×10⁶ porque o diagrama começa descendo; não é bug (tentei mudar `dm_otimizar_unica` e desfiz).
- **Equipamentos** (aula 9): aba "Equipamentos" na planilha e slide `equipamentos` (moto-scraper para DMT 160–250 m, trator de lâmina na onda de 42 m, pé-de-carneiro, pneumático, motoniveladora…).
- **Apresentação por etapas** (pedido): 21 slides; slides de abertura `etapa1`, `etapa2`, `etapa3`; em cada etapa Pedro, Guilherme e Gilberto têm uma parte (Etapa 1: Pedro método+região, Guilherme sítio, Gilberto vento+OLS; Etapa 2: Pedro Civil 3D, Guilherme seção-tipo, Gilberto greide; Etapa 3: Pedro seções, Guilherme volumes+mão, Gilberto Brückner+distribuição+equipamentos); Pedro abre e fecha. Novos slides `distribuicao` e `equipamentos`.
- **Roteiro** reescrito: por etapa e por pessoa, cada parte com suas perguntas prováveis e respostas; tabela-resumo e "se parar na etapa N, pule para o slide 21".
- **Artefato explicativo** (pedido): https://claude.ai/artifact/9kwHf7hYZsok92DvXD9j2D (privado) — fonte `explicacao/modelo.html`, gerado por `PYTHONPATH=. python explicacao/gerar.py`.
- **Apresentação publicada** (versão 12, autorizada pelo Guilherme): figuras enviadas como asset e marcadores trocados por `apresentacao_deck/trocar_blobs.py` (no Git Bash, com `MSYS_NO_PATHCONV=1`: sem isso o /_blob/ virou C:/Program Files/Git/_blob/ em 4 slides; corrigido na versão 13). O modo automático bloqueia envio a artefato compartilhado por link sem autorização explícita.
- Civil 3D: `civil3d_vistas_secoes.ps1` passou a falhar ("Parâmetro incorreto") em todas as vistas, mesmo rodando sozinho e sem redefinir o exagero; o mesmo laço sem `$ErrorActionPreference = Stop` e sem a etapa de apagar funciona: `civil3d_vistas_faltantes.ps1` (cria só as que faltam). 104 vistas criadas, DWG salvo. Capturas do Civil 3D (`figuras/08–10`) ainda são do modelo com Fh = 1,1 (diferença visual mínima).

## 10/11 (manhã) — faixa de 300 m e pasta da apresentação
- Faixa de 300 m mantida: a nota de serviço da aula 7 é só exemplo (ver item (a) abaixo). Apresentação v14 publicada.
- **Pasta `../Apresentacao_aeroporto/`** (pedido: "Organize uma pasta aqui que tenham os arquivos desta apresentação"), montada por `montar_pasta_apresentacao.py`: `Apresentacao_PPD.html` (slides offline; setas, F = tela cheia, N = notas), `Apresentacao_PPD.pdf` (Edge headless, 21 páginas), `img/`, cópias do roteiro, memorial e DWG, `LEIA-ME.md`. As imagens /_blob/ do deck foram baixadas e conferidas por sha256: são idênticas às de `figuras/` (mapa `BLOBS` no script; 09_c3d_perfil não é usada). A pasta só tem cópias e fica fora do git; **rodar o script de novo depois de mudar slides, figuras, roteiro, memorial ou DWG.**
- Slide `distribuicao` estourava a altura (título em 2 linhas + figura de 660 px; o parágrafo final ficava sob o rodapé). Corrigido no fonte: título "Linhas de compensação do programa da aula 8" e figura com 560 px. Publicado com autorização: apresentação versão 15.

- **Área de busca exata** (pergunta: "A busca ocorreu somente no Vale do Paraíba ou em todo o Estado?"): nem um nem outro. Modelo de terreno (`dados/grade_utm30.npz`): lat −23,40 a −22,85, long −46,00 a −45,35 (67 × 61 km). Centros com 4 km de margem: lat −23,36 a −22,89, long −45,96 a −45,39 (59 × 53 km), em torno de São José dos Campos até Pindamonhangaba; 35 066 centros a cada 300 m → 28 099 fora dos 10 km de SBSJ/SBTA → 25 062 fora da várzea (≥ 12 m), × 36 rumos. O recorte foi premissa (região do ITA), não resultado da busca. Escrito no slide `metodo` (apresentação v16, publicada a pedido), no roteiro (pergunta nova), na página explicativa (v4) e no README.
- `montar_pasta_apresentacao.py` agora avisa e segue quando uma cópia está aberta em outro programa (o roteiro estava aberto em 10/11; copiado depois de fechado).

- **Texto explicativo completo** (pedido: "Gere um texto explicando do começo ao fim tudo que foi feito", fora do roteiro e da apresentação): documento Claude Docs https://claude.ai/artifact/L9u1kecHSBQXH3pUDuYMbt (privado), 11 seções, do enunciado às pendências.

- **Sítio × bairro** (pergunta: "a faixa amarela pega um pouco da cidade, está tudo bem?"): ESA WorldCover (10 m) no sítio 3000 × 1500 centrado: 10,9 ha construídos (2,4%), quase todos no canto sul (perto da cabeceira 06, lado SE); faixa 2020 × 300: 0 ha; construído mais próximo a ~160 m da borda da faixa. Varredura de 11 979 posições do sítio com a faixa dentro: nenhuma zera; a melhor (+470 m para NE, −230 m para NW) deixa 0,45 ha. Decisão do Guilherme (opção 2): **manter o sítio e justificar** — pergunta nova no roteiro (parte do Guilherme). Observação não corrigida: o WorldCover dá 70% de cultivo e 23% de pasto/campo no sítio, e os textos dizem "pasto".

- **Data do relevo** (pergunta: "isso está escrito na apresentação?"): não estava. Conferido na página oficial (https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM): Copernicus DEM = DSM, radar TanDEM-X, aquisições 2011–2015, precisão vertical absoluta < 4 m (LE90). Escrito no rodapé e nas notas do slide `regiao` (apresentação v17, autorizada) e no roteiro ("Que dados foram usados?" e "O modelo de terreno é confiável?").

## 10/11 (tarde) — depois da prévia: azimute e posição pelo MESA (em andamento)
- Pedido: "Vamos manter essa região, mas avaliar como o azimute da pista impacta e tentar equilibrar esse aspecto pelo método MESA. Pode ser alterado/movido em algum nível pra tentar fugir da cidade. Sobre a geologia, procure rapidamente e confirme o Fh. Verificar se a conta à mão é só o método das áreas médias."
- **Conta à mão:** a regra anotada (`../anotacoes.md`, 20/10) é só "o volume pelo método das áreas médias entre duas estacas consecutivas, feito à mão (mostrar a conta); o resto pode ser automatizado". Fh, compensação lateral e ordenada na aba são extras.
- **Geologia (busca rápida):** Verdade et al. (1961, Bragantia 20, levantamento de solos da Bacia de Taubaté): sobre os sedimentos terciários ocorrem latossolos argilosos e podzólicos vermelho-amarelos (hoje argissolos); os terraços (associação F) têm textura média a arenosa. A Formação Pindamonhangaba (Riccomini et al. 1991) recobre o Grupo Taubaté nos platôs de Caçapava–Taubaté–Pindamonhangaba. Fh = 1,25 continua razoável para solo argiloso poroso; trocar a frase por "solos argilosos (latossolos e argissolos vermelho-amarelos) sobre sedimentos terciários da Bacia de Taubaté".
- **MESA (manual em `../Manual_prospeccao_...pdf`)**, pontos usados: vento em setores de 10°, limite de través 20 kt para CBP ≥ 1500 m mas "sempre que possível 10 kt", utilização ≥ 95% (I-2.1.3); PPSit código 3/4 IFR-NP: área física = PPD + 600 m × 500 m; externo (75 dB) = PPD + 1420 m × 540 m (I-2.2); eliminatórios ESP, AMB, IMP, INF, PER, URB (buffer de 2 km da mancha urbana, flexibilizável) (II-2, III-1.1); TOPAlt (ΔH na área física ≤ X, X = 20 m plano / 40 m ondulado) e OBS (sem obstrução em aproximação, decolagem, transição; exceções: removíveis e dentro do PPSit) (III-2); classificatórios GEO, TOPVol, RUI (edificações na curva de 65 dB), DIS, ACE, DIP com AHP e normalização 1/x ÷ Σ(1/x) para "menor é melhor" (V; conferido com as tabelas V-6/V-7); pesos do exemplo do manual (vetor final): GEO 28,0%, TOPVol 33,3%, RUI 7,9%, DIS 12,7%, ACE 12,5%, DIP 5,6%.
- **RBAC 161, Tabela C-1** (PBZR, classe 4, 4001–7000 mov./ano): 75 dB L1 = 550 m, R1 = 160 m; 65 dB L2 = 700 m, R2 = 500 m (semicírculos centrados no prolongamento do eixo, a L da cabeceira). Cópia em `tmp/rbac161/`.
- **Scripts:** `mesa_sitio.py` (eliminatórios em 2821 centros a cada 200 m num raio de 6 km × 18 rumos = 50 778 combinações → `dados/mesa.json`, ~5 min) e `mesa_ranking.py` (candidatos, AIP, sensibilidade e figuras `figuras/12_mesa_azimute.png`, `13_mesa_candidatos.png`, `14_mesa_sensibilidade.png`). Dados novos: OSM (rodovias, ferrovia, linhas de transmissão) em `dados/osm/infra.json` (Overpass, 10/11).
  - 1ª rodada sem várzea: os "melhores" caíam na várzea (3–5 m acima do fundo do vale). Acrescentado **ALAG** (≤ 5% da área física a menos de 8 m do fundo do vale num raio de 3 km), como camada de áreas propensas a alagamento (Tabela II-4).
  - 1º ranking errado: com URB flexibilizado, ganhava um sítio dentro da cidade só por estar a 100 m de rodovia (1/x explode perto de zero). Corrigido: URB só se flexibiliza se não houver área viável (III-1.1) — há, então os colados à cidade (inclusive a prévia) saem do ranking; piso de 1 km em DIS e ACE.
- **Resultados (MESA):** vento não restringe (utilização 99,9–100% a 10 kt em todos os rumos); OBS limita o rumo a 20°–80° (eixo do vale); 379 combinações viáveis, 35 delas a ≥ 2 km da mancha urbana (rumos 40°–60°, todas ~5 km ao norte, além do rio). **Prévia: viável, mas a 0 km da mancha urbana (URB) e 19 ha construídos na curva de 65 dB.**
  - Ranking (pesos do exemplo do manual): **C1 = (−22,8885; −45,4874), rumo 060°, 4,8 km ao norte da prévia**, TOPVol 369 mil m³ (prévia 1154 mil), RUI 8,4 ha, URB 3,4 km, ACE 0,5 km, DIS 4,8 km, ΔH 15 m; nota 0,312. Depois C2 (0,259), C3, C4. Sensibilidade: C1 só perde com peso de RUI > 31% ou de TOPVol < 8%.
- **Conferência na imagem e no OSM (10/11):** em C1/C2 há o aeródromo particular **"Fazenda Santa Helena"** (nó OSM em −22,8904; −45,4933; faixa de terra de ~1,2 km a ~20° visível na imagem `tmp/mesa/sitio_C1.png`), um aglomerado de chácaras no meio da faixa (construído: C1 0,99 ha na faixa e 2,4 ha na área física; prévia 0,00 e 0,06), arrozais a leste e uma lagoa a ~130 m da faixa (PER). **Pindamonhangaba já tem o aeródromo SDPD** ("Aeroporto de Pindamonhangaba", −22,9432; −45,4313, ~7 km a leste da prévia): pista de terra de ~1110 m a 37° (OSM). Menor que a nossa PPD → não elimina por ESP (manual: só aeroportos de mesmo porte ou maior), mas precisa ser citado (o novo aeroporto o substituiria). A busca original não considerou o SDPD.
- **Volume real (otimizador de greide, 5 PIVs, Fh 1,25, `tmp/mesa/greide_C*.json`):** C1 corte 435.880 m³ / aterro 348.704 m³ (prévia: 1.227.480 / 981.911 → **−64%**), greide ~541 m, rampas ≤ 0,28%; C2 corte 588.065 m³. C1 fica mais baixo que a prévia (~541 × ~557 m), mais perto da várzea (hv mín. 6,8 m).
- **Custo de desapropriação (pedido: "Sim, inclua o custo de desapropriação")** — `custo_sitios.py` → `dados/custo_sitios.json`. Preços: SICRO 5501712 (escavação/carga/transporte 1ª cat., motoscraper, DMT 200–400 m, SP, ref. 2026-07) R$ 14,05/m³; SICRO 5502978 (compactação 100% PN, SP, 2026-07) R$ 6,38/m³ (ambos lidos em orcamentor.com, espelho do SICRO — conferir na planilha oficial do DNIT); CUB/SP R1-N set/2026 sem desoneração R$ 2.690,33/m² (portaldori, tabela Sinduscon-SP); terra rural: anúncios em Pindamonhangaba (reland.com.br) R$ 59–67 mil/ha → base 65 mil, faixa 40–120 mil (IEA não publica por município; planilha VTN da Receita não acessível). Construções = área construída WorldCover × ocupação 40% (25–60%) × CUB.
  - Terraplenagem: prévia R$ 23,5 mi; C1 8,3; C2 11,3. (A) sítio 3000 × 1500 (450 ha) deslocado para o mínimo de construções: prévia 0,48 ha → total 57,9 mi; C1 3,97 ha → 80,3; C2 81,4. (B) PPSit MESA 75 dB (179 ha): prévia 3,99 ha → 78,1; C1 3,10 ha → 53,4; C2 61,6. **O vencedor inverte conforme a área desapropriada**: as construções dominam (≈ R$ 11 mi por ha construído). Faixas (A): prévia 44,7–85,3; C1 53,1–126,4. Não captado: terra periurbana da prévia provavelmente mais cara; WorldCover "construído" inclui estradas.
- **Decisão pendente (Guilherme):** mudar para C1 (refazer etapas 2 e 3 inteiras: Civil 3D, memorial, Brückner, slides, roteiro, documento) ou manter a prévia justificando URB flexibilizado. Ver resumo dado a ele em 10/11.
- `projeto.py` aceita `GEO55_SITIO="lat,lon,rumo"` (cache de terreno próprio) e `otimiza_greide.py` aceita `GEO55_SAIDA`, para testar outro sítio sem tocar no da prévia.

## 10/11 (fim da tarde) — identidade visual do modelo de advocacia
- Pedido: "Estou insatisfeito com o modelo da apresentação, pois fica igual a de todas as pessoas que geraram pelo Claude. Utilize o modelo de apresentação de advocacia que eu mandei para gerar a identidade visual." Modelo: `../Apresentação Advocacia Básico Azul e Bege.pptx` (Canva, 10 slides).
- Extraído do XML: índigo #33335B, marfim #FFFBF5, ardósia #273348, cinza #9B9B9B, lavanda = índigo a 53% (#9F9DB6), azuis-petróleo #147699/#006A78/#88C0E6; fonte **Anaphora** (paga, embutida no .pptx) → trocada por **Spectral** (Google Fonts). Motivos: título em caixa alta num bloco índigo com linha cinza até a borda, barra lavanda na lateral, moldura deslocada atrás das imagens (`box-shadow`), bloco índigo no rodapé, fotos em preto e branco (`filter:grayscale`).
- `apresentacao_deck/estilo_advocacia.py`: lê os slides ITA de `apresentacao_deck/slides_ita/` (cópia de segurança) e escreve `project/slides/`; capa refeita no layout do modelo com `figuras/15_capa_sitio.png` (asset `/_blob/197e509a97d1b790a3cdfbc713a07011`, sem eixos); caixas das figuras ajustadas à proporção do arquivo para a moldura acompanhar o desenho; faixas coloridas dos cartões removidas. **Para mudar conteúdo de um slide daqui em diante: editar `slides_ita/<slide>.html` e rodar o script**, ou editar direto `project/slides/` e não rodar mais o script.
- `deck.json`: faces = Spectral. Apresentação **versão 18**, publicada a pedido. Pasta offline refeita.
- **Gráficos na paleta nova (pedido):** `paleta.py` (cores + fonte Spectral de `comum/fontes`, OFL) usado por `figuras.py` e `distribuicao.py` (`--so-figura` reaproveita `dados/distribuicao.json`, sem MATLAB). Corte = petróleo #147699, aterro = lavanda escura #6B6990, terreno = cinza, projeto = índigo, fundo marfim; relevo em tons de cinza (`bone`). Corrigida a legenda antiga "Pavimento (desconsiderado no volume)" → "fora do volume de terraplenagem". Textos de cor atualizados (rodapé do slide de seções, notas da região e da capa, legendas da página explicativa). Novos assets enviados e ids trocados em `slides_ita/` e em `montar_pasta_apresentacao.py`. Apresentação **versão 19**; página explicativa versão 5.
- Possível melhoria: foto em P&B nos slides de abertura de etapa (hoje com espaço vazio no meio).

## 10/11 (noite) — mudança para C1 (pedido: "Vamos mudar para C1")
- Prévia preservada: tag git `previa-10-11` (commit 711276b) + cópias em `dados/previa/` (greide, memorial, áreas, distribuição, pontos do terreno, 00_sitio, 15_capa_sitio).
- `projeto.py`: centro = C1 (−22,8885; −45,4874), rumo 060°. `dados/pontos_terreno.npy` regenerado.
- `otimiza_greide.py 5`: PIVs 0/542,391; 500/540,975 (L 160); 1000/542,027 (L 120); 1520/541,233 (L 60); 2020/541,227; rampas −0,283/+0,210/−0,153/−0,001%; Δi máx. 0,493%. Memorial com PCV3/PTV3 em 1490/1550 (extras) dava −649 m³ → greide baixado **2 mm** (`dados/greide.json`: `pvis_otimizado` + `rebaixo_m`): Vc 436.172, Va 348.356, ×1,25 = 435.445, **saldo +727 m³**, limpeza 93.010 m³ (motor Python, 104 seções).
- `exporta_civil3d.py` (8219 pontos, imagem nova 4,1 × 3,5 km) e `landxml.py` rodados. Civil 3D aberto pelo atalho métrico (`acad.exe /ld AecBase.dbx /p <<C3D_Metric>> /product C3D /language pt-BR` + DWG) — COM pronto em ~65 s. `civil3d_aeroporto.ps1 -Etapa todas` passou de 10 min (rodando em segundo plano).
- **Achado na imagem nova (`figuras/15_capa_sitio.png`)**: o "aeródromo Fazenda Santa Helena" é uma **pista asfaltada com marcação, ~1,4 km, rumo ~020°, que cruza a ponta SW da nossa faixa**; núcleo de chácaras logo a SE da faixa e casas na ponta NE. Perguntado ao Guilherme se segue com C1 (absorvendo/desativando essa pista) antes de rodar as etapas longas. **Resposta: seguir com C1** — o novo aeroporto substitui a pista particular (desativada e desapropriada); entra na justificativa e no custo.
- Civil 3D (1ª rodada, rebaixo 2 mm): superfícies, imagem, eixo, 104 seções (190 m para cada lado) e extração OK; `areas_civil3d.py`: Vc 434.011, Va 348.775 (−0,50% / +0,12% contra o Python) → **saldo Civil 3D −1.958 m³** (déficit). Greide baixado para **5 mm** no total (saldo Python +2.812); `exporta_civil3d.py` falhou ao regravar a imagem (arquivo aberto no Civil 3D; imagem igual) → `projeto.json` atualizado à mão só com os PIVs; `landxml.py` ok; refazendo superfícies + alinhamento + seções + extração no Civil 3D.
- Guilherme (10/11): "Não sei se 5 mm é praticável… não é melhor colocar 1 cm de vez?" → rodada de 5 mm parada. **Cotas dos PIVs ao centímetro, 1 cm abaixo do ótimo arredondado**: 542,38 / 540,97 / 542,02 / 541,22 / 541,22 m (rebaixo de 5,5 a 13 mm). Python: Vc 438.259, Va 346.319, saldo +5.361 (1,2%); esperado no Civil 3D ≈ +2.700 (0,6%). Cadeia do Civil 3D refeita com essas cotas.
- Civil 3D (cotas ao cm): superfícies, eixo, 104 seções e extração OK; **Vc 435.440, Va 344.978, ×1,25 = 431.223, saldo +4.216 m³ (0,97%; eu tinha escrito +2.217 por erro de conta — o Brückner estava certo)** (Python 438.259 / 346.319; −0,64% / −0,39%). Vistas de seção: 86 falhas "Violação de bloqueio" → DWG salvo, fechado e reaberto pelo COM → `civil3d_vistas_faltantes.ps1` sem falhas, **104 vistas**.
- `distribuicao.py` (MATLAB): solução com escavação do empréstimo = **2 LCs, MT 7,03 × 10⁶ m³·dam** (prévia 14,34), BF 4.216 m³, Vint 132.563 m³, **onda principal de 79 mil m³ com DMT de 745 m** (DMT média 494 m) → rever equipamento (moto-scraper vai até ~400–600 m; acima, escavadeira + caminhão) e o preço SICRO por faixa de DMT. Ótimo livre (150 m): 7 LCs, MT 3,37 × 10⁶, BF 62.840 / EMP 58.624.
- Planilha: regra do par à mão trocada (antes "> 300 m²", sem par em C1) por "par de estacas seguidas com o maior mínimo das quatro áreas" (também em `explicacao/gerar.py`) → **par 52 → 53** (1040–1060 m: corte 286,27 / 231,39 m²; aterro 252,72 / 271,10 m²).
- Gráficos refeitos; `05_perfil` com eixo y fixo da prévia (vazio) — corrigir; `07_brueckner` com ordenada final +4.216 = saldo do Civil 3D (conferido).
- **Achado grave (OLS, todas as superfícies, malha de 90 m):** C1 tem **horizontal interna furada em 146 m / 665 ha e cônica em 205 m / 1107 ha** (morros ~4 km ao N, pé da Mantiqueira, ~(−22,858; −45,507)); aproximação 1,3 m / 2 ha. Prévia: tudo livre (aprox. 1,8 m / 3 ha). O OBS do MESA (manual III-2.2) só elimina por aproximação/decolagem/transição; as demais "devem ser documentadas" — por isso C1 passou. A busca original (todas as superfícies) não aceitaria C1. Perguntado ao Guilherme como seguir. **Resposta: seguir com C1 e documentar.**
- **Correção de dados (10/11):** a grade da busca (`dados/grade_utm30.npz`) termina em −22,85°; C1 fica a ~4 km da borda, e a amostragem antiga repetia a borda fora dela. `ols.amostra` passou a ler os tiles Copernicus inteiros (−22° a −24°). Com o terreno completo, C1: **aproximação 3,9 m / 3 ha** (árvores perto das pontas; OBS do MESA continua OK), **horizontal interna 144 m / 675 ha, cônica 255 m / 1422 ha** (morros ao N, pé da Mantiqueira). Mapa em planta novo: `ols_planta.py` → `figuras/16_ols_planta.png`. As combinações de `mesa_sitio.py` perto da borda norte foram verificadas com a grade antiga (não refeito).
- Gráficos: títulos e eixos do perfil e dos obstáculos agora calculados (perfil de C1: rampa máx. 0,28%, efetiva 0,06%).
- Capturas do Civil 3D (08–10) refeitas para C1 (DWG reaberto) e recortadas para a área do desenho.
- **Textos para C1:** `apresentacao_deck/atualiza_slides_c1.py` reescreve as fontes `slides_ita/` (sítio, obstáculos com o mapa 16, perfil, volumes, mão 52→53, Brückner, distribuição, equipamentos com DMT 745 m e SICRO 5501714, fechamento) e cria 4 slides MESA (`mesa_criterios`, `mesa_azimute`, `mesa_ranking`, `mesa_custo`): **25 slides**. Depois `estilo_advocacia.py`. Assets novos enviados (16 imagens; ids no `BLOBS` de `montar_pasta_apresentacao.py`). Roteiro (`tmp/roteiro_c1.py`), página explicativa (versão 6, publicada; `tmp/explicacao_c1.py`) e README (`tmp/readme_c1.py`) atualizados. Limpeza = 92.401 m³ (Civil 3D).
- Apresentação publicada (25 slides, **versão 20**) com autorização do Guilherme ("Publique").

## Retomar daqui (10/11/2026, noite) — sítio C1
- Projeto em **C1** (−22,8885; −45,4874; rumo 060°). Prévia preservada na tag git `previa-10-11` e em `dados/previa/`.
- Pendente: documento explicativo (Claude Docs) ainda descreve a prévia, recálculo da planilha no LibreOffice (fórmulas), conferir `custo_sitios.py` com DMT 745 m (SICRO 5501714, R$ 18,14/m³), corredor/assembly, Compute Materials, pranchas, memorial final em PDF, conta à mão (Guilherme, estacas 52→53), conferir a geologia no mapa.

## Retomar daqui (fim da sessão de 09/11/2026, ~21h) — HISTÓRICO, sítio da prévia

### Estado
- Prévia pronta para ter 10/11, 13h30. Arquivos: DWG (Fh = 1,25, 104 seções e 104 vistas), `../Memorial_terraplenagem_PPD.xlsx` (recalculada, 0 erros) e `../Roteiro_aeroporto.pdf` (por etapas, com perguntas por parte).
- Apresentação: https://claude.ai/artifact/8Ugecg9baS44AKMVL9Zja2, versão 19 (10/11, identidade do modelo de advocacia e gráficos na paleta nova), **compartilhada por link** (todos veem as atualizações). Tem 21 slides, divididos nas etapas 1, 2 e 3.
- Página explicativa: https://claude.ai/artifact/9kwHf7hYZsok92DvXD9j2D (**privada**; compartilhar pelo Share se Pedro e Gilberto forem usar). Para atualizar: `PYTHONPATH=. python explicacao/gerar.py`, depois publicar de novo o mesmo `explicacao/index.html` (root `explicacao/`, com `img/`).
- GitHub público: https://github.com/psychoww/geo55-aeroporto-pindamonhangaba, último commit `6edc590`. Depois de cada mudança: `git add` + commit + push na pasta `geo55/` (o .gitignore é lista branca; `aeroporto_trabalho/tmp/` fica fora).

### Primeira coisa na próxima sessão
1. **Perguntar o que a Cláudia respondeu na prévia** e registrar aqui e em `../anotacoes.md`:
   - ~~(a) faixa de 300 m toda nivelada ou só ±75 m?~~ **Resolvido (10/11, Guilherme):** a nota de serviço do slide 21 da aula 7 (parte 1) é só um exemplo e não vale para o projeto. Mantém-se a faixa de 300 m toda nivelada (`B_FAIXA = 150.0` de cada lado). Texto corrigido no roteiro (PDF regenerado), no slide `proximos` (pergunta removida; apresentação versão 14, publicada com autorização), na página explicativa (versão 3) e no README.
   - ~~(b) taludes 1V:1,5H / 1V:2H?~~ **Resolvido (10/11, Guilherme): os taludes podem ser mantidos assim.**
   - (c) Fh = 1,25?
   - (d) quanto das etapas foi pedido e o que ela comentou.
2. Se algo mudar (por exemplo, `B_FAIXA`, taludes ou `FH` em `projeto.py`), rodar de novo, **nesta ordem**:
   1. `otimiza_greide.py 5` (com `PYTHONUTF8=1`; conferir o saldo no memorial e, se der déficit, baixar o greide alguns mm como em 09/11);
   2. `memorial.py`, depois atualizar os `pvis` de `civil3d/projeto.json`;
   3. `landxml.py`;
   4. `civil3d_aeroporto.ps1 -Etapa superficies` e `-Etapa alinhamento`;
   5. `civil3d_secoes.ps1`;
   6. `civil3d_extrai_secoes.ps1` (~25 min; rodar em segundo plano);
   7. `civil3d_vistas_faltantes.ps1` (veja abaixo);
   8. `areas_civil3d.py`;
   9. `distribuicao.py` (MATLAB, ~1 min);
   10. `planilha_memorial.py`, `figuras.py`, `explicacao/gerar.py` e `roteiro_aeroporto.py`;
   11. atualizar os números escritos nos slides, no README e no roteiro.
   - Não rodar MATLAB nem outros scripts junto com os scripts do Civil 3D.

### Ideias para depois (Guilherme, 10/11, vendo as apresentações dos colegas)
**Objetivo das três ideias:** deixar o método de escolha do sítio mais claro e objetivo. Proposta de forma: critérios eliminatórios (passa/não passa) separados dos classificatórios (com nota e peso), cada um com fonte e limite; uma tabela de notas dos candidatos; e um teste de quanto a escolha muda se os pesos mudarem.
1. **Seguir o documento de escolha de sítio aeroportuário do professor CJ (ITA).** Baixado em 10/11: `../Manual_prospeccao_sitios_aeroportuarios_regionais_SAC-ITA_2021.pdf` ("Manual de Apoio à Prospecção de Sítios Aeroportuários Regionais", SAC/MInfra + ITA, jul/2021, 100 p., coordenação Cláudio Jorge Pinto Alves). Método **MESA**: critérios eliminatórios (reduzem a área de busca) e classificatórios, agregados por prioridades (AIP). Siglas da lista de abreviaturas (ler o capítulo de cada uma antes de usar):
   - eliminatórios: AMB (ambiental), DIM (dimensionamento/disponibilidade de área), ESP (espaço aéreo), IMP (outros impactos), INF (área ocupada por infraestrutura), MET (cobertura de ventos), OBS (obstáculos aos planos de proteção), TOPAlt (variação altimétrica na área), URB (ruído nas áreas vizinhas);
   - classificatórios: ACE (distância à rodovia pavimentada), DIP (serviços de utilidade pública), DIS (distância ao polo gerador de demanda), GEO (geotecnia), RUI (edificações afetadas pelo ruído), TOPVol (proxy do volume de terraplenagem); PER (perigos na aproximação, como aves e fumaça) também aparece.
   - Já cobertos de algum jeito na busca: TOPVol/TOPAlt (índice de terraplenagem), OBS, MET, URB/RUI (área urbana nos cones; o bairro no canto sul cabe em RUI), PER (água a 3 km), ESP (só como 10 km de SBSJ/SBTA). Faltam: AMB, ACE, DIP, DIS, GEO (ligado à pendência da geologia) e a agregação por pesos.
2. **Gráficos das orientações possíveis da pista com uma nota** que pese o ajuste ao anemograma contra o custo de terraplenagem (e as superfícies de proteção como restrição). Os dados já existem: índice de terraplenagem por rumo (busca) e vento ERA5. Cuidado: no sítio atual, a cobertura de vento passa de 99,9% em qualquer rumo, então o vento só diferencia rumos com um limite de vento cruzado mais apertado (por exemplo, 10 ou 13 kt) ou com a componente de proa/cauda.
3. **Se for escolhido outro sítio: uma região mais carente de infraestrutura aeroportuária.** Muda a área de busca (hoje um recorte em volta de São José dos Campos) e acrescenta um critério de demanda (por exemplo, distância ao aeroporto com voo regular mais próximo e população atendida). Trocar o sítio refaz as etapas 2 e 3 inteiras: a cadeia de scripts roda de novo, mas o Civil 3D, as figuras e os slides também.

### Para a versão final (Guilherme, 10/11)
- ~~Estaqueamento de 5 em 5 m~~ **Descartado (10/11, Guilherme): a versão final fica com estacas de 20 em 20 m.** (Ele lembrou que em aeroportos a estaca costuma ser de 5 m, mas decidiu manter 20 m.)

### Pendências
- **A fazer depois (pedido em 10/11): conferir geologia e solo do sítio.** A frase "latossolo vermelho-amarelo poroso sobre o Grupo Taubaté" (slide `volumes`, roteiro, página explicativa, documento explicativo) foi escrita sem consultar mapa. Consultar no ponto (−22,9300; −45,4993) o mapa geológico do Serviço Geológico do Brasil (GeoSGB) e o mapa pedológico do Estado de SP. Suspeita: o terraço pode estar sobre a **Formação Pindamonhangaba** (Mioceno–Quaternário, sobre o Grupo Taubaté em discordância; Riccomini et al. 1991) ou terraços mais novos. Se der diferente, corrigir a frase nesses lugares (publicar slide só com autorização). O raciocínio do Fh = 1,25 (solo argilo-arenoso poroso) deve continuar valendo.
- **Conta à mão (estacas 10 → 11): é do Guilherme.** Não preencher a aba "Cálculo à mão" nem os "[ … ]" do slide 16.
- **Capturas do Civil 3D** (`figuras/08_c3d_planta.png`, `09_c3d_perfil.png`, `10_c3d_secoes.png`, usadas nos slides civil3d e c3dsecoes) ainda são do modelo com Fh = 1,1. Refazer com `captura_civil3d.ps1` e trocar na apresentação.
- **Para 17/11:**
  - corredor com assembly da seção-tipo no Civil 3D (o COM não cria assembly: fazer à mão pelo roteiro ou plugin .NET, mas não há SDK .NET instalado);
  - Compute Materials;
  - pranchas (planta, perfil e seções);
  - memorial final em PDF.
- `civil3d_vistas_secoes.ps1` passou a falhar ("Parâmetro incorreto") em todas as vistas. Usar `civil3d_vistas_faltantes.ps1`, que cria só as vistas que faltam; para recriar todas, apagar as antigas antes. A causa não foi descoberta.
- Oferecido e ainda sem resposta: incluir no repositório as anotações das aulas 7 e 8.

### Cuidados
- **Publicar na apresentação** (enviar figuras ou slides) só com autorização explícita do Guilherme: o modo automático bloqueia envio a artefato compartilhado por link.
- Fluxo da apresentação: enviar as figuras como asset → `trocar_blobs.py` → publicar `project/...` com root `apresentacao_deck`. No Git Bash, `MSYS_NO_PATHCONV=1 python apresentacao_deck/trocar_blobs.py ...`; sem isso, `/_blob/` vira `C:/Program Files/Git/_blob/` (aconteceu em 09/11).
- Heredoc no Bash às vezes falha com HTML e aspas. Para editar slides, usar a ferramenta Write/Edit ou um script `.py` em `tmp/`.
- Os scripts do Civil 3D precisam do Civil 3D aberto com `Aeroporto_PPD_Civil3D.dwg` ativo.
