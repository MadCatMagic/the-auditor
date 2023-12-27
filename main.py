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

from utilities import *

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
import emoji
linkRegex = re.compile("(?i)\\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\\s()<>{}\\[\\]]+|\\([^\\s()]*?\\([^\\s()]+\\)[^\\s()]*?\\)|\\([^\\s]+?\\))+(?:\\([^\\s()]*?\\([^\\s()]+\\)[^\\s()]*?\\)|\\([^\\s]+?\\)|[^\\s`!()\\[\\]{};:'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\\b/?(?!@)))")
def filterMessage(message: str, emojiDict: dict[str, int], wordDict: dict[str, int]) -> str:
    global linkRegex

    # filter out links
    links = linkRegex.findall(message)
    filtered = message
    for l in links:
        filtered = filtered.replace(l, "")

    # filter out discord custom emojis
    emojis = re.findall("[<][:][a-zA-Z_~+0-9]+[:][0-9]+[>]", filtered)
    for e in emojis:
        filtered = filtered.replace(e, "")

    # add all the unicode emojis
    filtered = emoji.demojize(filtered)
    emojisTrue = re.findall("[:][a-zA-Z_~+0-9]+[:]", filtered)
    for e in emojisTrue:
        filtered = filtered.replace(e, "")
    emojisTrue = map(emoji.emojize, emojisTrue)
    emojis.extend(emojisTrue)

    # count words
    words = re.findall("[a-zA-Z][a-zA-Z']*", filtered)
    for word in words:
        if word in wordDict:
            wordDict[word] += 1
        else:
            wordDict[word] = 1

    # count emojis
    for e in emojis:
        if len(e) < 3 and not emoji.is_emoji(e):
            continue
        if e in emojiDict:
            emojiDict[e] += 1
        else:
            emojiDict[e] = 1
    
    return filtered

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
    gifDict: dict[str, int] = {}
    mostReactedMessages: list[tuple[int, discord.Message]] = []

    async for message in messageIterator:
        # ignore the bot
        if message.author == bot.user:
            continue

        filtered = filterMessage(message.content, emojiDict, wordDict)

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

        # count all the gifs
        for embed in message.embeds:
            if embed.type == "gifv":
                print(embed.url)
                if embed.url in gifDict:
                    gifDict[embed.url] += 1
                else:
                    gifDict[embed.url] = 1
	
    # sort wordDict and stuff
    sendersSorted = sorted(list(senders.items()), key=lambda x: x[1], reverse=True)[:5]
    wordDictSorted = sorted(list(wordDict.items()), key=lambda x: x[1], reverse=True)[:20]
    emojiDictSorted = sorted(list(emojiDict.items()), key=lambda x: x[1], reverse=True)[:5]
    reactionDictSorted = sorted(list(reactionDict.items()), key=lambda x: x[1], reverse=True)[:3]
    gifDictSorted = sorted(list(gifDict.items()), key=lambda x: x[1], reverse=True)[:3]

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
    await ctx.send("*Top 3 most popular gifs:*")
    for i, (link, num) in enumerate(gifDictSorted):
        await ctx.send(f"#{i + 1}: {num} sent\n{link}")

# load .env file
load_dotenv()
TOKEN = getenv("DISCORD_TOKEN")
# run bot
bot.run(TOKEN)