import asyncio
from datetime import datetime, timezone, timedelta
import discord
import settings

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('hello')
    activity = discord.Game(name="플래그 시간 체크")
    await client.change_presence(status=discord.Status.idle, activity=activity)


async def check_time():
    now = datetime.now(timezone(timedelta(hours=9)))
    if now.hour == 12 or now.hour == 19 or now.hour == 21:
        if (now.minute == 56 and now.second >= 30) or (now.minute == 57 and now.second < 30):
            channel = client.get_channel(settings.flag_channel_id)
            if channel is None:
                print(f'Channel not connected ({now})')
            else:
                await channel.send('플래그')


async def flag_loop(timeout=60):
    while True:
        await check_time()
        await asyncio.sleep(timeout)


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(client.login(settings.bot_id))
    asyncio.ensure_future(client.connect())
    asyncio.ensure_future(flag_loop())
    loop.run_forever()
except KeyboardInterrupt:
    loop.run_until_complete(client.logout())
finally:
    loop.close()
