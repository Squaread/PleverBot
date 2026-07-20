import discord
from discord.ext import commands

from config import bot_prefix
from core import state
from utils.logs import logger

from data.data_manager import UpCustomCommand

class custom_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
# ==================== Comando makecmd ====================
    @commands.command(name="makecmd")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def makecmd(self, ctx, *, cmd):
        parts = cmd.split("output:", 1)
        if len(parts) != 2:
            await ctx.send(f"`{bot_prefix}makecmd input <invoker> output: <response>`")
            return

        input_part, output_part = parts
        get_input = input_part.replace("input:", "").strip()
        input_text = bot_prefix + get_input
        output_text = output_part.strip()

        if get_input in self.bot.all_commands:
            await ctx.send(f"**❌ |** `{input_text}` já é um comando nativo do bot 🤓☝️")
            return
        
        # Armazenar o comando customizado com o ID do autor
        state.custom_commands[input_text] = {
            'output': output_text,
            'author_id': str(ctx.author.id)
        }
        UpCustomCommand(state.custom_commands)

        # Feedback do novo comando feito ao usuario
        embed_new_cmd = discord.Embed(title="Novo comando", description=f"**Input:** ``{input_text}`` \n **Output:** ``{output_text}``", color=0x0c6940)
        embed_new_cmd.set_footer(text=f"{ctx.author} | {ctx.author.id}")
        await ctx.channel.send(embed=embed_new_cmd)
        
        # Enviar log
        await logger(self.bot, "makecmd", f"**Input:** `{input_text}` \n **Output:** `{output_text}` \n\n **Criador:** `{ctx.author}` | `{ctx.author.id}` \n **Server:** `{ctx.guild}` | `{ctx.guild.id}`", 0x1abc9c)
    
# ==================== Comando cmd ====================
    @commands.command(name="cmd")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cmd(self, ctx, *, command_name):
        command_name = bot_prefix + command_name
    
        if command_name in state.custom_commands:
            command_data = state.custom_commands[command_name]
            author_id = command_data.get('author_id', 'Unknown')
            response_cmd = command_data.get('output', 'Unknown')

            try: author_cmd = await self.bot.fetch_user(int(author_id))
            except discord.errors.NotFound: author_cmd = 'Unknown'
    
            embed_cmdinfo = discord.Embed(title=command_name, description=f"**Criador:** ``{author_cmd}`` | ``{author_cmd.id}`` \n **Output:** ``{response_cmd}``", color=0x897ec2)
            await ctx.send(embed=embed_cmdinfo)
        else:
            await ctx.send("Não encontrado.")


# ======================================================================
async def setup(bot: commands.Bot):
    print("[ ✅ ] Cogs custom_commands")
    await bot.add_cog(custom_commands(bot))
