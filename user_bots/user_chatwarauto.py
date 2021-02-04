#Script to auto upgrade hero level in @ChatWarsBot
from telethon.sync import TelegramClient, events
from telethon.tl.functions.users import GetFullUserRequest
from emoji import emojize
from config import api_id, api_hash
from time import sleep
import re
#from loguru import logger
from os import popen
from loguru import logger

defence = emojize(":shield:Защита")
hero = emojize(":sports_medal:Герой")
quests = emojize(":world_map:Квесты")

logger.add("debug.json", format="{time} {level} {message}", level="INFO", rotation="5 MB", compression="zip", serialize=True)

def parse_sessions():
    """ Take to array all sessions from 'session/' dir """
    DIR = "sessions"
    ls = popen("ls "+DIR+"/").read()
    rels = re.findall(".+\.session", ls)
    return rels

def forest_gump(cli):
    """ Function that go client to forest while have stamina """
    if hero_stamina(cli) > 0:
        logger.info("Session have stamina, have we go!")
        cli.send_message("ChatWarsBot", quests)
        msg1 = cli.get_messages("ChatWarsBot")
        sleep(2)
        if msg1[0].click(0) == None:
            logger.error("Click failed")
            forest_gump(cli)
        else:
            msg_time = cli.get_messages("ChatWarsBot")
            logger.debug(msg_time[0].message)
            msg_time = re.findall("\d", str(msg_time[0].text))
            msg_time = str(msg_time[0])
            msg_time = int(msg_time)
            msg_time *= 60
            logger.info("Time in forest :"+str(msg_time))
            msg_time += 30
            sleep(msg_time)
            return True
    else:
        sleep(3)
        #logger.debug("No stamina, go to sleep for 5 hours...")
        cli.send_message("ChatWarsBot", defence)
        return False


def hero_stamina(cli):
    """ Check how many stamina client have  """
    cli.send_message("ChatWarsBot", hero)
    sleep(1)
    msg = cli.get_messages("ChatWarsBot")
    msg = str(msg[0].message)
    stamina = re.findall("Выносливость: .\/.", msg)
    stamina = re.findall("\d", stamina[0])
    stamina = int(stamina[0])
    return stamina

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
        krob_de_karavan(cli)


def main():
    sessions = parse_sessions()
    for session in sessions:
        sessdir = "sessions/"+session
        with TelegramClient(sessdir, api_id, api_hash) as client:
            full = client(GetFullUserRequest(session.split(".")[0]))
            logger.info(full.user.username,"in FOR!")
            while forest_gump(client):
                logger.info(sessdir,"{continue...}")
                continue
            else:
                pass
                logger.debug(sessdir,"{pass...}")


        #client.run_until_disconnected()

main()
