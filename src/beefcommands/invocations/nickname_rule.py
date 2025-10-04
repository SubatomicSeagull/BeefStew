import random
import discord
import os
from beefutilities.IO.json_handling import load_element
from beefutilities import TTS
from data.postgres import log_error

# nickname rule, handles logic for they call you slash command
async def change_nickname(ctx, victim: discord.Member, new_name: str, self_invoke = False):
    # checks to see if the interaction is through an interaction object or a message object, effectively switches between using the slash command and having the command run inline
        if isinstance(ctx, discord.Interaction):
            interaction = ctx
            # not allowed to rename the bot
            if victim.id != os.getenv("CLIENTID"):
                # not allowed to rename yourself
                if victim.id == interaction.user.id and self_invoke == False:
                    await interaction.response.send_message(f"**{interaction.user.name}** tried to invoke the rule on themselves... for some reason")
                else:
                    try:
                        print(f"> \033[32m{interaction.user.name} invoked the rule on {victim.name}\033[0m")
                        await victim.edit(nick=new_name)
                        response = await print_nickname(victim)
                        await interaction.response.send_message(f"**{interaction.user.name}** invoked the rule on **{victim.global_name}**!\n{response}")
                        await TTS.speak_output(interaction, f"{interaction.user.name} invoked the rule on {victim.global_name}!{response}")
                    except discord.Forbidden as e:
                        print(f"\031[32mError while trying to invoke the rule: {e}\033[0m")
                        await interaction.response.send_message(f"**{interaction.user.name}** tried to invoked the rule on **{victim.global_name}**!\nbut it didnt work :( next time get some permissions pal")
                    except Exception as e:
                        print(f"\031[32mError while trying to invoke the rule: {e}\033[0m")

            else:
                await interaction.response.send_message(f"**{interaction.user.name}** tried to invoked the rule on **{victim.global_name}**!\nnice try fucker...")
                await TTS.speak_output(interaction, f"{interaction.user.name} tried to invoked the rule on {victim.global_name}! nice try fucker...")

        elif isinstance(ctx, discord.Message):
            message = ctx
            # not allowed to rename the bot
            if victim.id !=os.getenv("CLIENTID"):
                # not allowed to rename yourself
                if victim.id == message.author.id and self_invoke == False:
                    await message.channel.send(f"**{message.author.name}** tried to invoke the rule on themselves... for some reason")
                else:
                    try:
                        print(f"> \033[32m{message.author.name} invoked the rule on {victim.name}\033[0m")
                        await victim.edit(nick=new_name)
                        response = await print_nickname(victim)
                        await message.channel.send(f"**{message.author.name}** invoked the rule on **{victim.global_name}**!\n{response}")
                        await TTS.speak_output(interaction, f"{interaction.user.name} invoked the rule on {victim.global_name}!{response}")

                    except Exception as e:
                        print(f"\031[32mError while trying to invoke the rule: {e}\033[0m")
                        await message.channel.send(f"**{message.author.name}** tried to invoked the rule on **{victim.global_name}**!\nbut it didnt work :( next time get some permissions okay?")
            else:
                await message.channel.send(f"**{message.author.name}** tried to invoked the rule on **{victim.global_name}**!\nnice try fucker...")

async def print_nickname(victim: discord.Member):
    # load responses.json
    responses = load_element("responses.json", "nickname_change_responses")

    chosen_response = random.choice(responses)
    chosen_response = chosen_response.format(name = victim.global_name, tag = victim.mention)
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