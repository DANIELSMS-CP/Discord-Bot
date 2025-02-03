import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(intents=intents, command_prefix='!')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command()
async def hello(ctx):
    await ctx.send('Hello!')

@client.command()
async def ping(ctx):
    await ctx.send('pong')

@client.command()
async def stalk(ctx, handle: str):
    await ctx.send(f'{handle}: last 10 problems solved')
    link = f'https://codeforces.com/api/user.status?handle={handle}'
    req_info = requests.get(link)
    json_obj = req_info.json()
    last_correct_problems = []
    counter = 0
    for submissions in json_obj['result']:
        if submissions['verdict'] == 'OK':
            last_correct_problems.append(submissions['problem']['name'])
    for problem in last_correct_problems:
        if counter == 10:
            break
        await ctx.send(problem)
        counter += 1

# TODO : 
@client.command()
async def ()

@client.event # TODO: fix
async def on_member_join(member):
    channel = client.get_channel(1282737788084555928)
    await channel.send('Hi, welcome!')

client.run(os.getenv('TOKEN'))