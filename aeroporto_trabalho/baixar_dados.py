"""Baixa os dados brutos usados na busca do sítio (≈ 230 MB, não versionados) para dados/.
Uso: python baixar_dados.py
  - Copernicus GLO-30 (DSM 1"), tiles S23W046 e S24W046 — AWS Open Data
  - ESA WorldCover 2021 v200, tile S24W048 (uso do solo, 10 m)
  - ERA5 (Open-Meteo, arquivo histórico): vento a 10 m, 2015–2024, ponto (−22,98; −45,55)
O memorial, as figuras e o LandXML rodam sem isso (usam dados/pontos_terreno.npy e os JSON versionados).
"""
import os
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(AQUI, 'dados')
os.makedirs(D, exist_ok=True)
URLS = {
    'cop_S23_00_W046_00.tif': 'https://copernicus-dem-30m.s3.amazonaws.com/Copernicus_DSM_COG_10_S23_00_W046_00_DEM/Copernicus_DSM_COG_10_S23_00_W046_00_DEM.tif',
    'cop_S24_00_W046_00.tif': 'https://copernicus-dem-30m.s3.amazonaws.com/Copernicus_DSM_COG_10_S24_00_W046_00_DEM/Copernicus_DSM_COG_10_S24_00_W046_00_DEM.tif',
    'worldcover_S24W048.tif': 'https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_S24W048_Map.tif',
    'vento_era5.json': ('https://archive-api.open-meteo.com/v1/archive?latitude=-22.98&longitude=-45.55&start_date=2015-01-01'
                        '&end_date=2024-12-31&hourly=wind_speed_10m,wind_direction_10m&wind_speed_unit=kn&timezone=America%2FSao_Paulo'),
}
for nome, url in URLS.items():
    destino = os.path.join(D, nome)
    if os.path.exists(destino):
        print('já existe:', nome); continue
    print('baixando', nome, '...')
    urllib.request.urlretrieve(url, destino)
    print('  ok', os.path.getsize(destino) // 1_000_000, 'MB')
