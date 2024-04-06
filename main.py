import discord
from discord.ext import commands
import json
import random
import os
import re
import asyncio
import platform
from discord.ui import Button, View

import pytz
import json
from datetime import datetime

# Importar configurações | Import config
from config import TOKEN
from config import bot_prefix
from config import bot_log_channel

# Fuso horario | Time zone
start_time = datetime.utcnow()
# Custom commands cache
custom_commands = {}

time_zone_utc3 = pytz.timezone('America/Sao_Paulo') # Time zone, change to your region (optional), example: America/New_York

# Carregar comandos customizados | Load custom commands
try:
    with open('custom.json', 'r', encoding='utf-8') as json_file:
        try:
         custom_commands = json.load(json_file)
        except:
           custom_commands = {}
        
        print("\n [ ✅ ] Custom commands loaded \n")
        
except FileNotFoundError:
    custom_commands = {}
    print("\n [ ❌ ] FileNotFoundError - Custom commands \n")

# Carregar blacklist | Load blacklist
with open('ban.json', 'r') as ban_file:
    ban_users = json.load(ban_file)
with open('servers_data.json', 'r', encoding='utf-8') as f:
    servers_data = json.load(f)

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
     print (e)

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
   
   with open('servers_data.json', 'w') as file:
        json.dump(servers_data, file, indent=2)

   log_channel = await bot.fetch_channel(bot_log_channel)
   embed_new_guild = discord.Embed(title="New guild", description=f"**Server:** ``{guild.name}`` | ``{guild.id}`` \n **Owner:** ``{guild.owner}`` | ``{guild.owner.id}`` \n **Members:** ``{guild.member_count}``", color=0x1f8b4c)
   await log_channel.send(embed=embed_new_guild)

# ==================== Atualizar dados dos servidores no json | Update server data in json ====================
def upServerData():
    with open('servers_data.json', 'w') as file:
        json.dump(servers_data, file, indent=2)

# ==================== Ignorar a mensagem CommandNotFound (alerta inutil e evita spam no console) | Ignore the CommandNotFound message (useless alert and avoids console spam) ====================
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass

# ==================== Detectar mensagens enviadas no chat | Detect messages sent in chat ====================
@bot.event
async def on_message(message):
    # Verificar se o usuario está na blacklist | Check if the user is on the blacklist
    if message.author.bot or message.guild is None or str(message.author.id) in ban_users:
        return
    
    message_content = message.content
    json_path = os.path.join('triggers', f'{message.guild.id}.json')
    
    # Caso a mensagem conter um comando padrão do bot | If the message contains a standard bot command
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
              print(message_content, " | ", key, " ", response)
        
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

                    if argument == '':
                        pass

                    else:
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
    elif os.path.exists(json_path):
     with open(json_path, 'r',  encoding='utf-8') as file:
      data_triggers = json.load(file)
      for key, value in data_triggers.items():
            if value["exact"] and key.lower() == message_content.lower():
                output = value["output"]
                await message.channel.send(output)
                break
            elif not value["exact"] and key.lower() in message_content.lower():
                output = value["output"]
                await message.channel.send(output)
                break
    
    await bot.process_commands(message)    

# ==================== Sicronizar comandos slash manualmente | Manually sync slash commands ====================
@bot.command()
@commands.is_owner() 
async def sync2(ctx,guild=None):
    
    if guild == None:
        await bot.tree.sync()
    else:
        await bot.tree.sync(guild=discord.Object(id=int(guild)))
    await ctx.send("Sicronizado")
@sync2.error
async def sync_error():
   pass
   
# ==================== Comando de ajuda | Help command ====================
@bot.hybrid_command(name="ajuda", description="Tutorial")
@commands.cooldown(1, 5, commands.BucketType.user)
async def ajuda(ctx):

 embed_mainPage = discord.Embed(title="Ajuda - Comandos Gerais", description="Muitos comandos são por prefixo e slash, alguns são somente prefixo para evitar poluição. Todo comando com slash também é prefixo, mas nem todo de prefixo é slash\n\n- **/ajuda** ``Explicação dos comandos e funções``\n- **/reagir [message_id] [emoji]** ``Bot reagir a uma mensagem``\n- **/bottle [message]** ``Envie uma mensagem para um servidor aleatório``\n- **/correio [user] [message]** ``Envie uma mensagem anônima para alguém num canal do servidor``\n- **/mesclar [word1] [word2]** ``Mescle 2 palavras diferentes``\n- **/update** ``Ver mudanças na versão mais recente do bot``", color=0x7289da)
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
    
    embed_modulePage = discord.Embed(title="Ajuda - Módulos & Funções", description="Os módulos e funções são adicionais que podem ser ativados ou desativados\n- **;ativar [module_code]** ``Ativar um módulo``\n- **;desativar [module_code]** ``Desativar um módulo``\n- **;config [module_code] [channel_id]** ``Configurar um módulo a um canal``", color=0xe91e63)
    embed_modulePage.add_field(name="Correio anônimo", value="Envio de cartas anônimas num canal especificado\nCódigo: ``mail``\nComandos: ``/correio``")
    embed_modulePage.add_field(name="Bottle", value="Permite enviar e receber cartas de outros servidores num canal especificado\nCódigo: ``bottle``\nComandos: ``/bottle``")
    embed_modulePage.set_thumbnail(url=bot.user.avatar)
    embed_modulePage.set_footer(text=f"{ctx.author} | {ctx.author.id}")

    await interaction.response.edit_message(embed=embed_modulePage)
 button_modulePage.callback = button_modulePage_callback

 # categoria trigger & makecmd
 button_triggerMakecmdPage = Button(label="Trigger & makecmd", style=discord.ButtonStyle.green)
 async def button_triggerMakecmdPage_callback(interaction):
    
    embed_triggerMakecmdPage = discord.Embed(title="Ajuda - Trigger & Makecmd", color=0xe91e63)
    embed_triggerMakecmdPage.add_field(name="Trigger", value="- ``;maketrigger input: [trigger] output: [response] exact: [boolean (True or False)]``\n\n Cria um gatilho de texto que faz o bot enviar uma mensagem pré-definida. Se ``exact`` for False, ele será ativado mesmo se o gatilho estiver junto de outras palavras", inline=False)
    embed_triggerMakecmdPage.add_field(name="Makecmd", value=f"- ``;makecmd input: [invoker] output: [response]``\n\n Parâmetros\n``%arg`` Obter o primeiro argumento após o invoker\n``%author`` Pegar quem acionou o comando\n``%random[number]`` Número aleatório de 1 até onde você limitou, exemplo: %random15 = 1 até 15\n``%randomMember`` Pegar um membro aleatório\n\n Exemplos:\n``;makecmd input: cavalos output: %author bebeu %random7 litros de água de cavalo``\n``;makecmd input: carlinhos output: %arg é %random100% carlinhos``\n\n ⛔ Evite colocar espaço nos invokers, tipo ``;make input: cavalos carlinhos output: vdd``. Pode acontecer comportamentos inesperados, será corrigido futuramente", inline=False)
    embed_triggerMakecmdPage.set_thumbnail(url=bot.user.avatar)
    embed_triggerMakecmdPage.set_footer(text=f"{ctx.author} | {ctx.author.id}")

    await interaction.response.edit_message(embed=embed_triggerMakecmdPage)
 button_triggerMakecmdPage.callback = button_triggerMakecmdPage_callback

 # categoria regras
 button_rulesPage = Button(label="📚 | Diretrizes", style=discord.ButtonStyle.red)
 async def button_rulesPage_callback(interaction):
    
    embed_rulesPage = discord.Embed(title="Os 7 Mandamentos Sagrados", description="Regras... Quem é que gosta de regras? Bem, elas existem, engole o choro e faz o L \n\n - 1º Não usarás o bot para fins maliciosos, ilegais ou que vão contra às [Diretrizes da Comunidade](https://discord.com/guidelines). \n- 2º Não usarás contas alternativas para obter benefícios, vantagens ou ganhos no bot (isso se aplica somente ao sistema de economia). \n- 3º Não burlarás banimento por meio de contas alternativas. \n- 4º Não enviarás conteúdo criminoso, >exageradamente< violento ou sexual nos Triggers e Comandos Customizáveis. \n- 5º Não enviarás nenhum tipo de propaganda/divulgação nos Comandos Customizáveis. \n- 6º Nunca forçarás o celeron do bot com comandos ou ações repetitivas com intuito de derrubar/prejudicar (coisa de bobão). \n- 7º Jamais compartilharás ou abusarás de uma falha no bot. Lembre-se, vacilão não dura muito.\n\n Última modificação: 28/01/2024", color=0x992d22)
    embed_rulesPage.set_thumbnail(url="https://media.discordapp.net/attachments/1021215486979088475/1201201999258063050/25551989_376542819462618_7976604231910069571_n.png")
    embed_rulesPage.set_footer(text=f"{ctx.author} | {ctx.author.id}")

    await interaction.response.edit_message(embed=embed_rulesPage)
 button_rulesPage.callback = button_rulesPage_callback

 view = View()
 view.add_item(button_mainPage)
 view.add_item(button_modulePage)
 view.add_item(button_triggerMakecmdPage)
 view.add_item(button_rulesPage)
 msg = await ctx.send(embed=embed_mainPage, view=view)

# Tratamento de erros do comando [ajuda] | # Command error handling [help]
@ajuda.error
async def ajuda_error(ctx, error):
   print("error ", error)
   if isinstance(error, commands.CommandOnCooldown):
       await ctx.send(f"Quer explodir meu celeron baka?! - tente novamente em **{error.retry_after:.2f}** segundos**", ephemeral=True)

# ==================== Comando makecmd | Makecmd command ====================
@bot.command(name="makecmd")
@commands.cooldown(1, 2, commands.BucketType.user)
async def makecmd(ctx, *, cmd):
    if str(ctx.author.id) in ban_users:
        return

    parts = cmd.split("output:", 1)
    if len(parts) != 2:
        await ctx.send(f'É assim que se faz, seu bobão - ``;makecmd input [invoker] output: [response]')
        return

    input_part, output_part = parts
    get_input = input_part.replace("input:", "").strip()
    input_text = bot_prefix + get_input
    output_text = output_part.strip()

    if get_input in bot.all_commands:
        await ctx.send(f'O comando ``{input_text}`` já é um comando nativo do bot 🤓☝️')
        return
    
    # Armazenar o comando customizado com o ID do autor | # Save the custom command with the author ID
    custom_commands[input_text] = {
        'output': output_text,
        'author_id': str(ctx.author.id)
    }
    
    # Salvar no json | Save in json
    with open('custom.json', 'w', encoding='utf-8') as json_file:
        json.dump(custom_commands, json_file, ensure_ascii=False, indent=4)

    # Enviar mensagem confirmando o novo comando | Send message confirming the new command
    embed_new_cmd = discord.Embed(title="Novo Comando", description=f"**Input:** ``{input_text}`` \n **Output:** ``{output_text}``", color=0x0c6940)
    embed_new_cmd.set_footer(text=f"{ctx.author} | {ctx.author.id}")
    await ctx.channel.send(embed=embed_new_cmd)
    
    # Enviar log | Send log
    log_channel = bot.get_channel(bot_log_channel)
    embed_log = discord.Embed(title="Novo Comando", description=f"**Input:** ``{input_text}`` \n **Output:** ``{output_text}`` \n\n **Criador:** ``{ctx.author}`` | ``{ctx.author.id}`` \n **Server:** ``{ctx.guild}`` | ``{ctx.guild.id}``", color=0x1abc9c)
    await log_channel.send(embed=embed_log)

# Tratamento de erros do comando [makecmd] | # Command error handling [makecmd]
@makecmd.error
async def makecmd_error(ctx, error):
   if isinstance(error, commands.CommandOnCooldown):
       await ctx.send(f"Quer explodir meu celeron baka?! - tente novamente em **{error.retry_after:.2f} segundos**", ephemeral=True)
   elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('É assim que se faz, seu bobão - ``;makecmd output: [invoker] output: [response]``')

# ==================== Comando maketrigger | Maketrigger command ====================
@bot.command(name="maketrigger")
@commands.has_permissions(manage_guild = True)
@commands.cooldown(1, 2, commands.BucketType.user)
async def maketrigger(ctx, *, trigger):
   if str(ctx.author.id) in ban_users:
        return
   
   parts = trigger.split("output:", 1)
   if trigger.startswith(bot_prefix):
           await ctx.send(f'❌ | O ``input`` não pode começar com o prefixo do bot 🙄')
   
   if len(parts) != 2:
        await ctx.send('É assim que se faz, seu bobão - ``;maketrigger input: <invoker> output: <response> exact: <boolean (True ou False)>``')
        return
   
   input_part, remaining_part = parts
   exact_parts = remaining_part.split("exact:", 1)
   
   if len(exact_parts) != 2:
        await ctx.send('É assim que se faz, seu bobão - ``;maketrigger input: <invoker> output: <response> exact: <boolean (True ou False)>``')
        return

   output_part, exact_part = exact_parts
   input_text = input_part.replace("input:", "").strip()
   output_text = output_part.strip()
   exact_text = exact_part.strip().lower()

   guild_id = ctx.guild.id
   author_id = ctx.author.id

   if exact_text == 'false':
      exact_text = False

   # Salvar o novo trigger | Save the new trigger
   new_trigger = {
    input_text: {
        "output": output_text,
        "exact": bool(exact_text),
        "guild_id": str(guild_id),
        "author_id": str(author_id)
     }
   }
   json_path = os.path.join('triggers', f'{guild_id}.json')
   
   if os.path.exists(json_path):
    with open(json_path, 'r',  encoding='utf-8') as file:
      data_triggers = json.load(file)
   else:
      data_triggers = new_trigger

   data_triggers.update(new_trigger)
   # Salvar no json | Save in json
   with open(json_path, 'w', encoding='utf-8') as f:
     json.dump(data_triggers, f, ensure_ascii=False, indent=4)

   # Enviar mensagem confirmando o novo trigger | Send message confirming the new trigger
   embed_new_trigger = discord.Embed(title="Trigger criado", description=f"**Input:** ``{input_text}`` \n **Output:** ``{output_text}`` \n **Exact:** ``{str(exact_text).lower()}``", color=0x0c6940)
   embed_new_trigger.set_footer(text=f"{ctx.author} | {ctx.author.id}")
   await ctx.channel.send(embed=embed_new_trigger)

   # Enviar log | Send log
   log_channel = bot.get_channel(bot_log_channel)
   embed_log = discord.Embed(title="Trigger criado", description=f"**Input:** ``{input_text}`` \n **Output:** ``{output_text}`` \n **Exact:** ``{str(exact_text).lower()}`` \n\n **Criador:** ``{ctx.author}`` | ``{ctx.author.id}`` \n **Server:** ``{ctx.guild}`` | ``{ctx.guild.id}``", color=0x489cbd)
   await log_channel.send(embed=embed_log)

# Tratamento de erros do comando [maketrigger] | # Command error handling [maketrigger]
@maketrigger.error
async def maketrigger_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
       await ctx.send(f"Quer explodir meu celeron baka?! - tente novamente em {error.retry_after:.2f} segundos")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f"Você não tem a permissão ``Gerenciar Servidor`` 🤭") 
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('É assim que se faz, seu bobão - ``;maketrigger input: <invoker> output: <response> exact: <boolean (True ou False)>``')

# ==================== Comando deltrigger | Deltrigger command ====================
@bot.hybrid_command(name="deltrigger", description="[MOD] Deletar um trigger")
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
            await ctx.send(f'Not found')
    else:
        await ctx.send(f'Not found')

# Tratamento de erros do comando [deltrigger] | # Command error handling [deltrigger]
@deltrigger.error
async def deltrigger_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
       await ctx.send(f"Quer explodir meu celeron baka?! - tente novamente em **{error.retry_after:.2f} segundos**", ephemeral=True)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f"Você não tem a permissão ``Gerenciar Servidor`` 🤭") 
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"É assim que se faz, seu bobão - ``;deltrigger [trigger]") 

          
# ==================== Comando cmd | Cmd command ====================
@bot.hybrid_command(name="cmd", description="Veja as informações de um comando feito por alguém")
async def cmd(ctx, *, command_name):
    command_name = ";" + command_name
    print(command_name)
    if command_name in custom_commands:
        command_data = custom_commands[command_name]
        author_id = command_data.get('author_id', 'Unknown')
        response_cmd = command_data.get('output', 'Unknown')


        try:
            author_cmd = await bot.fetch_user(int(author_id))
        except discord.errors.NotFound:
            author_cmd = 'Unknown'
 
        embed_cmdinfo = discord.Embed(title=command_name, description=f"**Criador:** ``{author_cmd}`` | ``{author_cmd.id}`` \n **Output:** ``{response_cmd}``", color=0x897ec2)
        await ctx.send(embed=embed_cmdinfo)
    else:
        await ctx.send('Not found')

# ==================== Comando botinfo | Botinfo command ====================
@bot.hybrid_command(name="botinfo", description="Minhas informações 😏")
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

# Tratamento de erros do comando [botinfo] | # Command error handling [botinfo]
@botinfo.error
async def botinfo_error(ctx, error):
   if isinstance(error, commands.CommandOnCooldown):
       await ctx.send(f"Quer explodir meu celeron baka?! - tente novamente em **{error.retry_after:.2f} segundos**", ephemeral=True)
       return
   
# ==================== Comando block (blacklist) | Block command (blacklist) ====================
@bot.command(name="block")
@commands.is_owner()
async def block(ctx, id: str, *, reason: str=None):
   target_id = int(id)
   target = await bot.fetch_user(id)
   if reason == None:
      reason = "Meia noite te conto (nenhum motivo definido)"

      with open('ban.json', 'r') as ban_file:
        ban_users = json.load(ban_file)
      ban_users[id] = True
      
      with open('ban.json', 'w') as ban_file:
        json.dump(ban_users, ban_file)
   
   embed_ban = discord.Embed(title="Blacklist", description=f"``{target}`` foi adicionado a lista negra 😈 \n **Motivo:** {reason}", color=0x992d22)
   embed_ban.set_footer(text=f"{ctx.author} | {ctx.author.id}")
   await ctx.send(embed=embed_ban)

   # Enviar log | Send log
   log_channel = bot.get_channel(bot_log_channel)
   await log_channel.send(embed=embed_ban)

# Tratamento de erros do comando [block] | # Command error handling [block]
@block.error
async def block_error(ctx):
   pass
 
# ==================== Comando update | Update command ====================
@bot.hybrid_command(name="update", description="Veja a atualização mais recente do bot")
@commands.cooldown(1, 2, commands.BucketType.user)
async def update(ctx):
    embed_update = discord.Embed(title="Atualização mais Recente v0.7", description="Bugs no makecmd resolvidos\n **19/02/2024**", color=0x7289da)
    embed_update.set_footer(text=f"{ctx.author} | {ctx.author.id}")
    await ctx.send(embed=embed_update)

# Tratamento de erros do comando [update] | # Command error handling [update]
@update.error
async def update_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
       await ctx.send(f"Quer explodir meu celeron baka?! - tente novamente em **{error.retry_after:.2f} segundos**", ephemeral=True)

# ==================== Comando ativar | Ativar command ====================
@bot.command(name="ativar")
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.has_permissions(manage_guild=True)
async def ativar(ctx, module: str):
    modules = ["mail", "bottle"]
    if not module in modules:
        await ctx.send("Código do módulo incorreto 😡")
        return
    
    if module == "mail":
        servers_data["servers"][str(ctx.guild.id)]["mail"]["enabled"] = True
    elif module == "bottle":
        servers_data["servers"][str(ctx.guild.id)]["bottle"]["enabled"] = True    
    upServerData()
    await ctx.send(f"``{module}`` foi ativado. Não esqueça de configurar usando ;config\nhttps://media.discordapp.net/attachments/1021215486979088475/1201541071168098344/image.png")

# Tratamento de erros do comando [ativar] | # Command error handling [ativar]
@ativar.error
async def ativar_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Quer explodir meu celeron baka?! - tente novamente em **{error.retry_after:.2f} segundos**", ephemeral=True)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"É assim que se faz, seu bobão - ``;ativar [module_code]``")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f"Você não tem a permissão ``Gerenciar Servidor`` 🤭") 

# ==================== Comando desativar | Desativar command ====================
@bot.command(name="desativar")
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.has_permissions(manage_guild=True)
async def desativar(ctx, module: str):
    modules = ["mail", "bottle"]
    if not module in modules:
        await ctx.send("Código do módulo incorreto 😡")
        return
    
    if module == "mail":
        servers_data["servers"][str(ctx.guild.id)]["mail"]["enabled"] = False
    elif module == "bottle":
        servers_data["servers"][str(ctx.guild.id)]["bottle"]["enabled"] = False    
    upServerData()
    await ctx.send(f"``{module}`` foi desativado")

# Tratamento de erros do comando [desativar] | # Command error handling [desativar]
@desativar.error
async def desativar_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Quer explodir meu celeron baka?! - tente novamente em **{error.retry_after:.2f} segundos**", ephemeral=True)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"É assim que se faz, seu bobão - ``;desativar [module_code]``")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f"Você não tem a permissão ``Gerenciar Servidor`` 🤭") 
        
# ==================== Comando config | Config command ====================
@bot.command(name="config")
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.has_permissions(manage_guild=True)
async def config(ctx, module: str, channel_id: str):
    modules = ["mail", "bottle"]
    if not module in modules:
        await ctx.send("Código do módulo incorreto 😡")
        return
    channel = await bot.fetch_channel(channel_id)
    if not channel:
        await ctx.send("Não tenho permissões pra ver ou o canal não existe 😰", ephemeral=True)
        return
    
    if module == "mail":
        servers_data["servers"][str(ctx.guild.id)]["mail"]["channel_id"] = int(channel_id)
    elif module == "bottle":
        servers_data["servers"][str(ctx.guild.id)]["bottle"]["channel_id"] = int(channel_id)    
    upServerData()
    await ctx.send(f"**{module}** foi configurado para ``{channel_id}``")

# Tratamento de erros do comando [config] | # Command error handling [config]
@config.error
async def config_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Quer explodir meu celeron baka?! - tente novamente em **{error.retry_after:.2f} segundos**", ephemeral=True)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"É assim que se faz, seu bobão - ``;config [module_code] [channel_id]``")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f"Você não tem a permissão ``Gerenciar Servidor`` 🤭") 
    else:
        await ctx.send("Não tenho permissões pra ver ou o canal não existe 😰", ephemeral=True)
    


# ==================== Carregar cogs | Load cogs ====================
async def load_cogs():
    print("[ 💠 ] Loading cogs")
    initial_extensions = ['modules.mail', 'modules.bottle']
    for extension in initial_extensions:
        await bot.load_extension(extension)

async def main():
    await load_cogs()

asyncio.run(main())
    
# -- RUN --
bot.run(TOKEN) 

