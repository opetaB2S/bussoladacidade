"""Gera a mesma pagina PHP como HTML para hospedagem estatica."""
import json,re,shutil
from pathlib import Path
p=Path(__file__).resolve().parents[1]
data=json.loads((p/'dist/dados.json').read_text(encoding='utf-8'))
src=(p/'index.php').read_text(encoding='utf-8')
blocks=list(re.finditer(r'<\?php.*?\?>',src,re.S))
assert len(blocks)==2
payload=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
src=src[:blocks[1].start()]+payload+src[blocks[1].end():]
src=re.sub(r'<\?php.*?\?>','',src,flags=re.S).lstrip()
(p/'dist/index.html').write_text(src,encoding='utf-8')
# Arquivos de producao PHP: podem ser servidos na raiz sem expor dados brutos de coleta.
for name in ['style.css','app.js','local.js','dados.json','bussola.css','bussola.js','fonts.css','grupos-indice.json','bussola-resumo.json']:
    shutil.copyfile(p/'dist'/name,p/name)
shutil.copytree(p/'dist/fotos',p/'fotos',dirs_exist_ok=True)
if (p/'dist/propostas').exists():
    shutil.copytree(p/'dist/propostas',p/'propostas',dirs_exist_ok=True)
if (p/'dist/busca').exists():
    shutil.copytree(p/'dist/busca',p/'busca',dirs_exist_ok=True)
shutil.copytree(p/'dist/assets',p/'assets',dirs_exist_ok=True)
print('Previa Bussola e arquivos PHP preparados.')
