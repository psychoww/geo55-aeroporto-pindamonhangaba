# Novo aeroporto em Pindamonhangaba — PPD 06/24

**ITA · Engenharia Civil-Aeronáutica · GEO-55 Projeto e Construção de Pistas** (Profa. Cláudia Azevedo Pereira)
Trabalho do 2º bimestre de 2026 (exame): projeto geométrico e de terraplenagem de uma pista de pouso e decolagem no Civil 3D.

**Grupo:** Pedro Feitosa Guttemberg · Guilherme Rodrigues · Gilberto Patri

## Entregas

| Arquivo | O que é |
|---|---|
| `Aeroporto_PPD_Civil3D.dwg` | Modelo no Civil 3D 2027: imagem georreferenciada, superfícies TN / TN_limpo / TERRAPLENAGEM / ACABADA, eixo "EIXO PPD 06-24", perfis (terreno e greide), 106 linhas de amostragem e vistas de seção |
| `Memorial_terraplenagem_PPD.xlsx` | Memorial de cálculo com fórmulas: premissas, greide e verificações, volumes por áreas médias (106 seções), aterro corrigido (Fh), ordenadas e diagrama de Brückner, cálculo à mão (estacas 29 → 30) e conferência |
| `Roteiro_aeroporto.pdf` | Roteiro da apresentação: divisão dos slides, notas de fala e perguntas prováveis |
| `aeroporto_trabalho/figuras/` | Figuras da apresentação (PNG) |
| `aeroporto_trabalho/apresentacao_deck/` | Fonte dos slides (formato Slides do claude.ai) |

## O projeto em números

- **Sítio:** terraço a oeste de Pindamonhangaba-SP, centro (−22,9300; −45,4993), SIRGAS 2000 / UTM 23S. PPD de 1900 × 45 m, rumo 060°/240° (cabeceiras 06 e 24), faixa de pista de 2020 × 300 m.
- **Escolha do sítio:** busca automática em ~25 mil centros × 36 rumos no Vale do Paraíba. Critérios: terraplenagem, fora da várzea do Paraíba, superfícies limitadoras de obstáculos do Anexo 14 (código 4) livres, entorno (cidade, água, mata) e ≥ 10 km de SBSJ e SBTA. Vento (ERA5 2015–2024): cobertura ≥ 99,9% em qualquer rumo.
- **Seção-tipo:** PPD 22,5 m para cada lado a −1,5% (pavimento 1,10 m); acostamento 7,5 m a −2,5% (0,50 m); faixa até 150 m a −2,5%; taludes 1V:1,5H (corte) e 1V:2H (aterro, adotados).
- **Greide:** 5 PIVs e 3 curvas verticais (R ≥ 30 000 m), rampa máx. 0,80%, declividade efetiva 0,16%, otimizado para corte = Fh × aterro.
- **Volumes (áreas médias, seções do Civil 3D):** corte 1.151.744 m³; aterro 1.046.648 m³ (× 1,1 = 1.151.313 m³); saldo +431 m³; limpeza de 15 cm 95.023 m³. Conferência independente: 0,06% de diferença.

Regras da disciplina aplicadas (aula 7): limpeza de 15 cm em toda a área, aterro nunca sobre a camada vegetal, pavimento desconsiderado (seções no greide de terraplenagem), Fh = 1,1 numa coluna de aterro corrigido. Aula 8: o volume entre duas estacas consecutivas é feito à mão.

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

- Linhas de compensação, DMT e momento de transporte.
- Corredor com a assembly da seção-tipo e tabela de volumes do Civil 3D (Compute Materials).
- Pranchas (planta, perfil, seções) e memorial final.
- Confirmar com a professora: nivelamento da faixa inteira (300 m) ou só da parte central; taludes; Fh.
