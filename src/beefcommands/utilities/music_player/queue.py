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
    status = await ctx.send("Queuing songs...")
    media_type = validate_input(url)
    if media_type == "invalid":
        await status.edit(content="invalid link")
        return
    
    ytlinks = await link_parser(ctx, url, media_type)
    if not ytlinks:
        await status.edit(content="failed to get youtube link")
        return
    
    queue = get_queue()
    added = 0
    print(ytlinks)
    
    for playlist in ytlinks:
        if insert == True: reversed(playlist)
        for track in playlist:
            if insert == True:
                queue.insert(0, track)
            else:
                print(f"appending {track}")
                queue.append(track)
            added += 1
    if added == 1:
        await status.edit(content=f"**{ctx.author.name}** added 1 track to the queue")
    else:
        await status.edit(content=f"**{ctx.author.name}** added {added} tracks to the queue")

async def qlist(ctx):
        queue = get_queue()
        if not queue:
            await ctx.send("the queue is empty")
            return
        
        content = ""
        
        for i in range(len(queue)):
            print(queue[i])
            if i < 10:
                content += f"**{i+1}**. {queue[i][1]}\n"
            else:
                content += f"... and {len(queue) - 10} more tracks."
                break
      
        listembed = discord.Embed(title="StewQueue", description="\n", color=discord.Color.orange())
        if get_current_track:
            listembed.add_field(name="", value=f"**Currently playing:** {get_current_track_title()}", inline=False) 
        listembed.add_field(name="", value=content)   
        await ctx.send(embed = listembed)   

async def qadd(ctx, *args):
        url = " ".join(args)
        await handle_queue(ctx, url, insert=False)

async def qinsert(ctx, *args):
        url = " ".join(args)
        await handle_queue(ctx, url, insert=True)

async def qpop():
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
        if get_loop_flag() == False:
            set_loop_flag(True)
            await ctx.send(f"toggled loop **ON**")
            print(get_loop_flag())
        else:
            set_loop_flag(False)
            await ctx.send(f"toggled loop **OFF**")
            print(get_loop_flag())
            
        
    
    
            
