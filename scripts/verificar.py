"""Verifica invariantes relevantes para nao atribuir dados a pessoas erradas."""
import json,re
from pathlib import Path
from urllib.parse import urlparse
p=Path(__file__).resolve().parents[1];d=json.loads((p/'dist/dados.json').read_text(encoding='utf-8'))
ids={x['id'] for x in d['pessoas']}
assert len(ids)==len(d['pessoas'])==51
rows=json.loads((p/'data/propostas_todas.json').read_text(encoding='utf-8'))
assert len({x['id'] for x in rows})==len(rows)==62271
assert sum(x['tipo']=='Projeto de lei' for x in rows)==2771
assert all(x['ano_referencia'] in (2025,2026) for x in rows)
october=next(x for x in d['frequencia'] if x['mes']==10)
assert {r['pessoa'] for r in october['registros']}==ids
for m in d['frequencia']:
    for r in m['registros']:assert r['faltas']-r['abonadas']==r['total']
for v in d['votacoes']:
    assert '2026-11-03'<=v['data']<='2026-11-11'
    assert len({x['pessoa'] for x in v['votos']})==len(v['votos'])
    assert all(x['pessoa'] in ids and x['voto'] in ('Sim','N\u00e3o') for x in v['votos'])
    assert not any(x['fonte']==v['fonte'] for x in d['votacoes_pendencias'])
for obj in rows+d['votacoes']+d['pessoas']+d['frequencia']:
    assert urlparse(obj['fonte']).hostname in ('www.camara.rio','aplicnt.camara.rj.gov.br')
for x in d['pessoas']:assert (p/'dist'/x['foto']).read_bytes().startswith((b'\xff\xd8',b'\x89PNG\r\n\x1a\n'))
assert sum(len(v['votos']) for v in d['votacoes'])==497
assert len(d['votacoes_pendencias'])==1
assert '\ufffd' not in (p/'dist/dados.json').read_text(encoding='utf-8')
assert all('pessoas' in x for x in rows)
print('Dados conferidos: 51 vereadores, 62271 propostas e oficios, 17 votacoes, 497 votos.')
