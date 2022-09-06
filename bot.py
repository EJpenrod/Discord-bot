import nextcord
from nextcord.ext import commands
import wavelink
import os

intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
path = "C:/Users/notlykedis/Desktop/Dbd/surv"
files = os.listdir(path)
for file in files:
    if file.endswith(('.jpg', '.png', 'jpeg')):
        image_path = path + file


@bot.event
async def on_ready():
    print("Bot is ready")
    bot.loop.create_task(node_connect())


@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f"Node {node.identifier} is ready!")


@bot.event
async def on_wavelink_track_end(player: wavelink.Player, track: wavelink.Track, reason):
    ctx = player.ctx
    vc: player = ctx.voice_client
    if vc.loop:
        return await vc.play(track)
    next_song = vc.queue.get()
    await vc.play(next_song)
    emb = nextcord.Embed(title="Now Playing",
                         description=f"{next_song.title}", color=nextcord.Color.green())
    await ctx.send(embed=emb)


async def play_next(ctx):
    if not ctx.voice_client.is_playing():
        next_song = ctx.voice_client.queue.get()
        await ctx.voice_client.play(next_song)
        emb = nextcord.Embed(title="Now Playing",
                             description=f"{next_song.title}", color=nextcord.Color.green())
        await ctx.send(embed=emb)
    else:
        await ctx.voice_client.stop()
        return ctx.send("Queue is empty")


async def node_connect():
    await bot.wait_until_ready()
    await wavelink.NodePool.create_node(bot=bot, host="lavalink.oops.wtf", port=443, password="www.freelavalink.ga", https=True)


@bot.command(aliases=["p"])
async def play(ctx, *, search: wavelink.YouTubeTrack):
    if not ctx.voice_client:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    elif not getattr(ctx.author.voice, "channel", None):
        embed = nextcord.Embed(
            description=f"{ctx.author.mention}: No song(s) are playing.", color=nextcord.Color.blue())
        return await ctx.send(embed=embed)
    else:
        vc: wavelink.Player = ctx.voice_client

    if vc.queue.is_empty and vc.is_connected and vc._source is None:
        await vc.play(search)
        embe = nextcord.Embed(
            description=f"Now playing [{search.title}]({search.uri}) ", color=nextcord.Color.green())

        embe.set_image(url=search.thumbnail)
        await ctx.send(embed=embe)
    else:
        print("Added to queue")
        await vc.queue.put_wait(search)
        emb = nextcord.Embed(
            description=f"Added [{search.title}]({search.uri}) to the queue.", color=nextcord.Color.green())

        emb.set_image(url=search.thumbnail)
        await ctx.send(embed=emb)
    vc.ctx = ctx
    setattr(vc, "loop", False)


@bot.command()
async def queue(ctx):
    if not ctx.voice_client:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    elif not getattr(ctx.author.voice, "channel", None):
        embed = nextcord.Embed(
            description=f"{ctx.author.mention}: No song(s) are playing.", color=nextcord.Color.blue())
        return await ctx.send(embed=embed)

    else:
        vc: wavelink.Player = ctx.voice_client

    if vc.queue.is_empty:
        emb = nextcord.Embed(
            description=f"{ctx.author.mention}: The queue is empty. Try adding songs.", color=nextcord.Color.red())
        return await ctx.send(embed=emb)
    lp = nextcord.Embed(title="Queue", color=nextcord.Color.blue())
    queue = vc.queue.copy()
    song_count = 0
    for song in queue:
        song_count += 1
        lp.add_field(name=f"[{song_count}] Song", value=f"{song.title}")
        return await ctx.send(embed=lp)


@bot.command(name="stop", aliases=["s"])
async def stop(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("I am not connected to a voice channel.")
    await ctx.voice_client.stop()
    await ctx.send("Stopped playing.")


@bot.command(name="pause")
async def pause(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("I am not connected to a voice channel.")
    await ctx.voice_client.pause()
    await ctx.send("Paused the player.")


@bot.command(name="resume", aliases=["unpause", "continue"])
async def resume(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("I am not connected to a voice channel.")
    await ctx.voice_client.resume()
    await ctx.send("Resumed the player.")


@bot.command(name="skip", aliases=["s-"], pass_context=True)
async def skip(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("I am not connected to a voice channel.")
    await ctx.voice_client.pause()
    await play_next(ctx)
    await ctx.send("Skipped the song.")


@bot.command(name="disconnect", aliases=["dc", "leave"])
async def disconnect(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("I am not connected to a voice channel.")
    await ctx.voice_client.disconnect()
    await ctx.send("Disconnected from the voice channel.")


@bot.command()
async def seek(ctx: commands.Context, time: int):
    if not ctx.voice_client:
        return await ctx.send("I am not connected to a voice channel.")
    await ctx.voice_client.seek(time)
    await ctx.send(f"Seeked to {time} seconds.")


@ bot.command()
async def join(ctx: commands.Context):
    if not ctx.author.voice:
        return await ctx.send("You are not connected to a voice channel.")
    channel = ctx.author.voice.channel
    await channel.connect()


bot.run("YOUR DISCORD BOT KEY GOES HERE if you dont know how to get the key go to the readme and follow the link to discord dev. website and go to get started")
