# mail
import discord
from discord.ext import commands

from core import state
from data.data_manager import UpServerData

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
# ==================== Comando config ====================
    @commands.hybrid_command(name="setchannel", description="Configure um canal num módulo [bottle, mail]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def setchannel(self, ctx, module: str, channel_id: str):
        modules = ["mail", "bottle"]
        if not module in modules:
            await ctx.send(f"**❌ |** Eita parece que `{module}` não é válido!")
            return
        
        try: await self.bot.fetch_channel(channel_id)
        except: return await ctx.send(f"**❌ |** Eu não tenho permissão nesse canal ou ele não existe ~~assim como seu pai~~")

        state.servers_data["servers"][str(ctx.guild.id)][module]["channel_id"] = int(channel_id) 
        UpServerData(state.servers_data)

        await ctx.send(f"**{module}** foi configurado para ``{channel_id}``")

# ======================================================================
async def setup(bot: commands.Bot):
    print("[ ✅ ] Cogs moderation")
    await bot.add_cog(moderation(bot))
