"""Leitura do MDE Copernicus GLO-30 e do WorldCover, e conversão para UTM 23S (SIRGAS 2000, EPSG:31983)."""
import os
import numpy as np
import tifffile
from pyproj import Transformer

AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(AQUI, 'dados')
EPSG_UTM = 31983
geo2utm = Transformer.from_crs(4326, EPSG_UTM, always_xy=True)
utm2geo = Transformer.from_crs(EPSG_UTM, 4326, always_xy=True)


def _georef(path):
    with tifffile.TiffFile(path) as tf:
        p = tf.pages[0]
        tie = p.tags['ModelTiepointTag'].value
        scale = p.tags['ModelPixelScaleTag'].value
    lon0, lat0 = tie[3], tie[4]
    return lon0, lat0, scale[0], scale[1]


class Raster:
    """Raster geográfico (lon/lat) com consulta bilinear ou vizinho mais próximo."""

    def __init__(self, arr, lon0, lat0, dlon, dlat, pixel_is_area=True):
        self.a = arr
        self.lon0, self.lat0, self.dlon, self.dlat = lon0, lat0, dlon, dlat
        self.off = 0.5 if pixel_is_area else 0.0

    def ij(self, lon, lat):
        j = (np.asarray(lon) - self.lon0) / self.dlon - self.off
        i = (self.lat0 - np.asarray(lat)) / self.dlat - self.off
        return i, j

    def bilinear(self, lon, lat):
        i, j = self.ij(lon, lat)
        i0 = np.clip(np.floor(i).astype(int), 0, self.a.shape[0] - 2)
        j0 = np.clip(np.floor(j).astype(int), 0, self.a.shape[1] - 2)
        fi, fj = i - i0, j - j0
        a = self.a
        return ((1 - fi) * (1 - fj) * a[i0, j0] + (1 - fi) * fj * a[i0, j0 + 1]
                + fi * (1 - fj) * a[i0 + 1, j0] + fi * fj * a[i0 + 1, j0 + 1])

    def nearest(self, lon, lat):
        i, j = self.ij(lon, lat)
        i = np.clip(np.round(i).astype(int), 0, self.a.shape[0] - 1)
        j = np.clip(np.round(j).astype(int), 0, self.a.shape[1] - 1)
        return self.a[i, j]


def carrega_dem():
    """Junta os tiles S23 e S24 (W046) num raster só. Copernicus: PixelIsPoint (tiepoint no centro do pixel)."""
    tiles = ['cop_S23_00_W046_00.tif', 'cop_S24_00_W046_00.tif']
    arrs, refs = [], []
    for t in tiles:
        arrs.append(tifffile.imread(os.path.join(DADOS, t)).astype(np.float64))
        refs.append(_georef(os.path.join(DADOS, t)))
    lon0, lat0, dlon, dlat = refs[0]
    a = np.vstack(arrs)  # S23 em cima (lat -22..-23), S24 embaixo (-23..-24)
    return Raster(a, lon0, lat0, dlon, dlat, pixel_is_area=False)


_WC = None


def carrega_worldcover(lon_min, lon_max, lat_min, lat_max):
    """Recorte do WorldCover (uint8) na janela pedida. Lê o arquivo inteiro uma vez (memória ~1,3 GB)."""
    global _WC
    path = os.path.join(DADOS, 'worldcover_S24W048.tif')
    lon0, lat0, dlon, dlat = _georef(path)
    if _WC is None:
        _WC = tifffile.imread(path)
    j0 = int((lon_min - lon0) / dlon); j1 = int((lon_max - lon0) / dlon) + 1
    i0 = int((lat0 - lat_max) / dlat); i1 = int((lat0 - lat_min) / dlat) + 1
    sub = _WC[i0:i1, j0:j1]
    return Raster(sub, lon0 + j0 * dlon, lat0 - i0 * dlat, dlon, dlat, pixel_is_area=True)


def cota_utm(dem, x, y):
    lon, lat = utm2geo.transform(x, y)
    return dem.bilinear(lon, lat)
