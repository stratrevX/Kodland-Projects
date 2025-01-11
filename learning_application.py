import random, discord, time, os, platform, sqlite3
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
    
    cursor.execute("SELECT * FROM tokens WHERE tag = '#0214'")
    profile = cursor.fetchall()
    for data in profile:
        token = data[1]
    client.run(token)

if __name__ == '__main__':
    initialization()