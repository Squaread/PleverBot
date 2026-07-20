import discord
from discord.ext import commands

from core import state
from utils.logs import logger
from data.data_manager import UpBlacklist

class bot_admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
# ==================== Comando block ====================
    @commands.command(name="block")
    @commands.is_owner()
    async def block(self, ctx, id: str, *, reason: str=None):
        target = await self.bot.fetch_user(id)
        if reason == None: reason = "sei la"

        state.banned_users[id] = {
            "reason": reason
        }
        UpBlacklist(state.banned_users)

        await ctx.send(f"`{target}` foi adicionado a blacklist pois `{reason}`")
        await logger(self.bot, "Blacklist", f"`{target}` foi adicionado a blacklist\n**Motivo:** {reason}", 0x992d22)

# ==================== Comando unblock ====================
    @commands.command(name="unblock")
    @commands.is_owner()
    async def unblock(self, ctx, id: str):
        target = await self.bot.fetch_user(id)
        if not target: return await ctx.send("Usuário não encontrado....")

        if id not in state.banned_users:
            await ctx.send("**❌ |** Não encontrado na blacklist.")
            return

        del state.banned_users[id]
        UpBlacklist(state.banned_users)

        await ctx.send(f"`{target}` foi removido da blacklist.")
        await logger(self.bot, "Blacklist", f"`{target}` foi removido da blacklist.", 0x57F287)

# ======================================================================
async def setup(bot: commands.Bot):
    print("[ ✅ ] Cogs bot_admin")
    await bot.add_cog(bot_admin(bot))
