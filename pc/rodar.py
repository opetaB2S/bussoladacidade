"""Scheduled entry point. No publication happens before collection approval."""
import contextlib,datetime as dt,hashlib,json,msvcrt,os,shutil,subprocess,sys,time
from pathlib import Path

ROOT=Path(__file__).resolve().parent
REPO='opetab2s/bussoladacidade'; BRANCH='site-publicado'
GH=ROOT/'tools/gh.exe'; PY=ROOT/'.venv/Scripts/python.exe'
LOG=ROOT/'logs'; LOG.mkdir(exist_ok=True)
STATUS=ROOT/'estado.json'
GIT=Path('C:/Program Files/Git/cmd/git.exe')

def run(args,**kw):
    if not kw.get('capture_output'):
        kw.setdefault('stdout',sys.stdout);kw.setdefault('stderr',sys.stderr)
    kw.setdefault('creationflags',subprocess.CREATE_NO_WINDOW)
    return subprocess.run([str(a) for a in args],check=True,**kw)

def api(path,*args):
    return run([GH,'api',path,*args],capture_output=True,text=True,encoding='utf8').stdout

def git(*args,cwd=None,capture=False):
    return run([GIT,'-c','http.sslBackend=openssl','-c','credential.helper=','-c','credential.helper=!gh auth git-credential',*args],cwd=cwd,capture_output=capture,text=True,encoding='utf8')

def write_status(data):
    temp=STATUS.with_suffix('.tmp');temp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8');os.replace(temp,STATUS)

def main():
    state={'inicio':dt.datetime.now(dt.timezone.utc).isoformat(),'resultado':'em andamento','publicado':False}
    try:
        os.environ['PATH']=str(GH.parent)+';C:/Program Files/Git/usr/bin;'+os.environ['PATH']
        os.environ['PYTHONUTF8']='1'
        run([GH,'auth','status'])
        run([PY,ROOT/'scripts/preparar_tls.py'])
        os.environ['REQUESTS_CA_BUNDLE']=str(ROOT/'data/ca-completa.pem')
        run([PY,ROOT/'scripts/test_travas.py'])
        run([PY,ROOT/'scripts/atualizar.py'])
        report=json.loads((ROOT/'reports/execucao.json').read_text(encoding='utf8'))
        if not report.get('publicavel') or not report.get('base_preservada'):raise ValueError('Coleta não aprovada')
        candidate=ROOT/'.candidate/dist'
        (candidate/'ultima-atualizacao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
        manifest={p.relative_to(candidate).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in candidate.rglob('*') if p.is_file() and p.name!='pacote-sha256.json'}
        (candidate/'pacote-sha256.json').write_text(json.dumps(manifest,sort_keys=True,indent=2),encoding='utf8')
        run([PY,ROOT/'verificar_pacote.py',candidate])
        # A separate checkout keeps code and partially collected data out of deployment.
        checkout=ROOT/'publicacao';checkout.mkdir(exist_ok=True)
        if not (checkout/'.git').exists():
            git('init',str(checkout));git('remote','add','origin','https://github.com/'+REPO+'.git',cwd=checkout)
        git('config','credential.helper','!gh auth git-credential',cwd=checkout)
        git('config','user.name','Bussola da Cidade',cwd=checkout)
        git('config','user.email','134148792+opetaB2S@users.noreply.github.com',cwd=checkout)
        remote=git('ls-remote','--heads','origin',BRANCH,cwd=checkout,capture=True).stdout.strip()
        if remote:
            git('fetch','origin',BRANCH,cwd=checkout)
            git('checkout','-B',BRANCH,'FETCH_HEAD',cwd=checkout)
        else:
            local=git('branch','--list',BRANCH,cwd=checkout,capture=True).stdout.strip()
            if local:git('checkout',BRANCH,cwd=checkout)
            else:git('checkout','--orphan',BRANCH,cwd=checkout)
        dest=checkout/'dist'
        if dest.exists():
            if dest.resolve().parent!=checkout.resolve():raise ValueError('Destino fora do checkout')
            shutil.rmtree(dest)
        shutil.copytree(candidate,dest)
        workflows=checkout/'.github/workflows';workflows.mkdir(parents=True,exist_ok=True)
        shutil.copy2(ROOT/'publicar.yml',workflows/'atualizar.yml')
        shutil.copy2(ROOT/'verificar_pacote.py',checkout/'verificar_pacote.py')
        git('add','dist','.github','verificar_pacote.py',cwd=checkout)
        git('commit','-m','Publica coleta conferida de '+dt.datetime.now().strftime('%Y-%m-%d %H:%M'),cwd=checkout)
        sha=git('rev-parse','HEAD',cwd=checkout,capture=True).stdout.strip()
        git('push','origin','HEAD:refs/heads/'+BRANCH,cwd=checkout)
        state['commit']=sha;write_status(state)
        api('repos/'+REPO+'/actions/workflows/atualizar.yml/dispatches','--method','POST','-f','ref=main','-f','inputs[source_sha]='+sha)
        # The workflow runs on protected main, checking out this exact package commit.
        deadline=time.monotonic()+1800;url=None
        while time.monotonic()<deadline:
            rows=json.loads(api('repos/'+REPO+'/actions/workflows/atualizar.yml/runs?event=workflow_dispatch&branch=main&per_page=20'))['workflow_runs']
            matching=[r for r in rows if r['path']=='.github/workflows/atualizar.yml' and r['head_branch']=='main' and r['display_title']=='Publicar coleta '+sha]
            if matching:
                job=matching[0];state['execucao_github']=job['html_url'];write_status(state)
                if job['status']=='completed':
                    if job['conclusion']!='success':raise RuntimeError('GitHub não publicou: '+job['html_url'])
                    url=json.loads(api('repos/'+REPO+'/pages'))['html_url'];break
            time.sleep(15)
        if not url:raise TimeoutError('Publicação não confirmada dentro de 30 minutos; base local preservada')
        backup=ROOT/'ultima-base-anterior'
        if backup.exists():
            if backup.resolve().parent!=ROOT.resolve():raise ValueError('Backup fora do projeto')
            shutil.rmtree(backup)
        shutil.copytree(ROOT/'dist',backup)
        shutil.copytree(candidate,ROOT/'dist',dirs_exist_ok=True)
        # Drop files absent from candidate, after successful deployment only.
        for path in (ROOT/'dist').rglob('*'):
            if path.is_file() and not (candidate/path.relative_to(ROOT/'dist')).is_file():path.unlink()
        state.update({'resultado':'publicado','publicado':True,'url':url,'documentos':report['documentos'],'dados_sha256':report['dados_sha256']})
        print('SITE PUBLICADO:',url)
    except Exception as e:
        state.update({'resultado':'bloqueado','erro':str(e)})
        raise
    finally:
        state['fim']=dt.datetime.now(dt.timezone.utc).isoformat();write_status(state)

if __name__=='__main__':
    with (ROOT/'execucao.lock').open('a+b') as lock:
        lock.seek(0);lock.write(b'0');lock.flush();lock.seek(0)
        try:msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
        except OSError:sys.exit('Já existe uma execução em andamento.')
        with (LOG/(dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+'.log')).open('w',encoding='utf8',buffering=1) as log:
            with contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
                try:main()
                except Exception:
                    import traceback;traceback.print_exc();sys.exit(1)
