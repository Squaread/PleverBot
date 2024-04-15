# PleverBot
Bot baseado no CleverBot do iFunny para o Discord, com várias funcionalidades como o famoso "makecmd" e outras funções.

Não tenho nenhuma relação com os desenvolvedores do CleverBot (do iFunny), esse código apenas tem funções inspiradas nas funcionalidades dele, Fan-Made. 

Contém funções que não são comuns nos bots do Discord, entre elas a possibilidade de fazer comandos customizaveis, triggers, jogar garrafas, poll (enquete), etc.

## Comandos/Funcionalidades
* ``;maketrigger input: [trigger] output: [response] exact: [boolean (True or False)]`` - Crie comandos personalizados (com parâmetros)
* ``;makecmd input: [invoker] output: [response]`` - Crie triggerss, "o que são triggers?", são certas palavras chaves que o bot consegue detectar no chat e enviar uma resposta pra elas [REQUER PERMISSÃO ESPECIAL (manage_guild)]
* ``;help`` - Mostra todas as funções e comandos do bot
* ``;deltrigger [trigger]`` - Delete um trigger [REQUER PERMISSÃO ESPECIAL (manage_guild)]
* ``;cmd [user]`` - Veja as informações de um comando feito por alguém
* ``;botinfo`` - Informações gerais do bot
* ``;block [user_id]`` - Adicionar um usuário a blacklist
* ``img [search]`` - Pesquise uma imagem na internet
* ``quote [user]`` - Pega uma mensagem aleatório de um determinado membro num canal (últimas 300 mensagens, dá pra mudar porém não recomendo por conta do rate limit)
* ``;bottle [message]`` - Enviar uma mensagem para um outro servidor completamente aleatório [REQUER ATIVAÇÃO]
* ``;mail [user] [message]`` - Envie uma mensagem anônimo direcionada a alguém num canal [REQUER ATIVAÇÃO]
* ``;poll [title]: [options]`` - Crie uma enquente com até 10 opções, os membros podem votar anonimamente [REQUER ATIVAÇÃO]
* ``vote [number]`` - Vote numa enquete [REQUER ATIVAÇÃO]
---
**Módulos** 

Os módulos são funcionalidades que você pode ativar ou desativar separadamente (``;bottle``, ``;mail``, ``poll``)
* ``;setchannel [module_code] [channel_id`` - Ver a configuração dos módulos no servidor
* ``;enable [module_code]`` - Ativar um módulo
* ``;disable [module_code]`` - Desativar um módulo

A programação é bastante comentada, para que você possa modificar do jeito que quiser. Porém você ainda precisa do conhecimento básico para manipular, sem isso você nem vai conseguir executar.

Você deve mexer no arquivo de configuração (config.py) antes de executar o código, as instruções se encontram lá.

### Dependências
Discord.py [2.3.2] - ``pip install discord.py``

Requests [2.31.0] - ``pip install requests``

Beautifulsoup4 [4.12.2] - ``pip install beautifulsoup4``

bs4 [0.0.1] - ``pip install bs4``

## Avisos

- Use como um bot fechado, pois ele pode ser facilmente abusado.
- Você deve ativar todas as intents do bot (PRESENCE INTENT, SERVER MEMBERS INTENT e MESSAGE CONTENT INTENT) para funcionar perfeitamente, [Discord Applications](https://discord.com/developers/applications).
- O código NÃO possui um sistema de moderação automática nos comandos, então qualquer pessoa pode encher ele de porcarias. Por isso existe o sistema de logs, toda entrada é mostrada, qualquer coisa adicione o usuário a blacklist. Isso é de sua responsabilidade.
- A única forma de ver o criador de comandos anônimos é por meio do registro das logs.
- O código NÃO foi feito com a intenção de se tornar algo sério, então espere algumas gambiarras ali e aqui.
- Mais uma vez falando, esse projeto não tem nenhum ligamento com o CleverBot, considere isso como uma Fan-Made.

> Projeto livre, faça o que quiser com o código. Se encontrar algum bug, por favor me avise ;]

![kkkk imagem falhou](https://images7.memedroid.com/images/UPLOADED866/5fb051be3b4b0.jpeg)


