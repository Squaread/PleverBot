# mail
import discord
from discord.ext import commands
import json
from config import bot_log_channel

servers_data = {}

class mail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # ==================== Comando correio | Correio (mail) command ==================== 
    @commands.hybrid_command(name="correio", description="Envie uma mensagem anônima pra alguém num canal")
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def correio(self, ctx, destinatario: discord.Member, *,mensagem: str):
        target = destinatario
    
        with open('servers_data.json', 'r', encoding='utf-8') as f:
         servers_data = json.load(f)

        server_data = servers_data["servers"][str(ctx.guild.id)]
        status_mail = server_data["mail"]["enabled"]
        
        if status_mail == False:
           await ctx.send("**mail** está desativado neste servidor - ``/ajuda``")
           return
        
        
        channelId_mail = server_data["mail"]["channel_id"]
        
        
    
        channel_mail = self.bot.get_channel(channelId_mail)
        if not channel_mail:
            await ctx.send("Não tenho permissões pra ver ou o canal configurado não existe 😰")
            return

        # Enviar log | Send log
        log_channel = self.bot.get_channel(bot_log_channel)
        embed_log = discord.Embed(title="Nova Carta", description=f"**Mensagem:** ``{mensagem}`` \n\n **Criador:** ``{ctx.author}`` | ``{ctx.author.id}`` \n **Server:** ``{ctx.guild}`` | ``{ctx.guild.id}``", color=0x1abc9c)
        await log_channel.send(embed=embed_log)

        # Enviar correio | Send mail
        embed_mail = discord.Embed(title="📧 | Correio anônimo", description=f"Destinatário: {target.mention}\n\n{mensagem}", color=0x9B533B)
        await channel_mail.send(f"{target.mention} você recebeu uma carta 😨",embed=embed_mail)
        await ctx.send("Carta enviada 🥳", ephemeral=True)
    
    # Tratamento de erros do comando [correio] | # Command error handling [correio]
    @correio.error
    async def correio_error(self, ctx, error):
       if isinstance(error, commands.CommandOnCooldown):
         await ctx.send(f"Agora tem q esperar **{error.retry_after:.2f} segundos** pra enviar outra carta 🤣😂", ephemeral=True)
       elif isinstance(error, commands.MissingRequiredArgument):
          await ctx.send(f"É assim que se faz, seu bobão - ``;correio [user] [message]``")
       else:
         try:
          await ctx.send(f"Aconteceu coisas 😳 - ``{error.original}``")
         except:
            await ctx.send(f"Aconteceu coisas 😳 - ``{error}``")

# ======================================================================
async def setup(bot: commands.Bot):
    print("[ ✅ ] Cogs mail")
    await bot.add_cog(mail(bot))