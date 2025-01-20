import os
from beefutilities.json_handling import load_element
import random
import discord


async def get_insult():
    insults = load_element("responses.json", "insults")
    return random.choice(insults)

async def insult(interaction: discord.Interaction, victim: discord.Member):
    await interaction.response.defer()
    if victim.id != os.getenv("CLIENTID"):
        try:
            insult = await get_insult()
            if victim.id == interaction.user.id:
                await interaction.followup.send(f"{interaction.user.mention} tried to cast Vicious Mockery on themselves for some reason...\nit still works tho, {interaction.user.mention} {insult} ")
            else:
                await interaction.followup.send(f"{victim.mention} {insult}")
        except Exception as e:
            await interaction.followup.send(f"{interaction.user.mention} tried to cast Vicious Mockery on {victim.mention}... but it failed ({e})")
    else:
        await interaction.followup.send(f"{interaction.user.mention} tried to cast Vicious Mockery on me...BITCH") 