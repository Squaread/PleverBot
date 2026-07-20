# mail
import discord
from discord.ext import commands

from config import bot_prefix
from core import state
from utils.logs import logger

class mail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
# ==================== Comando mail ==================== 
    @commands.hybrid_command(name="mail", aliases=['correio'], description="Envie uma mensagem anônima para alguém")
    @commands.cooldown(1, 5, commands.BucketType.user) # Cooldown default 5 segundo
    async def mail(self, ctx, destinatario: discord.Member, *,mensagem: str):
        target = destinatario
    
        server_data = state.servers_data["servers"][str(ctx.guild.id)]
        channelId_mail = server_data["mail"]["channel_id"]
        channel_mail = self.bot.get_channel(channelId_mail)
        
        if not channel_mail:
            await ctx.send(f"**❌ |** [MAIL] Eu não tenho permissão ou ele ainda não foi configurado `{bot_prefix}setchannel mail <channel_id>`")
            return
        
        # Enviar log
        await logger(self.bot, "Novo mail", f"**Mensagem:** `{mensagem}` \n\n **Creator:** `{ctx.author}` | `{ctx.author.id}` \n **Server:** `{ctx.guild}` | `{ctx.guild.id}`", 0x1abc9c)
        
        # Enviar correio
        embed_mail = discord.Embed(title="📧 | Correio Anônimo", description=f"Destinatário: {target.mention}\n\n{mensagem}", color=0x9B533B)
        await channel_mail.send(f"{target.mention} Você recebeu uma carta 😨",embed=embed_mail)
        await ctx.message.delete()

# ======================================================================
async def setup(bot: commands.Bot):
    print("[ ✅ ] Cogs mail")
    await bot.add_cog(mail(bot))
