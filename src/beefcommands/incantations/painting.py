import discord
import random
from random import randint
from beefutilities.IO import file_io
from beefutilities.IO.json_handling import load_element

async def show_painting(interaction: discord.Interaction):
    await interaction.response.defer()
    await interaction.followup.send(content=await generate_aflictions(), file=discord.File(fp= await get_painting(), filename="SPOILER_painting.png"))
    return

async def generate_aflictions():
    pronoun = random.choice(["His", "Her", "Their"])
    aflictions = load_element("responses.json", "painting_aflictions")
    body_parts = load_element("responses.json", "painting_bodyparts")
    sentences = "Police discovered a body late last night...\n"
    for i in range(randint(1,5)):
        sentences = sentences + (f"{pronoun} {random.choice(body_parts)} {random.choice(aflictions)}...\n")
    sentences = sentences +(f"There were {randint(1,500)} stab wounds...\n**HERE IS THE PAINTING:**")
    return sentences

async def get_painting():
    return file_io.construct_media_path(f"paintings/{randint(0, 39)}.png")