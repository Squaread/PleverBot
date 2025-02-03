# mail
import discord
from discord.ext import commands
import json
from config import bot_log_channel

from functions import Load_ServersData

servers_data = {}

class mail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # ==================== Comando mail | Mail command ==================== 
    @commands.command(aliases=['correio'])
    @commands.cooldown(1, 300, commands.BucketType.user) # Aqui você pode mudar o cooldown | Here you can change the cooldown - Default: 300
    async def mail(self, ctx, destinatario: discord.Member, *,mensagem: str):
        target = destinatario
    
        servers_data = Load_ServersData()

        server_data = servers_data["servers"][str(ctx.guild.id)]
        status_mail = server_data["mail"]["enabled"]
        
        if status_mail == False:
           await ctx.send("**mail** está desativado - ``;help``")
           return
        
        channelId_mail = server_data["mail"]["channel_id"]
        channel_mail = self.bot.get_channel(channelId_mail)
        if not channel_mail:
            await ctx.send(f"**❌ |** [MAIL] Eu não tenho permissão no canal configurado ou ele não existe ~~~configurou errado fdp.~~")
            return

        # Enviar log | Send log
        log_channel = self.bot.get_channel(bot_log_channel)
        embed_log = discord.Embed(title="New mail", description=f"**Mensagem:** ``{mensagem}`` \n\n **Creator:** ``{ctx.author}`` | ``{ctx.author.id}`` \n **Server:** ``{ctx.guild}`` | ``{ctx.guild.id}``", color=0x1abc9c)
        await log_channel.send(embed=embed_log)

        # Enviar correio | Send mail
        embed_mail = discord.Embed(title="📧 | Correio Anônimo", description=f"Destinatário: {target.mention}\n\n{mensagem}", color=0x9B533B)
        await channel_mail.send(f"{target.mention} Você recebeu uma carta 😨",embed=embed_mail)
        await ctx.message.delete()

# ======================================================================
async def setup(bot: commands.Bot):
    print("[ ✅ ] Cogs mail")
    await bot.add_cog(mail(bot))
