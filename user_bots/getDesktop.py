from telethon.sync import TelegramClient, events
from config import api_id, api_hash
from time import sleep
from os import system
from telethon.tl.functions.users import GetFullUserRequest

client = TelegramClient('sessions/name.session', api_id, api_hash)
arr = ["Telegram"]
@client.on(events.NewMessage(chats=(arr)))
async def main(event):
        n = await client(GetFullUserRequest('me'))
        print("NUMBER:",n.user.phone)
        new_msg = event.message
        print(new_msg.message)

client.start()
client.run_until_disconnected()
