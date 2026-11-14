import collections,json,unittest
from pathlib import Path
from classificar import classify,GROUPS,VERSION
class RuleTests(unittest.TestCase):
 def test_examples_and_precedence(self):
  cases=[
   ('Indicação','Requer urbanização na Rua Avelino Moreira, em Guaratiba.','melhorias'),
   ('Indicação','Requer iluminação para toda a cidade.','melhorias'),
   ('Indicação','Solicita reposição de placa em homenagem a Maria.','melhorias'),
   ('Indicação','Indica apoio institucional ao calendário oficial de regatas.','melhorias'),
   ('Requerimento de informação','Requer informações sobre os ônibus.','cobrancas'),
   ('Requerimento','Convoca secretário para prestar esclarecimentos.','cobrancas'),
   ('Moção','Moção de congratulações e aplausos a Maria.','homenagens'),
   ('Moção','Moção de pesar pelo falecimento de Maria.','homenagens'),
   ('Moção','Moção de repúdio ao fechamento de uma empresa.','outros'),
   ('Projeto de decreto legislativo','Concede o título de cidadã benemérita a Maria.','homenagens'),
   ('Projeto de lei','Dá o nome de Maria a um logradouro público.','homenagens'),
   ('Indicação','Denominação de logradouro público como Praça Maria.','homenagens'),
   ('Projeto de lei','Inclui o Dia do Compositor no Calendário Oficial da Cidade.','homenagens'),
   ('Projeto de lei','Institui a Semana Municipal de Prevenção de Doenças.','homenagens'),
   ('Projeto de lei','Estabelece a gratuidade dos ônibus em dia de realização de eleição dos Conselhos Tutelares.','leis'),
   ('Projeto de lei','Institui o dia de folga para trabalhadores.','leis'),
   ('Projeto de lei','Institui regras para a acessibilidade nos ônibus.','leis'),
   ('Projeto de lei complementar','Altera as regras do licenciamento de empresas.','leis'),
   ('Proposta de emenda à Lei Orgânica','Acrescenta princípio da equidade na infraestrutura verde.','leis'),
   ('Requerimento','Requer inclusão como coautor de projeto que concede medalha de mérito.','outros'),
   ('Ofício','Requer a correção de erro no nome do homenageado.','outros'),
   ('Requerimento','Requer concessão da medalha Pedro Ernesto a Maria.','homenagens'),
   ('Projeto de resolução','Altera a composição da Comissão de Defesa da Mulher.','outros'),
  ]
  for tipo,text,expected in cases:
   with self.subTest(text=text):self.assertEqual(classify(tipo,text)[0],expected)
 def test_dataset_partition_and_every_person(self):
  p=Path(__file__).resolve().parents[1];d=json.loads((p/'dist/dados.json').read_text(encoding='utf-8'))
  rows=json.loads((p/'data/propostas_todas.json').read_text(encoding='utf-8'));groups={g['id'] for g in GROUPS}
  self.assertEqual(len({r['id'] for r in rows}),len(rows));self.assertEqual(len(rows),d['classificacao']['total_documentos'])
  for r in rows:
   self.assertIn(r['grupo'],groups);self.assertEqual((r['grupo'],r['motivo_grupo']),classify(r['tipo'],r['ementa']));self.assertEqual(r['regra_versao'],VERSION)
  for person in d['pessoas']:
   expected={r['id'] for r in rows if person['id'] in r['pessoas']}
   items=json.loads((p/'dist/propostas'/(person['id']+'.json')).read_text(encoding='utf-8'))
   self.assertEqual({r['id'] for r in items},expected)
   self.assertEqual(len(items),sum(d['propostas_resumo'][person['id']].values()))
   for group in groups:self.assertEqual(sum(r['grupo']==group for r in items),d['propostas_resumo'][person['id']][group])
if __name__=='__main__':unittest.main()
