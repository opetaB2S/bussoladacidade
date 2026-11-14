# Bússola da Cidade — Rio de Janeiro

Versão visual inspirada em radarptlandia.org, com a logo Bússola da Cidade fornecida pelo usuário. O PDF fornecido é um guia de criação, não um pacote de código-fonte. A versão foi preparada localmente, sem publicar alterações.

Site PHP com fundo branco e interface para celular. Permite buscar os 51 vereadores atuais, filtrar por partido, consultar faltas mensais, abrir grupos de propostas, buscar assuntos dentro de cada grupo e ler os votos nominais identificados. Não há notas ou ranking. Valores de atividade e cada documento têm links para as fontes oficiais.

## GitHub Pages e atualização diária

O fluxo e o estado de ativação estão em [AUTOMACAO.md](AUTOMACAO.md). `dist/` contém a exportação estática inicial. `index.php` é o modelo utilizado na geração; o GitHub Pages publica HTML e não executa PHP. O pacote PHP independente entregue anteriormente continua disponível separadamente.

Não publique a pasta de coleta nem `.candidate/` inteira: o workflow envia apenas `.candidate/dist/` depois de aprovar a coleta. Execute `pip install -r requirements.txt`, `python scripts/test_travas.py` e `python scripts/atualizar.py` para verificar localmente. Falhas preservam a versão anterior.

## Dados desta versão

Fontes oficiais consultadas em 14/11/2026:

- Cadastro dos 51 vereadores em exercício, com fotos, partidos e contatos públicos.
- Faltas: consultas mensais de janeiro a novembro de 2026. Março, abril, maio, junho, agosto, setembro e outubro têm tabelas. Os demais meses informavam que não havia dados atualizados. Outubro contém os 51 vereadores atuais e é o mês padrão. Não se inferem horas de permanência nem presença em cada sessão.
- 62.271 documentos de 2025 e 2026: 2.771 projetos de lei, 135 projetos de lei complementar, 8 propostas de emenda à Lei Orgânica, 207 projetos de decreto legislativo, 8 projetos de resolução, 12.175 indicações, 42.306 moções, 1.207 requerimentos de informação, 1.564 requerimentos e 1.890 ofícios.
- Votos: 158 documentos de 3 a 11/11/2026, com 17 listas nominais aproveitadas e 497 votos individuais. Uma votação com quantidade declarada diferente do número de nomes foi excluída integralmente. Não representam o histórico completo do mandato.

O conjunto geral inclui documentos do Executivo e de pessoas fora do cadastro atual. Cada perfil mostra somente os documentos ligados ao seu nome. Autoria conjunta aparece nos perfis dos autores identificados; o documento entra uma vez em cada perfil. Não há aproximação de nomes: acentos e maiúsculas são desconsiderados; variantes não confirmadas ficam sem vínculo. Emendas avulsas e pareceres não fazem parte destas consultas de propostas iniciais.

## Regra de classificação — versão 2026-11-14-v1

O agrupamento é calculado por este site, não publicado pela Câmara. A função recebe apenas tipo oficial e ementa; nunca recebe autor, partido ou voto. A primeira regra aplicável define um único grupo:

1. Requerimentos ou ofícios com pedidos de coautoria, correção, republicação, arquivamento, desarquivamento, adiamento, retirada ou inclusão na pauta vão para **Outros**. Não viram uma nova homenagem por citar o título de uma proposta anterior.
2. Indicações que pedem reparo, reposição, revitalização, conservação, manutenção, restauração, limpeza, troca, substituição ou apoio institucional/financeiro vão para **Melhorias nos bairros**, mesmo citando homenagem ou calendário.
3. Ementas com parabéns, congratulações, aplausos, louvor, pesar ou homenagem; concessão de título de cidadão, medalha, menção honrosa ou diploma de mérito; nomes de ruas ou outros espaços públicos; e criação de datas, semanas, meses comemorativos ou inclusão no calendário oficial vão para **Homenagens**, independentemente do tipo. A simples menção a um dia numa política de transporte não satisfaz a regra de data comemorativa.
4. As demais indicações vão para **Melhorias nos bairros**, incluindo pedidos de alcance municipal.
5. Requerimentos de informação e requerimentos, ofícios ou moções com menção explícita a informação, esclarecimento, fiscalização, apuração, investigação, prestação de contas, denúncia ou CPI vão para **Perguntas e cobranças**.
6. Os demais projetos de lei, projetos de lei complementar e propostas de emenda à Lei Orgânica vão para **Propostas de lei**.
7. O restante fica em **Outros**, incluindo apoio/repúdio sem os sinais anteriores e procedimentos internos. Não se presume assunto ausente da ementa.

Distribuição geral: 12.163 em Melhorias nos bairros; 1.275 em Perguntas e cobranças; 42.287 em Homenagens; 2.409 em Propostas de lei; 4.137 em Outros. Não são indicadores de qualidade ou importância. Assuntos mistos seguem a ordem acima. Cada item exibe o motivo e preserva o tipo, a ementa e a fonte originais.

## Coleta e reprodução

Instale `requests` e `beautifulsoup4` e execute:

```
python scripts/coletar.py
python scripts/ampliar_propostas.py
python scripts/reclassificar.py
python scripts/gerar_busca_local.py
python scripts/gerar_previa.py
```

Os períodos de 2025–2026 e de votos de novembro de 2026 são explícitos. Para outro período, adaptar e validar consultas e datas. Os coletores reutilizam o cache de `data/originais/` e `data/propostas_originais/`; para nova consulta à rede, arquive essas pastas antes de executar. Não foi agendada atualização automática.

Os ofícios usam paginação por categoria (`Start=1.1`, `Start=1.1001`, etc.). As demais consultas usam páginas de até mil posições. Há deduplicação por documento. Cinco indicações tinham ano malformado no número do índice; a data oficial de publicação permitiu incluí-las em 2025/2026 sem alterar o número exibido.

`data/propostas_todas.json` conserva todos os documentos classificados, inclusive os sem vínculo atual. O manifesto registra URLs, tamanhos, hashes, cache e validação TLS. As listas públicas são separadas por vereador em `propostas/` e carregadas apenas ao abrir o perfil, para não baixar tudo na entrada pelo celular. Busca e botão de mais registros permitem percorrer a lista inteira.

Neste ambiente a cadeia de certificados dos hosts da Câmara não foi reconhecida; a coleta usou explicitamente `--diagnostico-sem-validar-tls`, registrado no manifesto. O coletor valida TLS por padrão: corrigir a cadeia de confiança antes das atualizações de produção. Os hashes comprovam integridade local, não autenticidade criptográfica do servidor.

## Verificações

Sintaxe PHP e JavaScript; PHP servido por HTTP; testes de nomes de ruas, datas, medalhas, pesar, repúdio, coautoria, manutenção de placa e gratuidade de transporte em dia de eleição; unicidade, partição em um único grupo e conferência das listas e totais dos 51 perfis. No navegador móvel foram testados abertura de grupos, mais itens, busca, motivo e acesso à regra completa. Não foram observados erros de JavaScript.

Os originais e manifestos estão no pacote separado de evidências. Para testes que leem `data/`, descompacte também esse pacote na pasta do projeto.

## Busca por bairro ou rua e repetição de pedidos

A busca usa o texto das 62.271 ementas coletadas; não faz nova consulta à rede e não pesquisa o corpo integral dos documentos. O filtro padrão inclui os 13.438 registros dos grupos Melhorias nos bairros e Perguntas e cobranças. A opção Todos os tipos de registro inclui os demais documentos, sempre identificados pelo tipo e pelo grupo. Menção a um local não confirma, por si só, um pedido de serviço para ele.

Os termos são normalizados sem acentos e maiúsculas; preposições são ignoradas e abreviações usuais de vias são reconhecidas. Há busca pelo começo da última palavra quando não existe uma palavra exata no índice. Para via seguida de primeiro nome, o índice registra também a sequência, evitando que Rua A seja interpretada apenas como uma letra A solta no documento. A busca retorna palavras em resumos, sem geocodificação, validação do endereço em mapa ou confirmação de pertencimento a um bairro oficial. Nomes compostos podem aparecer ao buscar um termo que eles contenham: confira o local na ementa.

O cruzamento final identificou 139 grupos. Só entram indicações classificadas como melhoria, com uma única rua/avenida/estrada/travessa identificada e bairro explicitamente informado na ementa. Os nomes da via e do bairro devem ser iguais após normalização de acentos, maiúsculas e pontuação. Não são corrigidas grafias nem unificados nomes parecidos; bairros diferentes não são fundidos. Sub-bairro sem bairro, cruzamentos, nomes genéricos como Rua A/Rua 1/Rua Cinquenta e Cinco e ambiguidades ficam fora. Comunidades explicitamente diferentes também impedem o agrupamento.

Os tipos de serviço são reconhecidos por termos explícitos. Nomes de via e bairro são retirados antes dessa leitura: Mato em Estrada da Boca do Mato não vira um pedido de roçada. As categorias reúnem serviços relacionados, como asfalto/pavimentação/buracos e drenagem/bueiros/ralos. Não se trata de identidade literal de problemas. Resumos com mais de um serviço podem aparecer em mais de um grupo; a lista de pedidos encontrados não duplica o documento por isso.

Cada grupo exige documentos distintos e pelo menos duas datas de publicação diferentes. Autoria conjunta não multiplica a contagem. As datas são de publicação na Câmara, não de apresentação presumida, execução ou resposta da Prefeitura. Datas não reconhecidas ficam visíveis como indisponíveis na busca e não entram no cruzamento. A contagem de cada grupo cobre a rua e o bairro inteiros, incluindo outros números ou trechos; não é reduzida pelo filtro de busca do usuário.

O aviso visível no site é: **Pedido repetido não prova que a Prefeitura ignorou.** As fontes não confirmam, por si só, execução ou falta de execução do serviço. A ausência de um agrupamento também não prova ausência de pedidos repetidos.

Os índices e documentos são divididos em arquivos pequenos em `busca/` e carregados conforme a pesquisa. O endereço da busca pode ser compartilhado pelos parâmetros `local` e `escopo`. `data/busca_local_resumo.json` registra os critérios e os motivos de exclusão do cruzamento. Execute `python scripts/test_busca_local.py` após regenerar os arquivos para verificar separação de bairros, ambiguidades, acentos, fontes, datas e contagens. O teste inclui um caso real de oito documentos da Rua Barão do Bom Retiro, Engenho Novo, e verifica que a lista bate com a contagem.


## Verificação desta versão visual

PHP sem erros de sintaxe; JavaScript validado; interface conferida em desktop e em 390 px, sem rolagem horizontal. Testados: busca de rua (29 resultados para Rua Barão do Bom Retiro), filtro de vereadores, abertura de grupo no perfil e paginação geral (15 para 35 registros). Os dados não foram alterados pela mudança visual. A auditoria está em `assets/auditoria.md`. Não existe atualização automática configurada. Fontes tipográficas e suas licenças estão em `assets/fonts/`.
