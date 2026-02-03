import discord
import datetime
from beefutilities.guilds.guild_text_channel import read_guild_quotes_channel

async def quote_embed(message, quoter):
    # construct the embed
    quote_embed = discord.Embed(description = f"# {message.content}", color = discord.Color.purple())
    quote_embed.set_author(name = f"{message.author.name} said:", icon_url = message.author.avatar.url)
    quote_embed.set_image(url = message.attachments[0].url) if message.attachments else None
    quote_embed.set_footer(text = f"Quoted from #{message.channel.name} by {quoter.name}\n{message.guild.name} • {datetime.datetime.now().strftime('%d/%m/%Y - %H:%M')}")



    return quote_embed


async def quote_message(message, quoter):
    # retrieve the guild's quote channel
    quote_channel_id = await read_guild_quotes_channel(message.guild.id)
    if not quote_channel_id:
        return None

    quote_channel = message.guild.get_channel(quote_channel_id)
    if not quote_channel:
        return None
    
    embed = await quote_embed(message, quoter)
    if quote_channel and embed:
        await quote_channel.send(embed = embed)
    return

