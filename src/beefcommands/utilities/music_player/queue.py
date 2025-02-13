import random
import discord
from beefcommands.utilities.music_player.link_parser import validate_input, link_parser

g_queue = []
g_current_track = [(None, "Nothing")]
g_loop = False

def get_queue():
        return g_queue
    
def clear_queue():
    g_queue.clear()
    
def get_current_track():
    return g_current_track

def get_current_track_link():
    return g_current_track[0][0]

def get_current_track_title():
    return g_current_track[0][1]

def set_current_track(track):
    g_current_track.clear()
    g_current_track.append(track)
    
def clear_current_track():
    g_current_track.clear()
    
def get_loop_flag():
    return g_loop

def set_loop_flag(value):
    global g_loop 
    g_loop = value
    
async def handle_queue(ctx, url, insert):
    # send the status message
    status = await ctx.send("Queuing songs...")
    
    # validate the url
    media_type = validate_input(url)
    if media_type == "invalid":
        await status.edit(content="invalid link")
        return
    
    # retrive the youtube links from the given query
    ytlinks = await link_parser(ctx, url, media_type)
    if not ytlinks:
        await status.edit(content="failed to get youtube link")
        return
    
    queue = get_queue()
    added = 0
    
    # unwrap the arrays returned by the link parser and add each tuple to the queue, inserting if insert = true
    for playlist in ytlinks:
        if insert == True: playlist = reversed(playlist)
        for track in playlist:
            # insert at the front
            if insert == True:
                queue.insert(0, track)
            
            # push to the back
            else:
                queue.append(track)
            added += 1
    if added == 1:
        await status.edit(content=f"**{ctx.author.name}** added 1 track to the queue")
    else:
        await status.edit(content=f"**{ctx.author.name}** added {added} tracks to the queue")

async def qlist(ctx):
    # retrive the queue array
        queue = get_queue()
        if not queue:
            await ctx.send("the queue is empty")
            return
        
        content = ""
        
        # for each song in the queue up to a limit of 10, print just the title with an index number and add it to the content
        for i in range(len(queue)):
            if i < 10:
                content += f"**{i+1}**. {queue[i][1]}\n"
            else:
                # add if there are more than 10 songs
                content += f"... and {len(queue) - 10} more tracks."
                break
      
      # generate the list embed
        listembed = discord.Embed(title="StewQueue", description="\n", color=discord.Color.orange())
        
        # list the current track if there is one
        if get_current_track():
            listembed.add_field(name="", value=f"**Currently playing:** {get_current_track_title()}", inline=False) 
        listembed.add_field(name="", value=content)   
        await ctx.send(embed = listembed)   

async def qadd(ctx, *args):
    # handle the arbitrary arguments and add to the back of the queue
        url = " ".join(args)
        await handle_queue(ctx, url, insert=False)

async def qinsert(ctx, *args):
    # handle the arbitrary arguments and insert to the front of the queue (unused and superceded by /play i think)
        url = " ".join(args)
        await handle_queue(ctx, url, insert=True)

async def qpop():
    # retrive the first item off of the queue
        queue = get_queue()
        if queue:
            queue.pop(0)
            
async def qclear(ctx):
        get_queue().clear()
        await ctx.send(f"**{ctx.author.name}** cleared the queue")
        
async def qshuffle(ctx):
        queue = get_queue()
        random.shuffle(queue)
        await ctx.send(f"**{ctx.author.name}** shuffled the queue")

async def qloop(ctx):
    # toggle loop flag if its off, and off if its on
        if get_loop_flag() == False:
            set_loop_flag(True)
            await ctx.send(f"toggled loop **ON**")
        else:
            set_loop_flag(False)
            await ctx.send(f"toggled loop **OFF**")
            
        
    
    
            
