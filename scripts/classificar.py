"""Regra v1: so usa tipo oficial e ementa. Nunca usa autor, partido ou voto."""
import re,unicodedata
VERSION='2026-11-14-v1'
GROUPS=[
 {'id':'melhorias','nome':'Melhorias nos bairros','descricao':'Pedidos de obras, serviços e outras providências para a cidade.'},
 {'id':'cobrancas','nome':'Perguntas e cobranças','descricao':'Pedidos de informação, explicação, apuração ou fiscalização.'},
 {'id':'homenagens','nome':'Homenagens','descricao':'Parabéns, pesar, títulos, medalhas, nomes de espaços públicos e datas comemorativas.'},
 {'id':'leis','nome':'Propostas de lei','descricao':'Propostas para criar ou alterar leis e a Lei Orgânica, que não entraram nos grupos anteriores.'},
 {'id':'outros','nome':'Outros','descricao':'Os demais assuntos e os registros que não se encaixam claramente nas regras anteriores.'},
]
def normalize(s):return re.sub(r'\s+',' ',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().upper()).strip()
def classify(tipo,ementa):
    t=normalize(ementa)
    if tipo in ('Requerimento','Ofício') and re.search(r'\b(COAUTORIA|COAUTOR|COAUTORA|COAUTORES|REPUBLICAR|REPUBLICACAO|CORRIGIR|CORRECAO|ERRO MATERIAL|ARQUIVAMENTO|DESARQUIVAMENTO|ADIAMENTO|RETIRADA|INCLUSAO NA PAUTA|INCLUSAO NA ORDEM DO DIA)\b',t):
        return 'outros','É pedido de coautoria, correção, republicação ou outra providência de tramitação; não é contado novamente pelo assunto da proposta citada.'
    if tipo=='Indicação' and re.search(r'\b(REPARO|REPOSICAO|REVITALIZACAO|CONSERVACAO|MANUTENCAO|RESTAURACAO|LIMPEZA|TROCA|SUBSTITUICAO|APOIO INSTITUCIONAL|APOIO FINANCEIRO)\b',t):
        return 'melhorias','A indicação pede conserto, conservação, serviço ou apoio institucional/financeiro, mesmo que cite uma homenagem, nome de espaço ou calendário.'
    # Ordem fixa: reconhecimento explicito; indicacao; informacao/fiscalizacao;
    # lei em sentido amplo; demais. Todas as decisoes sao mutuamente exclusivas.
    if re.search(r'\b(CONGRATULAC|APLAUS|LOUVOR|PARABEN|PESAR|HOMENAGE)[A-Z]*\b',t):
        return 'homenagens','A ementa declara parabéns, aplausos, louvor, pesar ou homenagem.'
    if re.search(r'\b(CONCEDE|CONCEDER|OUTORGA|CONFERE|CONCESSAO|CONFERIR)\b',t) and re.search(r'\b(TITULO DE CIDADA[OÃ]|TITULO DE CIDADA|MEDALHA|MEDALHAS|MENCAO HONROSA|DIPLOMA DE MERITO)\b',t):
        return 'homenagens','A ementa concede ou pede título de cidadão, medalha ou outra honraria expressamente prevista na regra.'
    if re.search(r'\bDA O NOME\b',t) or (re.search(r'\b(DENOMINA|DENOMINAR|DENOMINACAO|NOMEIA)\b',t) and re.search(r'\b(RUA|LOGRADOURO|PRACA|AVENIDA|TRAVESSA|LARGO|BECO|ESCOLA|CRECHE|HOSPITAL|UNIDADE DE SAUDE|ESPACO PUBLICO|EQUIPAMENTO PUBLICO|PARQUE|PONTE|VIADUTO|ESTRADA|VIA PUBLICA)\b',t)):
        return 'homenagens','A ementa dá nome ou denominação a rua ou outro espaço público.'
    if re.search(r'\bCALENDARIO OFICIAL\b',t) or (re.search(r'\b(INSTITUI|CRIA|INCLUI|ESTABELECE|DECLARA|INSERE)\s+(?:(?:O|A|UM|UMA)\s+)?(?:DIA|SEMANA|MES)\s+(?:MUNICIPAL|DO|DA|DE|EM MEMORIA)\b',t) and not re.search(r'\bDIA DE (FOLGA|DESCANSO|PAGAMENTO|TRABALHO)\b',t)):
        return 'homenagens','A ementa cria ou inclui data, semana, mês comemorativo ou evento no calendário oficial.'
    if tipo=='Indicação':return 'melhorias','O tipo oficial é indicação: um pedido de providência ao poder público.'
    if tipo=='Requerimento de informação':return 'cobrancas','O tipo oficial é requerimento de informação.'
    if tipo in ('Requerimento','Ofício','Moção') and re.search(r'\b(INFORMACOES|ESCLARECIMENTOS|FISCALIZACAO|FISCALIZAR|APURACAO|APURAR|INVESTIGACAO|INVESTIGAR|PRESTACAO DE CONTAS|DENUNCIA|DENUNCIAR|CPI|COMISSAO PARLAMENTAR DE INQUERITO)\b',t):
        return 'cobrancas','A ementa de requerimento, ofício ou moção pede informação, esclarecimento, fiscalização, apuração, investigação ou prestação de contas, ou menciona denúncia/CPI.'
    if tipo in ('Projeto de lei','Projeto de lei complementar','Proposta de emenda à Lei Orgânica'):
        return 'leis','É proposta de lei ou de mudança da Lei Orgânica e não se enquadrou nas regras anteriores.'
    return 'outros','O tipo e a ementa não atendem às regras dos outros grupos; não foi presumido um assunto.'

