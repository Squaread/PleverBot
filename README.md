# PleverBot
Bot baseado no CleverBot do iFunny para o Discord, com várias funcionalidades como o famoso "makecmd" e outras funções.

Não tenho nenhuma relação com os desenvolvedores do CleverBot (do iFunny), esse código apenas tem funções inspiradas nas funcionalidades dele, Fan-Made. 

Contém um monte de funções que não são comuns nos bots do Discordd, entre elas a possibilidade de fazer comandos customizaveis, triggers, jogar garrafas, etc.

## Comandos/Funcionalidades
* ``;makecmd`` - Crie comandos personalizados (com parâmetros)
* ``;maketrigger`` - Crie triggerss, "o que são triggers?", são certas palavras chaves que o bot consegue detectar no chat e enviar uma resposta pra elas [REQUER PERMISSÃO ESPECIAL (manage_guild)]
* ``;sync2`` - Sicronize slashs commands manualmente [EXCLUSIVO PRO DONO]
* ``;ajuda`` - Mostra todas as funções e comandos do bot
* ``;deltrigger`` - Delete um trigger [REQUER PERMISSÃO ESPECIAL (manage_guild)]
* ``;cmd`` - Veja as informações de um comando feito por alguém
* ``;botinfo`` - Informações gerais do seu bot
* ``;block`` - Adicionar um usuário a blacklist
* ``;update`` - Mostra a última atualização do bot, praticamente um update log
* ``;bottle`` - Enviar uma mensagem para um outro servidor completamente aleatório [REQUER ATIVAÇÃO]
* ``;correio`` - Envie uma mensagem anônimo direcionada a alguém num canal [REQUER ATIVAÇÃO]
---
**Módulos** 

Os módulos são funcionalidades que você pode ativar ou desativar separadamente (``;bottle``, ``;correio``)
* ``;config`` - Ver a configuração dos módulos no servidor
* ``;ativar`` - Ativar um módulo
* ``;desativar`` - Desativar um módulo

A programação é bastante comentada, para que você possa modificar do jeito que quiser.

Você deve mexer no arquivo de configuração (config.py) antes de executar o código, as instruções se encontram lá.

### Dependências
Discord.py [2.3.2] - ``pip install discord.py``

Pytz [2023.3] - ``pip install pytz``

## Avisos

- Pela primeira vez rodado o código vai retornar um alerta no módulo bottle, isso é normal, já que ainda não possui nenhum servidor guardado nos arquivos. Além que você deve rodar o código ANTES de adicionar o bot a um servidor.
- O código NÃO possui um sistema de moderação nos comandos, então qualquer pessoa pode encher ele de porcaria. Por isso existe o sistema de logs, toda entrada é mostrada, qualquer coisa adicione o usuário a blacklist. Isso é de sua responsabilidade.
- A única forma de ver o criador de uma mensagem anônima é por meio do registro das logs.
- O código NÃO foi feito com a intenção de se tornar algo sério, então espere algumas gambiarras ali e aqui.
- Mais uma vez falando, esse projeto não tem nenhum ligamento com o CleverBot, considere isso como uma Fan-Made.

> Projeto livre, faça o que quiser com o código. Se encontrar algum bug, por favor me avise ;]

![kkkk imagem falhou](https://images7.memedroid.com/images/UPLOADED866/5fb051be3b4b0.jpeg)


