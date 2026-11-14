"""Build isolated candidate; never overwrite last good dist on collection failure."""
import collections, datetime as dt, hashlib, json, shutil, subprocess, sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def treehash(folder):
    digest=hashlib.sha256()
    for p in sorted(folder.rglob('*')):
        if p.is_file():
            digest.update(str(p.relative_to(folder)).replace('\\','/').encode())
            digest.update(p.read_bytes())
    return digest.hexdigest()

def require(ok, message):
    if not ok:
        raise ValueError(message)

def records(folder):
    return [r for p in sorted((folder/'busca/registros').glob('*.json')) for r in read(p)]

def validate(old, candidate, rows):
    d = read(candidate/'dados.json'); baseline = read(old/'dados.json')
    ids = {p['id'] for p in d['pessoas']}
    require(len(ids)==len(d['pessoas'])==51, 'Cadastro não contém 51 pessoas únicas')
    require(ids=={p['id'] for p in baseline['pessoas']}, 'Cadastro mudou: exige revisão humana')
    require(d['tls_validado'], 'TLS não validado')
    require(len(rows)==len({r['id'] for r in rows}), 'Documentos duplicados')
    oldrows={r['id']:r for r in records(old)}
    newrows={r['id']:r for r in rows}
    require(oldrows.keys() <= newrows.keys(), 'Documentos antigos desapareceram')
    changed=sum(any(r.get(k)!=newrows[key].get(k) for k in ('ementa','autores_fonte','grupo')) for key,r in oldrows.items())
    require(changed<=max(10,len(oldrows)*0.02), 'Muitos documentos antigos mudaram: exige revisão humana')
    before=baseline['classificacao']['total_documentos']
    require(before<=len(rows)<=before*1.15, 'Volume fora da faixa: exige revisão humana')
    require(len(d['classificacao']['tipos'])==10 and all(t['completa_no_periodo'] and t['quantidade']>0 for t in d['classificacao']['tipos']), 'Tipo de documento ausente/incompleto')
    require(sum(t['quantidade'] for t in d['classificacao']['tipos'])==len(rows), 'Contagem por tipo diverge')
    require(dict(collections.Counter(r['grupo'] for r in rows))==d['classificacao']['por_grupo'], 'Grupos não fecham')
    require(all(r['autores_fonte'].strip() for r in rows), 'Documento sem autoria')
    known_empty={key for key,r in oldrows.items() if not r['ementa'].strip()}
    require({r['id'] for r in rows if not r['ementa'].strip()}<=known_empty, 'Novo documento sem resumo: revisar fonte')
    require('\ufffd' not in json.dumps(d,ensure_ascii=False)+json.dumps(rows,ensure_ascii=False), 'Erro de codificação')
    for r in rows+d['pessoas']+d['frequencia']+d['votacoes']:
        require(urlparse(r['fonte']).hostname in ('www.camara.rio','aplicnt.camara.rj.gov.br'), 'Fonte não oficial')
    require(all(r['pessoas'] and set(r['pessoas'])<=ids or not r['pessoas'] for r in rows), 'Autoria inválida')
    for person in d['pessoas']:
        require((candidate/person['foto']).read_bytes().startswith((b'\xff\xd8',b'\x89PNG')), 'Foto inválida')
    for month in d['frequencia']:
        rr=month['registros']
        require(len({r['nome_fonte'] for r in rr})==len(rr), 'Frequência duplicada')
        for r in rr:
            require(0<=r['total']==r['faltas']-r['abonadas'] and r['abonadas']>=0, 'Faltas inconsistentes')
        previous=next((m for m in baseline['frequencia'] if m['rotulo']==month['rotulo']),None)
        if previous and previous['registros']:
            require(len(rr)>=len(previous['registros']), 'Tabela de frequência encolheu')
    known={r['fonte'] for r in baseline['votacoes_pendencias']}
    require(all(r['fonte'] in known for r in d['votacoes_pendencias']), 'Nova votação inconsistente: revisar')
    for v in d['votacoes']:
        require(len(v['votos'])==len({r['pessoa'] for r in v['votos']}), 'Votos duplicados')
        require(all(r['pessoa'] in ids and r['voto'] in ('Sim','Não') for r in v['votos']), 'Voto sem identidade confirmada')
    oldvotes={v['id'] for v in baseline['votacoes'] if v['data'][:7]==d['coletado_em'][:7]}
    require(oldvotes<={v['id'] for v in d['votacoes']}, 'Votação antiga desapareceu')
    return {'vereadores':len(ids),'documentos':len(rows),'votacoes':len(d['votacoes']),'votos':sum(len(v['votos']) for v in d['votacoes'])}

def main():
    stage=ROOT/'.candidate'
    if stage.exists():
        require(stage.resolve().parent==ROOT.resolve(), 'Pasta temporária fora do projeto')
        shutil.rmtree(stage)
    stage.mkdir(); shutil.copytree(ROOT/'scripts',stage/'scripts'); shutil.copytree(ROOT/'dist',stage/'dist')
    shutil.copy2(ROOT/'index.php',stage/'index.php')
    report={'iniciado_em':dt.datetime.now(dt.timezone.utc).isoformat(),'publicavel':False,'base_sha256_antes':treehash(ROOT/'dist')}
    reports=ROOT/'reports'; reports.mkdir(exist_ok=True)
    try:
        for script in ['coletar.py','ampliar_propostas.py']:
            logfile=reports/(script+'.log')
            with logfile.open('w',encoding='utf8') as output:
                result=subprocess.run([sys.executable,'-u',str(stage/'scripts'/script)],stdout=output,stderr=subprocess.STDOUT)
            require(result.returncode==0, script+' falhou: '+logfile.read_text(encoding='utf8',errors='replace')[-1200:])
        rows=read(stage/'data/propostas_todas.json')
        for name in ['manifesto.json','propostas_manifesto.json']:
            manifest=read(stage/'data'/name)
            require(manifest and all(not r['cache_reutilizado'] and r['tls_validado'] for r in manifest), 'Coleta reutilizou cache ou TLS inseguro')
        report.update(validate(ROOT/'dist',stage/'dist',rows))
        shutil.rmtree(stage/'dist/busca')
        subprocess.run([sys.executable,str(stage/'scripts/gerar_busca_local.py')],check=True)
        m=read(stage/'dist/busca/manifesto.json')
        groups={g['id']:[i for i in m['ordem'] if rows[i]['grupo']==g['id']] for g in read(stage/'dist/dados.json')['grupos']}
        (stage/'dist/grupos-indice.json').write_text(json.dumps(groups),encoding='utf8')
        (stage/'dist/bussola-resumo.json').write_text(json.dumps({'repeticoes':m['repeticoes'][:6],'servicos':m['servicos']},ensure_ascii=False),encoding='utf8')
        date=read(stage/'dist/dados.json')['coletado_em'][:10]
        page=(stage/'index.php').read_text('utf8').replace('__DATA_ISO__',date).replace('__DATA_COLETA__',date[8:10]+'/'+date[5:7]+'/'+date[:4])
        (stage/'index.php').write_text(page,encoding='utf8')
        subprocess.run([sys.executable,str(stage/'scripts/gerar_previa.py')],check=True)
        require(len(records(stage/'dist'))==len(rows), 'Índice de busca incompleto')
        report['publicavel']=True
        report['dados_sha256']=hashlib.sha256((stage/'dist/dados.json').read_bytes()).hexdigest()
        (stage/'dist/ultima-atualizacao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
        print('CANDIDATO APROVADO. Publicação deve usar somente .candidate/dist',flush=True)
    except Exception as e:
        report['erro']=str(e); print('PUBLICAÇÃO BLOQUEADA:',e,flush=True)
        raise
    finally:
        report['base_sha256_depois']=treehash(ROOT/'dist')
        report['base_preservada']=report['base_sha256_antes']==report['base_sha256_depois']
        (reports/'execucao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')

if __name__=='__main__':
    main()
