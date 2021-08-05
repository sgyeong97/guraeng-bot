import asyncio, discord
from dice import *
from discord.ext import commands, tasks
from itertools import cycle
#키워드 알림기에 필요한 것 import

prefix = "#"
bot = commands.Bot(command_prefix = prefix)
dream = cycle(["꿈나라 여행-", "잠은 잘 자야해", "잘자고 일어나서 봐"])
work = cycle(["구랭 굴러다니며 활동","데굴데굴","공과 물아일체"])

@tasks.loop(seconds=30)
async def status_start():
    await bot.change_presence(activity=discord.Game(next(work)))

@tasks.loop(seconds=30)
async def status_stop():
    await bot.change_presence(activity=discord.Game(next(dream)),status=discord.Status.idle)

@bot.event
async def on_ready():
    status_start.start()
    print("Guraeng-bot run")
    print("Ready")

@bot.command()
async def help():
    await ctx.send("개발중이라 도울 수 없-다")

@bot.command(aliases=["down"])
async def sleep(ctx):
    print("command_sleep")
    status_stop.start()

@bot.command(aliases=["up"])
async def getup(ctx):
    print("command_getup")
    status_start.start()

@bot.command(aliases=["hi"])
async def hello(ctx):
    print("say hello")
    await ctx.send("hello")

@bot.command()
async def join(ctx):
    print("voice channel join")
    channel=ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    print("voice channel leave")
    await ctx.voice_client.disconnect()

@bot.command()
async def dice(ctx):
    print("dice")
    await ctx.send("주사위를 굴립니다.")
    await ctx.send(dice())
    print("dice roll")

@bot.command()
async def command(ctx, *, text = None):
    print("command")
    if(text != None):
        await ctx.send("접두사를 %s로 바꿀게!"%text)
        prefix = text
        bot = commands.Bot(command_prefix = prefix)
    else:
        await ctx.send("command 뒤에 바꾸길 원하는 접두사를 붙여줘")

@bot.event
async def on_command_error(ctx, error):
    print("on_command_error")
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("명령어를 찾지 못했습니다.")

bot.run("ODcyMzgzMzQ5NDkzMjIzNDM0.YQpETg.cFNtAX-7wywqvH3mzY69Rr8l_PE")
