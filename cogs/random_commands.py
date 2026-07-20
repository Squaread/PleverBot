# mail
import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import platform
import io
import random

from core import state

class random_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
# ==================== Comando img ====================
    @commands.hybrid_command(name="img", description="Pegue uma imagem")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def img(self, ctx, *, search: str):
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
            await ctx.send("Achei nada")

# ==================== Comando quote ====================
    @commands.hybrid_command(name="quote", description="Pegue uma mensagem aleatória de alguém")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def quote(self, ctx, user: discord.Member):
        messages = []
        async for message in ctx.channel.history(limit=300):
            messages.append(message)
        user_messages = [msg.content for msg in messages if msg.author.id == user.id]
        if user_messages:
            random_message = random.choice(user_messages)
            await ctx.send(random_message)
        else:
             await ctx.send(f"Tem nadinha")

# ==================== Comando botinfo ====================
    @commands.hybrid_command(name="bot", description="Informações aleatórias sobre mim")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def botinfo(self, ctx):
        custom_commands_quant = len(state.custom_commands)
        bot_guilds_quant = len(self.bot.guilds)
        bot_ping = round(self.bot.latency * 1000, 2)
        bot_name = self.bot.user.name
        
        embed_bot_info = discord.Embed(title=f"{bot_name}", description=f"**🫂Servidores:** {bot_guilds_quant} \n **🔧Custom commands:** {custom_commands_quant} \n **📶Ping:** {bot_ping}ms  \n\n **<:discordpy:1162698533942595726>Discord.py:** {discord.__version__} \n **<:python:1076971789743292426>Python:** {platform.python_version().split(' ')[0]}\n[Repositório](https://github.com/Squaread/PleverBot)", color=0x844fc4)
        embed_bot_info.set_thumbnail(url=self.bot.user.avatar)
        embed_bot_info.set_footer(text=f"{ctx.author} | {ctx.author.id}")
        
        await ctx.send(embed=embed_bot_info)

# ======================================================================
async def setup(bot: commands.Bot):
    print("[ ✅ ] Cogs random_commands")
    await bot.add_cog(random_commands(bot))
