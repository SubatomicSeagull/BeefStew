import random
import discord
import os
from beefutilities.json_handling import load_element
from data.postgres import log_error

# nickname rule, handles logic for they call you slash command
async def change_nickname(ctx, victim: discord.Member, new_name: str):
    # checks to see if the interaction is through an interaction object or a message object, effectivly switches between using the slash command and having the command run inline
        if isinstance(ctx, discord.Interaction):
            interaction = ctx
            # not allowed to rename the bot
            if victim.id != os.getenv("CLIENTID"):
                # not allowed to rename yourself
                if victim.id == interaction.user.id:
                    await interaction.response.send_message(f"**{interaction.user.name}** tried to invoke the rule on themselves... for some reason")
                else:
                    try:
                        await victim.edit(nick=new_name)
                        await interaction.response.send_message(f"**{interaction.user.name}** invoked the rule on **{victim.global_name}**!\n{await nicknameprint(victim)}")           
                    except discord.Forbidden as e:
                        print(e)
                        await interaction.response.send_message(f"**{interaction.user.name}** tried to invoked the rule on **{victim.global_name}**!\nbut it didnt work :( next time get some permissions pal")
                    except Exception as e:
                        print(e)
            else:
                await interaction.response.send_message(f"**{interaction.user.name}** tried to invoked the rule on **{victim.global_name}**!\nnice try fucker...")
                
        elif isinstance(ctx, discord.Message):
            message = ctx
            # not allowed to rename the bot
            if victim.id !=os.getenv("CLIENTID"):
                # not allowed to rename yourself
                if victim.id == message.author.id:
                    await message.channel.send(f"**{message.author.name}** tried to invoke the rule on themselves... for some reason")
                else:
                    try:
                        await victim.edit(nick=new_name)
                        await message.channel.send(f"**{message.author.name}** invoked the rule on **{victim.global_name}**!\n{await nicknameprint(victim)}")
                    except Exception as e:
                        print(e)
                        await message.channel.send(f"**{message.author.name}** tried to invoked the rule on **{victim.global_name}**!\nbut it didnt work :( next time get some permissions okay?")
            else:
                await message.channel.send(f"**{message.author.name}** tried to invoked the rule on **{victim.global_name}**!\nnice try fucker...")

async def nicknameprint(victim: discord.Member): 
    # load responses.json
    responses = load_element("responses.json", "nickname_change_responses")
    
    chosen_response = random.choice(responses)
    print(chosen_response)
    chosen_response = chosen_response.format(name=victim.global_name, tag=victim.mention)
    return chosen_response

async def invoke_nickname_rule(interaction: discord.Interaction, victim: discord.Member, new_name: str):  
    #dm restriction
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.channel.send("we are literally in DMs rn bro u cant do that here...")
        return
    try:
        await change_nickname(interaction, victim, new_name)
    except Exception as e:
        log_error(e)
        await interaction.response.send_message(f"Failed to change nickname: {e}")