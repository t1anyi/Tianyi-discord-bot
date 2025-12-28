import os
from dotenv import load_dotenv
import discord
import random
from discord.ext import commands
from discord import app_commands

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening, name="为了你唱下去"
        )
    )
    try:
        print(f"Logged in as {bot.user} (ID: {bot.user.id})")
        bot.tree.clear_commands(guild=None)
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(e)
    print("loading ready")


# /echo
@bot.tree.command(name="echo", description="Echoes a message")
@app_commands.describe(message="The message to echo")
async def echo(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)


# /hello
@bot.tree.command(name="hello", description="Tianyi says hello")
async def hello(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Hello!",
        description="大家好,我是虚拟歌手洛天依\n안녕하세요 저는 뤄톈이입니다",
    )
    await interaction.response.send_message(embed=embed)


# /ping
@bot.tree.command(name="ping", description="Returns pong")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Pong!\n```fix\n{round(bot.latency * 1000)} ms```"
    )


# /rng
@bot.tree.command(name="random", description="Random Number Generator")
@app_commands.describe(min="Lower bound", max="Upper bound")
async def randomnum(interaction: discord.Interaction, min: int, max: int):
    if max < min:
        await interaction.response.send_message(
            "Cannot have max number smaller than min"
        )

    number = random.randint(min, max)
    await interaction.response.send_message(f"**{number}**")


# /dice
@bot.tree.command(name="dice", description="Roll d6 dice")
@app_commands.describe(amount="How many dice")
async def roll(interaction: discord.Interaction, amount: int):
    if amount <= 0:
        await interaction.response.send_message("Amount must be at least 1")
        return

    rolls = [random.randint(1, 6) for _ in range(amount)]
    total = sum(rolls)

    await interaction.response.send_message(
        "🎲 Rolls: " + ", ".join(map(str, rolls)) + f"\n**Total:** {total}"
    )


bot.run(TOKEN)
