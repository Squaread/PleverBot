# PleverBot
Bot baseado no CleverBot do iFunny para o Discord, com várias funcionalidades como o makecmd e outras funções.

Não tem nenhuma relação com os desenvolvedores do CleverBot (do iFunny), esse bot apenas tem funções inspiradas nas funcionalidades dele. 

Contém funções que não são comuns nos bots do Discord, entre elas a possibilidade ilimitada dos membros de fazer comandos customizaveis, triggers, jogar garrafas, poll (enquete), etc.

Você pode baixar, editar o quanto quiser e hospedar.

## Comandos/Funcionalidades
* ``;maketrigger input: [trigger] output: [response] exact: [boolean (True or False)]`` - Crie comandos personalizados (com parâmetros)
* ``;makecmd input: [invoker] output: [response]`` - Crie triggers, "o que são triggers?", são certas palavras chaves que o bot consegue detectar no chat e responder a elas
* ``;help`` - Mostra todas as funções e comandos do bot
* ``;deltrigger [trigger]`` - Delete um trigger
* ``;cmd [user]`` - Veja as informações de um comando feito por alguém
* ``;bot`` - Informações gerais do bot
* ``;block [user_id]`` - Adicionar um usuário a blacklist
* ``;unblock [user_id]`` - Remover um usuário da blacklist
* ``img [search]`` - Pesquise uma imagem na internet
* ``quote [user]`` - Pega uma mensagem aleatório de um determinado membro num canal (últimas 300 mensagens, dá pra mudar porém não recomendo por conta do rate limit)
* ``;setchannel [module] [channel_id]`` - Configure um módulo a um canal (bottle, mail)
* ``;bottle [message]`` - Enviar uma mensagem para um outro servidor completamente aleatório [REQUER setchannel]
* ``;mail [user] [message]`` - Envie uma mensagem anônima direcionada a alguém num canal [REQUER setchannel]
* ``;poll [title]: [options]`` - Crie uma enquete com até 10 opções, os membros podem votar anonimamente
* ``;vote [number]`` - Vote numa enquete
---
Você deve mexer no arquivo de configuração (config.py) antes de executar o código, as instruções se encontram lá.

### Dependências
Discord.py [2.3.2] - ``pip install discord.py``

Requests [2.31.0] - ``pip install requests``

Beautifulsoup4 [4.12.2] - ``pip install beautifulsoup4``

bs4 [0.0.1] - ``pip install bs4``

> Bot foi programado no ambiente do Python 3.12.3, mas é esperado que funcione normalmente em versões posteriores (teoricamente)

## Como usar

1.  Vá em code e download zip.
2. Clique em extrair tudo.
3. Instale as dependências.
4. Pegue o token do seu bot e bote no config.py
5. Você deve ativar todas as intents do bot no DEVELOPER PORTAL do Discord (PRESENCE INTENT, SERVER MEMBERS INTENT e MESSAGE CONTENT INTENT) para funcionar perfeitamente, [Discord Applications](https://discord.com/developers/applications).
- Esse bot foi feito para um grupo seleto de comunidades, você pode hospedar sua própria versão dele, mas saiba que a moderação é extremamente básica baseada em logs e blacklist, então é melhor configurar um canal de log no config.py e não o manter 100% público.

![kkkk imagem falhou](https://images7.memedroid.com/images/UPLOADED866/5fb051be3b4b0.jpeg)


