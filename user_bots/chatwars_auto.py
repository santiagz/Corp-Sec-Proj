#Script to auto upgrade hero level in @ChatWarsBot
from telethon.sync import TelegramClient, events
from telethon.tl.functions.users import GetFullUserRequest
from emoji import emojize
from config import api_id, api_hash
from time import sleep
from os import popen
from loguru import logger
import re
import asyncio
#TODO: optimyze cli send and get msg
defence = emojize(":shield:Защита")
hero = emojize(":sports_medal:Герой")
quests = emojize(":world_map:Квесты")
castle = emojize("🏰Замок")

logger.add("debug.json", format="{time} {level} {message}", level="INFO", rotation="5 MB", compression="zip", serialize=True)

def parse_sessions():
    """ Take to array all sessions from 'session/' dir """
    DIR = "sessions"
    ls = popen("ls "+DIR+"/").read()
    rels = re.findall(".+\.session", ls)
    return rels

def get_game_time(cli):
    cli.send_message("ChatWarsBot", castle)
    sleep(0.6)
    msg = cli.get_messages("ChatWarsBot")
    spl = msg[0].message.split("\n")
    r = re.findall("\w+",spl[1])
    if(r[0] == "Утро"):
        logger.debug("Mountains!")
        return 2
    elif(r[0] == "День"):
        logger.debug("Forest!")
        return 0
    else:
        logger.debug("Swamp!")
        return 1

def quest_auto(cli, lvl):
    """ Function that go client to forest while have stamina """
    stam = hero_stamina(cli)
    logger.debug("Stamina: "+str(stam))
    if stam > 0:
        logger.info("Session have stamina, have we go!")
        cli.send_message("ChatWarsBot", quests)
        msg1 = cli.get_messages("ChatWarsBot")
        sleep(2)
        if lvl >= 20:
            button = get_game_time(cli)
        elif lvl < 20:
            button = 0

        if msg1[0].click(button) == None:
            logger.error("Click failed")
            quest_auto(cli,lvl)
        else:
            msg_time = cli.get_messages("ChatWarsBot")
            logger.debug(msg_time[0].message)
            msg_time = re.findall("\d+", str(msg_time[0].text))
            try:
                msg_time = str(msg_time[0])
                msg_time = int(msg_time)
                msg_time *= 60
                logger.info("Time in quest: "+str(msg_time))
                msg_time += 20
                sleep(msg_time)
                return True
            except Exception:
                logger.error("Something gone wrong!")

    else:
        sleep(3)
        logger.debug("No stamina! Return False")
        cli.send_message("ChatWarsBot", defence)
        return False


def hero_stamina(cli):
    """ Check how many stamina client have  """
    cli.send_message("ChatWarsBot", hero)
    sleep(1)
    msg = cli.get_messages("ChatWarsBot")
    msg = str(msg[0].message)
    stamina = re.findall("Выносливость: \d+\/\d+", msg)
    logger.debug("Re_Stamina: "+str(stamina))
    stamina = re.findall("\d", stamina[0])
    logger.debug("Stamina[0]: "+str(stamina))
    stamina = int(stamina[0])
    return stamina


def hero_level(cli):
    cli.send_message("ChatWarsBot", hero)
    sleep(1)
    msg = cli.get_messages("ChatWarsBot")
    msg = str(msg[0].message)
    rd = re.findall("Уровень: \d+", msg)
    rs = int(re.findall("\d+",rd[0])[0])
    return rs

def krob_de_karavan(cli):
    """ Same as 'forest_gump' but client goes on karavan  """
    #TODO: return True, False
    if hero_stamina(cli) > 1:
        logger.info("Session have stamina to robe karavan, have we go!")
        cli.send_message("ChatWarsBot", quests)
        sleep(1)
        msg = cli.get_messages("ChatWarsBot")
        if msg[0].click(1) == None:
            logger.error("Click failed,trying again...")
            krob_de_karavan(cli)
        else:
            msg_time = cli.get_messages("ChatWarsBot")
            logger.info("Session near the karavan, wait 5 minutes")
            tmp = (6*60)+5
            sleep(tmp)
            msg_time = cli.get_messages("ChatWarsBot")
            logger.info(msg_time[0].message)
    else:
        sleep(3)
        logger.debug("No stamina, go to sleep for 5 hours...")
        cli.send_message("ChatWarsBot", defence)
        sleep(18000)


def main():
    #with TelegramClient("sessions/name.session", api_id, api_hash) as client:
    #    get_game_time(client)
    sessions = parse_sessions()
    logger.debug("Sessions: "+str(sessions))
    for session in sessions:
        sessdir = "sessions/"+session
        logger.debug("Sessdir: "+str(sessdir))
        with TelegramClient(sessdir, api_id, api_hash) as client:
            loop = hero_stamina(client)
            lvl = hero_level(client)
            for i in range(loop):
                quest_auto(client,lvl)

        """
            lvl = hero_level(client)
            full = client(GetFullUserRequest(session.split(".")[0]))
            logger.debug(full.user.username+" in FOR!")
            while quest_auto(client,lvl):
                logger.debug(f"While is working with {sessdir}")
                continue
            else:
                logger.debug(f"Else worked in while with {sessdir}")
                #pass

        """
        #client.run_until_disconnected()

main()
