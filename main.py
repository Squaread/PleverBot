import discord
from discord.ext import commands
import random
import re
import asyncio
from discord.ui import Button, View

# Importar config
from config import TOKEN
from config import bot_prefix
from config import bot_log_channel

# Importar variaveis globais cache
from core import state

# Importar funcoes para armazenamento de dados
from data.data_manager import Load_CustomCommands
from data.data_manager import Load_ServersData
from data.data_manager import Load_Triggers
from data.data_manager import Load_Blacklist

from data.data_manager import UpCustomCommand
from data.data_manager import UpServerData
from data.data_manager import UpTrigger
from data.data_manager import UpBlacklist

# ===== Carregar dados ====
state.servers_data = Load_ServersData()
state.custom_commands = Load_CustomCommands()
state.custom_triggers = Load_Triggers()
state.banned_users = Load_Blacklist()

# ============================================================ Bot ============================================================
bot = commands.Bot(command_prefix =bot_prefix, intents=discord.Intents.all())

# Primeiras acoes
@bot.event
async def on_ready():
    print(f"Bot online {bot.user}")
    try:
     await bot.tree.sync()
     print("✅ | Synchronized Commands")
    except Exception as e:
     print(e)

     # Detectar se falta algum servidor no servers_data.json
    for guild in bot.guilds:
        guild_id = str(guild.id)

        if guild_id not in state.servers_data["servers"]:
            state.servers_data["servers"][guild_id] = {
                "bottle": {
                    "channel_id": None
                },
                "mail": {
                    "channel_id": None
                }
            }
    UpServerData(state.servers_data)

    # Modificar as atividades do bot em loop
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
     
# Remover o comando padrão help
bot.remove_command('help')

# ==================== Evento bot adicionado num servidor novo ====================
@bot.event
async def on_guild_join(guild):
   # Salvar na database
   state.servers_data["servers"][str(guild.id)] = {
        "bottle": {
            "channel_id": None
        },
        "mail": {
            "channel_id": None
        }
    }
   UpServerData(state.servers_data)

   log_channel = await bot.fetch_channel(bot_log_channel)
   embed_new_guild = discord.Embed(title="Novo server", description=f"**Server:** `{guild.name}` | `{guild.id}` \n **Owner:** `{guild.owner}` | `{guild.owner.id}` \n **Members:** `{guild.member_count}`", color=0x1f8b4c)
   await log_channel.send(embed=embed_new_guild)

# ========================= Tratamento de erros =========================
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound): # Command not found
        pass
    elif isinstance(error, commands.CommandOnCooldown): # Cooldown
      await ctx.send(f"**⌛ |** Cooldown `{error.retry_after:.2f} segundos`")
    elif isinstance(error, commands.MissingRequiredArgument): # Missing parameter
        await ctx.send(f"**❌ |** Parameter error, veja `{bot_prefix}help`.")
    elif isinstance(error, commands.MissingPermissions): # Member without permission
        await ctx.send(f"**❌ |** Você não tem permissão `" + "".join(error.missing_permissions) + "`.")
    elif (hasattr(error, 'original')): 
            original_error = error.original
            if isinstance(original_error, discord.Forbidden) and '50013' in str(original_error):  
                    try: await ctx.send("**❌ |** Eu não tenho permissões o suficiente para fazer essa ação :(")
                    except: pass
    else: # Desconhecido
        print(f"FATAL ERROR -> {error}")
        try: await ctx.send(error)
        except: pass

# ==================== Detectar mensagens enviadas no chat ====================
@bot.event
async def on_message(message):
    # Verificar se o usuario é um bot ou está na blacklist
    if message.author.bot or message.guild is None or str(message.author.id) in state.banned_users:
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
            for key, value in state.custom_commands.items():
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
     triggers = state.custom_triggers
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
   
# ==================== Comando help ====================
@bot.hybrid_command(name="ajuda", aliases=['help'], description="Helper")
@commands.cooldown(1, 5, commands.BucketType.user)
async def help(ctx):

 embed_mainPage = discord.Embed(title="Ajuda - Comandos Gerais", description=f"- **{bot_prefix}help**\n`Esse painel que você vê.`\n- **{bot_prefix}bottle <message>**\n`Envie uma mensagem para um servidor aleatório. [REQUER setchannel]`\n- **{bot_prefix}mail <@member> <message>**\n`Envie uma mensagem anônima para alguém num canal do servidor. [REQUER setchannel]`\n- **{bot_prefix}setchannel <module_code> <channel_id>**\n`Configure um módulo [bottle, mail] a um canal.` \n- **{bot_prefix}img <search>**\n`Pesquise imagens pela internet.`\n- **{bot_prefix}quote <@member>**\n`Pega uma mensagem aleatório de um determinado membro no canal (últimas 300 mensagens).`\n- **{bot_prefix}botinfo**\n`Informações gerais do bot.`\n- **{bot_prefix}poll <title>: <options>**\n`Faça enquetes de até 10 opções, exemplo: {bot_prefix}poll Melhor comida: Arroz e feijão, Pizza, Batata Frita, Hamburguer`\n- **{bot_prefix}vote <number>**\n`Vote em enquetes pelo número da opção correspondente.`", color=0x7289da)
 embed_mainPage.set_thumbnail(url=bot.user.avatar)
 embed_mainPage.set_footer(text=f"{ctx.author} | {ctx.author.id}")

 # categoria comandos gerais
 button_mainPage = Button(label="Geral", style=discord.ButtonStyle.green)
 async def button_mainPage_callback(interaction):
    await interaction.response.edit_message(embed=embed_mainPage)
 button_mainPage.callback = button_mainPage_callback

 # categoria trigger & makecmd
 button_triggerMakecmdPage = Button(label="Trigger & makecmd", style=discord.ButtonStyle.green)
 async def button_triggerMakecmdPage_callback(interaction):
    
    embed_triggerMakecmdPage = discord.Embed(title="Ajuda - Trigger & Makecmd", color=0xe91e63)
    embed_triggerMakecmdPage.add_field(name="Trigger", value=f"- ``{bot_prefix}maketrigger input: <trigger> output: <response> exact: <boolean (True or False)>``\n\n Cria um gatilho de texto que faz o bot enviar uma mensagem pré-definida. Se ``exact`` for False, ele será ativado mesmo se o gatilho estiver junto de outras palavras.", inline=False)
    embed_triggerMakecmdPage.add_field(name="Makecmd", value=f"- ``{bot_prefix}makecmd input: <invoker> output: <response>``\n\n Parâmetros\n``%arg`` Obter o primeiro argumento após o invoker.\n``%author`` Pegar quem acionou o comando.\n``%random[number]`` Número aleatório de 1 até onde você limitou, exemplo: %random15 = 1 até 15.\n``%randomMember`` Pegar um membro aleatório.\n\n Exemplos:\n``{bot_prefix}makecmd input: cavalos output: %author bebeu %random7 litros de água de cavalo``\n``{bot_prefix}makecmd input: carlinhos output: %arg é %random100% carlinhos``\n\n ⛔ Evite colocar espaço nos invokers, tipo ``{bot_prefix}make input: cavalos carlinhos output: vdd``. Pode acontecer comportamentos inesperados.", inline=False)
    embed_triggerMakecmdPage.set_thumbnail(url=bot.user.avatar)
    embed_triggerMakecmdPage.set_footer(text=f"{ctx.author} | {ctx.author.id}")

    await interaction.response.edit_message(embed=embed_triggerMakecmdPage)
 button_triggerMakecmdPage.callback = button_triggerMakecmdPage_callback

 # Apagar menu
 button_delete = Button(label="✖", style=discord.ButtonStyle.gray)
 async def button_delete_callback(interaction):
     await msg.delete()
 button_delete.callback = button_delete_callback

 view = View()
 view.add_item(button_mainPage)
 view.add_item(button_triggerMakecmdPage)
 view.add_item(button_delete)
 msg = await ctx.send(embed=embed_mainPage, view=view)
   
# ==================== Carregar cogs ====================
async def load_cogs():
    print("\n[ 💠 ] Loading cogs")
    initial_extensions = ['cogs.mail', 'cogs.bottle', 'cogs.poll', 'cogs.random_commands', 'cogs.moderation', 'cogs.bot_admin', 'cogs.custom_commands', 'cogs.custom_triggers']
    for extension in initial_extensions:
        await bot.load_extension(extension)

async def main():
    await load_cogs()

asyncio.run(main())
    
# -- RUN --
bot.run(TOKEN) 