from datetime import timedelta
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("token")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("Logged in as", bot.user)


@bot.command()
@has_permissions(administrator=True)
async def kick(ctx, user: discord.Member, reason=None):
    await user.kick(reason=reason)

    if reason:
        await ctx.send(f"{user} has been kicked by {ctx.author.mention} for {reason}!")
    else:
        await ctx.send(f"{user} has been kicked by {ctx.author.mention}!")


@bot.command()
@has_permissions(administrator=True)
async def ban(ctx, user: discord.Member, reason=None):
    await user.ban(reason=reason)

    if reason:
        await ctx.send(f"{user} has been banned by {ctx.author.mention} for {reason}!")
    else:
        await ctx.send(f"{user} has been banned by {ctx.author.mention}!")


@bot.command()
@has_permissions(administrator=True)
async def timeout(ctx, user: discord.Member, *args):
    if args[0] == "reason":
        reason = args[1]
        args = args[2:]
    else:
        reason = None

    days = hours = mins = secs = 0

    for arg in args:
        if arg.endswith("d"):
            days = int(arg[:-1])
        elif arg.endswith("h"):
            hours = int(arg[:-1])
        elif arg.endswith("m"):
            mins = int(arg[:-1])
        elif arg.endswith("s"):
            secs = int(arg[:-1])

    duration = timedelta(days=days, hours=hours, minutes=mins, seconds=secs)

    day = "day" if days == 1 else "days"
    hour = "hour" if hours == 1 else "hours"
    minute = "minute" if mins == 1 else "minutes"
    second = "second" if secs == 1 else "seconds"

    await user.timeout(duration, reason=reason)

    if reason:
        await ctx.send(f"{user.mention} has been timed out for {days} {day}, {hours} {hour}, {mins} {minute} and {secs} {second} by {ctx.author.mention} for {reason}!")
    else:
        await ctx.send(f"{user.mention} has been timed out for {days} {day}, {hours} {hour}, {mins} {minute} and {secs} {second} by {ctx.author.mention}!")

    return


@ban.error
@kick.error
@timeout.error
async def error_handler(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"You need to have adminstrator permissions to use this command.")
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Please mention a user.")
        return
    elif isinstance(error, TypeError):
        await ctx.send(f"Wrong type given.")
        return
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("Duration can't be more than 28 days, non-integers can't be passed in, and blank arguments can't be passed in.")
    else:
        raise error


# @bot.command()
# @has_permissions(administrator=True)
# async def mute(ctx, user: discord.Member, reason=None):
#     try:
#         await user.mute(reason=reason)
#     except:
#         await ctx.send(f"{ctx.author.mention} Please mention a user!")
#         return


# @bot.command()
# @has_permissions(administrator=True)
# async def unmute(ctx, user: discord.Member, reason=None):
#     try:
#         await user.unmute(reason=reason)
#     except:
#         await ctx.send(f"{ctx.author.mention} Please mention a user!")
#         return


bot.run(token)
