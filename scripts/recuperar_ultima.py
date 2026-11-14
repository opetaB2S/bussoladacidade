"""Use only artifact from a fully successful workflow (including deployment)."""
import io,json,os,shutil,zipfile
import requests
from pathlib import Path

root=Path(__file__).resolve().parents[1]
repo=os.environ['GITHUB_REPOSITORY']
headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'}
def get(path):
    # requests removes Authorization when redirecting to the artifact storage host.
    r=requests.get('https://api.github.com/repos/'+repo+path,headers=headers,timeout=60)
    r.raise_for_status()
    return r.content
runs=json.loads(get('/actions/workflows/atualizar.yml/runs?status=success&per_page=1'))['workflow_runs']
if not runs:
    print('Primeira execução: comparando com a versão inicial auditada do repositório.')
else:
    run=runs[0]
    artifacts=json.loads(get('/actions/runs/'+str(run['id'])+'/artifacts'))['artifacts']
    artifact=next((a for a in artifacts if a['name']=='ultima-versao-boa' and not a['expired']),None)
    if artifact is None:
        raise RuntimeError('Última publicação sem artefato válido: revisão necessária; não usar base antiga silenciosamente')
    content=get('/actions/artifacts/'+str(artifact['id'])+'/zip')
    target=root/'dist'
    with zipfile.ZipFile(io.BytesIO(content)) as z:
        if any(not (target/n).resolve().is_relative_to(target.resolve()) for n in z.namelist()):
            raise ValueError('Caminho inválido no artefato')
        shutil.rmtree(target); target.mkdir(); z.extractall(target)
    print('Base recuperada da publicação bem-sucedida:',run['html_url'])
