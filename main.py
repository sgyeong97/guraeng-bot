import asyncio, discord
import json
import os
from dice import *
from discord.ext import commands, tasks
from itertools import cycle
#키워드 알림기에 필요한 것 import

dream = cycle(["꿈나라 여행-", "잠은 잘 자야해", "잘자고 일어나서 봐"])
work = cycle(["구랭 굴러다니며 활동","데굴데굴","공과 물아일체"])
notice_path = "https://gurae.notion.site/5c9c7fb8ba7d482786cf3f59f85d04d6"


def get_prefix(bot, message):
    with open(f'prefixes.json', "r") as f:
        prefixes = json.load(f)

    if str(message.guild.id) not in prefixes:
        return commands.when_mentioned_or('.')(bot, message)

    prefix = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(prefix)(bot, message)
    
bot = commands.Bot(command_prefix = get_prefix)

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

@bot.command(aliases=["down"])
async def sleep(ctx):
    print("command_sleep")
    status_stop.start()

@bot.command(aliases=["up"])
async def getup(ctx):
    print("command_getup")
    status_start.start()
@bot.command(aliases=["규칙"])
async def notice(ctx):
    print("send server notice url")
    guild_name = ctx.guild.name
    guild_icon = ctx.guild.icon_url
    embed=discord.Embed(description=":star2: 서버 규칙 :star2:", color=0xFF5733)
    embed.set_author(name=guild_name, url=notice_path)
    embed.set_thumbnail(url=guild_icon)
    embed.set_footer(text="위에 있는 서버 이름을 누르면 연결됩니다.\n자세한 내용은 서버 규칙 채널 확인 해주세요!")
    await ctx.send(embed=embed)

@bot.command()
async def chat(ctx):
    print("send channel chat")
    content = ctx.message.content
    if ctx.author.nick == None:
        nick = ctx.author.name
    else:
        nick = ctx.author.nick
    empty = content.split('/')
    #기본 채널 Chat에 만 보냄
    await ctx.send("해당 명령어는 하루에 한번으로 사용을 제한합니다.\n어기면 때찌 뛔찌")
    if len(empty) == 1:
        channel = bot.get_channel(870286437436768306)
        text = content.split(' ')[1:]
        contents = ''
        for x in text:
           contents += x+' '
        print(contents)
        embed = discord.Embed(description=":star2: {} ".format(contents), color=0xeeff4f)
        embed.set_author(name=nick)
        await channel.send(embed=embed)
    elif len(empty) >= 2:
        empty = content.split('/')
        empty2 = empty[0].split(' ')[1]
        channel_id = int(empty2)
        text = empty[1:]
        contents = ''
        for x in text:
            contents += x+' '
        print(channel_id, text)
        channel = bot.get_channel(channel_id)
        embed = discord.Embed(description=":star2: {}".format(contents), color=0xeeff4f)
        embed.set_author(name=nick)
        await channel.send(embed=embed)
    else:
        print("오류발생")
        channel = bot.get_channel(870286437436768306)
        await channel.send("사용자 {} ```{}```\nChat명령어 사용에 알 수 없는 오류 발생".format(nick, content))
        await ctx.send("오류발생 명령어 확인 또는 Guraeng 에게 문의")

@bot.command(aliases=["hi"])
async def hello(ctx):
    print("say hello")
    await ctx.send("hello")

#명령어 접두사 변경
@bot.command(name="repre")
async def change_prefix(ctx, new_prefix=None):
    print("change_prefix")

    if not ctx.guild:
        await ctx.send("DM기능 미지원")
        return

    if new_prefix is None:
        await ctx.send("공백은 지원하지 않습니다.")
        return

    with open(f'prefixes.json','r') as f:
        prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix

    with open(f'prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent='\t')

    await ctx.send(f"{new_prefix}로 변경되었습니다.")
#접두사 초기화
@bot.command(name="oripre")
async def change_prefix(ctx):
    print("ini prefixe")
    if not ctx.guild:
        await ctx.send("DM기능 미지원")
        return
    with open(f'prefixes.json', 'r') as f:
        prefixes = json.load(f)
    if str(ctx.guild.id) not in prefixes:
        await ctx.send("초기의 # 접두사 그대로 입니다.")
        return
    prefixes.pop(ctx.guild.id)

    with open(f'prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent='\t')

    await ctx.send("접두사 '#'로 초기화 완료")

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

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("명령어를 찾지 못했습니다.")
        print("on_command_error")

bot.run("ODcyMzgzMzQ5NDkzMjIzNDM0.YQpETg.cFNtAX-7wywqvH3mzY69Rr8l_PE")
