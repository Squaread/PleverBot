# bottle
import discord
from discord.ext import commands, tasks
import json
import random

from config import bot_log_channel
from config import bottle_interval

from functions import Load_ServersData

servers_data = {}

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
     try:
      with open('servers_data.json', 'r', encoding='utf-8') as f:
            servers_data = json.load(f)
      
      for guild_id, config in servers_data["servers"].items():
         if config["bottle"]["enabled"]:
      
               guild = self.bot.get_guild(int(guild_id))

               if not bottles == {}:
                     try:
                        channel = await self.bot.fetch_channel(config["bottle"]["channel_id"])
                     except:
                        channel = False
                     if channel:
                           chosen_bottle = random.choice(list(bottles.values()))
                           bottle_origin_id = int(list(bottles.keys())[list(bottles.values()).index(chosen_bottle)])
                           try:
                              bottle_origin =  self.bot.get_guild(bottle_origin_id)
                           except:
                              bottle_origin = False
                           
                           if bottle_origin:
                                 if bottle_origin_id != guild.id:
                                       embed_bottle = discord.Embed(title="🌊 | A bottle appeared 😱", description=chosen_bottle, color=0x6CA9F8)
                                       embed_bottle.set_footer(icon_url=bottle_origin.icon, text=f"{bottle_origin.name} | {bottle_origin.id}")
                                       await channel.send(embed=embed_bottle)

                                       for key, value in bottles.items():
                                          if value == chosen_bottle:
                                             bottles.pop(key)
                                             break
                                 else:
                                    # Mesmo servidor do autor original | Same server as the original author - CANCELED
                                    pass
                           else:
                              # Erro ao pegar server de origem | Error when getting origin server - CANCELED
                              pass

                     else:
                        # Falha ao pegar canal | Failed to get channel - CANCELED
                        pass
               else:
                  # Não há garrafas disponiveis | No bottles available 
                  pass
     except:
      print("[BOTTLE] FATAL ERROR")

    # ==================== Comando bottle | Bottle command ====================
    @commands.command(name="bottle")
    @commands.cooldown(1, 3600, commands.BucketType.guild) # Aqui você pode mudar o cooldown | Here you can change the cooldown - Default: 3600 (seconds)
    async def bottle(self, ctx, *,mensagem: str):
    
        with open('servers_data.json', 'r', encoding='utf-8') as f:
         servers_data = json.load(f)

        server_data = servers_data["servers"][str(ctx.guild.id)]
        status_bottle = server_data["bottle"]["enabled"]
        
        if status_bottle == False:
           await ctx.send("**bottle** está desativado - ``;help``")
           return
        
        channelId_bottle = server_data["bottle"]["channel_id"]
        channel_bottle = self.bot.get_channel(channelId_bottle)
        if not channel_bottle:
            await ctx.send("**❌ |** Esse servidor precisa ter um canal configurado para receber bottles antes de poder enviar uma - ``;help``.")
            return

        # Enviar log | Send log
        log_channel = self.bot.get_channel(bot_log_channel) 
        embed_log = discord.Embed(title="New bottle", description=f"**Message:** ``{mensagem}`` \n\n **Creator:** ``{ctx.author}`` | ``{ctx.author.id}`` \n **Server:** ``{ctx.guild}`` | ``{ctx.guild.id}``", color=0x1abc9c)
        await log_channel.send(embed=embed_log)

        # Enviar bottle | Send bottle
        bottles[ctx.guild.id] = mensagem
        await ctx.send(f"Garrafa lançada ao mar 🌊🌊\n``{mensagem}``")

# ======================================================================
async def setup(bot: commands.Bot):
    print("[ ✅ ] Cogs bottle")
    await bot.add_cog(bottle(bot))
