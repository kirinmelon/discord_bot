import os
import discord
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
API_URL = os.getenv("API_URL")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot connected as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!sv_start"):
        resp = requests.post(API_URL, json={"action": "start"})
        await message.channel.send(resp.text)

    elif message.content.startswith("!sv_stop"):
        resp = requests.post(API_URL, json={"action": "stop"})
        await message.channel.send(resp.text)

    elif message.content.startswith("!sv_ip"):
        resp = requests.get(API_URL)
        await message.channel.send(resp.text)

client.run(TOKEN)
