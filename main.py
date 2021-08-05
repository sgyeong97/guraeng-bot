import asyncio, discord
from dice import *
from discord.ext import commands, tasks
from itertools import cycle
#키워드 알림기에 필요한 것 import
import configparser
import os
import embed_colors
import sys
from pytz import timezone
from datetime import datetime

prefix = "$"
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
    print("Ready")

@bot.command(aliases=["down"])
async def sleep(ctx):
    status_stop.start()

@bot.command(aliases=["up"])
async def getup(ctx):
    status_start.start()

@bot.command(aliases=["hi"])
async def hello(ctx):
    await ctx.send("hello")

@bot.command()
async def join(ctx):
    channel=ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def dice(ctx):
    await ctx.send("주사위를 굴립니다.")
    await ctx.send(dice())

@bot.command()
async def command(ctx, *, text = None):
    if(text != None):
        await ctx.send("접두사를 %s로 바꿀게!"%text)
        prefix = text
        bot = commands.Bot(command_prefix = prefix)
    else:
        await ctx.send("command 뒤에 바꾸길 원하는 접두사를 붙여줘")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("명령어를 찾지 못했습니다.")

#키워드 알림 기능
read_message_status = False

@bot.command()
async def read_message(ctx):
    if read_message_status == True:
        await ctx.send("키워드 알림 기능 종료!")
        read_message_status = False
    else
        await ctx.send("키워드 알림 기능 시작!")
        read_message_status = True

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.author.bot:
        return
    if read_message_status:
        await bot.process_commands(message)

        keyword_list_path=f"{os.path.dirname(os.path.realpath(__file__))}/keyword_list.txt"

        with open(keyword_list_path, "r", encoding="utf-8") as f:
            keywords=f.read().split("\n")
        push_path = f"{os.path.dirname(os.path.realpath(__file__))}/Push_notification.txt"

        with open(push_path, "r", encoding="utf-8") as f:
            push=f.read().split("\n")

        for i in keywords:
            if i in message.content:
                count = 0
                for y in pushs:
                    try:
                        embed=discord.Embed(title=


bot.run("ODcyMzgzMzQ5NDkzMjIzNDM0.YQpETg.cFNtAX-7wywqvH3mzY69Rr8l_PE")
