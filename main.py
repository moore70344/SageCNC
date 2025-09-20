# main.py
import os, threading, uvicorn
import discord
from discord.ext import commands
from dotenv import load_dotenv
from web.app import app  # FastAPI dashboard

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True  # for channel name caching / analytics

bot = commands.Bot(command_prefix="!", intents=intents)

INITIAL_EXTS = [
    "cogs.woodworking",
    "cogs.cnctutor",
    "cogs.brainstorm",
    "cogs.ingest",
]

def run_api():
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run("web.app:app", host="0.0.0.0", port=port, log_level="info")

@bot.event
async def on_ready():
    # Load cogs
    for ext in INITIAL_EXTS:
        try:
            await bot.load_extension(ext)
            print(f"Loaded {ext}")
        except Exception as e:
            print(f"Failed {ext}: {e}")

    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Slash sync error: {e}")

    print(f"✅ {bot.user} is online.")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong!")

if __name__ == "__main__":
    threading.Thread(target=run_api, daemon=True).start()
    if not TOKEN:
        raise SystemExit("Missing DISCORD_TOKEN")
    bot.run(TOKEN)
