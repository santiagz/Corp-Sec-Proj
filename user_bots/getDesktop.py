from telethon.sync import TelegramClient, events
from telethon.tl.functions.users import GetFullUserRequest
from config import api_id, api_hash
from time import sleep
from os import system
import asyncio

client = TelegramClient('sessions/name.session', api_id, api_hash)

@client.on(events.NewMessage(incoming=True,from_users=777000))
async def return_num(event):
    new_msg = event.message
    print(new_msg.message)

async def main():
    await client.send_message('username',"Trying to log in this session!")
    n = await client(GetFullUserRequest('me'))
    print("NUMBER:",n.user.phone)

with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
