# main.py
import os
import threading
import uvicorn
import discord
from discord.ext import commands
from dotenv import load_dotenv

# ---- load env ----
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise SystemExit("Missing DISCORD_TOKEN in environment or .env")
if len(TOKEN) < 50 or TOKEN.count(".") < 2:
    raise SystemExit("DISCORD_TOKEN looks invalid (not a Bot token from the Bot tab).")

# ---- intents & bot ----
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

INITIAL_EXTS = [
    "cogs.help",        # slash /help
    "cogs.woodworking",
    "cogs.cnctutor",
    "cogs.brainstorm",
    "cogs.ingest",
]

# ---- dashboard server ----
def run_api() -> None:
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run("web.app:app", host="0.0.0.0", port=port, log_level="info")

@bot.event
async def on_ready():
    for ext in INITIAL_EXTS:
        try:
            await bot.load_extension(ext)
            print(f"Loaded {ext}")
        except Exception as e:
            print(f"Failed {ext}: {e}")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Slash sync error: {e}")

    print(f"✅ {bot.user} is online.")

# simple prefix ping (sanity check)
@bot.command(name="ping")
async def ping(ctx: commands.Context):
    await ctx.send("Pong!")

# admin-only manual resync for slash commands
@bot.command(name="resync")
@commands.has_permissions(administrator=True)
async def resync(ctx: commands.Context):
    synced = await bot.tree.sync()
    await ctx.send(f"🔁 Resynced {len(synced)} slash commands.")

if __name__ == "__main__":
    threading.Thread(target=run_api, daemon=True).start()
    bot.run(TOKEN)
