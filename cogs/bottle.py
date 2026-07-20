import discord
from discord.ext import commands, tasks
import random

from config import bot_prefix
from config import bottle_interval

from core import state
from utils.logs import logger

class bottle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    global bottles
    bottles = {}

    @commands.Cog.listener()
    async def on_ready(self):
       self.bottleSystem.start()

    # BOTTLE SYSTEM 
    @tasks.loop(minutes=bottle_interval)
    async def bottleSystem(self):
      servers_data = state.servers_data

      guilds = list(servers_data["servers"].items()) # pegar todos os servers
      random.shuffle(guilds) # embaralhar servers

      for guild_id, config in guilds: # listar cada server
         if config["bottle"]["channel_id"]: # se ha canal configurado
      
               guild = self.bot.get_guild(int(guild_id))

               if not bottles == {}: # se a lista de garrafas nao for vazia
                     try:
                        channel = await self.bot.fetch_channel(config["bottle"]["channel_id"])
                     except:
                        channel = False
                     if channel: # se o server de destino tem um canal valido
                           chosen_bottle = random.choice(list(bottles.values()))
                           bottle_origin_id = int(list(bottles.keys())[list(bottles.values()).index(chosen_bottle)])
                           try:
                              bottle_origin = self.bot.get_guild(bottle_origin_id)
                           except:
                              bottle_origin = False
                           
                           if bottle_origin:
                                 if bottle_origin_id != guild.id:
                                       embed_bottle = discord.Embed(title="🌊 | Uma garrafa apareceu 😱", description=chosen_bottle, color=0x6CA9F8)
                                       embed_bottle.set_footer(icon_url=bottle_origin.icon, text=f"{bottle_origin.name} | {bottle_origin.id}")
                                       await channel.send(embed=embed_bottle)

                                       for key, value in bottles.items():
                                          if value == chosen_bottle:
                                             bottles.pop(key)
                                             break
                                 else:
                                    # Mesmo servidor do autor original
                                    pass
                           else:
                              # Erro ao pegar server de origem
                              pass

                     else:
                        # Falha ao pegar canal
                        pass
               else:
                  # Não há garrafas disponiveis
                  pass

    # ==================== Comando bottle ====================
    @commands.command(name="bottle")
    @commands.cooldown(1, 3600, commands.BucketType.guild) # Cooldown default 3600 segundos
    async def bottle(self, ctx, *,mensagem: str):

        server_data = state.servers_data["servers"][str(ctx.guild.id)]
        
        channelId_bottle = server_data["bottle"]["channel_id"]
        channel_bottle = self.bot.get_channel(channelId_bottle)
        if not channel_bottle:
            await ctx.send(f"Faça `{bot_prefix}setchannel bottle <channel_id>` para receber garrafas de outros servidores")
        
        # Enviar bottle
        bottles[ctx.guild.id] = mensagem
        # Enviar log
        await logger(self.bot, "Novo bottle", f"**Mensagem:** `{mensagem}` \n\n **Criador:** `{ctx.author}` | `{ctx.author.id}` \n **Server:** `{ctx.guild}` | `{ctx.guild.id}`", 0x1abc9c)
        # Responder
        await ctx.send(f"Garrafa lançada ao mar 🌊🌊\n`{mensagem}`")

# ======================================================================
async def setup(bot: commands.Bot):
    print("[ ✅ ] Cogs bottle")
    await bot.add_cog(bottle(bot))
