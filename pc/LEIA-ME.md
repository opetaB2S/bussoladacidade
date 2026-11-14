# Coletor no seu PC

Abra **INSTALAR.cmd** nesta pasta, pela sua conta normal do Windows. Deixe a pasta neste local: a tarefa usa o caminho absoluto. Não mova nem apague a pasta depois de instalar. Não é necessário abrir como administrador.

O instalador prepara um Python separado, abre a autenticação oficial do GitHub no navegador (sem tokens no chat), configura GitHub Pages, registra a tarefa diária **BussolaDaCidade - Atualizar** às **03h37 no horário local do Windows** e executa o primeiro teste completo. Neste computador o fuso observado é o de Brasília/Rio. Se o GitHub já estiver autenticado sem permissão de workflows, use `tools\gh.exe auth refresh -h github.com -s workflow` no terminal da sua conta e rode o instalador novamente.

**A tarefa só está instalada quando INSTALAR.cmd terminar essa etapa sem erro.** O primeiro site só estará publicado quando `estado.json` mostrar `publicado: true`, com a URL e a execução do GitHub. Se houver erro, não presuma que a publicação ocorreu.

O PC precisa estar ligado, com internet e com sua sessão do Windows conectada (a tela pode estar bloqueada). A tarefa solicita acordar o PC se o Windows/hardware permitir; não liga um PC desligado. Se perder o horário, tenta quando estiver disponível. Se o computador ficar desligado por vários dias, o site mantém a última versão publicada. A rotina não depende deste chat ficar aberto.

## Como funciona

1. Coleta do zero na Câmara, com validação de HTTPS e sem reaproveitar as respostas anteriores.
2. Compara com a última base aprovada: pessoas, documentos desaparecidos, variação de volume, autoria, grupos, faltas/abonos, votos, fontes e fotos. Os oito resumos já ausentes no índice oficial continuam explicitamente identificados; novos resumos ausentes bloqueiam.
3. Só após aprovação gera o pacote e o manifesto SHA-256 de todos os arquivos.
4. Envia um commit à branch `site-publicado`. Nunca usa envio forçado. O GitHub confere o pacote e publica no Pages, sem coletar na Câmara.
5. Só atualiza a base de comparação local após confirmar o sucesso da publicação daquele commit. Uma cópia da base anterior fica em `ultima-base-anterior/`.

Falhas interrompem a execução e conservam o deploy anterior. Se um envio foi feito mas a publicação falhou, consulte a URL da execução em `estado.json`. O arquivo e os logs registram o resultado. A pasta `publicacao/` contém apenas o pacote destinado ao GitHub, não os HTMLs brutos da coleta, logs locais ou credenciais.

## Acompanhar e parar

- `EXECUTAR-AGORA.cmd`: nova tentativa manual completa.
- `estado.json`: situação da última execução e link do site quando confirmado.
- `logs/`: registro de cada execução; `reports/`: conferência da coleta.
- Agendador de Tarefas do Windows → **BussolaDaCidade - Atualizar**: conferir próxima execução, desabilitar ou excluir a tarefa.

Não compartilhe `.venv/`, `data/`, `logs/` nem credenciais. O GitHub CLI usa a autenticação da sua conta no Windows. O executável incluído foi baixado da distribuição oficial `cli/cli` e seu SHA-256 foi conferido; a origem está em `tools/origem-gh.json`.

Os servidores do GitHub não conseguiram acessar a Câmara nos testes anteriores. Por isso, a coleta passa a ser local, e o GitHub fica responsável apenas pela publicação. A rotina completa nesta conta do Windows ainda depende de você abrir o instalador; o ambiente isolado do assistente não consegue criar a tarefa em seu nome nem autenticar a sua sessão.
