# Conferência dos dados — Câmara Municipal do Rio de Janeiro

Auditoria de 14/11/2026. Não foi publicada nenhuma alteração nesta etapa. A prévia anterior já estava hospedada com acesso privado.

## Resultado principal

Os números de faltas foram copiados corretamente das tabelas oficiais: nenhuma divergência encontrada em 363 linhas e 1.089 valores numéricos. A conferência alcançou todos os meses de 2026 consultados pelo site, incluindo os que não tinham tabela disponível. Isso confirma fidelidade à tabela, não validação independente da presença efetiva dos vereadores.

O site não calculou número de sessões frequentadas, percentual de presença ou tempo de permanência. Ele apresenta Faltas, Faltas Abonadas e Total de Faltas da Câmara. A única operação aritmética conferida foi Faltas menos Faltas Abonadas igual a Total de Faltas.

## O que foi comparado

1. Os dados salvos no site contra uma nova consulta ao formulário oficial de frequência.
2. O HTML dessa consulta contra a exportação oficial em Excel de cada mês. O arquivo .xls contém uma tabela HTML; não é uma apuração independente.
3. As 17 atas indexadas para outubro, mês padrão do site: HTML e respectivos DOCX baixados de outra base oficial, atas.nsf. Foram contados os nomes das listas de abertura e das verificações de quórum explicitamente identificadas.
4. O link Lista de Presença no Portal da Transparência. Ele leva ao mesmo formulário da Câmara; não é uma segunda apuração mensal.

Fontes: [frequência mensal](https://www.camara.rio/atividade-parlamentar/plenario/frequencia-dos-vereadores), [Excel de outubro](https://www.camara.rio/includes_php/vereadores_frequencia_excel.php?ano=2026&mes=10), [atas](https://aplicnt.camara.rj.gov.br/APL/Legislativos/atas.nsf/AtasInt?OpenForm&Count=1000), [Portal da Transparência](https://transparencia.camara.rj.gov.br/).

## Onde os números batem

- As 363 linhas publicadas nos sete meses com tabela são idênticas entre site, HTML consultado novamente e Excel oficial: março, abril, maio, junho, agosto, setembro e outubro.
- Os 1.089 campos numéricos comparados conferem, e a subtração de abonos confere em cada linha.
- Outubro possui 51 linhas correspondentes aos 51 nomes atuais. Somando-as: 29 faltas registradas, 19 abonadas e 10 faltas após abonos. São somas de faltas, não de vereadores nem de sessões.
- As 17 listas de abertura das atas de outubro têm quantidade de nomes igual ao total declarado no texto. Quatro listas posteriores de verificação de quórum também conferem internamente.
- Janeiro, fevereiro, julho e novembro não tinham dados atualizados para a seleção, tanto no snapshot do site como na nova consulta. Não foram convertidos em zero.

Exemplos de outubro, em que site, HTML e Excel conferem:

| Vereador, como na fonte | Faltas | Abonadas | Total após abonos |
|---|---:|---:|---:|
| Fabio Silva | 3 | 0 | 3 |
| Maíra do MST | 3 | 1 | 2 |
| Cesar Maia | 1 | 0 | 1 |
| Rick Azevedo | 2 | 2 | 0 |
| Talita Galhardo | 2 | 2 | 0 |

Fonte dos exemplos: [tabela oficial de outubro](https://www.camara.rio/includes_php/vereadores_frequencia_excel.php?ano=2026&mes=10), atualizada pela Câmara em 12/11/2026. Zero após abonos não equivale a comparecimento a todas as sessões: Rick Azevedo e Talita Galhardo são exemplos explícitos de duas faltas abonadas.

## Onde os números são diferentes — e o que isso significa

Não foi encontrada divergência numérica entre o site e a tabela oficial de faltas. A comparação de presença mensal com as atas, porém, não pôde ser fechada como uma reconciliação do mesmo indicador.

- Em [13/10/2026, 81ª sessão ordinária](https://aplicnt.camara.rj.gov.br/APL/Legislativos/atas.nsf/3f8037c08c436684032577040057cb8c/197c77b94f32717c03258e900057fe6c?OpenDocument), há nove presentes na abertura e três numa verificação posterior. Os nomes conferem nos dois momentos. São medições de momentos diferentes, não erro de soma ou nove presenças completas versus três.
- Em [20/10/2026, 84ª sessão ordinária](https://aplicnt.camara.rj.gov.br/APL/Legislativos/atas.nsf/3f8037c08c436684032577040057cb8c/0d5dfb605bf5a13803258e97005b37c3?OpenDocument), aparecem 12 na abertura e seis em verificação posterior. Novamente, os dois totais conferem com suas listas.
- Em [1º/10/2026, 77ª sessão ordinária](https://aplicnt.camara.rj.gov.br/APL/Legislativos/atas.nsf/3f8037c08c436684032577040057cb8c/8b290699f2d40e7503258e87005b9f9b?OpenDocument), consta apenas Deangeles Percy na chamada; o texto declara que não haverá sessão. O conjunto de 17 atas inclui oito com declaração de que não haveria sessão por falta de quórum e nove que descrevem abertura de sessão. Não é correto usar 17 como denominador automático de comparecimento ou atribuir faltas aos demais 50 nomes pela primeira ata.
- O quadro mensal inclui abonos posteriores e cita processos administrativos. As atas não substituem a apuração mensal de abonos, licenças e frequência. Não foi encontrada uma segunda planilha mensal independente que permita reconstituir cada falta e seu abono por data.

Portanto, a presença efetiva mensal continua **não validada independentemente**. Não atribuímos a divergência entre uma contagem de abertura e a tabela mensal a atraso, saída, licença ou erro da Câmara sem documentação individual suficiente.

Há ainda uma inconsistência já identificada em outra parte da base: o [registro do PL 951/2025 em 03/11/2026](https://aplicnt.camara.rj.gov.br/APL/Legislativos/discvot.nsf/5d50d39bd976391b83256536006a2502/0f9abb8494808f1303258ea4005f430b?OpenDocument) declara 18 votos SIM, mas enumera 19 nomes. O bloco foi excluído integralmente da extração de votos. Não sabemos qual informação da fonte deve ser corrigida; não escolhemos um vereador para excluir nem alteramos o placar por conta própria. Isso não é uma divergência nas tabelas de faltas.

## Tudo o que é calculado, inferido ou ainda não confirmado

### Presença e faltas

- Não há estimativa numérica de presença nem percentual no site. Contagens de presença na abertura/quórum são observações daquele momento, não presença integral.
- Não foi confirmado o denominador administrativo que a Câmara usa para as faltas mensais, nem quais sessões/ocorrências entram em cada linha.
- Não foram conferidos integralmente os processos de abono citados nas observações, as datas individuais das faltas, licenças, afastamentos ou substituições. A tabela é reproduzida como publicada.
- A falta de tabela em janeiro, fevereiro, julho e novembro não foi interpretada como ausência de sessões, recesso, falta de vereadores ou zero faltas.
- Niquinho não aparece nas tabelas de março e abril consultadas. Não foi confirmada a razão; o site não transforma a ausência do nome em zero.
- Março tem 56 linhas e abril 52 porque as tabelas contêm nomes fora do cadastro atual; isso não significa 56 ou 52 cadeiras simultâneas. Não foi validado todo o histórico de exercício de cada pessoa.

### Propostas e autoria

- As 62.271 entradas são documentos coletados dos tipos e período declarados, não total histórico garantido de tudo que cada vereador fez. Emendas avulsas, pareceres e documentos anteriores a 2025 estão fora dessas consultas. A completude foi verificada pela paginação usada, não por um total certificado pela Câmara ou por revisão manual de todos os documentos.
- As contagens por vereador são calculadas pelo site a partir da autoria registrada. Um documento conjunto aparece uma vez para cada autor identificado. Somar perfis duplica documentos conjuntos.
- A vinculação de nomes desconsidera acentos e maiúsculas, sem aproximação. Variantes não confirmadas podem ficar sem vínculo. Não foi feita auditoria manual integral de identidade/autoria de todas as entradas.
- Os cinco grupos são classificação automática do site por tipo e ementa, não classificação oficial da Câmara. Não houve leitura e validação manual do texto completo das 62.271 entradas. Assuntos mistos e expressões ambíguas podem ser classificados de forma incompleta.
- Não foi confirmado que os projetos apresentados foram aprovados, viraram lei ou tiveram seus efeitos executados. Essas conclusões não são dadas pelas contagens.
- Cinco indicações têm ano malformado no número do índice. Sua inclusão no período foi inferida pela data oficial de publicação; o número original não foi reescrito.

### Busca por local e repetições

- A busca pesquisa ementas, não o texto integral. Pode não encontrar endereço que apareça apenas no corpo do documento, em anexo, por outra grafia ou por nome antigo.
- Busca por palavras pode trazer nomes compostos que contêm esses termos; por exemplo, Tijuca pode aparecer dentro de Barra da Tijuca. O local deve ser conferido no resumo. Não há geolocalização do usuário.
- Nomes de rua, bairro e serviço são extraídos automaticamente da ementa. Não foi confirmado em cadastro geográfico que cada bairro informado seja um bairro oficial, nem que duas grafias iguais correspondam ao mesmo trecho físico. Variações de grafia também podem impedir cruzamentos legítimos.
- Os 139 grupos são possíveis repetições segundo a regra do site, não uma estatística oficial. A regra exige uma via, um bairro explícito, categoria de serviço, documentos distintos e datas de publicação diferentes. Nomes genéricos, sub-bairro sem bairro e ambiguidades são excluídos conservadoramente.
- Categorias como drenagem/bueiros/ralos ou asfalto/pavimentação/buracos reúnem serviços relacionados. Não foi confirmado que todos tratem do mesmo defeito, ponto, trecho ou providência exata. Um documento pode citar mais de um serviço e participar de mais de um grupo; isso não duplica o total dos resultados da busca.
- As contagens de repetição são do grupo completo da rua e bairro, não só dos documentos que passaram pelo termo de busca. Os documentos e suas datas ficam disponíveis para conferência.
- Data de publicação não confirma data do protocolo do pedido, envio à Prefeitura, execução, resposta, atendimento, recusa ou omissão. Não foi cruzado sistema administrativo de execução da Prefeitura. **Pedido repetido não prova que a Prefeitura ignorou.**

### Votos, atualização e integridade técnica

- Os 497 votos mostrados são os extraídos de 17 listas nominais do período de 3 a 11/11/2026. Não são o histórico do mandato, nem todos os tipos de votação. Uma lista inconsistente foi excluída. Não foi feita agora uma auditoria independente de todos os votos.
- Em votação simbólica, não foi atribuído voto SIM aos demais vereadores a partir de uma aprovação ou do registro de um voto contrário. Ausência de voto identificado não é falta nem voto NÃO.
- Uma página pode tratar de veto, emenda, adiamento ou outra decisão. O voto só deve ser lido com o objeto documentado; um NÃO a veto não foi convertido automaticamente em NÃO ao projeto.
- O cadastro atual, partidos e dados são snapshots de 14/11/2026. Não há atualização automática agendada. Alterações posteriores da Câmara, inclusive novos abonos, exigem nova coleta.
- A validação TLS falhou neste ambiente para os hosts da Câmara. As consultas por script foram feitas no modo diagnóstico sem validação de certificado, como já registrado nas entregas anteriores e nesta auditoria. URLs e arquivos são dos endereços oficiais acessados, mas não foi confirmada criptograficamente a cadeia do servidor. Hashes comprovam integridade local dos arquivos recebidos, não autenticidade da origem.

## Arquivos para conferir

- `conferencia_faltas_2026.csv`: cada uma das 363 linhas, com valores do site, HTML e Excel lado a lado e URL oficial.
- `conferencia_atas_outubro.csv`: as 17 atas, contagens de abertura, indicador de sessão não iniciada e links oficiais.
- `comparacao_tabelas.json` e `comparacao_atas.json`: valores, listas e trechos usados na comparação.
- `manifesto_auditoria.json`: URLs e hashes dos arquivos oficiais baixados.
- `evidencias_auditoria.zip`: arquivos originais usados na auditoria, sem alteração do site.


## Quadro de conferência mensal

| Mês de 2026 | Linhas | Faltas | Abonadas | Total após abonos | Site / HTML / Excel |
|---|---:|---:|---:|---:|---|
| Janeiro | Sem tabela | — | — | — | Mesma indisponibilidade |
| Fevereiro | Sem tabela | — | — | — | Mesma indisponibilidade |
| Março | 56 | 37 | 28 | 9 | Conferem |
| Abril | 52 | 28 | 21 | 7 | Conferem |
| Maio | 51 | 23 | 18 | 5 | Conferem |
| Junho | 51 | 45 | 28 | 17 | Conferem |
| Julho | Sem tabela | — | — | — | Mesma indisponibilidade |
| Agosto | 51 | 16 | 6 | 10 | Conferem |
| Setembro | 51 | 21 | 4 | 17 | Conferem |
| Outubro | 51 | 29 | 19 | 10 | Conferem |
| Novembro | Sem tabela | — | — | — | Mesma indisponibilidade |

## Todos os nomes da tabela de outubro

Valores da fonte; todos conferem entre site, HTML e Excel.

| Vereador | Faltas | Abonadas | Total após abonos |
|---|---:|---:|---:|
| ALANA PASSOS | 0 | 0 | 0 |
| ÁTILA NUNES | 0 | 0 | 0 |
| CARLO CAIADO | 0 | 0 | 0 |
| CESAR MAIA | 1 | 0 | 1 |
| DEANGELES PERCY | 0 | 0 | 0 |
| DIEGO FARO | 0 | 0 | 0 |
| DR. GILBERTO | 0 | 0 | 0 |
| DR. ROGERIO AMORIM | 0 | 0 | 0 |
| FABIO SILVA | 3 | 0 | 3 |
| FELIPE BORÓ | 0 | 0 | 0 |
| FELIPE MICHEL | 1 | 1 | 0 |
| FELIPE PIRES | 1 | 1 | 0 |
| FERNANDO ARMELAU | 1 | 1 | 0 |
| FLÁVIO VALLE | 1 | 0 | 1 |
| GIGI CASTILHO | 0 | 0 | 0 |
| HELENA VIEIRA | 0 | 0 | 0 |
| INALDO SILVA | 1 | 1 | 0 |
| JAIR DA MENDES GOMES | 0 | 0 | 0 |
| JORGE CANELLA | 3 | 2 | 1 |
| JOYCE TRINDADE | 0 | 0 | 0 |
| JUNIOR DA LUCINHA | 0 | 0 | 0 |
| LENIEL BOREL | 2 | 2 | 0 |
| LEONEL DE ESQUERDA | 0 | 0 | 0 |
| LUIZ RAMOS FILHO | 0 | 0 | 0 |
| MAÍRA DO MST | 3 | 1 | 2 |
| MARCELO DINIZ | 0 | 0 | 0 |
| MARCIO RIBEIRO | 0 | 0 | 0 |
| MARCOS DIAS | 2 | 1 | 1 |
| MONICA BENICIO | 1 | 1 | 0 |
| NIQUINHO | 1 | 1 | 0 |
| PAULO MESSINA | 0 | 0 | 0 |
| PEDRO DUARTE | 0 | 0 | 0 |
| POUBEL | 0 | 0 | 0 |
| RAFAEL ALOISIO FREITAS | 0 | 0 | 0 |
| RAFAEL SATIÊ | 0 | 0 | 0 |
| RENATO MOURA | 0 | 0 | 0 |
| RICK AZEVEDO | 2 | 2 | 0 |
| RODRIGO VIZEU | 1 | 1 | 0 |
| ROSA FERNANDES | 1 | 1 | 0 |
| SALVINO OLIVEIRA | 0 | 0 | 0 |
| TAINÁ DE PAULA | 0 | 0 | 0 |
| TALITA GALHARDO | 2 | 2 | 0 |
| TÂNIA BASTOS | 0 | 0 | 0 |
| TATIANA ROQUE | 0 | 0 | 0 |
| THAIS FERREIRA | 1 | 1 | 0 |
| VERA LINS | 0 | 0 | 0 |
| VITOR HUGO | 0 | 0 | 0 |
| WELINGTON DIAS | 0 | 0 | 0 |
| WILLIAM SIRI | 1 | 0 | 1 |
| WILLIAN COELHO | 0 | 0 | 0 |
| ZICO | 0 | 0 | 0 |

## Atas de outubro: contagem da abertura

| Ata | Declarado | Nomes contados | Situação descrita |
|---|---:|---:|---|
| [Ata da  77ª Sessão ORDINÁRIA ocorrida em 01/10/2026](https://aplicnt.camara.rj.gov.br/APL/Legislativos/atas.nsf/3f8037c08c436684032577040057cb8c/8b290699f2d40e7503258e87005b9f9b?OpenDocument) | 1 | 1 | Não haveria sessão |
| [Ata da  78ª Sessão ORDINÁRIA ocorrida em 06/10/2026](https://aplicnt.camara.rj.gov.br/APL/Legislativos/atas.nsf/3f8037c08c436684032577040057cb8c/39d7ed48091e579f03258e8900591666?OpenDocument) | 12 | 12 | Sessão aberta |
| [Ata da  79ª Sessão ORDINÁRIA ocorrida em 07/10/2026](https://aplicnt.camara.rj.gov.br/APL/Legislativos/atas.nsf/3f8037c08c436684032577040057cb8c/4b7bd7f37eac83c103258e8a00479d7b?OpenDocument) | 2 | 2 | Não haveria sessão |
| [Ata da  37ª Sessão EXTRAORDINÁRIA ocorrida em 07/10/2026](https://aplicnt.camara.rj.gov.br/APL/Legislativos/atas.nsf/3f8037c08c436684032577040057cb8c/3eb67613bcc3b39b03258e8a0047b260?OpenDocument) | 44 | 44 | Sessão aberta |
| [Ata da  80ª Sessão ORDINÁRIA ocorrida em 08/10/2026](https://aplicnt.camara.rj.gov.br/APL/Legislativos/atas.nsf/3f8037c08c436684032577040057cb8c/32a0aae107db110103258e8f005863a2?OpenDocument) | 1 | 1 | Não haveria sessão |
| [Ata da  81ª Sessão ORDINÁRIA ocorrida em 13/10/2026](https://aplicnt.camara.rj.gov.br/APL/Legislativos/atas.nsf/3f8037c08c436684032577040057cb8c/197c77b94f32717c03258e900057fe6c?OpenDocument) | 9 | 9 | Sessão aberta |
| [Ata da  82ª Sessão ORDINÁRIA ocorrida em 14/10/2026](https://aplicnt.camara.rj.gov.br/APL/Legislativos/atas.nsf/3f8037c08c436684032577040057cb8c/1b93768c1b05f14f03258e910046f4b0?OpenDocument) | 2 | 2 | Não haveria sessão |
| [Ata da  38ª Sessão EXTRAORDINÁRIA ocorrida em 14/10/2026](https://aplicnt.camara.rj.gov.br/APL/Legislativos/atas.nsf/3f8037c08c436684032577040057cb8c/d5d1768afb48504c03258e91004703c2?OpenDocument) | 43 | 43 | Sessão aberta |
| [Ata da  83ª Sessão ORDINÁRIA ocorrida em 15/10/2026](https://aplicnt.camara.rj.gov.br/APL/Legislativos/atas.nsf/3f8037c08c436684032577040057cb8c/622cf08cf528393f03258e92005722b9?OpenDocument) | 1 | 1 | Não haveria sessão |
| [Ata da  84ª Sessão ORDINÁRIA ocorrida em 20/10/2026](https://aplicnt.camara.rj.gov.br/APL/Legislativos/atas.nsf/3f8037c08c436684032577040057cb8c/0d5dfb605bf5a13803258e97005b37c3?OpenDocument) | 12 | 12 | Sessão aberta |
| [Ata da  85ª Sessão ORDINÁRIA ocorrida em 21/10/2026](https://aplicnt.camara.rj.gov.br/APL/Legislativos/atas.nsf/3f8037c08c436684032577040057cb8c/2094ffd6069a22ac03258e98004773f2?OpenDocument) | 3 | 3 | Não haveria sessão |
| [Ata da  39ª Sessão EXTRAORDINÁRIA ocorrida em 21/10/2026](https://aplicnt.camara.rj.gov.br/APL/Legislativos/atas.nsf/3f8037c08c436684032577040057cb8c/11f1c7056817704803258e980047858f?OpenDocument) | 49 | 49 | Sessão aberta |
| [Ata da  86ª Sessão ORDINÁRIA ocorrida em 22/10/2026](https://aplicnt.camara.rj.gov.br/APL/Legislativos/atas.nsf/3f8037c08c436684032577040057cb8c/96f3826cd745d26103258e9d0057eee1?OpenDocument) | 1 | 1 | Não haveria sessão |
| [Ata da  87ª Sessão ORDINÁRIA ocorrida em 27/10/2026](https://aplicnt.camara.rj.gov.br/APL/Legislativos/atas.nsf/3f8037c08c436684032577040057cb8c/37769a05aa45ffac03258e9e0059a52c?OpenDocument) | 16 | 16 | Sessão aberta |
| [Ata da  88ª Sessão ORDINÁRIA ocorrida em 28/10/2026](https://aplicnt.camara.rj.gov.br/APL/Legislativos/atas.nsf/3f8037c08c436684032577040057cb8c/9c0346d188e5619203258e9f004b4cb0?OpenDocument) | 3 | 3 | Não haveria sessão |
| [Ata da  40ª Sessão EXTRAORDINÁRIA ocorrida em 28/10/2026](https://aplicnt.camara.rj.gov.br/APL/Legislativos/atas.nsf/3f8037c08c436684032577040057cb8c/fcf1ef1bdf1fb5cf03258e9f004b711f?OpenDocument) | 45 | 45 | Sessão aberta |
| [Ata da  89ª Sessão ORDINÁRIA ocorrida em 29/10/2026](https://aplicnt.camara.rj.gov.br/APL/Legislativos/atas.nsf/3f8037c08c436684032577040057cb8c/04a197b620c2b42a03258ea40058ee25?OpenDocument) | 17 | 17 | Sessão aberta |
