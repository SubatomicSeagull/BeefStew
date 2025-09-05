import discord

async def pokeuser(interaction: discord.Interaction, victim: discord.Member, scope: bool, private: bool, bot):
    #dm channel restrictions
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send("we are literally in DMs rn bro u cant do that here...")
        return

    if scope:
        #fetch dm channel of the victim
        channel = await victim.create_dm()
    else:
        #else, fetch the channel of the interaction
        channel = interaction.channel

    if victim == interaction.user:
        await interaction.response.send_message("you poked yourself?")
        return

    # if private, send in dms
    if private:
        await channel.send(f"Someone poked {victim.mention}!")
    else:
        #else send in the interaction channel
        await channel.send(f"{interaction.user.mention} poked {victim.mention}!")

    # ephemeral message to resolve the interaction
    await interaction.response.send_message(f"you poked {victim.mention}!", ephemeral=True)

    return