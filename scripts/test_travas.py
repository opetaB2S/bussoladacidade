import copy,json,shutil,tempfile,unittest
from pathlib import Path
from atualizar import ROOT,read,records,validate

class Gates(unittest.TestCase):
    def test_tls_blocks(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder); d=read(ROOT/'dist/dados.json'); d['tls_validado']=False
            (p/'dados.json').write_text(json.dumps(d),encoding='utf8')
            with self.assertRaisesRegex(ValueError,'TLS'):
                validate(ROOT/'dist',p,records(ROOT/'dist'))

    def test_missing_record_blocks(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder); d=read(ROOT/'dist/dados.json'); d['tls_validado']=True; (p/'dados.json').write_text(json.dumps(d),encoding='utf8')
            with self.assertRaisesRegex(ValueError,'desapareceram'):
                validate(ROOT/'dist',p,records(ROOT/'dist')[:-1])

    def test_missing_person_blocks(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder); d=read(ROOT/'dist/dados.json'); d['pessoas'].pop()
            (p/'dados.json').write_text(json.dumps(d),encoding='utf8')
            with self.assertRaisesRegex(ValueError,'51 pessoas'):
                validate(ROOT/'dist',p,records(ROOT/'dist'))

if __name__=='__main__': unittest.main()
