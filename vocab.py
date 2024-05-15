import discord
from discord.ext import commands
import requests
from decouple import config

BOT_TOKEN = config("BOT_TOKEN")

intents = discord.Intents.default()
intents.typing = False  # Disables the typing indicator
intents.presences = False  # Disables the member presence tracking

bot = commands.Bot(command_prefix="", intents=discord.Intents.all())

async def get_api_response(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching API response: {e}")
        return None

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(help="Get the definition of a word")
async def define(ctx, *, word):
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
    data = await get_api_response(url)
    if data:
        meanings = [meaning['definitions'][0]['definition'] for meaning in data[0]['meanings']]
        definitions = "\n".join(meanings)
        await ctx.send(f"**{word.capitalize()}**:\n{definitions}")
    else:
        await ctx.send(f"Sorry, I couldn't find a definition for '{word}'")

@bot.command(help="Get a slang definition from Urban Dictionary")
async def slang(ctx, *, term):
    url = f'https://api.urbandictionary.com/v0/define?term={term}'
    data = await get_api_response(url)
    if data and data["list"]:
        definition = data["list"][0]["definition"]
        await ctx.send(f"**{term.capitalize()}**: {definition}")
    else:
        await ctx.send(f"Sorry, I couldn't find a definition for '{term}'")

@bot.command(help="Get words that rhyme with the given word")
async def rhymes(ctx, *, word):
    url = f'https://api.datamuse.com/words?rel_rhy={word}'
    data = await get_api_response(url)
    if data:
        rhymes = [entry['word'] for entry in data]
        if rhymes:
            await ctx.send(f"Words that rhyme with **{word.capitalize()}**: {' | '.join(rhymes)}")
        else:
            await ctx.send(f"Sorry, I couldn't find any rhymes for '{word}'")
    else:
        await ctx.send("Failed to fetch rhymes.")

@bot.command(help="Get synonyms and antonyms for the given word")
async def syno(ctx, *, word):
    url = f'https://api.datamuse.com/words?rel_syn={word}'
    data = await get_api_response(url)
    if data:
        synonyms = [entry['word'] for entry in data if 'word' in entry]
        await ctx.send(f"Synonyms for **{word.capitalize()}**: {' | '.join(synonyms)}\n")
    else:
        await ctx.send("Failed to fetch synonyms/antonyms.")

@bot.command(help="Get synonyms and antonyms for the given word")
async def anti(ctx, *, word):
    url = f'https://api.datamuse.com/words?rel_ant={word}'
    data = await get_api_response(url)
    if data:
        antonyms = [entry['word'] for entry in data if 'word' in entry]
        await ctx.send(f"Antonyms for **{word.capitalize()}**: {' | '.join(antonyms)}")
    else:
        await ctx.send("Failed to fetch synonyms/antonyms.")

@bot.command(help="Show available commands")
async def commands(ctx):
    await ctx.send("Available commands:\n"
                   "**define** *(word)* - Get the definition of a word.\n"
                   "**slang** *(term)* - Get a slang definition from Urban Dictionary.\n"
                   "**rhymes** *(word)* - Get words that rhyme with the given word.\n"
                   "**anti/syno** *(word)* - Get [synonyms/antonyms] for the given word.")

# Run the bot with your token
bot.run(BOT_TOKEN)
