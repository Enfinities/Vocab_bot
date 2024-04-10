import discord
from discord.ext import commands
import requests
from decouple import config

BOT_TOKEN = config("BOT_TOKEN")

intents = discord.Intents.default()
intents.typing = False  # Disables the typing indicator
intents.presences = False  # Disables the member presence tracking

bot = commands.Bot(command_prefix="", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def Define(ctx, *, word):
    # Call a dictionary API to get the definition.
    response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
    if response.status_code == 200:
        data = response.json()
        # Extract definition from the response
        definition = data[0]['meanings'][0]['definitions'][0]['definition']
        print(definition)
        await ctx.send(f"**{word.capitalize()}**: {definition}")
    else:
        await ctx.send(f"Sorry, I couldn't find a definition for '{word}'")

# Run the bot with your token
bot.run(BOT_TOKEN)