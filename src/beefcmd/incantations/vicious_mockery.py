import os
import json
from json_handling import load_element
import random
import discord


async def get_insult():
    insults = load_element("responses.json", "insults")
    return random.choice(insults)

async def insult(interaction: discord.Interaction, victim: discord.Member):
    if victim.id != os.getenv("CLIENTID"):
        try:
            insult = await get_insult()
            if victim.id == interaction.user.id:
                return(f"{interaction.user.mention} tried to cast Vicious Mockery on themselves for some reason...\nit still works tho, {interaction.user.mention} {insult} ")
            else:
                return(f"{victim.mention} {insult}")
        except Exception as e:
            return (f"{interaction.user.mention} tried to cast Vicious Mockery on {victim.mention}... but it failed ({e})")
    else:
        return(f"{interaction.user.mention} tried to cast Vicious Mockery on me...BITCH")