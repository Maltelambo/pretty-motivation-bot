import discord
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

client = discord.Client(intents=intents)

VOTING_CHANNEL_ID = int(os.environ["VOTING_CHANNEL_ID"])

@client.event
async def on_ready():
    print(f"Bot eingeloggt als {client.user}")
    print(f"Ueberwache Forum-Kanal ID: {VOTING_CHANNEL_ID}")

@client.event
async def on_thread_create(thread):
    print(f"Neuer Thread: {thread.name} | parent_id: {thread.parent_id}")
    if thread.parent_id == VOTING_CHANNEL_ID:
        # kurz warten bis die Starter-Message verfuegbar ist
        await asyncio.sleep(1)
        try:
            # Starter-Message des Forum-Posts holen
            starter_message = await thread.fetch_message(thread.id)
            await starter_message.add_reaction("\U0001f44d")
            await starter_message.add_reaction("\U0001f44e")
            print(f"Reaktionen hinzugefuegt zu: {thread.name}")
        except Exception as e:
            print(f"Fehler bei {thread.name}: {e}")
            # Fallback: erste Nachricht aus History
            try:
                async for message in thread.history(limit=1, oldest_first=True):
                    await message.add_reaction("\U0001f44d")
                    await message.add_reaction("\U0001f44e")
                    print(f"Fallback Reaktionen hinzugefuegt zu: {thread.name}")
            except Exception as e2:
                print(f"Fallback auch fehlgeschlagen: {e2}")

client.run(os.environ["DISCORD_TOKEN"])
