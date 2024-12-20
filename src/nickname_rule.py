import random
import discord
from json_handling import load_element

#nickname rule, handles logic for they call you slash command
async def change_nickname(ctx, victim: discord.Member, new_name: str):
    #checks to see if the interaction is through an interaction object or a message object, effectivly switches between using the slash command and having the command run inline
        if isinstance(ctx, discord.Interaction):
            interaction = ctx
            # not allowed to rename the bot
            if victim.id != 1283805971524747304:
                # not allowed to rename yourself
                if victim.id == interaction.user.id:
                    await interaction.response.send_message(f"**{interaction.user.name}** tried to invoke the rule on themselves... for some reason")
                else:
                    try:
                        await victim.edit(nick=new_name)
                        await interaction.response.send_message(f"**{interaction.user.name}** invoked the rule on **{victim.name}**!\n{await nicknameprint(victim)}")           
                    except discord.Forbidden as e:
                        print(e)
                        await interaction.response.send_message(f"**{interaction.user.name}** tried to invoked the rule on **{victim.name}**!\nbut it didnt work :( next time get some permissions pal")
                    except Exception as e:
                        print(e)
            else:
                await interaction.response.send_message(f"**{interaction.user.name}** tried to invoked the rule on **{victim.name}**!\nnice try fucker...")
                
        elif isinstance(ctx, discord.Message):
            message = ctx
            # not allowed to rename the bot
            if victim.id != 1283805971524747304:
                # not allowed to rename yourself
                if victim.id == message.author.id:
                    await message.channel.send(f"**{message.author.name}** tried to invoke the rule on themselves... for some reason")
                else:
                    try:
                        await victim.edit(nick=new_name)
                        await message.channel.send(f"**{message.author.name}** invoked the rule on **{victim.name}**!\n{await nicknameprint(victim)}")
                    except Exception as e:
                        print(e)
                        await message.channel.send(f"**{message.author.name}** tried to invoked the rule on **{victim.name}**!\nbut it didnt work :( next time get some permissions okay?")
            else:
                await message.channel.send(f"**{message.author.name}** tried to invoked the rule on **{victim.name}**!\nnice try fucker...")


#test this
async def nicknameprint(victim: discord.Member): 
    victim_name = type('Victim', (object,), {"mention": victim.name})()
    responses = load_element("responses.json", "nickname_change_responses")
    
    chosen_response = random.choice(responses)
    chosen_response = chosen_response.format(victim=victim_name, tag=victim.mention)
    return chosen_response