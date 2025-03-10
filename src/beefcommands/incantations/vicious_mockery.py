import os
from beefutilities.IO.json_handling import load_element
import random
import discord


async def get_insult():
    insults = load_element("responses.json", "insults")
    return random.choice(insults)

async def insult(interaction: discord.Interaction, victim: discord.Member):
    await interaction.response.defer()
    
    # not allowed to insult beefstew
    if victim.id != os.getenv("CLIENTID"):
        try:
            # retrive insule
            insult = await get_insult()
            
            # cant insult yourself
            if victim.id == interaction.user.id:
                await interaction.followup.send(f"{interaction.user.mention} tried to cast Vicious Mockery on themselves for some reason...\nit still works tho, {interaction.user.mention} {insult} ")
            else:
                await interaction.followup.send(f"{victim.mention} {insult}")
        except Exception as e:
            await interaction.followup.send(f"{interaction.user.mention} tried to cast Vicious Mockery on {victim.mention}... but it failed ({e})")
    
    # cant insult beefstew
    else:
        await interaction.followup.send(f"{interaction.user.mention} tried to cast Vicious Mockery on me...BITCH") 