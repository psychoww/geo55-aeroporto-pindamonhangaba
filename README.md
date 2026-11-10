# Novo aeroporto em Pindamonhangaba — PPD 06/24

**ITA · Engenharia Civil-Aeronáutica · GEO-55 Projeto e Construção de Pistas** (Profa. Cláudia Azevedo Pereira)
Trabalho do 2º bimestre de 2026 (exame): projeto geométrico e de terraplenagem de uma pista de pouso e decolagem no Civil 3D.

**Grupo:** Pedro Feitosa Guttemberg · Guilherme Rodrigues · Gilberto Patri

## Entregas

| Arquivo | O que é |
|---|---|
| `Aeroporto_PPD_Civil3D.dwg` | Modelo no Civil 3D 2027: imagem georreferenciada, superfícies TN / TN_limpo / TERRAPLENAGEM / ACABADA, eixo "EIXO PPD 06-24", perfis (terreno e greide), 104 linhas de amostragem e vistas de seção |
| `Memorial_terraplenagem_PPD.xlsx` | Memorial de cálculo com fórmulas: premissas, greide e verificações, volumes por áreas médias (104 seções), aterro corrigido (Fh = 1,25), compensação lateral, ordenadas e diagrama de Brückner, cálculo à mão (estacas 10 → 11, modelo a preencher), conferência, distribuição (LCs, bota-fora, empréstimo, momento de transporte) e equipamentos |
| `Roteiro_aeroporto.pdf` | Roteiro da apresentação, dividido pelas etapas 1, 2 e 3 do enunciado: cada integrante apresenta uma parte de cada etapa, com as notas de fala e as perguntas prováveis daquela parte |
| `aeroporto_trabalho/explicacao/` | Página explicativa (artefato): o que foi feito em cada etapa, de onde vem cada número e como explicar (`gerar.py` monta `index.html` a partir de `modelo.html`) |
| `aeroporto_trabalho/figuras/` | Figuras da apresentação (PNG) |
| `aeroporto_trabalho/apresentacao_deck/` | Fonte dos slides (formato Slides do claude.ai) |

## Arquivos que não estão no repositório

Estes arquivos ficaram de fora porque são material da professora, anotações pessoais, outro projeto, dados grandes ou dependem de um programa. Eles fazem falta para entender (ou refazer) o trabalho:

| Arquivo | Para que serve | Onde conseguir |
|---|---|---|
| `trabalho segundo bimestre 2026.pdf` | **Enunciado do trabalho**: PPD, faixa, seção, declividades, pavimento, etapas e datas. O texto fala em 2300 m, mas vale a figura: **1900 m**, como a professora confirmou em 03/11. | Classroom de GEO-55 (arquivo da Profa. Cláudia) |
| `aula 7 - anotacoes 13-10.md` | Anotações da aula de terraplenagem. Daí vêm as regras aplicadas: limpeza de 15 cm, aterro nunca sobre a camada vegetal, espessura do pavimento considerada (volume até o subleito), Fh, formato do memorial e ordenadas de Brückner. | Com o Guilherme (anotações pessoais de aula) |
| `aula 8 - anotacoes 20-10.md` | Anotações da aula de diagrama de massas: linha de compensação, DMT, momento de transporte em m³·dam, bota-fora e empréstimo a 150 m, e a regra de fazer à mão o volume entre duas estacas. | Com o Guilherme |
| Slides das aulas 7 e 8 (terraplenagem e diagrama de massas) | Teoria de referência para o memorial e para o diagrama de massas. | Classroom de GEO-55 |
| `diagrama_massas/` (programa em MATLAB) | Programa feito para a aula 8: lê o memorial, desenha o diagrama de Brückner e otimiza as linhas de compensação (DMT e momento de transporte). `aeroporto_trabalho/distribuicao_massas.m` usa as funções dele a partir de `../diagrama_massas/`. | Com o Guilherme (projeto separado) |
| Apresentação (Slides do claude.ai) | A versão para apresentar e baixar em .pptx/PDF. Neste repositório está só a fonte, em `aeroporto_trabalho/apresentacao_deck/`. | Link do Guilherme (precisa ser compartilhado com cada um) |
| `aeroporto_trabalho/dados/*.tif`, `vento_era5.json`, `tiles_esri/` | Dados brutos da busca do sítio: modelo de terreno Copernicus, uso do solo WorldCover, vento ERA5 e cache da imagem de satélite (≈ 230 MB). | `python baixar_dados.py` (a imagem é baixada de novo por `exporta_civil3d.py`) |
| Autodesk Civil 3D 2027 | Abrir o `Aeroporto_PPD_Civil3D.dwg` e rodar os scripts `civil3d_*.ps1`. | Licença educacional da Autodesk |

Para só ler o projeto, bastam este README, o enunciado, a planilha `Memorial_terraplenagem_PPD.xlsx`, o `Roteiro_aeroporto.pdf` e as figuras. As anotações das aulas 7 e 8 explicam o porquê das regras do memorial.

## O projeto em números

- **Sítio:** terraço a oeste de Pindamonhangaba-SP, centro (−22,9300; −45,4993), SIRGAS 2000 / UTM 23S. PPD de 1900 × 45 m, rumo 060°/240° (cabeceiras 06 e 24), faixa de pista de 2020 × 300 m.
- **Escolha do sítio:** busca automática em ~25 mil centros × 36 rumos no Vale do Paraíba. Critérios: terraplenagem, fora da várzea do Paraíba, superfícies limitadoras de obstáculos do Anexo 14 (código 4) livres, entorno (cidade, água, mata) e ≥ 10 km de SBSJ e SBTA. Vento (ERA5 2015–2024): cobertura ≥ 99,9% em qualquer rumo.
- **Seção-tipo:** PPD 22,5 m para cada lado a −1,5% (pavimento 1,10 m); acostamento 7,5 m a −2,5% (0,50 m); faixa até 150 m a −2,5%; taludes 1V:1,5H (corte) e 1V:2H (aterro, adotados).
- **Greide:** 5 PIVs e 3 curvas verticais (R ≥ 30 000 m), rampas −0,432% / +0,067% / +0,395% / −0,800%, declividade efetiva 0,16%, otimizado para corte = Fh × aterro.
- **Fh = 1,25** (adotado): latossolo vermelho-amarelo poroso sobre o Grupo Taubaté; faixa usual de 1,2 a 1,3.
- **Volumes (áreas médias, seções do Civil 3D):** corte 1.227.480 m³; aterro 981.911 m³ (× 1,25 = 1.227.389 m³); saldo +91 m³; compensação lateral 534.083 m³; limpeza de 15 cm 95.095 m³. Conferência independente: −0,04% (corte) e +0,05% (aterro).
- **Distribuição (programa da aula 8, DMT externa 150 m):** adotada uma LC do P0 ao PF que compensa tudo (MT = 14,34 × 10⁶ m³·dam, ondas com DMT de 42 a 248 m). O ótimo do modelo da aula (12,32 × 10⁶) troca 144 mil m³ de bota-fora por 143 mil m³ de empréstimo; contando a escavação do empréstimo (preços do exercício 6), compensar tudo sai mais barato.

Regras da disciplina aplicadas (aula 7): limpeza de 15 cm em toda a área, aterro nunca sobre a camada vegetal, espessura do pavimento considerada (seções no greide de terraplenagem = acabado − pavimento), Fh = 1,25 (adotado para o solo do sítio) numa coluna de aterro corrigido, coluna de compensação lateral. Aula 8: o volume entre duas estacas consecutivas é feito à mão.

## Como reproduzir

Os scripts ficam em `aeroporto_trabalho/` e rodam de dentro dessa pasta. O passo a passo detalhado, as decisões e as pegadinhas do Civil 3D estão em [`aeroporto_trabalho/PROGRESSO.md`](aeroporto_trabalho/PROGRESSO.md).

```bash
cd aeroporto_trabalho
pip install -r requirements.txt
```

**Só o projeto (sem refazer a busca do sítio)** — usa `dados/pontos_terreno.npy` e os JSON versionados:

| Script | Faz |
|---|---|
| `otimiza_greide.py 5` | otimiza o greide (5 PIVs) → `dados/greide.json` |
| `memorial.py` | seções e volumes → `dados/memorial.json`, `civil3d/estacas.json`, `Tabelas/` |
| `landxml.py` | superfícies em LandXML → `civil3d/sup_*.xml` |
| `areas_civil3d.py` | áreas a partir das seções extraídas do Civil 3D (`civil3d/secoes_civil3d.csv`) |
| `planilha_memorial.py` | planilha do memorial (fórmulas) |
| `distribuicao.py` | LCs, bota-fora e momento de transporte com o programa `../diagrama_massas/` (MATLAB, `distribuicao_massas.m`) → `dados/distribuicao.json`, `figuras/11_distribuicao.png` |
| `explicacao/gerar.py` | página explicativa (rodar com `PYTHONPATH=.`) |
| `figuras.py`, `roteiro_aeroporto.py` | figuras e roteiro |

**Civil 3D 2027 (Windows, PowerShell, Civil 3D aberto com o DWG):** `civil3d_aeroporto.ps1` (superfícies, imagem, eixo, perfis), `civil3d_secoes.ps1` (linhas de amostragem e seções), `civil3d_extrai_secoes.ps1` (exporta as seções), `civil3d_vistas_secoes.ps1` (vistas de seção). Controle via COM (`AeccXUiLand.AeccApplication.13.9`).

**Busca do sítio (opcional):** `python baixar_dados.py` (≈ 230 MB), depois `busca_sitio.py`, `busca_sitio2.py`, `refina_sitio.py`, `busca_global.py`, `ols.py`.

## Fontes de dados

- Relevo: Copernicus GLO-30 DEM (DSM, 1″), © DLR / Airbus, distribuído pela ESA (AWS Open Data).
- Uso do solo: ESA WorldCover 2021 v200 (CC BY 4.0).
- Vento: reanálise ERA5 (Copernicus Climate Change Service) via API do Open-Meteo.
- Imagem de satélite: Esri World Imagery (uso acadêmico).
- Brasão e cores: identidade visual do ITA.

## Pendências (entrega de 17/11)

- Corredor com a assembly da seção-tipo e tabela de volumes do Civil 3D (Compute Materials).
- Pranchas (planta, perfil, seções) e memorial final.
- Confirmar com a professora: nivelamento da faixa inteira (300 m) ou só da parte central; taludes; Fh = 1,25.
