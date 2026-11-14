"""Coleta limitada e rastreavel. pip install requests beautifulsoup4
python scripts/coletar.py [--diagnostico-sem-validar-tls]
"""
import argparse, base64, concurrent.futures, hashlib, json, re, time, unicodedata
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
SESSION=requests.Session()
SESSION.headers['User-Agent']='BussolaDaCidade/1.0 (+https://github.com/opetab2s/bussoladacidade)'
SESSION.mount('https://',HTTPAdapter(max_retries=Retry(total=3,backoff_factor=2,status_forcelist=[429,500,502,503,504],allowed_methods=['GET','POST'])))

ap=argparse.ArgumentParser();ap.add_argument('--diagnostico-sem-validar-tls',action='store_true');args=ap.parse_args()
ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/'data'/'originais';RAW.mkdir(parents=True,exist_ok=True)
DIST=ROOT/'dist';(DIST/'fotos').mkdir(parents=True,exist_ok=True)
TODAY=datetime.now().astimezone(); YEAR=TODAY.year; MONTH=TODAY.month
BASE='https://aplicnt.camara.rj.gov.br'; SITE='https://www.camara.rio'; log=[]
if args.diagnostico_sem_validar_tls:
    import urllib3;urllib3.disable_warnings()
def get(key,url,data=None):
    path=RAW/(key+'.html')
    if path.exists(): b=path.read_bytes();cached=True
    else:
        r=SESSION.request('POST' if data else 'GET',url,data=data,timeout=55,verify=not args.diagnostico_sem_validar_tls);r.raise_for_status();b=r.content;path.write_bytes(b);cached=False
    log.append({'arquivo':path.name,'url':url,'metodo':'POST' if data else 'GET','parametros':data,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'cache_reutilizado':cached,'tls_validado':not args.diagnostico_sem_validar_tls})
    return BeautifulSoup(b,'html.parser')
def norm(s):return re.sub(r'[^a-z0-9]+',' ',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()).strip()
rosterurl=SITE+'/includes_php/vereadores_atuais.php?imprimir=N'
s=get('cadastro',rosterurl);people=[]
for tr in s.select('tbody tr'):
    c=tr.find_all('td',recursive=False)
    if len(c)!=6:continue
    a=c[1].find('a');pid=re.search(r'cvd=(\d+)',a['href']).group(1);name=a.get_text(' ',strip=True)
    img=c[0].find('img')['src'];image_bytes=base64.b64decode(img.split(',',1)[1])
    photo='fotos/'+pid+('.png' if image_bytes.startswith(b'\x89PNG') else '.jpg')
    (DIST/photo).write_bytes(image_bytes)
    party=c[2].find('img').get('alt','').strip()
    if '\u00c3' in party:
        try:party=party.encode('latin1').decode('utf-8')
        except (UnicodeError,ValueError):pass
    people.append({'id':pid,'nome':name,'partido':party,'foto':photo,'fonte':urljoin(SITE+'/includes_php/',a['href']),'email':c[5].get_text(' ',strip=True),'telefone':c[4].get_text(' ',strip=True),'sala':c[3].get_text(' ',strip=True)})
assert len(people)==51,len(people)
print('Cadastro:',len(people),flush=True)
lookup={norm(p['nome']):p['id'] for p in people}
def identify(name):return lookup.get(norm(name))

# Tabelas mensais: faltas e abonos, sem inferir presenca diaria.
months=['Janeiro','Fevereiro','Mar\u00e7o','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'][:MONTH]
presence=[];purl=SITE+'/atividade-parlamentar/plenario/frequencia-dos-vereadores'
for month,label in enumerate(months,1):
    s=get('faltas_%s_%02d'%(YEAR,month),purl,{'ano':str(YEAR),'mes':str(month)+'|'+label,'sessao':'1','submit':' Consultar '})
    body=s.select_one('.item-page') or s;t=body.get_text(' ',strip=True)
    stamp=re.search(r'(?:vez em)\s*(\d{2}/\d{2}/\d{4})',t)
    note=t[t.find('OBSERVA\u00c7\u00c3O:'):] if 'OBSERVA\u00c7\u00c3O:' in t else ''
    records=[]
    for tr in body.select('table tr'):
        cells=[x.get_text(' ',strip=True) for x in tr.find_all('td',recursive=False)]
        if len(cells)==4 and all(re.fullmatch(r'\d+',v) for v in cells[1:]):
            name=cells[0].replace('*','').strip();records.append({'nome_fonte':cells[0],'pessoa':identify(name),'faltas':int(cells[1]),'abonadas':int(cells[2]),'total':int(cells[3])})
    presence.append({'mes':month,'rotulo':label+' de '+str(YEAR),'atualizado_fonte':stamp.group(1) if stamp else None,'registros':records,'observacoes':note,'fonte':SITE+'/includes_php/vereadores_frequencia_excel.php?ano='+str(YEAR)+'&mes='+str(month)})
    print('Faltas',label,len(records),flush=True)

# Projetos de lei de 2025 e 2026: percorre ate esgotar a consulta.
projects=[];seen=set();pages=[]
for start in range(1,6001,1000):
    url=BASE+'/APL/Legislativos/scpro.nsf/Internet/LeiInt?OpenForm&Start='+str(start)+'&Count=1000'
    s=get('projetos_'+str(start),url);n=0
    for a in s.select('a[href]'):
        num=a.get_text(strip=True)
        if not re.fullmatch(r'\d+(?:-A)?/\d{4}',num) or 'OpenDocument' not in a['href']:continue
        source=urljoin(BASE,a['href'])
        if source in seen:continue
        seen.add(source);n+=1
        c=[td.get_text(' ',strip=True) for td in a.find_parent('tr').find_all('td',recursive=False)]
        if len(c)!=6:raise ValueError('Estrutura de projeto mudou')
        authornorm=' '+norm(c[5])+' '
        ids=[p['id'] for p in people if ' '+norm(p['nome'])+' ' in authornorm]
        if 2025<=int(num.split('/')[-1])<=YEAR:
            projects.append({'numero':num,'tipo':'Projeto de lei','ementa':c[3].split('=>')[0].strip(),'publicacao_fonte':c[4],'autores_fonte':c[5],'pessoas':ids,'fonte':source})
    pages.append(url);print('Projetos pagina',start,n,flush=True)
    if n<1000 or any(re.fullmatch(r'\d+(?:-A)?/2024',a.get_text(strip=True)) for a in s.select('a[href]')):break
else:raise ValueError('Limite atingido: nao publicar contagem como completa')
assert len(projects)>2000

# Registros de discursos/deliberacoes do mes de novembro de 2026.
vurl=BASE+'/APL/Legislativos/discvot.nsf/anoint?OpenForm&Count=1000'
s=get('votacoes_indice',vurl);month=None;day=None;documents={};found_end=False
for tr in s.select('tr'):
    text=tr.get_text(' ',strip=True)
    if text in months:
        month=text
        if month!=months[-1] and documents:found_end=True;break
    if re.fullmatch(r'\d{1,2}/\d{2}',text):day=text
    if month!=months[-1]:continue
    for a in tr.select('a[href]'):
        if 'OpenDocument' not in a['href']:continue
        # Todos os documentos: requerimentos e verificacoes tambem podem ter votos.
        u=urljoin(BASE,a['href']);documents[u]={'indice':text,'dia':day}
assert found_end,'Indice sem limite do mÃªs: coleta nÃ£o comprovada'
print('Documentos de novembro:',len(documents),flush=True)
def load_doc(pair):
    url,meta=pair;key='voto_'+hashlib.sha256(url.encode()).hexdigest()[:20]
    s=get(key,url);text=s.get_text(' ',strip=True)
    title=re.search(r'Projeto De (?:Lei Complementar|Lei|Decreto Legislativo|Resolu\u00e7\u00e3o)\s+[\dA-Za-z/-]+',text,re.I)
    day,month=meta['dia'].split('/')
    date=str(YEAR)+'-'+month+'-'+day.zfill(2)
    actual=re.search(r'Data da Sess\u00e3o:\s*(\d{2})/(\d{2})/(\d{4})',text)
    if actual:
        assert date==actual.group(3)+'-'+actual.group(1)+'-'+actual.group(2),url
    return {'titulo':title.group(0) if title else meta['indice'].split('....')[0].strip(),'fonte':url,'data':date,'texto':text}
docs=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
    for i,d in enumerate(ex.map(load_doc,documents.items()),1):
        docs.append(d)
        if i%30==0:print('Documentos baixados',i,flush=True)
votes=[];unparsed=[]
for d in docs:
    text=d['texto'];events=[]
    # Delimitacao por cada bloco de apuracao evita misturar votacoes da mesma pagina.
    blocks=re.findall(r'\(Conclu\u00edda a vota\u00e7\u00e3o nominal,(.*?)(?=\)\s*(?:O SR\.|A SRA\.)|$)',text,re.S|re.I)
    for ix,block in enumerate(blocks):
        ballots=[];valid=True
        for m in re.finditer(r'votaram\s+(SIM|N\u00c3O)\s+os\s+(?:Senhores?\s+)?Vereadores?\s+(.*?)\s+(\d+)\s*\(',block,re.I|re.S):
            names=re.split(r',\s*| e ',m.group(2));expected=int(m.group(3))
            if len(names)!=expected:
                unparsed.append({'fonte':d['fonte'],'motivo':'contagem de nomes nao confere','declarado':expected,'nomes_listados':len(names)})
                valid=False;continue
            for name in names:ballots.append({'nome_fonte':name.strip(),'pessoa':identify(name),'voto':'Sim' if m.group(1).upper()=='SIM' else 'N\u00e3o'})
        announcement=re.search(r'ANUNCIA-SE:\s*(.*?)(?:\(INTERROMPENDO|Em discuss\u00e3o\.)',text,re.S|re.I)
        context=announcement.group(1).strip() if announcement else ''
        heading=d['titulo']
        if 'VETO TOTAL' in context:heading='Veto total ao '+heading
        elif 'VETO PARCIAL' in context:heading='Veto parcial ao '+heading
        if ballots and valid:events.append({'id':hashlib.sha256((d['fonte']+str(ix)).encode()).hexdigest()[:16],'titulo':heading,'data':d['data'],'fonte':d['fonte'],'votos':ballots,'trecho':block.strip(),'contexto_fonte':context})
    votes+=events
    if 'vota\u00e7\u00e3o nominal' in text.lower() and not events:unparsed.append({'fonte':d['fonte'],'motivo':'registro nominal nao extraido'})
print('Votacoes nominais extraidas',len(votes),'pendencias',len(unparsed),flush=True)
unparsed=list({x['fonte']:x for x in reversed(unparsed)}.values())
data={'coletado_em':datetime.now(timezone.utc).isoformat(),'cadastro_fonte':rosterurl,'pessoas':people,'frequencia':presence,'projetos':projects,'projetos_paginas':pages,'votacoes':votes,'votacoes_pendencias':unparsed,'documentos_votacoes':len(docs),'periodo_votos':months[-1]+' de '+str(YEAR)+' (atÃ© a coleta)','tls_validado':not args.diagnostico_sem_validar_tls}
(DIST/'dados.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
(ROOT/'data'/'manifesto.json').write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'data'/'documentos_votacoes.json').write_text(json.dumps(docs,ensure_ascii=False),encoding='utf-8')
print('Pronto:',len(people),'pessoas',len(projects),'projetos',len(votes),'votacoes',flush=True)
