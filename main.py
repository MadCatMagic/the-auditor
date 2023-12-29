# bot.py
# modules
from dotenv import load_dotenv
# from discord import Member, Embed, File
import discord
from discord import Intents, Activity, ActivityType
from discord.ext.commands import Context, Bot, MissingPermissions, MissingRequiredArgument, CommandNotFound, has_permissions
from os import getenv
from traceback import print_tb
import datetime

from utilities import *
from plot import *

# create bot
intents = Intents().all()
bot = Bot(command_prefix='?', intents=intents, help_command=None)

# bot connection ready function
@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to discord")
    await bot.change_presence(activity=Activity(type=ActivityType.watching, name="and waiting"))

#@bot.event
#async def on_message(message: discord.Message):
#    await bot.process_commands(message)

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

#@bot.event
#async def on_member_join(member: discord.Member):
#	pass
        
@bot.command(name="help")
async def help_command(ctx: Context):
    await ctx.send("The only thing I do is `?count`... but you need to be an admin to ask me to!")

# get positive/negative word lists
with open("positive-words.txt", "r") as f:
    positiveWords = {word.strip() for word in f.read().splitlines()}
with open("negative-words.txt", "r") as f:
    negativeWords = {word.strip() for word in f.read().splitlines()}

import re
import emoji
linkRegex = re.compile("(?i)\\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\\s()<>{}\\[\\]]+|\\([^\\s()]*?\\([^\\s()]+\\)[^\\s()]*?\\)|\\([^\\s]+?\\))+(?:\\([^\\s()]*?\\([^\\s()]+\\)[^\\s()]*?\\)|\\([^\\s]+?\\)|[^\\s`!()\\[\\]{};:'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\\b/?(?!@)))")
def filterMessage(message: str, emojiCounter: counter, wordCounter: counter) -> tuple[str, int, int, int]:
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
    emojisTrue = list(c for c, _ in emoji.analyze(filtered))
    for e in emojisTrue:
        filtered = filtered.replace(e, "")
    emojis.extend(emojisTrue)

    # count words and positivity
    positivityScore = 0
    words = re.findall("[a-zA-Z][a-zA-Z']*", filtered)
    for word in words:
        # count words equal regardless of case
        wordCounter.count(word.lower())
        if word.lower() in positiveWords:
            positivityScore += 1
        if word.lower() in negativeWords:
            positivityScore -= 1

    # count emojis
    for e in emojis:
        if len(e) < 3 and not emoji.is_emoji(e):
            continue
        emojiCounter.count(e)
    
    return filtered.strip(), len(words), len(emojis), positivityScore

def GetNameFromID(id: int, ctx: Context | None = None) -> str:
    if ctx != None:
        memb = ctx.message.guild.get_member(id)
        if memb != None:
            return memb.display_name
    user = bot.get_user(id)
    # special exception since he apparently keeps turning up
    if id == 627852809693429780:
        return "brug (deceased)"
    if user == None:
        return "[unknown user]"
    return user.display_name

@bot.command(name="count")
@has_permissions(administrator=True)
async def count_command(ctx: Context):
    # let them know it is working
    await ctx.send("`processing...`")

    # find the time
    # need to account for leap years
    currentTime = datetime.datetime.now()
    yearLength = 365
    if currentTime.year % 4 == 0 and (currentTime.year % 400 == 0 or currentTime.year % 100 != 0):
        yearLength += 1
    lastTime = currentTime - datetime.timedelta(days=yearLength)

    senders = counter()
    sendersNotAttachments = counter()
    sendersTotalLength = counter()
    wordCounter = counter()
    emojiCounter = counter()
    reactionCounter = counter()
    gifCounter = counter()
    mostReactedMessages: list[tuple[int, discord.Message]] = []
    mostActiveDays = counter()

    positivityCounter = counter()
    allMessageCounters: dict[str, counter] = {}

    messagesSent = 0
    wordsTyped = 0
    gifsSent = 0
    emojisUsed = 0
    reactionsApplied = 0
    translation: dict[int, str] = {}

    # need to scan all of the channels
    for channel in ctx.guild.text_channels:
        # look through channel
        messageIterator = channel.history(limit=None, after=lastTime)
        async for message in messageIterator:
            # ignore the bot
            if message.author == bot.user:
                continue

            if message.author == None:
                print("NONE")
            elif message.author.id not in translation:
                translation[message.author.id] = message.author.display_name
            
            messagesSent += 1

            # count the day
            mostActiveDays.count(message.created_at.date())

            if message.author.bot:
                continue

            filteredMessage, wordsTypedInMessage, emojisUsedInMessage, positivityScore = filterMessage(message.content, emojiCounter, wordCounter)
            wordsTyped += wordsTypedInMessage
            emojisUsed += emojisUsedInMessage
            positivityCounter.count(message.author.id, positivityScore)

            # count user messages
            senders.count(message.author.id)
            if filteredMessage != "":
                sendersNotAttachments.count(message.author.id)
                sendersTotalLength.count(message.author.id, len(filteredMessage))

            # for most common message and sender award
            if message.content != "":
                if message.content in allMessageCounters:
                    allMessageCounters[message.content].count(message.author.id)
                else:
                    allMessageCounters[message.content] = counter()
                    allMessageCounters[message.content].count(message.author.id)

            # count reactions
            for r in message.reactions:
                em = str(r.emoji)
                reactionCounter.count(em, r.count)
            
            # count most reacted messages
            reactions = 0
            for r in message.reactions:
                reactions += r.count
            if reactions > 0:
                mostReactedMessages.append((reactions, message))
                mostReactedMessages = sorted(mostReactedMessages, key=lambda x: x[0], reverse=True)[:5]
            reactionsApplied += reactions

            # count all the gifs
            for embed in message.embeds:
                if embed.type == "gifv":
                    gifCounter.count(embed.url)
                    gifsSent += 1
	
    # sort each counter to get only the top results
    emojiCounterSorted = sorted(emojiCounter, key=lambda x: x[1], reverse=True)[:8]
    reactionCounterSorted = sorted(reactionCounter, key=lambda x: x[1], reverse=True)[:8]
    gifCounterSorted = sorted(gifCounter, key=lambda x: x[1], reverse=True)[:5]

    # images data
    sendersSorted = sorted(senders, key=lambda x: x[1])[-10:]
    sendersSorted = [(translation[id], n) for id, n in sendersSorted]
    wordCounterSorted = sorted(wordCounter, key=lambda x: x[1])[-40:]

    # create images
    # always creates in the temp dir so don't worry about that
    CreateHorizBarChart(wordCounterSorted, "words.png", 16)
    wordsImage = discord.File("temp/words.png")
    CreateHorizBarChart(sendersSorted, "senders.png")
    sendersImage = discord.File("temp/senders.png")
    
    CreateActivityBarChart(mostActiveDays, lastTime.date(), currentTime.date(), "activity.png")
    activityImage = discord.File("temp/activity.png")
    
    #splitWordDict = [[f"{a}: {b}" for a, b in line] for line in splitIntoArray(wordCounterSorted, 4)]
    #if len(splitWordDict[-1]) < 4:
    #    splitWordDict[-1].extend(["" for _ in range(4 - len(splitWordDict[-1]))])

    # make message
    msg = f"# --- Discord Stats from {lastTime.date()} to today ---\n*bingus my beloved*\n"
    msg += "\n### Top 10 most sendiferous people on the server:\n*what weirdos...*\n"
    #msg += "\n".join(f"    \\- {ctx.message.guild.get_member(id).display_name}: {num}" for id, num in sendersSorted)
    await ctx.send(msg, file=sendersImage)
    
    # integrate words data with first message
    msg = "\n### Most Popular Words this year:\n*all the words we will go*"
    await ctx.send(msg, file=wordsImage)
    #await ctx.send("**Most Popular Words this year:**\n*oh the words we will go*", file=wordsImage)

    # send activity data
    await ctx.send("### Daily activity over the past year:\n*on that sigma grindset*", file=activityImage)

    # awards
    msg = "## Time for the annual awards ceremony...\n*the most prestigious in the land*"

    positivityRanking = sorted(positivityCounter, key=lambda x: x[1])
    mostNegativePerson, mostPositivePerson = positivityRanking[0], positivityRanking[-1]
    msg += "\n### The devil and angel/nicest and naughtiest Awards"
    msg += f"\nAnd the award for most negativity goes to... *{translation[mostNegativePerson[0]]}*, with a score of *{mostNegativePerson[1]}*! We hate you :)"
    msg += f"\nAnd the award for most positivity goes to... *{translation[mostPositivePerson[0]]}*, with a score of *{mostPositivePerson[1]}*! We hate you too, sicko."
    if len(positivityRanking) > 1:
        secondMostNegativePerson, secondMostPositivePerson = positivityRanking[1], positivityRanking[-2]
        msg += f"\nIn the runner up positions: *{translation[secondMostNegativePerson[0]]}* with *{secondMostNegativePerson[1]}* for negativity and *{translation[secondMostPositivePerson[0]]}* with *{secondMostPositivePerson[1]}* for positivity. A round of unamusement to them all!"

    averageMessageLengths = sorted([(id, totMessageLength / numMessages) for (id, numMessages), (_, totMessageLength) in zip(sendersNotAttachments, sendersTotalLength) if numMessages >= 10], key=lambda x: x[1])
    
    longestAverageMessage = (translation[averageMessageLengths[-1][0]], averageMessageLengths[-1][1])
    msg += "\n### \"i ain't reading that essay\" Award"
    msg += f"\nAnd the award for the longest average message, an award created by Goose for the benefit of illiterates everywhere, goes to... *{longestAverageMessage[0]}*, with an average message length of *{round(longestAverageMessage[1])}*! shut the fuck up."
    if len(averageMessageLengths) > 1:
        secondLongestAverageMessage = (translation[averageMessageLengths[-2][0]], averageMessageLengths[-2][1])
        msg += f"\nAnd in the runner up position we have *{secondLongestAverageMessage[0]}* with an average of *{round(secondLongestAverageMessage[1])}* characters per message. Wow. Just, wow."

    allMessagesSorted = sorted(allMessageCounters.items(), key=lambda x: x[1].sum())
    mostCommonMessage = (allMessagesSorted[-1][0], allMessagesSorted[-1][1].sum())
    mostCommonMessageSenders = sorted(allMessagesSorted[-1][1], key=lambda x: x[1])
    mostCommonMessageSender = (translation[mostCommonMessageSenders[-1][0]], mostCommonMessageSenders[-1][1])
    msg += "\n### Most Common Message Award"
    msg += "\nOddly enough, this award does not go to a real person... not that there are any real people on this server."
    msg += f"\nNevertheless, this award goes to... '*{mostCommonMessage[0]}*', sent *{mostCommonMessage[1]}* times!"
    msg += f"\nAs a special mention, this message was sent most often by *{mostCommonMessageSender[0]}*, a whole *{mostCommonMessageSender[1]}* times!"
    if len(allMessagesSorted) > 1:
        mostCommonMessageRunnerUp = (allMessagesSorted[-2][0], allMessagesSorted[-2][1].sum())
        secondMostCommonMessageSenders = sorted(allMessagesSorted[-2][1], key=lambda x: x[1])
        secondMostCommonMessageSender = (translation[secondMostCommonMessageSenders[-1][0]], secondMostCommonMessageSenders[-1][1])
        msg += f"\nIn second place was the message, '*{mostCommonMessageRunnerUp[0]}*', sent a measly *{mostCommonMessageRunnerUp[1]}* times, "
        msg += f"mostly by *{secondMostCommonMessageSender[0]}*, *{secondMostCommonMessageSender[1]}* times."
    await ctx.send(msg)

    # misc stuff
    msg = "## And, some more little things...\n*please, sir, can i have some more? ;-;*\n"
    msg += f"""
**Total messages sent:** {messagesSent}
**Total words typed:** {wordsTyped}
**Number of gifs sent:** {gifsSent}
**Total emoji's used:** {emojisUsed}
**Number of reactions applied:** {reactionsApplied}
"""
    msg += "\n### Top 8 most popular emojis:\n*oh, dearest penisbee; wherefore art thou?*\n"
    msg += "\n".join(f"    \\- {w}: {c}" for w, c in emojiCounterSorted)
    msg += "\n\n### Top 8 most popular reaction:\n*when the imposter is- UkGgh- eughh...*\n"
    msg += "\n".join(f"    \\- {w}: {c}" for w, c in reactionCounterSorted)
    msg += "\n\n### Top 5 most reacted messages:\n*mr popular are we?*\n"
    for i, (reactions, message) in enumerate(mostReactedMessages):
        msg += f"#{i + 1} with {reactions} reaction{'s' if reactions > 1 else ''}: {message.jump_url}\n"
    
    msg += "\n### Top 5 most popular gifs:\n*omw to that bingussy*"
    await ctx.send(msg)

    # send gifs data
    for i, (link, num) in enumerate(gifCounterSorted):
        await ctx.send(f"#{i + 1}: with {num} gif{'s' if num > 1 else ''} sent\n{link}")

# load .env file
load_dotenv()
TOKEN = getenv("DISCORD_TOKEN")
# run bot
bot.run(TOKEN)