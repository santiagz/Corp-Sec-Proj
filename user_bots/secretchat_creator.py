from telethon.sync import TelegramClient,events
from telethon_secret_chat import SecretChatManager
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from config import api_id, api_hash
import asyncio

client = TelegramClient("sessions/name.session",api_id,api_hash)

async def new_chat(chat, created_by_me):
    if created_by_me:
        print("User {} has accepted our secret chat request".format(chat))
    else:
        print("We have accepted the secret chat request of \n{}".format(chat))

chat = ["client","user","names"]
#check chats on "secret!" message and start new)secret chat
@client.on(events.NewMessage(chats=(chat),pattern='(?i)secret!+'))
async def handlr(event):
    new_msg = event.message
    whois = await client.get_entity(event.peer_id)
    print(whois.username)
    manager = SecretChatManager(client, auto_accept=True,new_chat_created=new_chat, session=db_conn)
    await manager.start_secret_chat(whois.username)

client.start()
client.run_until_disconnected()

#asyncio.run(main())
