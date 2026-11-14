"""Aplica a regra vigente aos originais ja coletados, sem nova consulta a rede."""
import collections,json
from pathlib import Path
from classificar import classify,VERSION,GROUPS
p=Path(__file__).resolve().parents[1]
rows=json.loads((p/'data/propostas_todas.json').read_text(encoding='utf-8'))
d=json.loads((p/'dist/dados.json').read_text(encoding='utf-8'))
for r in rows:
 r['grupo'],r['motivo_grupo']=classify(r['tipo'],r['ementa']);r['regra_versao']=VERSION
for person in d['pessoas']:
 items=[r for r in rows if person['id'] in r['pessoas']]
 items.sort(key=lambda r:(-r.get('ano_referencia',int(r['numero'].split('/')[-1])),r['tipo'],-int(r['numero'].split('/')[0].split('-')[0])))
 d['propostas_resumo'][person['id']]={g['id']:sum(r['grupo']==g['id'] for r in items) for g in GROUPS}
 (p/'dist/propostas'/(person['id']+'.json')).write_text(json.dumps(items,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
d['grupos']=GROUPS;d['classificacao']['versao']=VERSION;d['classificacao']['por_grupo']=dict(collections.Counter(r['grupo'] for r in rows))
(p/'dist/dados.json').write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
(p/'data/propostas_todas.json').write_text(json.dumps(rows,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print(len(rows),'registros classificados;',d['classificacao']['por_grupo'])
