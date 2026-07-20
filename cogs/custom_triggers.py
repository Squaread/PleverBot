import discord
from discord.ext import commands
import os

from config import bot_prefix
from core import state
from utils.logs import logger

from data.data_manager import Load_Triggers
from data.data_manager import UpTrigger

class custom_triggers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
# ==================== Comando maketrigger ====================
    @commands.command(name="maketrigger")
    @commands.has_permissions(manage_guild = True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def maketrigger(self, ctx, *, trigger):
        parts = trigger.split("output:", 1)
        if trigger.startswith(bot_prefix):
            await ctx.send(f"**❌ |** O `invoker` não pode conter o prefixo do bot.")
            return
        
        if len(parts) != 2:
            await ctx.send(f"`{bot_prefix}maketrigger input: <invoker> output: <response> exact: <boolean (True ou False)>`")
            return
        
        input_part, remaining_part = parts
        exact_parts = remaining_part.split("exact:", 1)

        if len(exact_parts) != 2:
            await ctx.send(f"`{bot_prefix}maketrigger input: <invoker> output: <response> exact: <boolean (True/False)>`")
            return
        
        output_part, exact_part = exact_parts
        input_text = input_part.replace("input:", "").strip()
        output_text = output_part.strip()
        exact_text = exact_part.strip().lower()

        guild_id = str(ctx.guild.id)
        author_id = str(ctx.author.id)

        exact_value = exact_text == "true"

        # Salvar o trigger
        if guild_id not in state.custom_triggers: state.custom_triggers[guild_id] = {}
        state.custom_triggers[guild_id][input_text] = {
            "output": output_text,
            "exact": exact_value,
            "author_id": author_id
        }
        UpTrigger(state.custom_triggers)

        await ctx.send(f"**✅ |** Trigger criado: `{input_text}` → `{output_text}`")

        # Enviar log
        await logger(self.bot, "maketrigger", f"**Input:** `{input_text}` \n **Output:** `{output_text}` \n **Exact:** `{exact_value}` \n\n **Criador:** `{ctx.author}` | `{ctx.author.id}` \n **Server:** `{ctx.guild}` | `{ctx.guild.id}`", 0x1abc9c)


# ==================== Comando deltrigger ====================
    @commands.command(name="deltrigger")
    @commands.has_permissions(manage_guild = True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def deltrigger(self, ctx, *, trigger):
        json_path = os.path.join('triggers', f'{ctx.guild.id}.json')
        if os.path.exists(json_path):
        
            if trigger in state.custom_triggers:
                del state.custom_triggers[trigger]
                UpTrigger(state.custom_triggers)
                await ctx.send(f'✅ | `{trigger}` deleted')
            else:
                await ctx.send(f'Não encontrado.')
        else:
            await ctx.send(f'Deu erro xd')
    

# ======================================================================
async def setup(bot: commands.Bot):
    print("[ ✅ ] Cogs bot_admin")
    await bot.add_cog(custom_triggers(bot))
