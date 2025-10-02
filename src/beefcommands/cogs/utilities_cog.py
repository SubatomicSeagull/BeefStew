import enum
import discord
from discord.ext import commands
from beefcommands.utilities.ccping import ccping
from beefutilities.TTS import speak
from beefutilities.guilds.guild_text_channel import set_info, set_logs, set_quotes
from beefcommands.utilities.help import help
from beefutilities.update_patch_notes import update_patch_notes_info
from beefcommands.visage.sniff import sniff_user
from beefutilities.users import user
from beefcommands.utilities.suggest_feature import create_suggestion
from beefutilities.TTS import speak, tts_engine

# gerate enumeration object for the tts voices dropdown
VoiceList = tts_engine.generate_voice_enum()
class UtilitiesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # pings ccserver and returns an average ping time
    @discord.app_commands.command(name="ccping", description="pings CCServer, please be responsible with this one...")
    async def ccping(self, interaction: discord.Interaction):
        print(f"> \033[32m{interaction.user.name} used /ccping\033[0m")
        await ccping(self.bot, interaction)

    # not implemented yet, will retrieve info about ccserver like storage, ping, etc
    @discord.app_commands.command(name="ccinfo", description="returns current info about CCServer")
    async def ccinfo(self, interaction: discord.Interaction, url: str):
        pass

    # sets the logs channel to the channel its run in
    @discord.app_commands.command(name="set_logs_channel", description="where should i spew...?")
    async def set_log_channel(self, interaction: discord.Interaction):
        print(f"> \033[32m{interaction.user.name} used /set_log_channel in #{interaction.channel.name}\033[0m")
        await set_logs(interaction)

    # sets the info channel to the channel its run in
    @discord.app_commands.command(name="set_info_channel", description="where should i spew...?")
    async def set_info_channel(self, interaction: discord.Interaction):
        print(f"> \033[32m{interaction.user.name} used /set_info_channel in #{interaction.channel.name}\033[0m")
        await set_info(interaction)

    # sets the quotes channel to the channel its run in
    @discord.app_commands.command(name="set_quotes_channel", description="where do *you* spew...?")
    async def set_quote_channel(self, interaction: discord.Interaction):
        print(f"> \033[32m{interaction.user.name} used /set_quotes_channel in #{interaction.channel.name}\033[0m")
        await set_quotes(interaction)

    # prints a list of commands
    @discord.app_commands.command(name="help", description="HELP!! HELP ME!!!!!!!")
    async def help(self, interaction: discord.Interaction):
        print(f"> \033[32m{interaction.user.name} used /help\033[0m")
        await help(self.bot, interaction)

    #prints the patch notes in a nice little embed
    @discord.app_commands.command(name="update", description="whats new?")
    async def update(self, interaction: discord.Interaction):
        print(f"> \033[32m{interaction.user.name} used /update\033[0m")
        await update_info(interaction, self.bot)    
    
    @commands.command(name="test", description="jamie delete this")
    async def test(self, ctx, *, input: str):
        await speak.speak_output(ctx, input)

    # registered the users bday in the database
    @discord.app_commands.command(name="bday", description="format like dd/mm/yyyy")
    async def set_bday(self, interaction: discord.Interaction, bday: str):
        print(f"> \033[32m{interaction.user.name} set their birthday to {bday}\033[0m")
        await interaction.response.send_message(await user.register_user_bday(interaction.user, bday), ephemeral = True)

    # sets the random swing message flag to true and sends a picture
    @discord.app_commands.command(name="sniff", description="what do u smell like")
    async def sniff(self, interaction: discord.Interaction):
        print(f"> \033[32m{interaction.user.name} used sniff\033[0m")
        await user.set_msg_flag(interaction.user, True)
        await sniff_user(interaction, interaction.user)

    # sets the random swing message flag to false
    @commands.command(name="unsniff", description="what dont u smell like")
    async def unsniff(self, ctx):
        print(f"> \033[32m{ctx.author.name} used unsniff \033[0m")
        await user.set_msg_flag(ctx.author, False)

        # adds a trello cards suggesting new features
    @discord.app_commands.command(name="feature", description="what else do you want from me?????")
    async def feature(self, interaction: discord.Interaction, name: str, description: str):
        print(f"> \033[32m{interaction.user.name} suggested a feature \"{name}\"\033[0m")
        await create_suggestion(interaction, name, description)

    # repeats the users message underneath and deletes the original
    @commands.command(name="say", description="say something")
    async def say(self, ctx, *, message):
        print(f"> \033[32m{ctx.author.name} used /say \"{message}\"\033[0m")
        await ctx.message.delete()

        if message != "" and message != None:
            await ctx.send(message)
            await speak.speak_output(ctx, message)

    # disable TTS
    @discord.app_commands.command(name="shutup", description="turn off TTS")
    async def shutup(self, interaction: discord.Interaction):
        print(f"> \033[32m{interaction.user.name} used /shutup\033[0m")
        speak.set_lock_state_global(True)
        await interaction.response.send_message("TTS disabled", ephemeral = True)

    # enable TTS
    @discord.app_commands.command(name="speak", description="turn on TTS")
    async def speak(self, interaction: discord.Interaction):
        print(f"> \033[32m{interaction.user.name} used /speak\033[0m")
        speak.set_lock_state_global(False)
        await interaction.response.send_message("TTS enabled", ephemeral=True)
    
    # change the tts voice
    @discord.app_commands.command(name="voice", description="set the TTS voice")
    @discord.app_commands.describe(voice="what should i sound like???")
    async def voice(self, interaction: discord.Interaction, voice: VoiceList):
        print(f"> \033[32m{interaction.user.name} set BeefStew's voice to {voice.name}\033[0m")
        tts_engine.set_voice(voice.value)
        await interaction.response.send_message(f"Voice set to **{voice.name}**", ephemeral=True)

# cog setup
async def setup(bot):
    print("- \033[32mbeefcommands.cogs.utilities_cog\033[0m")
    await bot.add_cog(UtilitiesCog(bot))
