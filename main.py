import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def get_price():
    api_url = "https://min-api.cryptocompare.com/data/generateAvg?fsym=BTC&tsym=USD&e=coinbase"
    response = requests.get(api_url)
    data = response.json()
    raw_data = data.get("RAW")
    if raw_data:
        pretty_data = json.dumps({"RAW": raw_data}, indent=4)
        return pretty_data
    else:
        return "Data not found"

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello! :3')
    elif message.content.startswith('$bitcoin'):
        price_data = get_price()
        await message.channel.send(f"```json\n{price_data}\n```")

client.run(os.getenv('TOKEN'))