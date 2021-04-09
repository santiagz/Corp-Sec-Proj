from telethon.sync import TelegramClient, events
from config import api_id, api_hash
from time import sleep
from os import system
from telethon.tl.functions.users import GetFullUserRequest
with TelegramClient('sessions/name.session', api_id, api_hash) as client:
    n = client(GetFullUserRequest('me'))
    print(n.user.phone)
    for i in range(5):
        sleep(3)
        system('clear')
        for message in client.iter_messages('Telegram',limit=3):
            print(message.text)
