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
- [ ] 5. Pendências para 17/11: corredor (assembly) no Civil 3D feito à mão pelo roteiro; Compute Materials do Civil 3D; DMT/momento de transporte
- [x] 4b. Grupo (igual ao projeto anterior): Pedro Feitosa Guttemberg · Guilherme Rodrigues · Gilberto Patri (na capa). Roteiro `roteiro_aeroporto.py` → `../Roteiro_aeroporto.pdf` (4 p.): Pedro slides 1–7 (enunciado e sítio), Guilherme 8–12 (Civil 3D, seção-tipo, greide, seções), Gilberto 13–16 (volumes, à mão, Brückner, próximos) + 12 perguntas prováveis.
- [x] 4c. Brasão com fundo transparente: `logo_transparente.py` → `figuras/ita_logo_transparente.png` (2700×1032, só o branco ligado à borda removido, bordas suavizadas). Usado em todos os 16 slides (inclusive os de fundo navy) e no roteiro. O original em geo48/comum não foi alterado.
