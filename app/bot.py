# app/bot.py

import os
import threading
import discord
import requests
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn

# .env から環境変数をロード
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
API_URL = os.getenv("API_URL")

# Discord Intents の設定
intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容を取得する場合は必須
client = discord.Client(intents=intents)

# FastAPI アプリ（Koyeb ヘルスチェック用）
app = FastAPI()

@app.get("/")
def root():
    return {"status": "running"}

# Discord Bot イベント
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

# Discord Bot を別スレッドで起動
def run_bot():
    client.run(TOKEN)

threading.Thread(target=run_bot).start()

# FastAPI サーバを起動（Koyeb のヘルスチェック用）
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
