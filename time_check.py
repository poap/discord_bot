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


async def check_flag():
    now = datetime.now(timezone(timedelta(hours=9)))
    if now.hour == 11 or now.hour == 18 or now.hour == 20:
        if (now.minute == 56 and now.second >= 30) or (now.minute == 57 and now.second < 30):
            channel = client.get_channel(settings.flag_channel_id)
            if channel is None:
                print(f'Channel not connected ({now})')
            else:
                await channel.send('플래그')
            return True
    return False


async def check_urus():
    now = datetime.now(timezone(timedelta(hours=9)))
    if now.hour == 21 and (now.minute == 45 or now.minute == 30):
        channel = client.get_channel(settings.urus_channel_id)
        if channel is not None:
            await channel.send('아 맞다, 우르스!')
        return True
    return False


async def check_bless_of_guild():
    now = datetime.now(timezone(timedelta(hours=9)))
    if now.weekday == 0 and now.hour == 23 and now.minute == 50:
        channel = client.get_channel(settings.bless_channel_id)
        if channel is not None:
            await channel.send('아 맞다, 길축!')
        return True
    return False


async def time_check(timeout=60):
    while True:
        await check_flag()
        await check_urus()
        await asyncio.sleep(timeout)


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(client.login(settings.bot_id))
    asyncio.ensure_future(client.connect())
    asyncio.ensure_future(time_check())
    loop.run_forever()
except KeyboardInterrupt:
    loop.run_until_complete(client.logout())
finally:
    loop.close()
