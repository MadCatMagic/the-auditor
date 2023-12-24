# bot.py
# modules
from dotenv import load_dotenv
# from discord import Member, Embed, File
import discord
from discord import Intents, Activity, ActivityType
from discord.ext.commands import Context, Bot, MissingPermissions, MissingRequiredArgument, CommandNotFound, EmojiConverter, EmojiNotFound
from os import getenv
from datetime import datetime
from traceback import print_tb

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

import re
@bot.command(name="count")
async def count_command(ctx: Context, channel: discord.TextChannel):
    iterator = channel.history(limit=None, after=datetime(year=2023,month=1,day=1))
    senders: dict[int, int] = {}
    wordDict: dict[str, int] = {}
    emojiDict: dict[str, int] = {}
    reactionDict: dict[str, int] = {}
    mostReactedMessages: list[tuple[int, discord.Message]] = []

    async for message in iterator:
        # count words, filtering out things which look like emojis (have a colon either side of the word)
        emojis = re.findall("[:][a-zA-Z_~+0-9]*[:]", message.content)
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
                reactionDict[em] = r.count
            else:
                reactionDict[em] += r.count
        
        # count most reacted messages
        reactions = 0
        for r in message.reactions:
            reactions += r.count
        if reactions > 0:
            mostReactedMessages.append((reactions, message))
            mostReactedMessages = sorted(mostReactedMessages, key=lambda x: x[0], reverse=True)[:3]
	
    # sort wordDict and stuff
    wordDictSorted = sorted(list(wordDict.items()), key=lambda x: x[1], reverse=True)[:10]
    emojiDictSorted = sorted(list(emojiDict.items()), key=lambda x: x[1], reverse=True)[:5]
    reactionDictSorted = sorted(list(reactionDict.items()), key=lambda x: x[1], reverse=True)[:5]

    # make message
    msg = "\n".join(f"{ctx.message.guild.get_member(id).display_name}: {num}" for id, num in senders.items())
    msg += "\n" + "\n".join(f"{w}: {c}" for w, c in wordDictSorted)
    msg += "\n" + "\n".join(f":{w}:: {c}" for w, c in emojiDictSorted)
    msg += "\n" + "\n".join(f"w: {c}" for w, c in reactionDictSorted)
    await ctx.send(msg)
    for i, (reactions, message) in enumerate(mostReactedMessages):
        await ctx.send(f"#{i + 1} with {reactions} reaction{'s' if reactions > 1 else ''}.", reference=message, mention_author=False)

# load .env file
load_dotenv()
TOKEN = getenv("DISCORD_TOKEN")
# run bot
bot.run(TOKEN)