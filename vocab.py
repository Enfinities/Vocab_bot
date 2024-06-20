import discord
from discord.ext import commands
import requests
from decouple import config
from googletrans import Translator

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

# Create a translator object
translator = Translator()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')
    if message.content == "hello":
        await message.reply("Hi! :)")
    await bot.process_commands(message)

@bot.command()
async def lang(ctx):
    await ctx.send("""af: Afrikaans
ak: Akan
sq: Albanian
am: Amharic
ar: Arabic
an: Aragonese
hy: Armenian
as: Assamese
av: Avaric
ae: Avestan
ay: Aymara
az: Azerbaijani
bm: Bambara
ba: Bashkir
eu: Basque
be: Belarusian
bn: Bengali
bh: Bihari
bi: Bislama
bs: Bosnian
br: Breton
bg: Bulgarian
my: Burmese
ca: Catalan
ch: Chamorro
ce: Chechen
zh: Chinese (not working)
cv: Chuvash
kw: Cornish
co: Corsican
cr: Cree
cs: Czech
cy: Welsh
da: Danish
de: German
dv: Divehi
dz: Dzongkha
el: Greek
en: English
eo: Esperanto
et: Estonian
eu: Basque
fa: Persian
fj: Fijian
fi: Finnish
ff: Fula
gl: Galician
ka: Georgian
gd: Scots Gaelic
gu: Gujarati
ht: Haitian Creole
ha: Hausa
haw: Hawaiian
he: Hebrew
hi: Hindi
ho: Hiri Motu
hr: Croatian
hu: Hungarian
hy: Armenian
ia: Interlingua
id: Indonesian
ie: Interlingue
ig: Igbo
io: Ido
is: Icelandic
it: Italian
iu: Inuktitut
ja: Japanese
jv: Javanese
kl: Kalaallisut
kn: Kannada
kr: Kanuri
ks: Kashmiri
kk: Kazakh
km: Central Khmer
ki: Kikuyu
rw: Kinyarwanda
ky: Kirghiz
kv: Komi
kg: Kongo
ko: Korean
ku: Kurdish
kj: Kwanyama
la: Latin
lb: Luxembourgish
ln: Lingala
lo: Lao
lt: Lithuanian
lu: Luba-Katanga
lv: Latvian
gv: Manx
mk: Macedonian
mg: Malagasy
ms: Malay
ml: Malayalam
mt: Maltese
mi: Maori
mr: Marathi
mh: Marshallese
mn: Mongolian
na: Nauru
nv: Navajo
nb: Norwegian Bokmål
nd: North Ndebele
ne: Nepali
ng: Ndonga
ng: Ndonga
nl: Dutch
nn: Norwegian Nynorsk
no: Norwegian
oc: Occitan
oj: Ojibwa
om: Oromo
or: Oriya
os: Ossetian
pa: Punjabi
pi: Pali
fa: Persian
pl: Polish
ps: Pashto
pt: Portuguese
qu: Quechua
rm: Romansh
ro: Romanian
ru: Russian
sa: Sanskrit
sc: Sardinian
sd: Sindhi
se: Northern Sami
sm: Samoan
sg: Sango
sh: Serbo-Croatian
sr: Serbian
sn: Shona
si: Sinhala
sk: Slovak
sl: Slovenian
so: Somali
st: Southern Sotho
es: Spanish
su: Sundanese
sw: Swahili
sv: Swedish""")
@bot.command()
async def translate(ctx, dest_lang, *, text):
    try:
        print(f'Translating to {dest_lang}: {text}')
        # Translate the text
        translator = Translator()
        translation = translator.translate(text, dest=dest_lang)
        await ctx.send(f'Translation: {translation.text}')
    except ValueError as e:
        print(f'Error: Invalid language code {dest_lang}')
        await ctx.send(f'Error: Invalid language code {dest_lang}')
    except Exception as e:
        print(f'Error: {str(e)}')
        await ctx.send(f'Error: {str(e)}')


@bot.command(help="Show available commands")
async def commands(ctx):
    await ctx.send("Available commands:\n"
                   "**define** *(word)* - Get the definition of a word.\n"
                   "**slang** *(term)* - Get a slang definition from Urban Dictionary.\n"
                   "**rhymes** *(word)* - Get words that rhyme with the given word.\n"
                   "**anti/syno** *(word)* - Get [synonyms/antonyms] for the given word.)\n"
                    "**translate** **[language code]** *(phrase)* - Get [translation] for the given text.)\n"
                   "**lang** - Get list of [language codes] .")

# Run the bot with your token
bot.run(BOT_TOKEN)
