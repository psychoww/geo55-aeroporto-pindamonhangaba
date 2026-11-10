"""Troca os marcadores NOVO_<figura> dos slides pelas URLs /_blob/... das figuras enviadas ao deck.
Uso: python trocar_blobs.py NOVO_05_perfil=/_blob/abc NOVO_06_secoes=/_blob/def ...
Figuras: 05_perfil, 06_secoes, 07_brueckner, 11_distribuicao (em ../figuras/).
ATENÇÃO: no Git Bash, rodar com MSYS_NO_PATHCONV=1 (senão /_blob/... vira C:/Program Files/Git/_blob/...),
ou rodar pelo PowerShell."""
import glob
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
mapa = dict(a.split('=', 1) for a in sys.argv[1:])
for f in glob.glob(os.path.join(AQUI, 'project', 'slides', '*.html')):
    s = open(f, encoding='utf-8').read()
    t = s
    for k, v in mapa.items():
        assert v.startswith('/_blob/'), f'URL inválida para {k}: {v}'
        t = t.replace(f'src="{k}"', f'src="{v}"')
    if t != s:
        open(f, 'w', encoding='utf-8').write(t)
        print('trocado:', os.path.basename(f))
resto = [os.path.basename(f) for f in glob.glob(os.path.join(AQUI, 'project', 'slides', '*.html')) if 'src="NOVO_' in open(f, encoding='utf-8').read()]
print('ainda com marcador:', resto or 'nenhum')
