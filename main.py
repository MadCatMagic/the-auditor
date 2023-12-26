# bot.py
# modules
from dotenv import load_dotenv
# from discord import Member, Embed, File
import discord
from discord import Intents, Activity, ActivityType
from discord.ext.commands import Context, Bot, MissingPermissions, MissingRequiredArgument, CommandNotFound, EmojiConverter, EmojiNotFound
from os import getenv
from traceback import print_tb
import datetime

# create bot
intents = Intents().all()
bot = Bot(command_prefix='?', intents=intents)

# bot connection ready function
@bot.event
async def on_ready():
	
    print(f"{bot.user.name} has connected to discord")
    await bot.change_presence(activity=Activity(type=ActivityType.watching, name="and waiting"))

@bot.event
async def on_message(message: discord.Message):
    await bot.process_commands(message)

# error handling
@bot.event
async def on_command_error(ctx, error):
    # missing perms
    if isinstance(error, MissingPermissions):
        text = ":exclamation:Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
        await ctx.send(text)
    # missing args
    elif isinstance(error, MissingRequiredArgument):
        text = ":exclamation:Command requires argument `{}`".format(error.param)
        await ctx.send(text)
    # invalid command
    elif isinstance(error, CommandNotFound):
        text = ":exclamation:Unknown command"
        await ctx.send(text)
    else:
        print(error)
        print_tb(error.__traceback__)

@bot.event
async def on_member_join(member: discord.Member):
	pass

from typing import TypeVar, Callable, Any
T = TypeVar('T')
def pprintMatrix(matrix: list[list[T]], prefix: str = "", spaces: int = 0, converter: Callable[[T], str] = str, returnAsString: bool = False) -> None | str:
    s = [[converter(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = (" " * spaces).join('{{:{}}}'.format(x) for x in lens)
    table = [prefix + fmt.format(*row) for row in s]
    res = '\n'.join(table)
    if returnAsString:
        return res
    print(res)

def splitIntoArray(array: list[Any], every: int) -> list[list[Any]]:
    arr = []
    for i in range(len(array) // every + 1):
        t = [v[1] for v in zip(range(every), array[i * every : i * every + every])]
        if t != []:
            arr.append(t)
    return arr

import re
@bot.command(name="count")
async def count_command(ctx: Context, channel: discord.TextChannel):
    # find the time
    # need to account for leap years
    currentTime = datetime.datetime.now()
    yearLength = 365
    if currentTime.year % 4 == 0 and (currentTime.year % 400 == 0 or currentTime.year % 100 != 0):
        yearLength += 1
    lastTime = currentTime - datetime.timedelta(days=yearLength)

    messageIterator = channel.history(limit=None, after=lastTime)
    senders: dict[int, int] = {}
    wordDict: dict[str, int] = {}
    emojiDict: dict[str, int] = {}
    reactionDict: dict[str, int] = {}
    mostReactedMessages: list[tuple[int, discord.Message]] = []

    async for message in messageIterator:
        # ignore the bot
        if message.author == bot.user:
            continue
        # count words, filtering out things which look like emojis (have a colon either side of the word)
        emojis = re.findall("[:][a-zA-Z_~+0-9]+[:]", message.content)
        filtered = message.content
        for e in emojis:
            filtered = filtered.replace(e, "")
        words = re.findall("[a-zA-Z][a-zA-Z']*", filtered)
        for word in words:
            if word in wordDict:
                wordDict[word] += 1
            else:
                wordDict[word] = 1

        # count emojis
        #econverter = EmojiConverter()
        for e in emojis:
            if len(e) < 3:
                continue
            try:
                #await econverter.convert(ctx, e[1:-1])
                if e in emojiDict:
                    emojiDict[e] += 1
                else:
                    emojiDict[e] = 1
            except EmojiNotFound as e:
                print(e)

        # count user messages
        if message.author.id not in senders:
            senders[message.author.id] = 1
        else:
            senders[message.author.id] += 1

        # count reactions
        for r in message.reactions:
            em = str(r.emoji)
            if em in reactionDict:
                reactionDict[em] += r.count
            else:
                reactionDict[em] = r.count
        
        # count most reacted messages
        reactions = 0
        for r in message.reactions:
            reactions += r.count
        if reactions > 0:
            mostReactedMessages.append((reactions, message))
            mostReactedMessages = sorted(mostReactedMessages, key=lambda x: x[0], reverse=True)[:3]
	
    # sort wordDict and stuff
    sendersSorted = sorted(list(senders.items()), key=lambda x: x[1], reverse=True)[:5]
    wordDictSorted = sorted(list(wordDict.items()), key=lambda x: x[1], reverse=True)[:20]
    emojiDictSorted = sorted(list(emojiDict.items()), key=lambda x: x[1], reverse=True)[:5]
    reactionDictSorted = sorted(list(reactionDict.items()), key=lambda x: x[1], reverse=True)[:3]

    splitWordDict = [[f"{a}: {b}" for a, b in line] for line in splitIntoArray(wordDictSorted, 4)]
    if len(splitWordDict[-1]) < 4:
        splitWordDict[-1].extend(["" for _ in range(4 - len(splitWordDict[-1]))])

    # make message
    msg = f"**--- Discord Stats from {lastTime.date()} to today ---**\n"
    msg += "*Top 5 most sendiferous people on the server:*\n"
    msg += "\n".join(f"    \\- {ctx.message.guild.get_member(id).display_name}: {num}" for id, num in sendersSorted)
    msg += "\n*Top 20 most popular words:*\n```"
    msg += pprintMatrix(splitWordDict, spaces=2, returnAsString=True)
    msg += "```\n*Top 5 most popular emojis:*\n"
    msg += "\n".join(f"    \\- {w}: {c}" for w, c in emojiDictSorted)
    msg += "\n*Top 5 most popular reaction:*\n"
    msg += "\n".join(f"    \\- {w}: {c}" for w, c in reactionDictSorted)
    msg += "\n*Top 3 most reacted messages:*"
    print(msg)
    await ctx.send(msg)
    for i, (reactions, message) in enumerate(mostReactedMessages):
        await ctx.send(f"#{i + 1} with {reactions} reaction{'s' if reactions > 1 else ''}.", reference=message, mention_author=False)

# load .env file
load_dotenv()
TOKEN = getenv("DISCORD_TOKEN")
# run bot
bot.run(TOKEN)