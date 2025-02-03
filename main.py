import discord
from discord.ext import commands
import json
import random
import os
import re
import io
import asyncio
import platform
from discord.ui import Button, View
import json
from bs4 import BeautifulSoup
import requests

# Importar configurações | Import config
from config import TOKEN
from config import bot_prefix
from config import bot_log_channel

from functions import Load_CustomCommands
from functions import Load_ServersData
from functions import Load_Triggers
from functions import Load_Blacklist

from functions import UpCustomCommand
from functions import UpServerData
from functions import UpTrigger
from functions import UpBlacklist

# ===== Carregar dados / Load data =====
servers_data = Load_ServersData()
custom_commands = Load_CustomCommands()
ban_users = Load_Blacklist()

# ============================================================ Bot ============================================================
bot = commands.Bot(command_prefix =bot_prefix, intents=discord.Intents.all())

# Primeiras ações | First actions
@bot.event
async def on_ready():
    print(f"Bot online {bot.user}")
    try:
     await bot.tree.sync()
     print("✅ | Synchronized Commands")
    except Exception as e:
     print(e)

     # Detectar se falta algum servidor no servers_data.json | Detect missing servers in servers_data.json 
    for guild in bot.guilds:
        guild_id = str(guild.id)

        if guild_id not in servers_data["servers"]:
            # Adicionar o servidor ao servers_data | Add the server to servers_data
            servers_data["servers"][guild_id] = {
                "bottle": {
                    "enabled": False,
                    "channel_id": None
                },
                "mail": {
                    "enabled": False,
                    "channel_id": None
                }, 
                "poll": {
                    "enabled": False
                }
            }

    # Atualizara dados servers_data.json | Update data servers_data.json
    UpServerData(servers_data)

    # Modificar status do bot, por exemplo, fazer aparecer que ele tá jogando um jogo | Modify the bot's status, for example, make it appear that it is playing a game
    async def change_activity():
         while True:
          await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Carlinhos Simulator"), status=discord.Status.idle)
          await asyncio.sleep(340) 
          await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="iFunny 2"), status=discord.Status.idle)
          await asyncio.sleep(340) 
          await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Shrek 7"), status=discord.Status.idle)
          await asyncio.sleep(340) 
          await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="You"), status=discord.Status.idle)
          await asyncio.sleep(340) 
          await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="O"), status=discord.Status.idle)
          await asyncio.sleep(340) 
          await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="👁👁"), status=discord.Status.idle)
          await asyncio.sleep(340) 
          await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Furry Love 2"), status=discord.Status.idle)
          await asyncio.sleep(340) 
    bot.loop.create_task(change_activity())
     
# Remover o comando padrão help | Remove the default help command 
bot.remove_command('help')

# ==================== Adicionar um servidor novo a base de dados | Add a new server to the database ====================
@bot.event
async def on_guild_join(guild):
   servers_data["servers"][str(guild.id)] = {
        "bottle": {
            "enabled": False,
            "channel_id": None
        },
        "mail": {
            "enabled": False,
            "channel_id": None
        }
    }
   
   UpServerData(servers_data)

   log_channel = await bot.fetch_channel(bot_log_channel)
   embed_new_guild = discord.Embed(title="New guild", description=f"**Server:** ``{guild.name}`` | ``{guild.id}`` \n **Owner:** ``{guild.owner}`` | ``{guild.owner.id}`` \n **Members:** ``{guild.member_count}``", color=0x1f8b4c)
   await log_channel.send(embed=embed_new_guild)

# ========================= Tratamento de erros | Error handling =========================
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound): # Command not found
        pass
    elif isinstance(error, commands.CommandOnCooldown): # Cooldown
      await ctx.send(f"**⌛ |** Cooldown ``{error.retry_after:.2f} segundos``.")
    elif isinstance(error, commands.MissingRequiredArgument): # Falta de parametro |Missing parameter
        await ctx.send(f"**❌ |** Parameter error, veja ``;help``.")
    elif isinstance(error, commands.MissingPermissions): # Membro sem permissão | Member without permission
        await ctx.send(f"**❌ |** You do not have permission ``" + "".join(error.missing_permissions) + "``.")
    elif (hasattr(error, 'original')): 
            original_error = error.original
            if isinstance(original_error, discord.Forbidden) and '50013' in str(original_error):  
                    try: await ctx.send("**❌ |** Eu não tenho permissões o suficiente para fazer essa ação.")
                    except: pass
    else: # Desconhecido
        print(f"FATAL ERROR -> {error}")
        try: await ctx.send(error)
        except: pass

# ==================== Detectar mensagens enviadas no chat | Detect messages sent in chat ====================
@bot.event
async def on_message(message):
    # Verificar se o usuario é um bot ou está na blacklist | Check if the user is a bot or blacklisted
    if message.author.bot or message.guild is None or str(message.author.id) in ban_users:
        return
    
    message_content = message.content
    
    # Caso a mensagem contém um comando padrão do bot | If the message contains a standard bot command
    try:
     if message_content.split()[0].replace(bot_prefix, '') in bot.all_commands: 
       await bot.process_commands(message)
       return
    except:
        pass

    # Se na mensagem contém o prefixo do bot | If the message contains the bot prefix
    if message_content.startswith(bot_prefix):
        parts = message_content.split()

        # MAKECMD RESPONSE SYSTEM
        for i in parts:
            for key, value in custom_commands.items():
             if i in key:      
              response = value['output']
        
              key_split = key.split()
             
              if not "%arg" in response and message_content != key: 
                  pass
              
              elif parts[:len(key_split)] == key_split:
                    argument = message_content.replace(key, '').strip()
                    
                    # Se há parametros | If there are parameters
                    try:
                        get_member = argument.replace('<@', '').replace('>', '')
                        getting_member = discord.utils.get(bot.get_all_members(), id=int(get_member))
                        argument = getting_member.display_name
                    except:
                        pass

                    if argument != '':
                     response = response.replace('%arg', f'{argument}')

                    response = response.replace('%author', f'{message.author.display_name}')
              
                    for i in range(response.count('%random')):
                            response = re.sub(r'%random(\d+)', lambda x: str(random.randint(1, int(x.group(1)))), response)
                
                    response = response.replace('%randomMember', f'{str(random.choice(message.guild.members).display_name)}')
                    
                    # Enviar resposta | Send reply
                    await message.channel.send(response)
                    return
              else:
                  pass
              
    # Verificar se é um trigger | Check if it is a trigger 
    else:
     triggers = Load_Triggers()
     guild_id = str(message.guild.id)
     if guild_id in triggers:
        for key, value in triggers[guild_id].items():
            if value["exact"] and key.lower() == message_content:
                await message.channel.send(value["output"])
                break
            elif not value["exact"] and key.lower() in message_content:
                await message.channel.send(value["output"])
                break
    
    await bot.process_commands(message)    

# ==================== Sistema de Logs | Logs System ====================
async def sendLog(title, description, color):
    if bot_log_channel == 0: # Nenhum canal especificado | No channel specified
        return
    log_channel = bot.get_channel(bot_log_channel)
    embed_log = discord.Embed(title=title, description=description, color=color)
    try:
        await log_channel.send(embed=embed_log) # Enviar log | Send log
    except: # Caso ID invalido | Invalid ID case
        print("[LOGS SYSTEM] Error when sending message, check that the ID is correct and that the bot has permission on the channel.")
   
# == PT-BR ==================== Comando de ajuda | Help command ==================== PT-BR ==
@bot.command(aliases=['ajuda'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def help(ctx):

 embed_mainPage = discord.Embed(title="Ajuda - Comandos Gerais", description="Os comandos são por prefixo e alguns poucos por slash, muitos são somente prefixo para evitar poluição. Todo comando com slash também é prefixo, mas nem todo de prefixo é slash\n\n- **;help** ``Explicação dos comandos e funções.``\n- **;bottle [message]** ``Envie uma mensagem para um servidor aleatório.``\n- **;mail [user] [message]** ``Envie uma mensagem anônima para alguém num canal do servidor.``\n- **;img [search]** ``Pesquise imagens pela internet.``\n- **;quote [user]** ``Pega uma mensagem aleatório de um determinado membro num canal (últimas 300 mensagens).``\n- **/botinfo** ``Informações gerais do bot.``\n- **;poll [title]: [options]** ``Faça enquetes de até 10 opções, exemplo: ;poll Melhor comida: Arroz e feijão, Pizza, Batata Frita, Hamburguer``\n- **;vote [number]** ``Vote em enquentes pelo número da opção correspondente.``", color=0x7289da)
 embed_mainPage.set_thumbnail(url=bot.user.avatar)
 embed_mainPage.set_footer(text=f"{ctx.author} | {ctx.author.id}")

 # categoria comandos gerais
 button_mainPage = Button(label="Geral", style=discord.ButtonStyle.green)
 async def button_mainPage_callback(interaction):
    await interaction.response.edit_message(embed=embed_mainPage)
 button_mainPage.callback = button_mainPage_callback

 # categoria módulos & funções
 button_modulePage = Button(label="Módulos", style=discord.ButtonStyle.green)
 async def button_modulePage_callback(interaction):
    
    embed_modulePage = discord.Embed(title="Ajuda - Módulos & Funções", description="Os módulos e funções são adicionais que podem ser ativados ou desativados.\n- **;enable [module_code]** ``Ativar um módulo.``\n- **;disable [module_code]** ``Desativar um módulo.``\n- **;setchannel [module_code] [channel_id]** ``Configurar um módulo a um canal.``", color=0xe91e63)
    embed_modulePage.add_field(name="Correio anônimo", value="Envio de cartas anônimas num canal especificado.\nCódigo: ``mail``\nComandos: ``;mail``")
    embed_modulePage.add_field(name="Bottle", value="Permite enviar e receber cartas de outros servidores num canal especificado.\nCódigo: ``bottle``\nComandos: ``;bottle``")
    embed_modulePage.add_field(name="Poll", value="Crie enquentes de até 10 opções, onde os membros poderão votar de forma anônima (não tem que ser configurado a um canal).\nCódigo: ``poll``\nComandos: ``;poll`` & ``;vote``")
    embed_modulePage.set_thumbnail(url=bot.user.avatar)
    embed_modulePage.set_footer(text=f"{ctx.author} | {ctx.author.id}")

    await interaction.response.edit_message(embed=embed_modulePage)
 button_modulePage.callback = button_modulePage_callback

 # categoria trigger & makecmd
 button_triggerMakecmdPage = Button(label="Trigger & makecmd", style=discord.ButtonStyle.green)
 async def button_triggerMakecmdPage_callback(interaction):
    
    embed_triggerMakecmdPage = discord.Embed(title="Ajuda - Trigger & Makecmd", color=0xe91e63)
    embed_triggerMakecmdPage.add_field(name="Trigger", value="- ``;maketrigger input: [trigger] output: [response] exact: [boolean (True or False)]``\n\n Cria um gatilho de texto que faz o bot enviar uma mensagem pré-definida. Se ``exact`` for False, ele será ativado mesmo se o gatilho estiver junto de outras palavras.", inline=False)
    embed_triggerMakecmdPage.add_field(name="Makecmd", value=f"- ``;makecmd input: [invoker] output: [response]``\n\n Parâmetros\n``%arg`` Obter o primeiro argumento após o invoker.\n``%author`` Pegar quem acionou o comando.\n``%random[number]`` Número aleatório de 1 até onde você limitou, exemplo: %random15 = 1 até 15.\n``%randomMember`` Pegar um membro aleatório.\n\n Exemplos:\n``;makecmd input: cavalos output: %author bebeu %random7 litros de água de cavalo``\n``;makecmd input: carlinhos output: %arg é %random100% carlinhos``\n\n ⛔ Evite colocar espaço nos invokers, tipo ``;make input: cavalos carlinhos output: vdd``. Pode acontecer comportamentos inesperados.", inline=False)
    embed_triggerMakecmdPage.set_thumbnail(url=bot.user.avatar)
    embed_triggerMakecmdPage.set_footer(text=f"{ctx.author} | {ctx.author.id}")

    await interaction.response.edit_message(embed=embed_triggerMakecmdPage)
 button_triggerMakecmdPage.callback = button_triggerMakecmdPage_callback

 # categoria regras
 button_rulesPage = Button(label="📚 | Diretrizes", style=discord.ButtonStyle.red)
 async def button_rulesPage_callback(interaction):
    
    embed_rulesPage = discord.Embed(title="Os 7 Mandamentos Sagrados", description="Regras... Quem é que gosta de regras? Bem, elas existem, engole o choro e faz o L \n\n - 1º Não usarás o bot para fins maliciosos, ilegais ou que vão contra às [Diretrizes da Comunidade](https://discord.com/guidelines). \n- 2º Não burlarás blacklist por meio de contas alternativas. \n- 3º Não enviarás conteúdo criminoso, >exageradamente< violento ou sexual nos Triggers e Comandos Customizáveis. \n- 4º Não enviarás nenhum tipo de propaganda/divulgação nos Comandos Customizáveis. \n- 5º Nunca forçarás o celeron do bot com comandos ou ações repetitivas com intuito de derrubar/prejudicar (coisa de bobão). \n\n Esses são alguns exemplos de regras. \n **Código open source -** [GitHub](https://www.github.com/Squaread/PleverBot)", color=0x992d22)
    embed_rulesPage.set_thumbnail(url="https://media.discordapp.net/attachments/1021215486979088475/1201201999258063050/25551989_376542819462618_7976604231910069571_n.png")
    embed_rulesPage.set_footer(text=f"{ctx.author} | {ctx.author.id}")

    await interaction.response.edit_message(embed=embed_rulesPage)
 button_rulesPage.callback = button_rulesPage_callback

 # Apagar menu | Delete menu
 button_delete = Button(label="✖", style=discord.ButtonStyle.gray)
 async def button_delete_callback(interaction):
     await msg.delete()
 button_delete.callback = button_delete_callback

 view = View()
 view.add_item(button_mainPage)
 view.add_item(button_modulePage)
 view.add_item(button_triggerMakecmdPage)
 view.add_item(button_rulesPage)
 view.add_item(button_delete)
 msg = await ctx.send(embed=embed_mainPage, view=view)

# ==================== Comando makecmd | Makecmd command ====================
@bot.command(name="makecmd")
@commands.cooldown(1, 2, commands.BucketType.user)
async def makecmd(ctx, *, cmd):
    parts = cmd.split("output:", 1)
    if len(parts) != 2:
        await ctx.send(f"``;makecmd input [invoker] output: [response]``")
        return

    input_part, output_part = parts
    get_input = input_part.replace("input:", "").strip()
    input_text = bot_prefix + get_input
    output_text = output_part.strip()

    if get_input in bot.all_commands:
        await ctx.send(f"**❌ |** ``{input_text}`` já é um comando nativo do bot 🤓☝️")
        return
    
    # Armazenar o comando customizado com o ID do autor | # Save the custom command with the author ID
    custom_commands[input_text] = {
        'output': output_text,
        'author_id': str(ctx.author.id)
    }
    
    UpCustomCommand(custom_commands)

    # Enviar mensagem confirmando o novo comando | Send message confirming the new command
    embed_new_cmd = discord.Embed(title="New command", description=f"**Input:** ``{input_text}`` \n **Output:** ``{output_text}``", color=0x0c6940)
    embed_new_cmd.set_footer(text=f"{ctx.author} | {ctx.author.id}")
    await ctx.channel.send(embed=embed_new_cmd)
    
    # Enviar log | Send log
    await sendLog("New command", f"**Input:** ``{input_text}`` \n **Output:** ``{output_text}`` \n\n **Criador:** ``{ctx.author}`` | ``{ctx.author.id}`` \n **Server:** ``{ctx.guild}`` | ``{ctx.guild.id}``", 0x1abc9c)

# ==================== Comando maketrigger | Maketrigger command ====================
@bot.command(name="maketrigger")
@commands.has_permissions(manage_guild = True)
@commands.cooldown(1, 2, commands.BucketType.user)
async def maketrigger(ctx, *, trigger):
    parts = trigger.split("output:", 1)
    if trigger.startswith(bot_prefix):
        await ctx.send(f"**❌ |** O ``invoker`` não pode conter o prefixo do bot.")
        return

    if len(parts) != 2:
        await ctx.send("``;maketrigger input: <invoker> output: <response> exact: <boolean (True ou False)>``")
        return

    input_part, remaining_part = parts
    exact_parts = remaining_part.split("exact:", 1)

    if len(exact_parts) != 2:
        await ctx.send("``;maketrigger input: <invoker> output: <response> exact: <boolean (True ou False)>``")
        return

    output_part, exact_part = exact_parts
    input_text = input_part.replace("input:", "").strip()
    output_text = output_part.strip()
    exact_text = exact_part.strip().lower()

    guild_id = str(ctx.guild.id)
    author_id = str(ctx.author.id)

    exact_value = exact_text == "true"

    # Atualizar o JSON com a nova trigger
    UpTrigger(guild_id, input_text, output_text, exact_value, author_id)

    await ctx.send(f"**✅ |** Trigger criado: `{input_text}` → `{output_text}`")

# ==================== Comando deltrigger | Deltrigger command ====================
@bot.command(name="deltrigger")
@commands.has_permissions(manage_guild = True)
@commands.cooldown(1, 2, commands.BucketType.user)
async def deltrigger(ctx, *, trigger):
    json_path = os.path.join('triggers', f'{ctx.guild.id}.json')
    if os.path.exists(json_path):
        
        with open(json_path, 'r', encoding='utf-8') as file:
            data_triggers = json.load(file)

        if trigger in data_triggers:
            del data_triggers[trigger]
            
            with open(json_path, 'w', encoding='utf-8') as file:
                json.dump(data_triggers, file, ensure_ascii=False ,indent=4)
            await ctx.send(f'✅ | ``{trigger}`` deleted')
        else:
            await ctx.send(f'Não encontrado.')
    else:
        await ctx.send(f'Fatal error.')
    
# ==================== Comando cmd | Cmd command ====================
@bot.command(name="cmd")
@commands.cooldown(1, 2, commands.BucketType.user)
async def cmd(ctx, *, command_name):
    command_name = ";" + command_name
   
    if command_name in custom_commands:
        command_data = custom_commands[command_name]
        author_id = command_data.get('author_id', 'Unknown')
        response_cmd = command_data.get('output', 'Unknown')

        try: author_cmd = await bot.fetch_user(int(author_id))
        except discord.errors.NotFound: author_cmd = 'Unknown'
 
        embed_cmdinfo = discord.Embed(title=command_name, description=f"**Criador:** ``{author_cmd}`` | ``{author_cmd.id}`` \n **Output:** ``{response_cmd}``", color=0x897ec2)
        await ctx.send(embed=embed_cmdinfo)
    else:
        await ctx.send("Não encontrado.")

# ==================== Comando botinfo | Botinfo command ====================
@bot.hybrid_command(name="botinfo")
@commands.cooldown(1, 3, commands.BucketType.user)
async def botinfo(ctx):
   custom_commands_quant = len(custom_commands)
   bot_guilds_quant = len(bot.guilds)
   bot_ping = round(bot.latency * 1000, 2)
   bot_name = bot.user.name
   
   embed_bot_info = discord.Embed(title=f"{bot_name}", description=f"**<:servers:1077559867906195576>Servers:** {bot_guilds_quant} \n **<:tool:1076982009550872656>Custom commands:** {custom_commands_quant} \n **<:latency:1076964520506949642>Ping:** {bot_ping}ms  \n\n **<:discordpy:1162698533942595726>Discord.py:** {discord.__version__} \n **<:python:1076971789743292426>Python:** {platform.python_version().split(' ')[0]}", color=0x844fc4)
   embed_bot_info.set_thumbnail(url=bot.user.avatar)
   embed_bot_info.set_footer(text=f"{ctx.author} | {ctx.author.id}")
   
   await ctx.send(embed=embed_bot_info)
   
# ==================== Comando block (blacklist) | Block command (blacklist) ====================
@bot.command(name="block")
@commands.is_owner()
async def block(ctx, id: str, *, reason: str=None):
   global ban_users
   target = await bot.fetch_user(id)
   if reason == None:
      reason = "Idk" # Motivo padrão | Default reason

      ban_users[id] = True
      UpBlacklist(ban_users)

   embed_ban = discord.Embed(title="Blacklist", description=f"``{target}`` foi adicionado na blacklist 😈 \n **Reason:** {reason}", color=0x992d22)
   embed_ban.set_footer(text=f"{ctx.author} | {ctx.author.id}")
   await ctx.send(embed=embed_ban)

   # Enviar log | Send log
   await sendLog("Blacklist", f"`{target}`` foi adicionado na blacklist 😈 \n **Reason:** {reason}", 0x992d22)
 
# ==================== Comando ativar | Ativar command ====================
@bot.command(aliases=['ativar'])
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.has_permissions(manage_guild=True)
async def enable(ctx, module: str):
    modules = ["mail", "bottle", "poll"]
    if not module in modules:
        await ctx.send(f"**❌ |** Eita, parece que ``{module}`` não existe!")
        return
    
    servers_data["servers"][str(ctx.guild.id)][module]["enabled"] = True
    UpServerData(servers_data)

    if module != "poll":
        await ctx.send(f"**:white_check_mark: |** ``{module}`` foi ativado! Não se esqueça de configurar o canal ``;setchannel {module} [channel_id]``.")
    else:
        await ctx.send(f"``{module}`` foi ativado!")

# ==================== Comando desativar | Desativar command ====================
@bot.command(aliases=['desativar'])
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.has_permissions(manage_guild=True)
async def disable(ctx, module: str):
    modules = ["mail", "bottle", "poll"]
    if not module in modules:
        await ctx.send(f"**❌ |** Eita, parece que ``{module}`` não existe!")
        return
    
    servers_data["servers"][str(ctx.guild.id)][module]["enabled"] = False
    UpServerData(servers_data)

    await ctx.send(f"``{module}`` foi desativado.")
        
# ==================== Comando config | Config command ====================
@bot.command(name="setchannel")
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.has_permissions(manage_guild=True)
async def setchannel(ctx, module: str, channel_id: str):
    modules = ["mail", "bottle"]
    if not module in modules:
        await ctx.send(f"**❌ |** Eita, parece que ``{module}`` não é válido!")
        return
    
    try: await bot.fetch_channel(channel_id)
    except: return await ctx.send(f"**❌ |** Eu não tenho permissão nesse canal ou ele não existe ~~~assim como seu pai.~~")

    servers_data["servers"][str(ctx.guild.id)][module]["channel_id"] = int(channel_id) 
    UpServerData(servers_data)

    await ctx.send(f"**{module}** foi configurado para ``{channel_id}``")
    
# ==================== Comando img | Img command ====================
@bot.command(name="img")
@commands.cooldown(1, 3, commands.BucketType.user)
async def img(ctx, *, search: str):
    url = f"https://www.bing.com/images/search?q={search}"
    search_response = requests.get(url)
    soup = BeautifulSoup(search_response.content, "html.parser")

    img_tag = soup.find("img", class_="mimg")
    if img_tag:
        image_url = img_tag["src"]
        image_response = requests.get(image_url)

        if image_response.ok:
            image_bytes = io.BytesIO(image_response.content)  
            file = discord.File(image_bytes, filename="image.png") 
            await ctx.send(file=file)
        else:
            await ctx.send("**❌ |** Erro ao procurar.")
    else:
        await ctx.send("Nada encontrado.")

# ==================== Comando quote | Quote command ====================
@bot.command(name="quote")
@commands.cooldown(1, 3, commands.BucketType.user)
async def quote(ctx, user: discord.Member):
    messages = []
    async for message in ctx.channel.history(limit=300):
        messages.append(message)
    
    user_messages = [msg.content for msg in messages if msg.author.id == user.id]

    if user_messages:
        random_message = random.choice(user_messages)
        await ctx.send(random_message)
    else:
        await ctx.send(f"Nadinha, assim como o sentido da vida. 🤖")

# ==================== Carregar cogs | Load cogs ====================
async def load_cogs():
    print("[ 💠 ] Loading cogs")
    initial_extensions = ['modules.mail', 'modules.bottle', 'modules.poll']
    for extension in initial_extensions:
        await bot.load_extension(extension)

async def main():
    await load_cogs()

asyncio.run(main())
    
# -- RUN --
bot.run(TOKEN) 