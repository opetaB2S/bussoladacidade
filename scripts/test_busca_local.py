import collections,json,unittest
from pathlib import Path
from busca_local import canonical,streets,neighborhood,services,generic_street,tokens
class AddressTests(unittest.TestCase):
 def test_address_boundaries(self):
  self.assertEqual(streets('TAPA-BURACO NA RUA BARÃO DO BOM RETIRO, Nº 1199, NO BAIRRO DE ENGENHO NOVO.'),['Rua BARÃO DO BOM RETIRO'])
  self.assertEqual(neighborhood('RUA A, NO BAIRRO DO ENGENHO NOVO.'),'ENGENHO NOVO')
  self.assertEqual(streets('PODA NA AV. BRASIL, ALTURA DO Nº 20, NO BAIRRO DE IRAJÁ.'),['Avenida BRASIL'])
  self.assertEqual(streets('LIMPEZA NA RUA ALFA EM FRENTE AO Nº 12, NO BAIRRO DE BETA.'),['Rua ALFA'])
 def test_ambiguity_is_not_inferred(self):
  self.assertIsNone(neighborhood('PODA NA RUA ALFA, EM COPACABANA.'))
  self.assertIsNone(neighborhood('RUA ALFA, NO SUB-BAIRRO FIGUEIRA EM CAMPO GRANDE.'))
  self.assertIsNone(neighborhood('RUA ALFA, NO BAIRRO DE TIJUCA E MARACANÃ.'))
  self.assertEqual(len(streets('PODA NA RUA ALFA E NA RUA BETA, NO BAIRRO DE GAMA.')),2)
  self.assertTrue(generic_street('Rua A'));self.assertTrue(generic_street('Rua 1'));self.assertTrue(generic_street('Rua Cinquenta e Cinco'))
  self.assertFalse(generic_street('Rua Primeiro de Maio'))
 def test_accents_abbreviations_and_categories(self):
  self.assertEqual(canonical('Rua Barão do Bom Retiro'),canonical('RUA BARAO DO BOM RETIRO'))
  self.assertIn('avenida_brasil',tokens('ILUMINAÇÃO NA AV. BRASIL'))
  self.assertIn('rua_a',tokens('LIMPEZA NA RUA A'))
  self.assertIn('poda',services('Poda de árvores'))
  self.assertIn('asfalto',services('Reparo no afundamento asfáltico'))
  self.assertNotIn('iluminacao',services('Ilustríssimo Senhor Vereador'))
  self.assertNotIn('rocada',services('Solicita iluminação na Estrada da Boca do Mato, no bairro de Vargem Pequena.'))
  self.assertIn('drenagem',services('Solicita drenagem na Estrada da Boca do Mato, no bairro de Vargem Pequena.'))
 def test_all_groups_preserve_sources_and_separate_bairros(self):
  p=Path(__file__).resolve().parents[1]/'dist/busca';m=json.loads((p/'manifesto.json').read_text(encoding='utf-8'))
  pages={}
  def row(i):
   if i//250 not in pages:pages[i//250]=json.loads((p/'registros'/(str(i//250)+'.json')).read_text(encoding='utf-8'))
   return pages[i//250][i%250]
  self.assertEqual(m['total'],62271);self.assertEqual(len(m['ordem']),m['total']);self.assertEqual(len(set(m['ordem'])),m['total'])
  for g in m['repeticoes']:
   records=[row(i) for i in g['registros']]
   self.assertGreaterEqual(len(records),2);self.assertGreaterEqual(len(set(r['data'] for r in records)),2)
   self.assertEqual(len({r['id'] for r in records}),len(records))
   self.assertEqual({canonical(r['bairro']) for r in records},{canonical(g['bairro'])})
   self.assertEqual({canonical(r['vias'][0]) for r in records},{canonical(g['rua'])})
   self.assertTrue(all(len(r['vias'])==1 and r['tipo']=='Indicação' and r['grupo']=='melhorias' and g['servico'] in r['servicos'] for r in records))
   self.assertTrue(all(g['id'] in r['repeticoes'] for r in records))
   self.assertTrue(all(d['fonte'] in {r['fonte'] for r in records if r['data']==d['data']} for d in g['datas_fontes']))
  known=next(g for g in m['repeticoes'] if canonical(g['rua'])=='rua barao do bom retiro' and canonical(g['bairro'])=='engenho novo' and g['servico']=='drenagem')
  self.assertEqual(len(known['registros']),8);self.assertEqual(known['datas'],['2025-11-26','2026-08-05'])
if __name__=='__main__':unittest.main()
