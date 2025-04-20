from re import purge
import discord
from discord.ext import commands
import os

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()


TOKEN = 'MTM2MTA0MTE2MzUwNjgxMDg5MA.GtmDRW.W-sVdZHMQHNIilrYl8aiXPCamtDqnhdK58uxQk'
#os.getenv('DISCORD_BOT_TOKEN')  # Ensure the environment variable is set

if TOKEN is None:
    raise ValueError("No token provided. Please set the DISCORD_BOT_TOKEN environment variable.")

# Create a bot instance with a command prefix
intents = discord.Intents.default()
intents.message_content = True  # Make sure to enable message content intent
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print(f'Bot is in {len(bot.guilds)} servers')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name="Keopi"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("Command not found.")
        await ctx.send("Try again later.")
    else:
        print(f"Error occurred: {error}")
        await ctx.send(f"An error occurred: {error}")

@bot.command()
async def ping(ctx):
    """Simple command to test if the bot is responding"""
    await ctx.send(f'Pong! *Latency:* {float(bot.latency * 1000)}ms')

@bot.command()
async def event(ctx):
    role = discord.utils.get(ctx.guild.roles, name='Staff team')
    try:
        # Delete the command message
        await ctx.message.delete()

        if role in ctx.author.roles:
            # Create an embed with more details
            embed = discord.Embed(
                title='🎉 New Event Announcement!',
                description='An event is starting soon! Please react with ✅ if you\'re coming or ❌ if you\'re not.',
                color=discord.Color.brown()
            )

            embed.add_field(name='Host', value=ctx.author.mention, inline=True)
            embed.add_field(name='Channel', value=ctx.channel.mention, inline=True)
            embed.set_footer(text='Event notification')
            embed.timestamp = discord.utils.utcnow()

            # Send the embed and add reactions
            message = await ctx.send(
                content="@everyone",
                embed=embed
            )
            await message.add_reaction('✅')
            await message.add_reaction('❌')
    except Exception as e:
        await ctx.send(f"Error creating event: {str(e)}")

@bot.command()
async def Purge(ctx, amount: int):
    role = discord.utils.get(ctx.guild.roles, name='Staff team')
    Limit = 900
    if role in ctx.author.roles:
        if amount <= Limit:
            await ctx.channel.purge(limit=amount)
            await ctx.send(f"{role.mention} has been successful!")
            await ctx.send(f"{amount} messages have been deleted")
        else:
            await ctx.send(f"{role.mention} has failed to purge!")

# Run the bot
keep_alive()
bot.run(TOKEN)
