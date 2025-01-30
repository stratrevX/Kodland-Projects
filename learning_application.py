import discord.ext.commands
import random, discord, time, os, platform, sqlite3, requests
from colorama import Fore, Style
from datetime import datetime
from discord.ext import commands, tasks

import discord.ext

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

commands_list = [
    '$hi ~ say hi to me.',
    '$flip_a_coin ~ maybe i will flip a coin.',
    '$generate_key <amount> <length> ~ i will generate different safe and complex keys.',
    '$roll_a_dice ~ i will roll a dice.',
    '$fox ~ perhaps a fox will join us.',
    '$cat ~ maybe a cat will appear.',
    ]
#-------------------------------------------------# Bot Functions
@bot.event
async def on_ready():
    make_os('clear')
    print(f'[{get_time('date')}] [{log('info')}]     {Fore.LIGHTMAGENTA_EX}System.Booted_as{Style.RESET_ALL} {bot.user}')
    if not random_meme.is_running():
        random_meme.start()

@bot.command('help_cmds')
async def help_cmds(ctx):
    await ctx.send('Available commands: \n' + '\n'.join(f'`{command}`' for command in commands_list))
    print(f'[{get_time('date')}] [{log('info')}]     {Fore.LIGHTMAGENTA_EX}System.Help_menu{Style.RESET_ALL}')

@bot.command('cat')
async def cat(ctx):
    image_url = get_cat_image_url()
    await ctx.send(image_url)
    print(f'[{get_time('date')}] [{log('info')}]     {Fore.LIGHTMAGENTA_EX}System.Sent_cat{Style.RESET_ALL}')

@bot.command('fox')
async def fox(ctx):
    image_url = get_fox_image_url()
    await ctx.send(image_url)
    print(f'[{get_time('date')}] [{log('info')}]     {Fore.LIGHTMAGENTA_EX}System.Sent_fox{Style.RESET_ALL}')

@bot.command('hi')
async def hi(ctx):
    await ctx.send(f'good {get_time('time_of_the_day')}, {ctx.author}')
    print(f'[{get_time('date')}] [{log('info')}]     {Fore.LIGHTMAGENTA_EX}System.Said_hi{Style.RESET_ALL} to {ctx.author}')

@bot.command('generate_key')
async def generate_key(ctx, amount: int, length: int):
    if amount <= 0:
        await ctx.send('Amount cannot be lower or equal to 0.')
    elif amount > 32:
        await ctx.send('Amount cannot be higher than 32.')

    if length <= 0:
        await ctx.send('Amount cannot be lower or equal to 0.')
    elif length > 128:
        await ctx.send('Amount cannot be higher than 128.')

    keys = key_generator(amount, length)
    await ctx.send(f'Generated {amount} key(s):\n' + '\n'.join(f'`donotshare==> {key} <==withanyone`' for key in keys))
    print(f'[{get_time('date')}] [{log('info')}]     {Fore.LIGHTMAGENTA_EX}System.Generated_keys{Style.RESET_ALL} for {ctx.author}')

@bot.command('flip_a_coin')
async def flip_a_coin(ctx):
    await ctx.send(random.choice(['heads','tails']))
    print(f'[{get_time('date')}] [{log('info')}]     {Fore.LIGHTMAGENTA_EX}System.Flipped_a_coin{Style.RESET_ALL}')

@bot.command('roll_a_dice')
async def roll_a_dice(ctx):
    await ctx.send(random.randint(1, 6))
    print(f'[{get_time('date')}] [{log('info')}]     {Fore.LIGHTMAGENTA_EX}System.Rolled_a_dice{Style.RESET_ALL}')

@tasks.loop(hours=6)
async def random_meme():
    meme = get_meme()
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    with open(f'{path}/images/{meme}', 'rb') as f:
        picture = discord.File(f)
        channel = bot.get_channel(1326946989342199929)
        if channel:
            await channel.send(file=picture)
            print(f'[{get_time('date')}] [{log('info')}]     {Fore.LIGHTMAGENTA_EX}System.Sent_meme{Style.RESET_ALL}')
#-------------------------------------------------# Side Functions
#def get_meme(): #!!!!!!!!!!!!!!!!PAY ATTENTION HERE#!!!!!!!!!!!!!!!!
#    meme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images') #make your own folder with memes, since i was not able to find any free API with memes i had to install a few online
#    meme_dir  = os.listdir(meme_path)
#return random.choice(meme_dir)

def get_fox_image_url():
    url = 'https://randomfox.ca/floof/'
    try:
        res = requests.get(url)
        data = res.json()
        if res.status_code == 200:
            return data['image']
    except Exception as e:
        return f'https://http.cat/{res.status_code}'

def get_cat_image_url():    
    url = 'https://api.thecatapi.com/v1/images/search?limit=1'
    try:
        res = requests.get(url)
        data = res.json()
        return data[0]['url']
    except Exception as e:
        return f'https://http.cat/{res.status_code}'

def get_time(time_type):
    if time_type == 'date':
        return datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    elif time_type == 'time_of_the_day':
        return 'morning' if 6 <= datetime.now().hour < 12 else 'afternoon' if 12 <= datetime.now().hour < 18 else 'evening' if 18 <= datetime.now().hour < 24 else 'night'

def make_os(command):
    if command == 'clear':
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')

def log(request):
    if request == 'info':
        return f'{Fore.LIGHTBLUE_EX}INFO{Style.RESET_ALL}'
    elif request == 'warn':
        return f'{Fore.RED}WARN{Style.RESET_ALL}'

def key_generator(amount, length):
    chars = '+-/*!&$#?=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    keys = []
    for i in range(amount):
        key = ''.join(random.choices(chars, k=length))
        keys.append(key)
    return keys

def initialization():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bots.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tokens WHERE tag = '#0214'")
    profile = cursor.fetchall()
    for data in profile:
        token = data[1]
    bot.run(token)

if __name__ == '__main__':
    initialization()import random, discord, time, os, platform, sqlite3
from colorama import Fore, Style
from datetime import datetime

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client  = discord.Client(intents=intents)
commands = [
    '$hi ~ say hi to me',
    '$flip_a_coin ~ maybe i will flip a coin',
    '$generate_key <amount> <length> ~ i will generate different safe and complex keys'
    ]

@client.event
async def on_ready():
    make_os('clear')
    print(f'[{get_time('date')}] [{log('info')}]     {Fore.LIGHTMAGENTA_EX}System.booted_as{Style.RESET_ALL} {client.user}')

@client.event
async def on_message(message):
    print(f'[{get_time('date')}] [{log('info')}]     {Fore.LIGHTMAGENTA_EX}author:{Style.RESET_ALL} {message.author} {Fore.LIGHTMAGENTA_EX}content:{Style.RESET_ALL} {message.content}')
    if message.author == client.user:
        return
    
    elif message.content.startswith('$help'):
        await message.channel.send('Available commands: \n' + '\n'.join(f'`{command}`' for command in commands))

    if message.content.startswith('$hi'):
        await message.channel.send(f'good {get_time('time_of_the_day')}, <@{message.author.id}>')

    elif message.content.startswith('$generate_key'):
        args = message.content.split()
        if len(args) < 3:
            await message.channel.send('Usage: `$generate_key <amount> <length>`')
            return
        try:
            amount, lenght = int(args[1]), int(args[2])
            if amount <= 0:
                await message.channel.send('Amount cannot be lower or equal to 0.')
            elif amount > 128:
                await message.channel.send('Amount cannot be higher than 128.')

            if lenght <= 0:
                await message.channel.send('Amount cannot be lower or equal to 0.')
            elif lenght > 128:
                await message.channel.send('Amount cannot be higher than 32.')

            keys = key_generator(amount, lenght)
            await message.channel.send(f'Generated {amount} key(s):\n' + '\n'.join(f'`{key}`' for key in keys))

        except ValueError as e:
            await message.channel.send(f'You must insert numbers as arguments.')

        except Exception as e:
            await message.channel.send(f'Unexpected error: {e}')

    elif message.content.startswith('$flip_a_coin'):
        await message.channel.send(f'{random.choice(['heads','tails'])}')

def key_generator(amount, lenght):
    chars = '+-/*!&$#?=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    keys = []
    for i in range(amount):
        key = ''.join(random.choices(chars, k=lenght))
        keys.append(key)
    return keys

def get_time(request):
    if request == 'date':
        return datetime.now().strftime(f'%Y-%m-%d %H:%M:%S')
    elif request == 'time_of_the_day':
        hour = int(datetime.now().strftime(f'%H'))
        if hour < 12:
            return 'morning'
        elif hour <18:
            return 'afternoon'
        elif hour <22:
            return 'evening'
        else:
            return 'night'

def log(request):
    if request == 'info':
        return f'{Fore.LIGHTBLUE_EX}INFO{Style.RESET_ALL}'
    elif request == 'warn':
        return f'{Fore.RED}WARN{Style.RESET_ALL}'

def make_os(command):
    if command == 'clear':
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')

def initialization():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bots.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tokens WHERE tag = 'heheguess :P'")
    profile = cursor.fetchall()
    for data in profile:
        token = data[1]
    client.run(token)

if __name__ == '__main__':
    initialization()
