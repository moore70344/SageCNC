import os, asyncio, threading
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN","").strip()
APP_ID = int(os.getenv("APPLICATION_ID","0") or "0")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents, application_id=APP_ID)

def start_api():
    import uvicorn
    try:
        from web.app import app
    except Exception:
        return
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")

t = threading.Thread(target=start_api, daemon=True)
t.start()

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands synced: {len(synced)}")
    except Exception as e:
        print("Slash sync failed:", e)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/help"))
    print(f"Logged in as {bot.user}")

@bot.command(name="ping")
async def ping(ctx): await ctx.send("Pong!")

@bot.tree.command(name="help", description="Show CNC Sage commands")
async def help_cmd(interaction: discord.Interaction):
    text = (
        "**CNC Sage — Commands**\n"
        "/askdocs — answer using your uploads (tries to cite)\n"
        "/woodworking — how-to woodworking\n"
        "/cnctutor — CNC Q&A\n"
        "/brainstorm — project ideas\n"
        "/ingest — upload files\n"
        "/listdocs — list files\n"
        "/vectorize — preview and DXF export\n"
        "/cutlist — starter list + PDF labels\n"
        "/reactionroles_setup — reaction role panel\n"
        "/rolechannel_create|archive|unarchive — role workspaces"
    )
    await interaction.response.send_message(text, ephemeral=True)

@bot.tree.command(name="resync", description="Admin: resync slash commands")
@app_commands.checks.has_permissions(administrator=True)
async def resync(interaction: discord.Interaction):
    synced = await bot.tree.sync()
    await interaction.response.send_message(f"Resynced {len(synced)} commands.", ephemeral=True)

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot: return
    if bot.user and bot.user.mentioned_in(message):
        await message.reply("Hey! Try `/askdocs`, `/woodworking`, or `/cnctutor`. Add refs with `/ingest`.")
    await bot.process_commands(message)

async def load_all():
    for ext in ("cogs.ingest","cogs.qa_generic","cogs.vector_tools","cogs.cutlist_labels","cogs.reaction_roles","cogs.role_channels"):
        try:
            await bot.load_extension(ext)
        except Exception as e:
            print("Failed to load", ext, e)

if __name__ == "__main__":
    if not TOKEN or len(TOKEN) < 50:
        raise SystemExit("DISCORD_TOKEN missing or looks invalid. Put it in .env (spaces around '=' allowed).")
    asyncio.run(load_all())
    bot.run(TOKEN)
