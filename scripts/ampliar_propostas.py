"""Coleta os indices oficiais de 2025/2026 e aplica a mesma regra a todos.
Use --diagnostico-sem-validar-tls apenas para diagnostico da cadeia local.
"""
import argparse,collections,concurrent.futures,hashlib,json,re,shutil
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
SESSION=requests.Session()
SESSION.headers['User-Agent']='BussolaDaCidade/1.0 (+https://github.com/opetab2s/bussoladacidade)'
SESSION.mount('https://',HTTPAdapter(max_retries=Retry(total=3,backoff_factor=2,status_forcelist=[429,500,502,503,504],allowed_methods=['GET','POST'])))
from classificar import classify,normalize,VERSION,GROUPS
ap=argparse.ArgumentParser();ap.add_argument('--diagnostico-sem-validar-tls',action='store_true');opt=ap.parse_args()
ROOT=Path(__file__).resolve().parents[1];RAW=ROOT/'data'/'propostas_originais';RAW.mkdir(parents=True,exist_ok=True)
YEAR=datetime.now().year
BASE='https://aplicnt.camara.rj.gov.br';manifest=[]
data=json.loads((ROOT/'dist/dados.json').read_text(encoding='utf-8'))
people=data['pessoas']
if opt.diagnostico_sem_validar_tls:
 import urllib3;urllib3.disable_warnings()
TYPES=[('LeiInt','Projeto de lei'),('LeiCompInt','Projeto de lei complementar'),('EmendaInt','Proposta de emenda à Lei Orgânica'),('DecretoInt','Projeto de decreto legislativo'),('ResolucaoInt','Projeto de resolução'),('IndInt','Indicação'),('mocaoInt','Moção'),('ReqInfInt','Requerimento de informação'),('ReqInt','Requerimento'),('OficioInt','Ofício')]
def fetch(key,url):
 p=RAW/(key+'.html')
 if p.exists():b=p.read_bytes();cached=True
 else:
  for attempt in range(3):
   try:
    r=SESSION.get(url,verify=not opt.diagnostico_sem_validar_tls,timeout=60);r.raise_for_status();b=r.content;p.write_bytes(b);break
   except requests.RequestException:
    if attempt==2:raise
  cached=False
 manifest.append({'arquivo':p.name,'url':url,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'cache_reutilizado':cached,'tls_validado':not opt.diagnostico_sem_validar_tls})
 return BeautifulSoup(b,'html.parser')
def collect(pair):
 key,tipo=pair[:2]
 category=pair[2] if len(pair)>2 else None
 if key=='OficioInt' and category is None:
  parts=[collect((key,tipo,c)) for c in range(1,10)]
  unique={r['id']:r for part in parts for r in part['registros']}
  return {'tipo':tipo,'registros':list(unique.values()),'paginas':[u for part in parts for u in part['paginas']],'completa_no_periodo':True}
 rows=[];seen=set();pages=[];allseen=set();end=False
 for start in range(1,180001,1000):
  position=str(category)+'.'+str(start) if category else str(start)
  u=BASE+'/APL/Legislativos/scpro.nsf/Internet/'+key+'?OpenForm&Start='+position+'&Count=1000'+('&Expand='+str(category) if category else '')
  soup=fetch(key+'_'+position,u);pages.append(u);current=[];older=False;new=0;years=[]
  for a in soup.select('a[href]'):
   number=a.get_text(' ',strip=True)
   if 'OpenDocument' not in a['href'] or not re.fullmatch(r'\d+(?:-[A-Z])?/\d{4}',number):continue
   source=urljoin(BASE,a['href']);unid=source.split('?')[0].split('/')[-1]
   if unid in allseen:continue
   allseen.add(unid);new+=1
   year=int(number.split('/')[-1])
   cells=[td.get_text(' ',strip=True) for td in a.find_parent('tr').find_all('td',recursive=False)]
   # Tipo PLC tem coluna vazia extra; oficios tem coluna vazia no fim.
   idx=cells.index(number);payload=[v for v in cells[idx+1:] if v.strip()]
   if not payload:raise ValueError((tipo,number,'sem ementa'))
   ementa=payload[0].split('=>')[0].strip()
   date=next((v for v in payload[1:] if re.match(r'^\d{2}/\d{2}/\d{4}',v)),None)
   if year<1900 and date:year=int(date[6:10])
   years.append(year)
   if not 2025<=year<=YEAR:continue
   authors=payload[-1] if len(payload)>1 and payload[-1]!=date else ''
   if not authors:raise ValueError((tipo,number,'sem autor'))
   authorsnorm=' '+normalize(authors)+' '
   ids=[p['id'] for p in people if ' '+normalize(p['nome'])+' ' in authorsnorm]
   group,reason=classify(tipo,ementa)
   rows.append({'id':key+'-'+unid,'numero':number,'ano_referencia':year,'tipo':tipo,'ementa':ementa,'autores_fonte':authors,'pessoas':ids,'publicacao_fonte':date,'fonte':source,'grupo':group,'motivo_grupo':reason,'regra_versao':VERSION})
  print(key,'pagina',start,'novos',new,'coletados',len(rows),flush=True)
  # Em oficio, cada tipo e uma secao: nao parar no primeiro ano antigo.
  if new==0 or (years and all(y<2025 for y in years[-20:])):
   end=True;break
 if not end:raise ValueError('Limite sem cobrir toda a consulta: '+key)
 return {'tipo':tipo,'registros':rows,'paginas':pages,'completa_no_periodo':True}
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 for result in ex.map(collect,TYPES):results.append(result)
allrows=[r for part in results for r in part['registros']]
assert len({r['id'] for r in allrows})==len(allrows)
folder=ROOT/'dist/propostas';folder.mkdir(exist_ok=True)
summary={}
for p in people:
 rows=[r for r in allrows if p['id'] in r['pessoas']]
 # Ordem cronologica por ano/numero dentro do tipo; sem ranking de pessoas.
 rows.sort(key=lambda r:(-r['ano_referencia'],r['tipo'],-int(re.match(r'\d+',r['numero']).group())))
 summary[p['id']]={g['id']:sum(r['grupo']==g['id'] for r in rows) for g in GROUPS}
 (folder/(p['id']+'.json')).write_text(json.dumps(rows,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
data.pop('projetos',None)
data['grupos']=GROUPS;data['propostas_resumo']=summary
data['classificacao']={'versao':VERSION,'periodo':'Desde 2025, até a coleta de '+datetime.now().date().isoformat(),'consultado_em':datetime.now(timezone.utc).isoformat(),'total_documentos':len(allrows),'por_grupo':dict(collections.Counter(r['grupo'] for r in allrows)),'tipos':[{'tipo':x['tipo'],'quantidade':len(x['registros']),'paginas':x['paginas'],'completa_no_periodo':True} for x in results],'fonte_geral':'https://www.camara.rio/atividade-parlamentar/processo-legislativo','base':'tipo oficial e ementa','inclui_oficios':True}
(ROOT/'dist/dados.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
(ROOT/'data/propostas_todas.json').write_text(json.dumps(allrows,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
(ROOT/'data/propostas_manifesto.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('FINAL',len(allrows),collections.Counter(r['grupo'] for r in allrows),flush=True)
