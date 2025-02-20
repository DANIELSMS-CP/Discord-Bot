import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import requests
import random

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

# TODO : Codeforces Problem Dispenser
@client.command()
async def gitgud(ctx, handle: str, rating: int):
    await ctx.send(f'Problem for {handle} with rating {rating}')
    link_problem = "https://codeforces.com/api/problemset.problems"
    link_handle = f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=10000"
    req_problem = requests.get(link_problem, timeout=10)
    req_handle = requests.get(link_handle, timeout=10)
    problem_data = req_problem.json()
    handle_data = req_handle.json()
    if problem_data.get('status') != 'OK':
        await ctx.send("Codeforces problems API is unavailable")
        return
    eligible_problems = [p for p in problem_data['result']['problems'] if p.get('rating') == rating]
    solved = [f"{sub['problem']['contestId']}{sub['problem']['index']}" for sub in handle_data['result'] if sub.get('verdict') == 'OK']
    MAX_ATTEMPTS = 180
    while MAX_ATTEMPTS:
        problem = random.choice(eligible_problems)
        id = f"{problem['contestId']}{problem['index']}"
        if id not in solved:
            url = f"https://codeforces.com/problemset/problem/{problem['contestId']}/{problem['index']}"
            await ctx.send(f"**Recommended problem for {handle}** (rating {rating}):\n{url}")
            return
        MAX_ATTEMPTS -= 1
    await ctx.send('No Problem Found :(')

# @client.event # TODO: fix
# async def on_member_join(member):
#     channel = client.get_channel(1282737788084555928)
#     await channel.send('Hi, welcome!')

client.run(os.getenv('TOKEN'))