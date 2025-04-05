import discord
from discord.ext import commands
from beefcommands.visage import react

# resends the picutre but with a reaction
@discord.app_commands.context_menu(name="React")
async def reaction_image(interaction: discord.Interaction, message: discord.Message):
    print(f"> \033[32m{interaction.user.name} used /react on {message.author.name}\033[0m")
    await react.react(interaction, message)
    pass

# cog startup
async def setup(bot: discord.Client):
    print("- \033[96mbeefcommands.cogs.visage_cog.context_menu\033[0m")
    bot.tree.add_command(reaction_image)