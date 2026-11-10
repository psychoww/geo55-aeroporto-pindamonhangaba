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

## Retomar daqui (fim da sessão de 09/11/2026, ~17h30)
- Prévia pronta para ter 10/11 13h30: DWG, memorial, apresentação (artifact 8Ugecg9baS44AKMVL9Zja2, privada: o Guilherme precisa compartilhar), roteiro por etapas (ver a seção de 09/11 noite).
- GitHub público https://github.com/psychoww/geo55-aeroporto-pindamonhangaba (README lista os arquivos que ficaram de fora). Após mudanças: `git add` + commit + push na pasta `geo55/` (o .gitignore é lista branca).
- Oferecido e sem resposta: incluir no repositório as anotações das aulas 7 e 8.
- **Depois da prévia, registrar o que a Cláudia respondeu:** (1) faixa de 300 m toda nivelada ou só a parte central (Anexo 14: ~75–105 m do eixo)? se só a central, mudar `B_FAIXA`/seção em `projeto.py` e rodar de novo otimiza_greide → memorial → landxml → civil3d_* → areas_civil3d → planilha_memorial → figuras; (2) taludes 1V:1,5H / 1V:2H; (3) Fh = 1,25 (adotado em 09/11).
- **Para 17/11:** corredor com assembly da seção-tipo no Civil 3D (o COM não cria assembly: fazer à mão ou plugin .NET; não há SDK .NET instalado) e Compute Materials; pranchas; memorial final em PDF.
- Civil 3D: o DWG está salvo; os scripts precisam do Civil 3D aberto com `Aeroporto_PPD_Civil3D.dwg` ativo.
