#Script to auto upgrade hero level in @ChatWarsBot
from telethon.sync import TelegramClient, events
from emoji import emojize
from config import api_id, api_hash
from time import sleep
import re
#TODO: print time

defence = emojize(":shield:Защита")
hero = emojize(":sports_medal:Герой")
quests = emojize(":world_map:Квесты")

def forest_gump(cli):
    if hero_stamina(cli) > 0:
        print("[+] You have stamina, have we go!")
        cli.send_message("ChatWarsBot", quests)
        msg1 = cli.get_messages("ChatWarsBot")
        sleep(2)
        if msg1[0].click() == None:
            print("[-]Click failed")
            forest_gump(cli)
        else:
            msg_time = cli.get_messages("ChatWarsBot")
            print("[+] Debug:", msg_time[0].message)
            msg_time = re.findall("\d", str(msg_time[0].text))
            msg_time = str(msg_time[0])
            msg_time = int(msg_time)
            msg_time *= 60
            print("[+] Time you gone forest (in seconds) ==", msg_time)
            msg_time += 30
            sleep(msg_time)
            forest_gump(cli)
    else:
        sleep(3)
        print("[-]No stamina, go to sleep for 5 hours...")
        cli.send_message("ChatWarsBot", defence)
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

def krob_de_karavan(cli):
    if hero_stamina(cli) > 1:
        print("[+]You have stamina to robe karavan, have we go!")
        cli.send_message("ChatWarsBot", quests)
        sleep(1)
        msg = cli.get_messages("ChatWarsBot")
        if msg[0].click(1) == None:
            print("[-]Click failed,trying again...")
            krob_de_karavan(cli)
        else:
            msg_time = cli.get_messages("ChatWarsBot")
            print(msg_time[0].message)
            print("[+] OK, you near the karavan, wait 5 minutes")
            tmp = (6*60)+5
            sleep(tmp)
            msg_time = cli.get_messages("ChatWarsBot")
            print(msg_time[0].message)
    else:
        sleep(3)
        print("[-]No stamina, go to sleep for 5 hours...")
        cli.send_message("ChatWarsBot", defence)
        sleep(18000)
        krob_de_karavan(cli)


with TelegramClient('gol0va4_l3na', api_id, api_hash) as client:
    krob_de_karavan(client)
    #forest_gump(client)

    client.run_until_disconnected()
