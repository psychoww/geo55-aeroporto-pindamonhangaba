"""Imagem de satélite (Esri World Imagery) reamostrada para UTM 23S, com arquivo de georreferência (world file)."""
import io
import math
import os
import urllib.request
import numpy as np
from PIL import Image
from dem import utm2geo, DADOS

URL = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
CACHE = os.path.join(DADOS, 'tiles_esri')
os.makedirs(CACHE, exist_ok=True)


def _tile(z, x, y):
    p = os.path.join(CACHE, f'{z}_{x}_{y}.jpg')
    if not os.path.exists(p):
        req = urllib.request.Request(URL.format(z=z, x=x, y=y), headers={'User-Agent': 'geo55-trabalho/1.0'})
        with urllib.request.urlopen(req, timeout=30) as r:
            open(p, 'wb').write(r.read())
    return np.asarray(Image.open(p).convert('RGB'))


def imagem_utm(x0, y0, x1, y1, res=2.0, z=17):
    """Raster RGB em UTM (linhas de cima para baixo) cobrindo [x0,x1]x[y0,y1] com pixel 'res' m."""
    xs = np.arange(x0 + res / 2, x1, res)
    ys = np.arange(y1 - res / 2, y0, -res)
    XX, YY = np.meshgrid(xs, ys)
    lon, lat = utm2geo.transform(XX, YY)
    n = 2 ** z
    px = (lon + 180) / 360 * n * 256
    lr = np.radians(lat)
    py = (1 - np.log(np.tan(lr) + 1 / np.cos(lr)) / math.pi) / 2 * n * 256
    tx, ty = (px // 256).astype(int), (py // 256).astype(int)
    out = np.zeros(XX.shape + (3,), np.uint8)
    for a, b in set(zip(tx.ravel().tolist(), ty.ravel().tolist())):
        m = (tx == a) & (ty == b)
        t = _tile(z, a, b)
        out[m] = t[(py[m] % 256).astype(int), (px[m] % 256).astype(int)]
    return out


def salva_georref(arr, path_jpg, x0, y1, res):
    """Salva JPG + world file (.jgw) em UTM: canto superior esquerdo = (x0, y1)."""
    Image.fromarray(arr).save(path_jpg, quality=90)
    with open(os.path.splitext(path_jpg)[0] + '.jgw', 'w') as f:
        f.write(f'{res}\n0\n0\n{-res}\n{x0 + res / 2}\n{y1 - res / 2}\n')
