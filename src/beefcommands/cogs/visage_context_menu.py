import os
import discord
from discord.ext import commands
from beefcommands.visage import react, boil_image, down_the_drain_image, add_speech_bubble_pfp, bday, bless_pfp, gay_baby_jail_image, JFK_image, mirror_img, water_filter

# resends the picutre but with a reaction
@discord.app_commands.context_menu(name="React")
async def reaction_image(interaction: discord.Interaction, message: discord.Message):
    print(f"> \033[32m{interaction.user.name} used /react on {message.author.name}'s image\033[0m")
    await react.react(interaction, message)
    return

@discord.app_commands.context_menu(name="Boil")
async def boil(interaction: discord.Interaction, message: discord.Message):
    print(f"> \033[32m{interaction.user.name} used /boil on {message.author.name}'s image\033[0m")
    await boil_image.boil(interaction, message)
    return

@discord.app_commands.context_menu(name="Down the Drain")
async def down_the_drain(interaction: discord.Interaction, message: discord.Message):
    print(f"> \033[32m{interaction.user.name} used /down_the_drain on {message.author.name}'s image\033[0m")
    await down_the_drain_image.drain(interaction, message)
    return

@discord.app_commands.context_menu(name="Gay Baby Jail")
async def gay_baby_jail(interaction: discord.Interaction, message: discord.Message):
    print(f"> \033[32m{interaction.user.name} used /GBJ on {message.author.name}'s image\033[0m")
    await gay_baby_jail_image.GBJ(interaction, message)
    return

@discord.app_commands.context_menu(name="JFK")
async def jfk(interaction: discord.Interaction, message: discord.Message):
    print(f"> \033[32m{interaction.user.name} used /JFK on {message.author.name}'s image\033[0m")
    await JFK_image.watch_out(interaction, message)
    return

@discord.app_commands.context_menu(name="Mirror")
async def mirror(interaction: discord.Interaction, message: discord.Message):
    print(f"> \033[32m{interaction.user.name} used /mirror on {message.author.name}'s image\033[0m")
    await mirror_img.mirror(interaction, message)
    return

@discord.app_commands.context_menu(name="Drown")
async def drown(interaction: discord.Interaction, message: discord.Message):
    print(f"> \033[32m{interaction.user.name} used /drown on {message.author.name}'s image\033[0m")
    await water_filter.drown(interaction, message)
    return


# cog startup
async def setup(bot: discord.Client):
    print("- \033[96mbeefcommands.cogs.visage_cog.context_menu\033[0m")
    guild = await bot.fetch_guild(os.getenv("GUILDID"))
    bot.tree.add_command(reaction_image, guild=guild)
    bot.tree.add_command(boil, guild=guild)
    bot.tree.add_command(down_the_drain, guild=guild)
    bot.tree.add_command(gay_baby_jail, guild=guild)
    bot.tree.add_command(jfk, guild=guild)
    bot.tree.add_command(drown)
    bot.tree.add_command(mirror)
    #bot.tree.add_command(rainbow)
    #bot.tree.add_command(explode)
    #bot.tree.add_command(bacteria)
    await bot.tree.sync(guild=guild)
