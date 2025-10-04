import discord

# TODO: make this prettier
async def help(bot, interaction: discord.Interaction):
    await interaction.response.defer()
    # dm restriction
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send("we are literally in DMs rn bro u cant do that here...")
        return

    # embed header
    view = HelpEmbed()
    page0embed = discord.Embed(title = "Beefstew Help", description = "You don't want to know what I can *really* do...", color = discord.Color.lighter_grey())
    page0embed.set_thumbnail(url = bot.user.avatar.url)
    page0embed.set_author(name = "Help", icon_url = bot.user.avatar.url)
    #embed body
    page0embed.add_field(name = "",value = "⠀", inline = False)
    page0embed.add_field(name = "Commands:",value = "", inline = False)
    page0embed.add_field(name = "",value = "Click on the buttons below for a list of commands", inline = False)
    page0embed.add_field(name = "",value = "⠀", inline = False)
    page0embed.add_field(name = "\nOther info:\n",value = "", inline = False)
    page0embed.add_field(name = "", value = "Privacy Policy", inline = True)
    page0embed.add_field(name = "", value = "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Terms of Service", inline = True)
    # embed footer
    page0embed.add_field(name = "", value = "[cosycraft.uk/privacy](https://www.cosycraft.uk/privacy)⠀⠀⠀⠀⠀⠀⠀[cosycraft/tos](https://www.cosycraft.com/tos)", inline = False)
    await interaction.channel.send(embed = page0embed, view = view)

class HelpEmbed(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.currentpage = 0

    @discord.ui.button(label = "Moderation", style = discord.ButtonStyle.primary)
    async def moderation(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.currentpage = 1
        page_moderation = discord.Embed(title = "Help - Moderation", description = "judge judy, and exeggutor", color = discord.Color.lighter_grey())
        page_moderation.set_thumbnail(url = f"https://media.discordapp.net/attachments/1287128763645165678/1409134797527453838/moderation_stew.png?ex=68ac468c&is=68aaf50c&hm=319fe454d766a6931fdafbb57b80b59246203d3765bbb5bb1ec0a83f7d0923f5&=&format=webp&quality=lossless&width=943&height=943")
        page_moderation.add_field(name = "Commands:",value = "", inline = False)
        page_moderation.add_field(name = "", value = "`/warn`: 🫵YOU", inline = False)
        page_moderation.add_field(name = "", value = "`/mute`: SHHHHHHHHHH", inline = False)
        page_moderation.add_field(name = "", value = "`/unmute`: HHHHHHHHHHS", inline = False)
        page_moderation.add_field(name = "", value = "`/kick`: OOT MAH HOOSE", inline = False)
        page_moderation.add_field(name = "", value = "`/ban`: KILL KILL KILL!!!", inline = False)

        await interaction.response.edit_message(embed = page_moderation)

    @discord.ui.button(label = "Utilities", style = discord.ButtonStyle.primary)
    async def utilities(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.currentpage = 2
        page_utilities = discord.Embed(title = "Help - Utilities", description = "TOOLS!! i need my TOOLS!!!!!", color = discord.Color.lighter_grey())
        page_utilities.add_field(name = "Commands:", value = "", inline = False)
        page_utilities.set_thumbnail(url = "https://media.discordapp.net/attachments/1287128763645165678/1409134533596549201/utilities_stew.png?ex=68ac464d&is=68aaf4cd&hm=bbc42561e8b38140d111a74342cd6ef663b7d499ab8d2c6920adecee38950e92&=&format=webp&quality=lossless&width=943&height=943")
        page_utilities.add_field(name = "", value = "`/ccping`: pings ccserver, be sensible with this one", inline = False)
        #page2embed.add_field(name="", value="`/ccinfo`: retrieve current info about CCServer", inline=False)
        page_utilities.add_field(name = "", value = "`/help`: this is the one you're using right now!", inline = False)
        page_utilities.add_field(name = "", value = "`/bday`: tell beefstew your birthday (format like dd/mm/yyyy)", inline = False)
        page_utilities.add_field(name = "", value = "`/sniff`: let beefstew sniff you", inline = False)
        page_utilities.add_field(name = "", value = "`/unsniff`: make beefstew forget your scent", inline = False)
        page_utilities.add_field(name = "", value = "`/feature`: suggest new features!", inline = False)
        page_utilities.add_field(name = "", value = "`/update`: whats new?", inline = False)
        page_utilities.add_field(name = "", value = "`/test`: <- jamie delete this", inline = False)
        page_utilities.add_field(name = "", value = "`/say`: make beefstew talk like some kind of flesh puppet!", inline = False)
        page_utilities.add_field(name = "", value = "`/shutup`: tape beefstew's mouth shut", inline = False)
        page_utilities.add_field(name = "", value = "`/speak`: untape beefstew's mouth", inline = False)
        page_utilities.add_field(name = "", value =" `/voice`: change beefstew's voice", inline = False)
        await interaction.response.edit_message(embed = page_utilities)

    @discord.ui.button(label = "Incantations", style = discord.ButtonStyle.primary)
    async def incantations(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.currentpage = 3
        page_incantation = discord.Embed(title = "Help - Incantations", description = "nuns commence incating as the lighting strikes mine temples", color=discord.Color.lighter_grey())
        page_incantation.set_thumbnail(url = "https://cdn.discordapp.com/attachments/1287128763645165678/1409134766326026281/incantation_stew.png?ex=68ac4684&is=68aaf504&hm=99f51b38a87491eace89232b6109ca9404c3f465544d6e7b8bd27979617afd18&")
        page_incantation.add_field(name = "Commands:", value = "", inline = False)
        page_incantation.add_field(name = "", value = "`/mock`: cast vicious mockery on someone", inline = False)
        page_incantation.add_field(name = "", value = "`/poke`: cast spectral hand and poke someone", inline = False)
        await interaction.response.edit_message(embed = page_incantation)

    @discord.ui.button(label = "Invocations", style = discord.ButtonStyle.primary)
    async def invocations(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.currentpage = 4
        page_invokation = discord.Embed(title = "Help - Invocations", description = "let ye who is without sin cast the first stone", color = discord.Color.lighter_grey())
        page_invokation.add_field(name = "Commands:", value = "", inline = False)
        page_invokation.set_thumbnail(url = "https://media.discordapp.net/attachments/1287128763645165678/1409134553041469471/invokation_stew.png?ex=68ac4651&is=68aaf4d1&hm=9f3c7e85f521b20b6b242df8f80c2fd9588afd6c87853337d76af9e9835972d4&=&format=webp&quality=lossless&width=943&height=943")
        page_invokation.add_field(name = "", value = "`[@victim] they call you [nickname]`: invoke the rule...", inline = False)
        page_invokation.add_field(name = "", value = "`[@victim] +2`: good joke <:beefsmile:1308701407007739974>", inline = False)
        page_invokation.add_field(name = "", value = "`[@victim] -2`: bad joke <:beefhusk:1287094093989679124>", inline = False)
        page_invokation.add_field(name = "", value = "`/leaderboard`: top 10 jokers", inline = False)
        page_invokation.add_field(name = "", value = "`/loserboard`: bottom 10 jokers", inline = False)
        page_invokation.add_field(name = "", value = "`/gamble`: spend a joke point to gamble it all...", inline = False)
        page_invokation.add_field(name = "", value = "`/score`: how funny r u?", inline = False)
        await interaction.response.edit_message(embed = page_invokation)

    @discord.ui.button(label = "Visage", style = discord.ButtonStyle.primary)
    async def visgae(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.currentpage = 5
        page_visage = discord.Embed(title = "Help - Visage", description = "alter the flesh, alter the mind...", color = discord.Color.lighter_grey())
        page_visage.add_field(name = "Commands:", value = "", inline = False)
        page_visage.set_thumbnail(url = "https://media.discordapp.net/attachments/1287128763645165678/1409134899356635289/weirdstew.png?ex=68ac46a4&is=68aaf524&hm=c6bd4521bc40fb045d84e9d1ee420f96b262ad2e5caff69fc71e2377879c78d1&=&format=webp&quality=lossless&width=375&height=375")
        page_visage.add_field(name = "", value = "`/boil`: boils the user", inline = False)
        page_visage.add_field(name = "", value = "`/slander`: i cant belive they just said that...", inline = False)
        page_visage.add_field(name = "", value = "`/drain`: yea we dropped them down there they got stucl ://", inline = False)
        page_visage.add_field(name = "", value = "`/bless`: bless you my child...", inline = False)
        page_visage.add_field(name = "", value = "`/jail`: go directly to jail!", inline = False)
        page_visage.add_field(name = "", value = "`/jfk`: MISTER PRESIDENT WATCH OUT", inline = False)
        page_visage.add_field(name = "", value = "`/drown`: imagine an old man drowning lol", inline = False)
        page_visage.add_field(name = "", value = "`/explode`: blow someone up!!!!!!!!", inline = False)        
        page_visage.add_field(name = "", value = "❗*Tip:* visage commands can be used on almost any image through the context menu!", inline = False)
        await interaction.response.edit_message(embed = page_visage)

    @discord.ui.button(label = "Music Player", style = discord.ButtonStyle.primary)
    async def music(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.currentpage = 6
        page_mpplayer = discord.Embed(title = "Help - Music Player", description = "DJ DJ DDDD DJ DJ        DJ", color = discord.Color.lighter_grey())
        page_mpplayer.add_field(name = "Commands:", value = "", inline = False)
        page_mpplayer.set_thumbnail(url = "https://media.discordapp.net/attachments/1287128763645165678/1409134493914234971/music_stew.png?ex=68ac4643&is=68aaf4c3&hm=1146b71a32405c7b9fba20328999f89550dd32cfe0661fcaca72821589236c67&=&format=webp&quality=lossless&width=375&height=375")
        page_mpplayer.add_field(name = "", value = "The music player can take tracks from:\n Direct youtube links (e.g youtube.com/watch[link])\nSpotify links (e.g open.spotify.com/track/[link])\n Search Terms (e.g 'jellyish fields forever')", inline = False)
        page_mpplayer.add_field(name = "", value = "`/play [link]`: adds the track to the front of the queue and starts playing", inline = False)
        page_mpplayer.add_field(name = "", value = "`/queue [link]`: adds the track to the back of the queue", inline = False)
        page_mpplayer.add_field(name = "", value = "`/pause`: pauses the current track", inline = False)
        page_mpplayer.add_field(name = "", value = "`/resume`: resumes the current track", inline = False)
        page_mpplayer.add_field(name = "", value = "`/skip`: skips the current track", inline = False)
        page_mpplayer.add_field(name = "", value = "`/list`: lists all tracks in the queue", inline = False)
        page_mpplayer.add_field(name = "", value = "`/shuffle`: shuffles the queue", inline = False)
        page_mpplayer.add_field(name = "", value = "`/clear`: clears the queue", inline = False)
        page_mpplayer.add_field(name = "", value = "`/loop`: loops the current track", inline = False)
        page_mpplayer.add_field(name = "", value = "`/join`: joins the voice channel", inline = False)
        page_mpplayer.add_field(name = "", value = "`/leave`: leaves the voice channel", inline = False)

        await interaction.response.edit_message(embed = page_mpplayer)