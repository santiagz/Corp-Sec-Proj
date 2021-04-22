from telethon.sync import TelegramClient, events
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.contacts import DeleteContactsRequest
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon import functions, types
from telethon.errors.rpcerrorlist import FloodWaitError
from fake_config import api_id, api_hash
from loguru import logger
from re import findall
import psycopg2
import asyncio
import datetime as dt
import time

logger.add("tg_parser.log", format="{time} {level} {message}", level="INFO", rotation="5 MB", compression="zip", serialize=True)

conn = psycopg2.connect(dbname="postgres", user="postgres", password="passwd",host="localhost")
conn.autocommit = True #or commit after parsing?
db_cur = conn.cursor()
cleardb_payload = "delete from tg_parser *;"

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

def stupid_make_phone_list(mask):
    #example
    #mask = "38098078XXXX"
    c = mask.count("X")
    rstr = ""
    for i in range(c):
        rstr += "9"
    print("counter="+rstr)

    fstr = ""
    for i in range(c):
        fstr += "0"

    fstr = fstr[0:-1]+"1"
    tfloat = "0."+fstr
    it = float(tfloat)

    fx = mask.find("X")
    tmp = it
    result = []
    for i in range(int(rstr)):
        tmp += it
        readystr = mask[0:fx]+str(toFixed(tmp,len(fstr))).split(".")[1]
        result.append(readystr)
    return result

def parse_telegram(phone_list):
    startime = dt.datetime.now()
    logger.info(f"START TIME {startime}")

    for i in phone_list:
        time.sleep(5)
        try:
            result = client(functions.contacts.ImportContactsRequest(
                contacts=[types.InputPhoneContact(
                    client_id=1498215433,
                    phone=f'+{i}',
                    first_name='ragul',
                    last_name='lugar'
                )]
            ))
            if(result.imported == []):
                #print(f"'{i}' didn`t registred or blocked")
                logger.debug(f"{i} not registred of blocked")
            else:
                uid = result.imported[0].user_id
                uusername = result.users[0].username
                phn = result.users[0].phone
                last_ent = client(functions.contacts.DeleteContactsRequest(id=[uid]))
                fn = last_ent.users[0].first_name
                ln = last_ent.users[0].last_name
                payload = f"insert into tg_parser(uid,username,phone,fn,ln) VALUES({uid},\'{uusername}\',\'{phn}\',\'{fn}\',\'{ln}\');"
                logger.debug(payload)
                db_cur.execute(payload)
        except FloodWaitError as FWE:
            FWE = str(FWE)
            delay = findall("\d+",FWE)
            delay = int(delay[0])
            logger.error(f"Flood Exception! Stoped at {i} number")
            logger.error(f"Going to sleep for in {str(delay)} seconds")
            endtime = dt.datetime.now()
            logger.info(f"Script worked for {endtime - startime}")
            time.sleep(delay)
            #break

    endtime = dt.datetime.now()
    logger.info(f"END TIME {endtime - startime}")

with TelegramClient("sessions/name.session",api_id, api_hash) as client:
    #client(ImportChatInviteRequest("QLodgkw2yVQXBUkn"))
    #hi = client.get_entity('https://t.me/joinchat/QLodgkw2yVQXBUkn')

    phone_list = stupid_make_phone_list("38098XXXXXXX")
    parse_telegram(phone_list)
