"""Brasão do ITA com fundo transparente e bordas suavizadas (a partir de geo48/comum/ita_logo.png, que não é alterado).
Remove só o branco ligado à borda da imagem (o triângulo branco dentro do brasão fica), amplia 3x (Lanczos)
e desfaz a mistura com o branco nas bordas (alpha = distância ao branco)."""
import numpy as np
from PIL import Image
from scipy.ndimage import label, binary_dilation

ESCALA = 3
src = Image.open('comum/ita_logo.png').convert('RGB')
big = src.resize((src.width * ESCALA, src.height * ESCALA), Image.LANCZOS)
a = np.asarray(big).astype(float) / 255.0
bg = np.array([252, 254, 251]) / 255.0
# distância ao branco do fundo (0 = fundo, 1 = cor cheia)
d = np.clip(((bg - a) / bg).max(axis=2), 0, 1)
quase_branco = d < 0.35
lab, n = label(quase_branco)
borda = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
fundo = np.isin(lab, list(borda))
zona = binary_dilation(fundo, iterations=2)          # faixa de transição em volta do fundo
alpha = np.ones(d.shape)
alpha[zona] = np.clip(d[zona] / 0.35, 0, 1)            # rampa suave na borda
alpha[fundo & (d < 0.08)] = 0
# desfaz a mistura com o branco: c = (obs - (1 - alpha) * bg) / alpha
with np.errstate(divide='ignore', invalid='ignore'):
    cor = np.where(alpha[..., None] > 0, (a - (1 - alpha[..., None]) * bg) / alpha[..., None], 0)
cor = np.clip(cor, 0, 1)
rgba = np.dstack([cor, alpha])
out = Image.fromarray((rgba * 255 + 0.5).astype(np.uint8), 'RGBA')
bbox = out.getbbox(); out = out.crop(bbox)
out.save('figuras/ita_logo_transparente.png', optimize=True)
print('salvo', out.size, 'componentes de fundo:', len(borda))
# provas: sobre navy e sobre papel
for nome, cor_f in [('navy', (19, 48, 107)), ('papel', (248, 246, 239))]:
    f = Image.new('RGBA', (out.width + 80, out.height + 80), cor_f + (255,)); f.alpha_composite(out, (40, 40))
    f.convert('RGB').save(f'dados/logo_prova_{nome}.png')
