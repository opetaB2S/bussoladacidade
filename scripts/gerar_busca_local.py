"""Indice de texto completo das ementas; cruzamentos conservadores de indicacoes."""
import collections,hashlib,json,re
from datetime import datetime
from pathlib import Path
from busca_local import tokens,canonical,streets,neighborhood,services,SERVICES,generic_street
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'dist/busca'
for f in ['indice','registros']:(OUT/f).mkdir(parents=True,exist_ok=True)
rows=json.loads((ROOT/'data/propostas_todas.json').read_text(encoding='utf-8'))
index=collections.defaultdict(lambda:collections.defaultdict(list));groups=collections.defaultdict(list);records=[];request_ids=[]
reasons=collections.Counter()
for i,r in enumerate(rows):
 for word in tokens(r['ementa']):index[word[0]][word].append(i)
 road=streets(r['ementa']);bairro=neighborhood(r['ementa']);cats=services(r['ementa'],[*road,bairro]);date=None
 if r['publicacao_fonte']:
  try:date=datetime.strptime(r['publicacao_fonte'][:10],'%m/%d/%Y').date().isoformat()
  except ValueError:pass
 record={k:r[k] for k in ['id','tipo','numero','ementa','autores_fonte','pessoas','fonte','grupo']}
 record.update({'data':date,'vias':road,'bairro':bairro,'servicos':cats,'repeticoes':[]})
 records.append(record)
 if r['grupo'] in ('melhorias','cobrancas'):request_ids.append(i)
 if r['tipo']!='Indicação' or r['grupo']!='melhorias':continue
 if len(road)!=1:reasons['sem_uma_unica_via']+=1;continue
 if not bairro:reasons['sem_bairro_explicito_unico']+=1;continue
 if generic_street(road[0]):reasons['nome_generico']+=1;continue
 if not cats:reasons['servico_nao_identificado']+=1;continue
 if not date:reasons['sem_data_publicacao']+=1;continue
 # Referencias de esquina/entre ruas tambem ficam fora para nao fundir trechos.
 if re.search(r'\b(ESQUINA|CRUZAMENTO|ENTRE AS RUAS|ENTRE A RUA)\b',r['ementa'],re.I):reasons['cruzamento_ou_multiplas_vias']+=1;continue
 for cat in cats:groups[(canonical(road[0]),canonical(bairro),cat)].append(i)

repetitions=[]
for (street,bairro,cat),ids in sorted(groups.items()):
 ids=list(dict.fromkeys(ids));dates={records[i]['data'] for i in ids}
 if len(ids)<2 or len(dates)<2:continue
 ids.sort(key=lambda i:(records[i]['data'],records[i]['id']))
 # Evita juntar comunidades diferentes quando explicitamente citadas.
 communities=set()
 for i in ids:
  for m in re.finditer(r'\bCOMUNIDADE\s+(?:(?:DE|DA|DO)\s+)?([^,;.]+)',rows[i]['ementa'],re.I):communities.add(canonical(m.group(1)))
 if len(communities)>1:reasons['comunidades_diferentes']+=1;continue
 groupid=len(repetitions)
 date_sources=[{'data':day,'fonte':next(records[i]['fonte'] for i in ids if records[i]['data']==day)} for day in sorted(dates)]
 repetitions.append({'id':groupid,'rua':records[ids[0]]['vias'][0],'bairro':records[ids[0]]['bairro'],'servico':cat,'registros':ids,'datas':sorted(dates),'datas_fontes':date_sources})
 for i in ids:records[i]['repeticoes'].append(groupid)

for bucket,words in index.items():
 (OUT/'indice'/(bucket+'.json')).write_text(json.dumps(words,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
for start in range(0,len(records),250):
 (OUT/'registros'/(str(start//250)+'.json')).write_text(json.dumps(records[start:start+250],ensure_ascii=False,separators=(',',':')),encoding='utf-8')
order=sorted(range(len(records)),key=lambda i:(records[i]['data'] or '',records[i]['id']),reverse=True)
meta={'versao':'2026-11-14-local-v1','total':len(records),'por_pagina':250,'pedidos':request_ids,'ordem':order,'repeticoes':repetitions,'servicos':[{'id':key,'nome':label,'padrao':pattern} for key,label,pattern in SERVICES],'periodo':'Desde 2025, até a coleta de '+datetime.now().date().isoformat(),'escopo_busca':'Texto das ementas oficiais coletadas. Não pesquisa o corpo integral de cada documento.','escopo_repeticoes':'Indicações de melhoria com uma única via e bairro explícito, mesmo nome de rua e bairro, categoria de serviço e pelo menos duas datas de publicação distintas.','fora_do_cruzamento':dict(reasons)}
(OUT/'manifesto.json').write_text(json.dumps(meta,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
(ROOT/'data/busca_local_resumo.json').write_text(json.dumps({k:v for k,v in meta.items() if k not in ['pedidos','repeticoes']},ensure_ascii=False,indent=2),encoding='utf-8')
print('Indice:',len(records),'registros;',len(request_ids),'pedidos;',len(repetitions),'grupos de repeticao')
for g in sorted(repetitions,key=lambda g:len(g['registros']),reverse=True)[:12]:print(g['rua'],g['bairro'],g['servico'],len(g['registros']),g['datas'])
