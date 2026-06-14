import discord
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

VOTING_CHANNEL_ID = int(os.environ["VOTING_CHANNEL_ID"])

@client.event
async def on_ready():
    print(f"Bot eingeloggt als {client.user}")
    print(f"Ueberwache Forum-Kanal ID: {VOTING_CHANNEL_ID}")

@client.event
async def on_thread_create(thread):
    if thread.parent_id == VOTING_CHANNEL_ID:
        await thread.join()
        async for message in thread.history(limit=1, oldest_first=True):
            await message.add_reaction("👍")
            await message.add_reaction("👎")
            print(f"Reaktionen hinzugefuegt zu: {thread.name}")

client.run(os.environ["DISCORD_TOKEN"])
