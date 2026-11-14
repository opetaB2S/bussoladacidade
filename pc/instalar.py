"""Run interactively as the PC owner, not as the Codex sandbox account."""
import getpass,json,os,shutil,subprocess,sys,venv
from pathlib import Path

ROOT=Path(__file__).resolve().parent
GH=ROOT/'tools/gh.exe'; PY=ROOT/'.venv/Scripts/python.exe'
TASK='BussolaDaCidade - Atualizar'; REPO='opetab2s/bussoladacidade'

def run(args,**kwargs):return subprocess.run([str(a) for a in args],check=True,**kwargs)
def psquote(value):return "'"+str(value).replace("'","''")+"'"

def main():
    user=run(['whoami'],capture_output=True,text=True).stdout.strip()
    if 'codexsandbox' in user.lower():
        raise RuntimeError('Abra INSTALAR.cmd pela sua conta normal do Windows. Não instalar na conta isolada do Codex.')
    if not Path('C:/Program Files/Git/cmd/git.exe').is_file():raise RuntimeError('Git para Windows não encontrado.')
    os.environ['PYTHONUTF8']='1'
    print('Conta Windows:',user)
    print('Preparando ambiente Python separado...')
    if not PY.exists():venv.EnvBuilder(with_pip=True).create(ROOT/'.venv')
    run([PY,'-m','pip','install','-r',ROOT/'requirements.txt'])
    print('Autenticando no GitHub. Conclua a autorização no navegador; não copie tokens para o chat.')
    if subprocess.run([GH,'auth','status'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode:
        run([GH,'auth','login','--hostname','github.com','--git-protocol','https','--web','--scopes','repo,workflow'])
    else:
        print('GitHub já autenticado. A publicação requer permissão de escrita e de workflows.')
    repo=json.loads(run([GH,'api','repos/'+REPO],capture_output=True,text=True,encoding='utf8').stdout)
    if not repo.get('permissions',{}).get('push'):raise RuntimeError('Conta sem permissão de escrita neste repositório.')
    existing=subprocess.run([GH,'api','repos/'+REPO+'/pages'],capture_output=True,text=True,encoding='utf8')
    if existing.returncode==0:
        page=json.loads(existing.stdout)
        if page.get('build_type')!='workflow':run([GH,'api','--method','PUT','repos/'+REPO+'/pages','-f','build_type=workflow'])
    else:
        if '404' not in existing.stderr:raise RuntimeError('Não foi possível consultar o GitHub Pages: '+existing.stderr)
        run([GH,'api','--method','POST','repos/'+REPO+'/pages','-f','build_type=workflow'])
    print('Criando tarefa diária às 03h37 no horário deste Windows, com sua sessão conectada...')
    command='''$ErrorActionPreference='Stop';
$action=New-ScheduledTaskAction -Execute %s -Argument %s -WorkingDirectory %s;
$trigger=New-ScheduledTaskTrigger -Daily -At '03:37';
$settings=New-ScheduledTaskSettingsSet -StartWhenAvailable -WakeToRun -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Hours 3);
$principal=New-ScheduledTaskPrincipal -UserId %s -LogonType Interactive -RunLevel Limited;
Register-ScheduledTask -TaskName %s -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description 'Coleta dados oficiais, valida e publica somente a versão aprovada. Requer usuário conectado.' -Force | Out-Null;
Get-ScheduledTask -TaskName %s | Select-Object TaskName,State | ConvertTo-Json;
Get-ScheduledTaskInfo -TaskName %s | Select-Object NextRunTime | ConvertTo-Json;
'''%(psquote(PY.with_name('pythonw.exe')),psquote('"'+str(ROOT/'rodar.py')+'"'),psquote(ROOT),psquote(user),psquote(TASK),psquote(TASK),psquote(TASK))
    run(['powershell.exe','-NoProfile','-Command',command])
    (ROOT/'instalacao.json').write_text(json.dumps({'conta_windows':user,'tarefa':TASK,'horario':'03:37','fuso':'horário local do Windows','projeto':str(ROOT)},ensure_ascii=False,indent=2),encoding='utf8')
    print('Tarefa registrada. Executando a primeira coleta e publicação agora...')
    run([PY,ROOT/'rodar.py'])
    print((ROOT/'estado.json').read_text(encoding='utf8'))
    print('Pronto. Consulte estado.json e a pasta logs para acompanhar as próximas execuções.')

if __name__=='__main__':
    try:main()
    except Exception as e:
        print('\nINSTALAÇÃO/TESTE NÃO CONCLUÍDO:',e)
        print('Nenhum sucesso de publicação deve ser presumido. Veja estado.json e logs, quando existirem.')
        status=ROOT/'estado.json'
        if status.exists():
            print('Motivo registrado:',json.loads(status.read_text(encoding='utf8')).get('erro','Veja o arquivo estado.json.'))
        sys.exit(1)
