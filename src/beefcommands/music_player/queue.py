import random
import discord
from beefcommands.music_player import link_parser

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

async def handle_queue(user, tx_channel, url, insert):
    # send the status message
    status = await tx_channel.send("Queuing songs...")

    # validate the url
    media_type = link_parser.validate_input(url)
    if media_type == "invalid":
        await status.edit(content="invalid link")
        return

    # retrieve the youtube links from the given query
    ytlinks = await link_parser.parse(tx_channel, url, media_type)
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
        await status.edit(content=f"**{user.name}** added **{track[1]}** to the queue")
    else:
        await status.edit(content=f"**{user.name}** added {added} tracks to the queue")

async def qlist(tx_channel):
    # retrieve the queue array
        queue = get_queue()
        if not queue and not g_current_track:
            await tx_channel.send("the queue is empty")
            return

        content = ""

        # for each song in the queue up to a limit of 10, print just the title with an index number and add it to the content
        if queue:
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
        await tx_channel.send(embed = listembed)

async def qadd(user, tx_channel, *args):
    # handle the arbitrary arguments and add to the back of the queue
        url = " ".join(args)
        await handle_queue(user, tx_channel, url, insert=False)

async def qinsert(user, tx_channel, *args):
    # handle the arbitrary arguments and insert to the front of the queue (unused and superceded by /play i think)
        url = " ".join(args)
        await handle_queue(user, tx_channel, insert=True)

async def qpop():
    # retrieve the first item off of the queue
        queue = get_queue()
        if queue:
            queue.pop(0)

async def qclear():
        get_queue().clear()

async def qshuffle(user, tx_channel):
        queue = get_queue()
        random.shuffle(queue)
        await tx_channel.send(f"**{user.name}** shuffled the queue")

async def qloop(tx_channel):
    # toggle loop flag if its off, and off if its on
        if get_loop_flag() == False:
            set_loop_flag(True)
            await tx_channel.send(f"toggled loop **ON**")
        else:
            set_loop_flag(False)
            await tx_channel.send(f"toggled loop **OFF**")





