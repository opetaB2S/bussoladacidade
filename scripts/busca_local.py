"""Extracao conservadora de via/bairro e categorias de servico, sem geocodificacao."""
import re,unicodedata
def fold(s):
 return ''.join(c for c in unicodedata.normalize('NFKD',s) if not unicodedata.combining(c)).lower()
def canonical(s):return re.sub(r'[^a-z0-9]+',' ',fold(s)).strip()
def tokens(s):
 s=fold(s)
 s=re.sub(r'\bav\.?(?=\s)','avenida',s)
 s=re.sub(r'\best\.(?=\s)','estrada',s)
 s=re.sub(r'\btrav\.(?=\s)','travessa',s)
 s=re.sub(r'\br\.(?=\s)','rua',s)
 seq=re.findall(r'[a-z0-9]+',s)
 out=set(seq)
 for i,w in enumerate(seq[:-1]):
  if w in ('rua','avenida','estrada','travessa'):out.add(w+'_'+seq[i+1])
 return out

SERVICES=[
 ('asfalto','Asfalto, pavimentação e buracos',r'\b(asfalt\w*|paviment\w*|recapeament\w*|buracos?|tapa[ -]?buracos?)\b'),
 ('iluminacao','Iluminação pública',r'\b(iluminacao|luminarias?|lampadas?)\b'),
 ('poda','Poda de árvores',r'\bpoda\b'),
 ('arvores','Retirada de árvores',r'\b(?:retirada|remocao|corte)\b.{0,30}\barvores?\b'),
 ('rocada','Roçada e capina',r'\b(rocada|capina\w*|(?:retirada|corte|remocao) de mato)\b'),
 ('limpeza','Limpeza e retirada de lixo',r'\b(limpeza|entulhos?|lixo|galhada|residuos solidos)\b'),
 ('esgoto','Rede de esgoto',r'\besgotos?\b'),
 ('drenagem','Drenagem, bueiros e ralos',r'\b(drenagem|bueiros?|ralos?|galerias? pluviais?|rede pluvial)\b'),
 ('calcadas','Calçadas e passeios',r'\b(calcadas?|passeios? publicos?)\b'),
 ('semaforos','Semáforos',r'\bsemafor\w*\b'),
 ('faixas','Faixas de pedestres',r'\bfaixas? (?:de )?pedestres?\b'),
 ('redutores','Lombadas e redutores de velocidade',r'\b(lombadas?|quebra[ -]?molas?|redutor\w* de velocidade)\b'),
 ('sinalizacao','Sinalização de trânsito',r'\bsinalizacao\b'),
 ('urbanizacao','Urbanização',r'\burbanizacao\b'),
 ('agua','Abastecimento e rede de água',r'\b(abastecimento de agua|rede de agua|vazamento de agua)\b'),
 ('fios','Cabos e fios',r'\b(caca[ -]?fios|fiacao|fios|cabos)\b'),
]
def services(text,places=None):
 t=canonical(text)
 if places is None:places=[*streets(text),neighborhood(text)]
 for place in places:
  if not place:continue
  name=canonical(place)
  if name.split(' ',1)[0] in ('rua','avenida','estrada','travessa'):name=name.split(' ',1)[-1]
  t=re.sub(r'\b'+re.escape(name)+r'\b',' ',t)
 return [key for key,_,pattern in SERVICES if re.search(pattern,t)]

ROAD=re.compile(r'\b(RUA|AVENIDA|AV\.|ESTRADA|EST\.|TRAVESSA|TRAV\.)\s+([^,;\n()]+)',re.I)
STOP=re.compile(r'\s+(?:NO BAIRRO|NA BAIRRO|BAIRRO|NA ALTURA|ALTURA|NAS PROXIMIDADES|NA PROXIMIDADE|PROXIMIDADE|PROXIMO|PRÓXIMO|EM FRENTE|LOCALIZAD\w*|LOCALIDADE|NA COMUNIDADE|NO TRECHO|TRECHO|ENTRE|ATÉ|ATE|ESQUINA|CRUZAMENTO|N[º°.]|NÚMERO|NUMERO|N\s*\d|EM\s+|NO\s+|NA\s+|S/N|PRÓX\.|PROX\.)',re.I)
ROAD_NEXT=re.compile(r'\s+(?:E|COM|DA|DO|À|A)\s+(?:(?:A|O|AS|OS)\s+)?(?:RUA|AVENIDA|ESTRADA|TRAVESSA)\b',re.I)
def streets(text):
 out={}
 for m in re.finditer(r'\b(RUA|AVENIDA|AV\.|ESTRADA|EST\.|TRAVESSA|TRAV\.)\s+',text,re.I):
  prefix=m.group(1).upper();tail=text[m.end():]
  tail=re.split(r'[,;\n()]|\s+[–—-]\s+',tail,1)[0]
  tail=ROAD_NEXT.split(tail,1)[0];tail=STOP.split(tail,1)[0].strip(' .:\"“”')
  if not tail or len(tail)>90 or len(tail.split())>13:continue
  if canonical(tail).startswith(('no municipio','do municipio','em situacao','para pessoas','de janeiro','e de ')):continue
  if prefix in ('AV.','AVENIDA'):prefix='Avenida'
  elif prefix in ('EST.','ESTRADA'):prefix='Estrada'
  elif prefix in ('TRAV.','TRAVESSA'):prefix='Travessa'
  else:prefix='Rua'
  label=prefix+' '+tail
  out[canonical(label)]=label
 return list(out.values())

def neighborhood(text):
 # Apenas bairro nomeado explicitamente. Localidade/comunidade nao vira bairro.
 matches=[]
 for m in re.finditer(r'(?<!SUB-)(?<!SUB )\bBAIRRO\s*(?:[-:]\s*)?(?:(?:DE|DA|DO)\s+)?([^,;\n().]+)',text,re.I):
  name=re.split(r'\s+[–—-]\s+|\s+(?:NA|NO|EM|LOCALIZAD\w*|CEP|RIO DE JANEIRO)\b',m.group(1),1,flags=re.I)[0].strip(' .:\"“”')
  key=canonical(name)
  if not key or len(key.split())>7 or re.search(r'\b(e|ou|rua|avenida|estrada|municipio|regiao)\b',key) or re.search(r'\d',key):return None
  matches.append(name)
 if len({canonical(n) for n in matches})!=1:return None
 return matches[0]

def generic_street(name):
 rest=canonical(name).split(' ',1)[-1]
 number_words=set('um uma dois duas tres quatro cinco seis sete oito nove dez onze doze treze quatorze catorze quinze dezesseis dezessete dezoito dezenove vinte trinta quarenta cinquenta sessenta setenta oitenta noventa cem cento e'.split())
 return bool(re.fullmatch(r'[a-z]|\d+',rest)) or all(w in number_words for w in rest.split())
