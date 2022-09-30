from datetime import timedelta
from discord import app_commands, Intents, Interaction, Member
from discord.ext.commands import Bot
import os
import typing
from server import server
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("token")

# token = os.environ['token']

bot = Bot(command_prefix="!", intents=Intents.all())

swears = ["nigga", "nigger", "niggar", "retard"]


@bot.event
async def on_ready():
    print("Logged in as", bot.user)
    try:
        await bot.tree.sync()
    except Exception as e:
        print(e)


@bot.event
async def on_message(msg):
    for w in swears:
        if w in msg.content.lower():
            await msg.delete()
            return


@bot.tree.command(name="kick", description="Kicks a user.")
@app_commands.checks.has_permissions(administrator=True)
async def kick(interaction: Interaction, user: Member,
               reason: typing.Union[str, None]):
    await user.kick(reason=reason)

    if reason:
        await interaction.response.send_message(
            f"{user} has been kicked for {reason}!", ephemeral=True)
    else:
        await interaction.response.send_message(f"{user} has been kicked!",
                                                ephemeral=True)


@bot.tree.command(name="ban", description="Bans a user.")
@app_commands.checks.has_permissions(administrator=True)
async def ban(interaction: Interaction, user: Member,
              reason: typing.Union[str, None]):
    await user.ban(reason=reason)

    if reason:
        await interaction.response.send_message(
            f"{user} has been banned for {reason}!", ephemeral=True)
    else:
        await interaction.response.send_message(f"{user} has been banned!",
                                                ephemeral=True)


@bot.tree.command(name="timeout",
                  description="Times out a user (max 28 days).")
@app_commands.checks.has_permissions(administrator=True)
async def timeout(interaction: Interaction,
                  user: Member,
                  reason: typing.Union[str, None],
                  days: int = 0,
                  hours: int = 0,
                  mins: int = 0,
                  secs: int = 0):
    duration = timedelta(days=days, hours=hours, minutes=mins, seconds=secs)

    day = "day" if days == 1 else "days"
    hour = "hour" if hours == 1 else "hours"
    minute = "minute" if mins == 1 else "minutes"
    second = "second" if secs == 1 else "seconds"

    await user.timeout(duration, reason=reason)

    if reason:
        await interaction.response.send_message(
            f"{user} has been timed out for {days} {day}, {hours} {hour}, {mins} {minute} and {secs} {second} for {reason}!",
            ephemeral=True)
    else:
        await interaction.response.send_message(
            f"{user} has been timed out for {days} {day}, {hours} {hour}, {mins} {minute} and {secs} {second}!",
            ephemeral=True)

    return


@bot.tree.command(name="untimeout", description="Removes a user's timeout.")
@app_commands.checks.has_permissions(administrator=True)
async def untimeout(interaction: Interaction, user: Member,
                    reason: typing.Union[str, None]):
    await user.timeout(None, reason=reason)

    if reason:
        await interaction.response.send_message(
            f"{user}'s timeout has been removed for {reason}!", ephemeral=True)
    else:
        await interaction.response.send_message(
            f"{user}'s timeout has been removed!", ephemeral=True)

    return


@ban.error
@kick.error
@timeout.error
@untimeout.error
async def error_handler(interaction: Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message(
            "You need to have adminstrator permissions to use this command.",
            ephemeral=True)
        return
    elif isinstance(error, app_commands.errors.CommandInvokeError):
        await interaction.response.send_message(
            "**Error 404:** Make sure roles are set up properly, the duration for timeout can't be more than 28 days, you cannot timeout yourself and putting in no inputs will result in a 0 second timeout.",
            ephemeral=True)
        return
    else:
        raise error


server()
bot.run(token)
