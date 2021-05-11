from telethon.tl.functions.users import GetFullUserRequest
from telethon.sync import TelegramClient, events
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from config import api_hash, api_id, priv_chat_link
from os import popen
from emoji import emojize
import re
import asyncio

hero = emojize(":sports_medal:Герой")

def parse_sessions():
    """ Take to array all sessions from 'session/' dir """
    DIR = "sessions"
    ls = popen("ls "+DIR+"/").read()
    rels = re.findall(".+\.session", ls)
    return rels

async def send_get(cli_name):
    """ tmp shity func """
    cli = TelegramClient(cli_name, api_id, api_hash)
    await cli.start()
    await cli.send_message('ChatWarsBot', hero)
    print(f"[+] {cli_name} message sended")
    await asyncio.sleep(3)
    msg = await cli.get_messages("ChatWarsBot")
    msg = str(msg[0].message)
    rmsg = msg.split("\n")
    lvlup = re.findall("Поздравляем! Новый уровень!",rmsg[0])
    ent = await cli.get_entity(priv_chat_link)
    prc = PeerChat(ent.id)
    if lvlup != []:
        #print("LevelUP!")
        print(rmsg[5])
        await cli.send_message(prc, emojize(rmsg[5]))
    else:
        print(rmsg[2])
        await cli.send_message(prc, emojize(rmsg[2]))
    await cli.disconnect()
    print(f"[-] {cli} disconnected")

async def main():
    sessions = parse_sessions()
    for s in range(len(sessions)):
        sessions[s] = "sessions/"+ sessions[s]
    print(sessions)
    await asyncio.gather(send_get(sessions[0]),send_get(sessions[1]),send_get(sessions[2]))

asyncio.run(main())
