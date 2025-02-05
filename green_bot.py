import discord, random, time, os, platform, sqlite3, requests
from discord import Embed
from colorama import Fore, Style
from discord.ext import commands, tasks
from datetime import datetime

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

commands_list = [
    '?_help ~ show available commands.',
    '?waste_categories ~ show waste categories.'
]

waste_categories = {
    'organic': {
        'food': [
            'banana peel', 'pasta', 'cake', 'bread', 'apple core', 'orange peel', 
            'vegetable scraps', 'coffee grounds', 'tea leaves', 'egg shells', 
            'rice', 'cooked grains', 'corn cob', 'fruit pits'],
        'nutshells': ['peanut shell', 'almond shell', 'hazelnut shell', 'pistachio shell'],
        'garden_waste': ['leaves', 'grass clippings', 'small branches', 'dead flowers']
    },
    'plastic': {
        'bottles': ['water bottle', 'coke bottle', 'juice bottle', 'oil bottle'],
        'containers': ['yogurt cup', 'milk carton', 'sauce tub', 'butter tub'],
        'cans': ['soda can', 'energy drink can', 'beer can'],
        'wrappers': ['chip bag', 'candy wrapper', 'plastic bag', 'straw']
    },
    'paper': {
        'clean': ['newspaper', 'magazine', 'book', 'printer paper', 'notebook', 'envelope'],
        'dirty': ['pizza box', 'greasy napkin', 'used tissue', 'paper towel'],
        'packaging': ['cardboard box', 'cereal box', 'shoe box', 'paper bag']
    },
    'glass': {
        'bottles': ['water bottle', 'coke bottle', 'juice bottle', 'wine bottle', 'beer bottle'],
        'jars': ['jam jar', 'pickles jar', 'sauce jar', 'honey jar', 'baby food jar'],
        'broken_glass': ['broken drinking glass', 'shattered jar'] 
    },
    'non-recyclable': {
        'misc': ['plastic cutlery', 'styrofoam', 'broken mirror', 'cigarette butt', 'rubber bands', 'toothpaste tube'],
        'hazardous': ['batteries', 'paint cans', 'light bulbs', 'expired medicine', 'motor oil']
    }
}

random_phrases = {
    'linux_related': [
        "Want to give your old PC a second life? Ubuntu's the way to go.",
        "Ubuntu is a lightweight option that saves resources and gets the job done.",
        "Switching to Linux can help reduce e-waste; try Ubuntu.",
        "Tired of Windows? Ubuntu helps you save energy while using your machine.",
        "Want to learn something new and eco-friendly? Ubuntu's a solid start.",
        "Old PC? Don't throw it away, install Ubuntu, run a minecraft server for you and your friends."
    ],
    'pc_related': [
        "Undervolt your PC to save energy, reduce heat, and cut noise.",
        "Keep your PC clean to enhance performance and prevent damage."
    ],
    'house_related': [
        "Turn off the lights when you don’t need 'em; save money and energy.",
        "Use a reusable water bottle to cut down on plastic waste.",
        "Keep the volume down and save energy; enjoy your tunes with headphones."
    ],
    'garden_related': [
        "Plant trees to cool down the neighborhood and help the planet.",
        "Grow your own veggies; it saves money and reduces food waste.",
        "Decorate your garden with flowers; they help bees and brighten your space.",
        "Remember, bees are crucial for our ecosystem; let them thrive.",
        "Remember when it wasn't this hot? A tree helps a lot. Plant one if you can."
    ],
    'animal_related': [
        "Adopt a pet if you can; give a little fella a second chance.",
        "Choose adoption over buying; shelters have amazing animals waiting for homes.",
        "Don’t abandon your pets; they rely on you just like family."
    ],
    'no_waste': [
        "Save leftovers for tomorrow; don’t let good food go to waste.",
        "Plan your meals to avoid overbuying and wasting food.",
        "Compost your scraps; it's a win for your garden and the planet.",
        "Only take what you need; it's better for the earth and your wallet.",
        "Use cloth bags for shopping; ditch the plastic and protect the planet.",
        "Before tossing something, think about how it could be reused or repurposed.",
        "Buy in bulk to cut down on packaging waste and save some cash."
    ]
}

#-------------------------------------------------# Bot Functions
#-----------------------------------------/Events

@bot.event
async def on_ready():
    make_os('clear')
    print(f'[{get_time('date')}] [{log('info')}]     {Fore.LIGHTMAGENTA_EX}System.Booted_as{Style.RESET_ALL} {bot.user}')

    channel = bot.get_channel(1326946989342199929)
    await channel.send("Hello there! Type `?_help` to see the available commands.")

    time.sleep(5)

    if not random_phrase.is_running():
        random_phrase.start()

    time.sleep(5)

    if not flyer.is_running():
        flyer.start()


#-----------------------------------------/Commands

@bot.command('_help')
async def help_cmds(ctx):
    await ctx.send('Available commands: \n' + '\n'.join(f'`{command}`' for command in commands_list))
    print(f'[{get_time('date')}] [{log('info')}]     {Fore.LIGHTMAGENTA_EX}System.Help_menu{Style.RESET_ALL}')


@bot.command('waste_categories')
async def show_waste_categories(ctx):
    embed = Embed(title="Waste Categories", color=0x00ff00)
    for category, subcategories in waste_categories.items():
        items = []
        for subcategory, items_list in subcategories.items():
            items.append(f"**{subcategory.replace('_', ' ').capitalize()}**: `{', '.join(items_list)}`")
        embed.add_field(name=f"{category.capitalize()} bin contains:", value="\n".join(items), inline=False)
    
    embed.add_field(name='Warning', value='Please make sure to check your local recycling guidelines as they may vary. Also check whatever you intend to throw away for warnings or directions.', inline=False)
    await ctx.send(embed=embed)

#-----------------------------------------/Tasks

@tasks.loop(minutes=45)
async def random_phrase():
    random_phrase = random.choice(random_phrases[random.choice(list(random_phrases.keys()))])
    await bot.get_channel(1326946989342199929).send(random_phrase)

#@tasks.loop(hours=4) you might want to add your own flyer
#async def flyer():
#    image = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'medias','volantino.jpg')
#    
#    try:
#        with open(image, 'rb') as f:
#            picture = discord.File(f)
#            channel = bot.get_channel(1326946989342199929)
#            if channel:
#                await channel.send(file=picture)
#                print(f'[{get_time('date')}] [{log('info')}]     {Fore.LIGHTMAGENTA_EX}System.Sent_fly{Style.RESET_ALL}')
#
#    except Exception as e:
#        print('An error occurred while sending the flyer:', e)

#-------------------------------------------------# Side Functions
def make_os(command):
    if command == 'clear':
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')

def get_time(time_type):
    if time_type == 'date':
        return datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    elif time_type == 'time_of_the_day':
        return 'morning' if 6 <= datetime.now().hour < 12 else 'afternoon' if 12 <= datetime.now().hour < 18 else 'evening' if 18 <= datetime.now().hour < 24 else 'night'

def log(request):
    if request in ['info', 'warn', 'fatal', 'error']:
        if request == 'info':
            return f'{Fore.LIGHTBLUE_EX}INFO{Style.RESET_ALL}'
        elif request == 'warn':
            return f'{Fore.YELLOW}WARN{Style.RESET_ALL}'
        elif request == 'fatal':
            return f'{Fore.LIGHTRED_EX}FATAL{Style.RESET_ALL}'
        elif request == 'error':
            return f'{Fore.LIGHTRED_EX}ERROR{Style.RESET_ALL}'
    else:
        print(f'{get_time("date")} {log('error')} {Fore.RED}Error{Style.RESET_ALL} Invalid log request.')

def init():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'green_bot.db') #delete this procedure and make your own.
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tokens WHERE tag = "#0965"') 
        token = cursor.fetchall()[0][1]
        bot.run(token)

    except Exception as e:
        print(f'{get_time("date")} {log("fatal")}     {Fore.RED}Error{Style.RESET_ALL} {e}')

if __name__ == '__main__':
    init()