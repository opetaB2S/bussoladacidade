# Atualização diária da Bússola da Cidade

Repositório previsto: https://github.com/opetab2s/bussoladacidade

O fluxo `.github/workflows/atualizar.yml` está preparado para rodar às **03:37 do Rio (06:37 UTC)**, por envio à branch `main` ou manualmente em Actions. O GitHub pode atrasar execuções agendadas. O site é exportado para HTML para o GitHub Pages; o arquivo PHP continua disponível como fonte, mas Pages não executa PHP.

## Estado da entrega

Projeto enviado ao GitHub. A agenda está registrada no workflow. As primeiras execuções nos servidores Linux e Windows do GitHub falharam por timeout/conexão encerrada pela Câmara, mantendo a publicação bloqueada. Está sendo testado o ambiente macOS. Localmente, a cadeia TLS foi completada com o intermediário da Sectigo, verificado contra as raízes do certifi; a coleta nova retornou 51 vereadores, 62.271 documentos, 17 votações e 497 votos e passou pela validação dos dados. Ainda falta comprovar a publicação e a rotina completa no GitHub.

A base inicial é armazenada comprimida em `.baseline/snapshot.part*`, com SHA-256 conferido antes da extração. Não é reutilizada como resposta de coleta; serve de comparação e fornece os recursos visuais. Os scripts e o modelo PHP ficam legíveis no repositório; `web/` contém os ajustes de interface.

## Garantias implementadas

- Toda coleta começa numa pasta temporária nova, sem reaproveitar páginas antigas.
- Não modifica `dist/`, que contém a versão inicial usada como base.
- Nas próximas execuções, recupera a base do artefato da última execução em que coleta **e publicação** terminaram com sucesso. Uma execução cuja publicação falhou não vira a nova base. Se esse artefato tiver expirado ou não puder ser recuperado, bloqueia.
- Exige cadastro completo de 51 vereadores com os mesmos identificadores. Mudanças de composição exigem revisão humana.
- Exige dez tipos de documentos, paginação concluída, nenhum documento anterior desaparecido, aumento máximo de 15% por execução e alteração de no máximo 2% (ou dez) documentos anteriores.
- Bloqueia novos documentos sem resumo. Os oito resumos já ausentes na base original permanecem identificados como não informados; não se inventa o texto.
- Confere grupos, fontes oficiais, fotos, autores identificados, codificação, contas de faltas e abonos, ausência de redução nas tabelas mensais já disponíveis, votos duplicados ou sem nome confirmado e perda de votações do mesmo mês. Novas inconsistências nas votações bloqueiam; a pendência já documentada continua excluída.
- Os votos coletados cobrem o mês corrente até a coleta, com esse limite exibido. Não constituem todo o mandato. Não calcula presença efetiva.
- Falha de conexão, certificado, interpretação, contagem, geração ou recuperação encerra a execução sem executar o trabalho de publicação. O GitHub Pages conserva o último deploy bem-sucedido.
- Logs e relatório ficam nos artefatos da execução por 30 dias; a última versão boa, por 90 dias, renovados por cada execução bem-sucedida. É uma rotina automática sujeita à disponibilidade do GitHub e da Câmara, não uma garantia absoluta de qualidade dos dados da fonte.

## Ativação e verificação pendentes

Após autenticação: enviar `main`; configurar Settings → Pages → Source → GitHub Actions; rodar o workflow; conferir os trabalhos `coletar` e `publicar` e o endereço retornado por `deploy-pages`. Não considerar ativo antes disso. Não é necessário cadastrar token secreto para a rotina: ela usa o `GITHUB_TOKEN` temporário do próprio workflow com permissões limitadas.

## Executar localmente

Python 3.10+:

```sh
pip install -r requirements.txt
python scripts/test_travas.py
python scripts/atualizar.py
```

Apenas `.candidate/dist/` de uma execução aprovada pode ser publicado. `reports/execucao.json` registra `publicavel: true` somente após gerar e verificar a busca. Isso significa candidato aprovado localmente, não confirmação de deploy; a confirmação é o resultado do trabalho `publicar`.

Se a Câmara corrigir/excluir registros legítimos ou mudar a estrutura do portal, a política conservadora pode bloquear. Revise a fonte e o relatório antes de alterar a base ou as travas; não publique preenchimentos estimados ou zeros artificiais.
