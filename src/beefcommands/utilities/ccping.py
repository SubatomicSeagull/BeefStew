import discord
import os
import json
from beefutilities.ping import ping_host
from beefutilities.generate_hosts import generate_hosts_file
from datetime import datetime


async def ccping(bot, interaction: discord.Interaction):
    await interaction.response.defer()
    # dm restriction
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send("we are literally in DMs rn bro u cant do that here...")
        return
    
    # retrive the bots pfp
    boturl = bot.user.avatar.url
    
    embed = await pingembed(interaction, boturl, interaction.channel.guild.name)
    await interaction.followup.send(embed=embed)
    
async def pingembed(interaction: discord.Interaction, icon_url, guild_name):
    # construct a file path to hosts.json
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, '..', '..')
    hosts_path = os.path.join(file_path, "data", "server_info", "hosts.json")
    
    # generate a new hosts file if there isnt one
    if not os.path.exists(hosts_path):
        await generate_hosts_file()
            
    #if the hosts file is older than one day, update it
    current_time = datetime.now()
    file_mod_time = datetime.fromtimestamp(os.path.getmtime(hosts_path))
    
    if (current_time - file_mod_time).days > 1:
        print(f"Hosts file older than 1 day ({(current_time - file_mod_time).days}), retriving updated info...")
        await generate_hosts_file()
    
    # open hosts.json
    with open(hosts_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    
    total_response_time = 0
    host_count = len(data)
    
    #embed header
    pingembed = discord.Embed(title=f"Pinged CCServer with {host_count} results:", description="", color=discord.Color.lighter_grey())
    pingembed.set_thumbnail(url=icon_url) # change to ccserver icon, actaully figure out how to add local files this time plz
    pingembed.set_author(name="Beefstew", icon_url=icon_url)
    
    #ping each host:port
    for i, host, in enumerate(data):
        
        host_response_time = 0
        host_response_time = await ping_host(os.getenv("SERVERIP"), data[host], 0.25, 3)    
        if host_response_time != 0:
            pingembed.add_field(name=f"✅ **{host}** is Online!", value="", inline=False)
            total_response_time = total_response_time + host_response_time
        else:
            pingembed.add_field(name=f"❌ **{host}** is Offline...", value="", inline=False)
    
    
    pingembed.add_field(name="", value=f"with an average response time of {round((total_response_time / host_count),2)}ms.", inline=False)
    pingembed.add_field(name="", value=f"{guild_name} - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    return pingembed
    