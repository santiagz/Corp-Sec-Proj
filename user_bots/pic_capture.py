from telethon.sync import TelegramClient, events
from telethon.tl.functions.messages import GetHistoryRequest
#from config import api_hash, api_id
from loguru import logger
import argparse
import asyncio

parser = argparse.ArgumentParser(description='Async script to save pictutes from telegram channels')
parser.add_argument('--link',help='Link to channel from which download pictures (example: --link justp1cture)',required=True)
parser.add_argument('--sessfile',help='Location of your telegram session file (example: --sessfile /home/kurassh/ppc/python/tg-bots/user_bots/sessions/justadoll.session)',required=True)
parser.add_argument('--lim',help='How many pictures you wanna download (int)',required=True)
parser.add_argument('--api_id',help='Api ID of yor telegram app (you can create it here https://my.telegram.org/apps)',required=True)
parser.add_argument('--api_hash',help='Api Hash of your app (https://my.telegram.org/apps)',required=True)
args = parser.parse_args()

async def main():
    link = args.link
    sessio = args.sessfile
    client = TelegramClient(sessio,args.api_id,args.api_hash)
    await client.connect()
    ent = await client.get_entity(link)
    posts = await client(GetHistoryRequest(peer=ent,
    limit=int(args.lim),
    offset_date=None,
    offset_id=0,
    max_id=0,
    min_id=0,
    add_offset=0,
    hash=0))
    for i in posts.messages:
        if i.media != None:
            await client.download_media(message=i)
        else:
            pass
    await client.disconnect()
asyncio.run(main())
