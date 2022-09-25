from datetime import timedelta
from discord import app_commands, Intents, Interaction, Member, User
from discord.ext.commands import Bot
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("token")


bot = Bot(command_prefix="!", intents=Intents.all())


@bot.event
async def on_ready():
    print("Logged in as", bot.user)
    try:
        await bot.tree.sync()
    except Exception as e:
        print(e)


@bot.tree.command(name="kickout")
@app_commands.checks.has_permissions(administrator=True)
async def kick(interaction: Interaction, user: Member, reason: str | None):
    await user.kick(reason=reason)

    if reason:
        await interaction.response.send_message(f"{user} has been kicked for {reason}!", ephemeral=True)
    else:
        await interaction.response.send_message(f"{user} has been kicked!", ephemeral=True)


@bot.tree.command(name="banish")
@app_commands.checks.has_permissions(administrator=True)
async def ban(interaction: Interaction, user: Member, reason: str | None):
    await user.ban(reason=reason)

    if reason:
        await interaction.response.send_message(f"{user} has been banned for {reason}!", ephemeral=True)
    else:
        await interaction.response.send_message(f"{user} has been banned!", ephemeral=True)


@bot.tree.command(name="timeout")
@app_commands.checks.has_permissions(administrator=True)
async def timeout(interaction: Interaction, user: Member, reason: str | None, days: int = 0, hours: int = 0, mins: int = 0, secs: int = 0):
    duration = timedelta(days=days, hours=hours, minutes=mins, seconds=secs)

    day = "day" if days == 1 else "days"
    hour = "hour" if hours == 1 else "hours"
    minute = "minute" if mins == 1 else "minutes"
    second = "second" if secs == 1 else "seconds"

    await user.timeout(duration, reason=reason)

    if reason:
        await interaction.response.send_message(f"{user} has been timed out for {days} {day}, {hours} {hour}, {mins} {minute} and {secs} {second} for {reason}!", ephemeral=True)
    else:
        await interaction.response.send_message(f"{user} has been timed out for {days} {day}, {hours} {hour}, {mins} {minute} and {secs} {second}!", ephemeral=True)

    return


# @bot.tree.command(name="unban")
# @app_commands.checks.has_permissions(administrator=True)
# async def unban(interaction: Interaction, user: User, reason: str | None):
#     await interaction.guild.unban(user, reason=reason)

#     if reason:
#         await interaction.response.send_message(f"{user} has been unbanned for {reason}!", ephemeral=True)
#     else:
#         await interaction.response.send_message(f"{user} has been unbanned!", ephemeral=True)

#     return


@bot.tree.command(name="untimeout")
@app_commands.checks.has_permissions(administrator=True)
async def untimeout(interaction: Interaction, user: Member, reason: str | None):
    await user.timeout(None, reason=reason)

    if reason:
        await interaction.response.send_message(f"{user}'s timeout has been removed for {reason}!", ephemeral=True)
    else:
        await interaction.response.send_message(f"{user}'s timeout has been removed!", ephemeral=True)

    return


@ban.error
@kick.error
@timeout.error
@untimeout.error
async def error_handler(interaction: Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message(f"You need to have adminstrator permissions to use this command.", ephemeral=True)
        return
    elif isinstance(error, app_commands.errors.CommandInvokeError):
        await interaction.response.send_message("Duration can't be more than 28 days, non-integers can't be passed in, and blank arguments can't be passed in.", ephemeral=True)
        return
    else:
        raise error


bot.run(token)
