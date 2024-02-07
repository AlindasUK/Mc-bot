from discord.ext import tasks, commands
import discord
import time
from random import randint 
import datetime

now = datetime.datetime.now()
displaytime = now.strftime("%Y-%m-%d %H:%M:%S")

global msglog
msglog = {}

dcbot = commands.Bot(command_prefix='>')
dcbot.remove_command('help')

colourlist = [0x1742cf, 0xd9271a, 0x2dd91a, 0x961ad9, 0xd91a86]

global sendlist
sendlist = []

global kekvar
kekvar = False

@tasks.loop(seconds=0.7)
async def senditall():
    print("loop is called")
    channel = dcbot.get_channel(channelid)
    channel2 = dcbot.get_channel(channelid)
    for x in sendlist:
        print("tries to send embed")
        await channel.send(embed=x)
        await channel2.send(embed=x)
        sendlist.remove(x)

@dcbot.event
async def on_message(message):
    if (str(message.channel.id) == "channelid") and (message.author.id != authorid):
        if "mfbot" in globals():
            mfbot.chat(f"[{message.author.name} > {message.content}]")
    elif (str(message.channel.id) == "channelid") and (message.author.id != authorid):
        if "mfbot" in globals():
            mfbot.chat(f"[{message.author.name} > {message.content}]")

@dcbot.event
async def on_ready():
    senditall.start()

    # You need to replace the channelid with the actual channel ID where you want to send messages.
    channel = dcbot.get_channel(channelid)

    global mineflayer
    global pathfinder

    mineflayer = require('mineflayer')
    pathfinder = require('mineflayer-pathfinder')

    RANGE_GOAL = 1
    BOT_USERNAME = 'mail'

    global mfbot

    mfbot = mineflayer.createBot({
        'host': 'serverip',
        'username': "username",
        'password': 'password',
        'version': 'version',
        'auth': 'microsoft'
    })
    mfbot.loadPlugin(pathfinder.pathfinder)

    @On(mfbot, 'spawn')
    def handle(*args):
        mcData = require('minecraft-data')(mfbot.version)
        movements = pathfinder.Movements(mfbot, mcData)

        pos = mfbot.entity.position

        x = [pos.x + 1, pos.y, pos.z + 1]
        mfbot.pathfinder.setMovements(movements)
        mfbot.pathfinder.setGoal(pathfinder.goals.GoalNear(x[0], x[1], x[2], RANGE_GOAL))
        print(f"Bot Connected to server")

    @On(mfbot, 'chat')
    def handleMsg(this, sender, message, *args):
        if str(int(time.time()/10)) + str(message) in msglog.keys():
            pass
        else:
            msglog[str(int(time.time()/10)) + str(message)] = True
            if (sender != "botname") and (sender != "Server"):
                msg = f"{message} \n{displaytime}"
                print("tries to append sendlist")
                sendlist.append(discord.Embed(title=sender, description=msg, color=colourlist[randint(0, 4)]))

# Replace with your actual bot token
dcbot.run("YOUR_BOT_TOKEN")
