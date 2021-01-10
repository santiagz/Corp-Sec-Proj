#Script to auto upgrade hero level in @ChatWarsBot
from telethon.sync import TelegramClient, events
from emoji import emojize
from config import api_id, api_hash
from time import sleep
import re

debug = emojize(":two_hearts: Obrigalovo")
hero = emojize(":sports_medal:Герой")
quests = emojize(":world_map:Квесты")

def forest_gump(cli):
    if hero_stamina(cli) > 0:
        print("[+]You have stamina, have we go!")
        cli.send_message("ChatWarsBot", quests)
        msg1 = cli.get_messages("ChatWarsBot")
        sleep(2)
        if msg1[0].click() == None:
            print("[-]Click failed")
            forest_gump(cli)
        else:
            msg_time = cli.get_messages("ChatWarsBot")
            print("[+]Debug:", msg_time[0].message)
            msg_time = re.findall("\d", str(msg_time[0].text))
            msg_time = str(msg_time[0])
            msg_time = int(msg_time)
            msg_time *= 60
            print("[+]NOTE: Time you gone forest (in seconds) ==", msg_time)
            msg_time += 30
            sleep(msg_time)
            forest_gump(cli)
    else:
        sleep(3)
        print("[-]No stamina, go to sleep for 5 hours...")
        sleep(18000)
        forest_gump(cli)


def hero_stamina(cli):
    cli.send_message("ChatWarsBot", hero)
    sleep(1)
    msg = cli.get_messages("ChatWarsBot")
    msg = str(msg[0].message)
    stamina = re.findall("Выносливость: .\/.", msg)
    stamina = re.findall("\d", stamina[0])
    stamina = int(stamina[0])
    return stamina

with TelegramClient('#USERNAME#', api_id, api_hash) as client:
    forest_gump(client)

    client.run_until_disconnected()
