import discord
import os
from beefutilities.ping import ping_host
from beefutilities.IO.generate_hosts import containers_json_reformat
from datetime import datetime
from beefutilities.IO import file_io

async def ccping(bot, interaction: discord.Interaction):
    await interaction.response.defer()
    # dm restriction
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send("we are literally in DMs rn bro u cant do that here...")
        return

    # retrieve the bots pfp
    boturl = bot.user.avatar.url

    embed, thumbnail = await ping_embed(boturl, interaction.channel.guild.name)
    await interaction.followup.send(embed = embed, file = thumbnail)

async def ping_embed(icon_url, guild_name):
    data = await containers_json_reformat()
    host_count = len(data)
    if host_count > 0:
        #embed header
        pingembed = discord.Embed(title = f"Pinged CCServer with {host_count} results:", description = "", color = discord.Color.green())
        thumbnail = discord.File(file_io.construct_assets_path('profile/ccserver_icon.png'), filename = "ccserver_icon.png")
        pingembed.set_thumbnail(url = f"attachment://ccserver_icon.png")
        pingembed.set_author(name = "Beefstew", icon_url = icon_url)

        #ping each host:port
                    
        total_response_time = 0
        for i, host, in enumerate(data):
            host_response_time = 0
            host_response_time = await ping_host(os.getenv("SERVERIP"), host["ports"], 0.15, 1)
            if host_response_time != 0:
                pingembed.add_field(name = f"✅ **{host["name"]}** is Online!", value = "", inline = False)
                total_response_time = total_response_time + host_response_time
            else:
                pingembed.add_field(name = f"❌ **{host["name"]}** is Offline...", value = "", inline = False)


        pingembed.add_field(name = "", value = f"with an average response time of {round((total_response_time / host_count),2)}ms.", inline = False)
        pingembed.add_field(name = "", value = f"{guild_name} - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    else:
        pingembed = discord.Embed(title = f"Could not connect to CCServer.", description = "", color = discord.Color.red())
        thumbnail = discord.File(file_io.construct_assets_path('profile/ccserver_icon_failed.png'), filename = "ccserver_icon_failed.png")
        pingembed.set_thumbnail(url = f"attachment://ccserver_icon_failed.png")
        pingembed.set_author(name = "Beefstew", icon_url = icon_url)
        pingembed.add_field(name = "", value = f"{guild_name} - {datetime.now().strftime('%d/%m/%Y - %H:%M')}")

    return pingembed, thumbnail
