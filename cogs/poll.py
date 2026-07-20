# poll
import discord
from discord.ext import commands, tasks

from utils.logs import logger

polls = {}

# ======== Criar poll  ========
def create_poll(title, options):
     emoji_numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
     poll_options = {}
     for i, option in enumerate(options):
         poll_options[emoji_numbers[i]] = {"option": option, "votes": 0}
     return {"title": title, "options": poll_options}

# ======== Display poll ========
def display_poll(poll):
     title = poll["title"]
     options = poll["options"]
     total_votes = sum(option["votes"] for option in options.values())
     poll_embed = discord.Embed(title=f"🗳️ Poll: {title}", color=0x99aab5)
     for emoji, option in options.items():
        votes = option["votes"]
        if total_votes > 0:
            percentage = votes / total_votes
        else:
            percentage = 0
        bar_length = int(percentage * 15)
        progress_bar = '█' * bar_length + ' ' * (10 - bar_length)
        poll_embed.add_field(name=f"{emoji} {option['option']}", value=f"Votos: {votes} ({percentage:.0%})\n{progress_bar}", inline=False)
        poll_embed.set_footer(text=f"Use ;vote [number] para votar")
     return poll_embed


class poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# ==================== Comando poll ====================
    @commands.command()
    async def poll(self, ctx, *, message):
     
     # Caso não tiver nenhum parametro uma poll ativa será mostrada
     if message == "":
      if ctx.guild.id in polls: # Verificar se tem alguma poll ativa
        poll = polls[ctx.guild.id]
        poll_embed = display_poll(poll)
        await ctx.send(embed=poll_embed) # Mostrar poll
      else: # Caso nenhuma poll exiba mensagem
        await ctx.send("Não há uma poll ativa.")
     
     title, options_text = message.split(":", 1)
     options_list = options_text.split(',')
     if len(options_list) > 10: # Limitar opções
            await ctx.send("**❌ |** O número máximo de opções é 10.")
            return
        
     poll = create_poll(title.strip(), options_list)
     polls[ctx.guild.id] = poll
     poll_embed = display_poll(poll)
     await ctx.send(embed=poll_embed) # Mostrar poll

     # Enviar log
     await logger(self.bot, "Novo poll", f"**Title:** `{title}` \n **Options:** `{options_list}` \n\n **Creator:** `{ctx.author}` | `{ctx.author.id}` \n **Server:** `{ctx.guild}` | `{ctx.guild.id}`", 0x979c9f)

    # ==================== Comando vote ====================
    @commands.command()
    async def vote(self, ctx, option_number: int):
        if ctx.guild.id not in polls:
            await ctx.send("Não há uma poll ativa.")
            return
    
        poll = polls[ctx.guild.id]
        emoji_numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        if 0 < option_number <= len(emoji_numbers):
            emoji = emoji_numbers[option_number - 1]
            if emoji in poll["options"]:
                author_id = str(ctx.author.id)
                for option, data in poll["options"].items():
                    if author_id in data.get("voters", []):
                        data["votes"] -= 1
                        data["voters"].remove(author_id)
                poll["options"][emoji]["votes"] += 1
                poll["options"][emoji].setdefault("voters", []).append(author_id)
                poll_embed = display_poll(poll)
                await ctx.send(embed=poll_embed)
            else:
                await ctx.send("Eita algo deu errado")
        else:
            await ctx.send("Essa opção não existe...")



# ======================================================================
async def setup(bot: commands.Bot):
    print("[ ✅ ] Cogs poll")
    await bot.add_cog(poll(bot))
