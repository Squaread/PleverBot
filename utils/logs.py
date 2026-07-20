import discord

from config import bot_log_channel

async def logger(bot, title, description, color=discord.Color.blue()):
    if bot_log_channel == 0: return
    channel = bot.get_channel(bot_log_channel)

    embed = discord.Embed(title=title, description=description, color=color)

    await channel.send(embed=embed)