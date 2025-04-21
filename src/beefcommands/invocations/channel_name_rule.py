import discord

async def invoke_channel_name_rule(ctx, new_name: str):
    # if the incomming context is a slash command interaction:
    if isinstance(ctx, discord.Interaction):
        interaction = ctx
    
        # check if the user is in a voice channel
        if not interaction.user.voice:
            return

        # check if the user is in a vc and change the name of the channel to the new name
        if interaction.user.voice.channel.name != new_name:
            try:
                await interaction.user.voice.channel.edit(name=new_name)
                await interaction.response.send_message(f"yea why are we in {new_name}") #pick from response.json
                return
            
            except Exception as e:
                print(f"Error: {e}")
                await interaction.response.send_message(f"ykno... idk if we *are* in {new_name}...{e}")
                return
        else:
            # if its the same, do nothing
            return
    # else, the conext is a message object
    else:
        message = ctx
        # check if the user is in a voice channel
        if not message.author.voice:
            return

        # check if the user is in a vc and change the name of the channel to the new name
        if message.author.voice.channel.name != new_name:
            try:
                await message.author.voice.channel.edit(name=new_name)
                await message.channel.send(f"yea why are we in {new_name}") #pick from response.json
                return
            
            except Exception as e:
                print(f"Error: {e}")
                await message.channel.send(f"ykno... idk if we *are* in {new_name}...{e}")
                return
        else:
            # if its the same, do nothing
            return