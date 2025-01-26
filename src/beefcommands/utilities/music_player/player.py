import discord

loop = False

async def play_queue(self, interaction: discord.Interaction):
    await interaction.response.send_message("not implemented yet sorry :(")
    #try to read the first item in the queue
    #join the channel if its not there already
    #play the first item in the queue
    #if loop is true, play that song again
    #if loop is false, remove the item from the queue when the track is over
    #check if the queue is empty, 
    # if not play the next item, if it is then call leave voice channel
    
async def play_next(self, interaction: discord.Interaction):
    await interaction.response.send_message("not implemented yet sorry :(")
    #sanitise the link through the link parser
    #if it checks out add it to the queue at the front
    #play the queue if its not already playing
    
async def pause(self, interaction: discord.Interaction):
    await interaction.response.send_message("not implemented yet sorry :(")
    #check if the player is playing
    #pause the video playback if it is
    
async def skip(self, interaction: discord.Interaction):
    await interaction.response.send_message("not implemented yet sorry :(")
    #check if the player is playing
    #stop the playback and remove the current item from the queue.
    #play the queue again
    

async def loop_queue(self, interaction: discord.Interaction):
    await interaction.response.send_message("not implemented yet sorry :(")
    #sets loop to true
