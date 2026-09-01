import json
import os
import pathlib
import emoji

import discord
from discord import app_commands
from discord.ext import commands

from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

storageFolder = pathlib.Path('names.json') # Storage .json file


load_dotenv()
bot = commands.Bot(command_prefix="%", intents=intents)
bot.remove_command("help")
# Define the bot token here
token = os.getenv("BOT_TOKEN") 


# Helper methods:
async def checkInList(user: int, userList: dict):
  return (str(user) in userList)

def checkValidReaction(reaction):
  return emoji.is_emoji(reaction) == True

async def replyToKeyword(context, keyword, reply):
  if keyword in context.content.lower():
    await context.channel.send_message(reply)


async def reactToKeyword(context, keyword, reaction):
  if isinstance(keyword, list):
    for i in range(0, len(keyword)):
      if keyword[i] in context.content.lower():
        await context.add_reaction(reaction)
        break
  else:
    if keyword in context.content.lower():
      await context.add_reaction(reaction)


@bot.event
async def on_ready():
  await bot.tree.sync()
  print(f"Logged in as {bot.user}!")


@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  else:
    with storageFolder.open(mode="r", encoding="utf-8") as readFile:
      users = json.load(readFile)
    if str(message.author.id) in users["users"] and users["users"][str(
        message.author.id)]["reacting"] == True:
      await message.add_reaction(users["users"][str(
          message.author.id)]["reaction"])

    await replyToKeyword(message, "nuts", "This place is nuts!")
    await bot.process_commands(message)


@bot.hybrid_command(name="add_user",
                    description="begin reacting to a user's messages.")
async def add_user(ctx, reaction):
  if checkValidReaction(reaction):
    with storageFolder.open(mode="r", encoding="utf-8") as readFile:
      users = json.load(readFile)
      users["users"][str(ctx.author.id)] = {}
      users["users"][str(ctx.author.id)]["reaction"] = reaction
      users["users"][str(ctx.author.id)]["reacting"] = True
    with storageFolder.open(mode="w", encoding="utf-8") as writeFile:
      json.dump(users, writeFile)
    await ctx.send("Now reacting to %s's messages with %s." %
                    (ctx.author.display_name, reaction),
                    ephemeral=True)
  else:
    await ctx.send("That is not a valid reaction! Please input only one emoji", ephemeral=True)


@bot.hybrid_command(name="remove_user",
                    description="stop reacting to a user's messages")
async def remove_user(ctx):
  with storageFolder.open(mode="r", encoding="utf-8") as readFile:
    users = json.load(readFile)
    users["users"].pop(str(ctx.author.id), None)
  with storageFolder.open(mode="w", encoding="utf-8") as writeFile:
    json.dump(users, writeFile)
  await ctx.send("Will no longer react to %s's messages." % (ctx.author.display_name),
                  ephemeral=True)


@bot.hybrid_command(name="disable_nuts",
                    description="turn off bot reactions for a user")
async def no_nuts(ctx):
  with storageFolder.open(mode="r", encoding="utf-8") as readFile:
    users = json.load(readFile)
    reaction = users["users"][str(ctx.author.id)]["reaction"]
    users["users"][str(ctx.author.id)]["reacting"] = False
  with storageFolder.open(mode="w", encoding="utf-8") as writeFile:
    json.dump(users, writeFile)
  await ctx.send(
      "Will temporarily stop reacting to %s's messages with %s. Enable with enable_nuts."
      % (ctx.author.display_name, reaction),
      ephemeral=True)


@bot.hybrid_command(name="enable_nuts",
                    description="turn on bot reactions for a user")
async def nuts(ctx):
  with storageFolder.open(mode="r", encoding="utf-8") as readFile:
    users = json.load(readFile)
    reaction = users["users"][str(ctx.author.id)]["reaction"]
    users["users"][str(ctx.author.id)]["reacting"] = True
  with storageFolder.open(mode="w", encoding="utf-8") as writeFile:
    json.dump(users, writeFile)
  await ctx.send(
      "This bot will now continue reacting to %s's messages with %s."
      % (ctx.author.display_name, reaction),
      ephemeral=True)

@bot.hybrid_command(name="help", description="Information on all commands")
async def help(ctx):
  helpMenu = discord.Embed(title="This Help Page Is Nuts!", 
                           color=0xFF6347, 
                           description='''This Bot Is Nuts! is a toggleable reaction macro, originally made as a prank for a moderator on the Discord server Moonframe.''')
  helpMenu.add_field(name="add_user", value="Starts reacting to your messages with the specified emoji", inline=False)
  helpMenu.add_field(name="remove_user", value="Stop reacting to your messages with the specified emoji", inline=False)
  helpMenu.add_field(name="disable_nuts", value="Temporarily stop reacting to your messages", inline=False)
  helpMenu.add_field(name="enable_nuts", value="If reactions were paused by disable_nuts, enable them again", inline=False)
  helpMenu.set_footer(text="this place is nuts!")

  await ctx.send(embed=helpMenu)
  
bot.run(token) # type: ignore
# Run bot token
