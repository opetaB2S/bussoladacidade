"""Checks the exact files approved on the PC before deploying on Pages."""
import hashlib,json,sys
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urlparse

def verify(folder):
    folder=Path(folder).resolve()
    manifest=json.loads((folder/'pacote-sha256.json').read_text(encoding='utf8'))
    files={p.relative_to(folder).as_posix():p for p in folder.rglob('*') if p.is_file() and p.name!='pacote-sha256.json'}
    if set(files)!=set(manifest):raise ValueError('Pacote com arquivos ausentes ou adicionais')
    for name,path in files.items():
        if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest()!=manifest[name]:
            raise ValueError('Arquivo diferente do aprovado: '+name)
    report=json.loads((folder/'ultima-atualizacao.json').read_text(encoding='utf8'))
    if report.get('publicavel') is not True or report.get('base_preservada') is not True:
        raise ValueError('Coleta não aprovada')
    datafile=folder/'dados.json'
    if hashlib.sha256(datafile.read_bytes()).hexdigest()!=report['dados_sha256']:raise ValueError('Dados divergem do relatório')
    d=json.loads(datafile.read_text(encoding='utf8'))
    if not d['tls_validado'] or len(d['pessoas'])!=51:raise ValueError('TLS/cadastro inválido')
    age=(datetime.now(timezone.utc)-datetime.fromisoformat(d['coletado_em'])).total_seconds()
    if not -300<=age<=36*3600:raise ValueError('Coleta antiga ou com data futura')
    for p in d['pessoas']:
        if urlparse(p['fonte']).hostname!='www.camara.rio' or not (folder/p['foto']).is_file():raise ValueError('Perfil/foto inválido')
    print('Pacote aprovado e íntegro:',report['documentos'],'documentos')

if __name__=='__main__':verify(sys.argv[1])
