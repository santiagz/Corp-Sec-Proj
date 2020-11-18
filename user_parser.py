#Imports
import config
from telethon.sync import TelegramClient
from telethon import connection
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.messages import GetHistoryRequest

import sqlite3 as sq

client = TelegramClient("USER_NAME",config.api_id, config.api_hash)
client.start()

async def main():
    url = "" #URL for chat which u want to parse
    channel = await client.get_entity(url)
    await dump_all_users(channel)

async def dump_all_users(channel):
    offset_user = 0
    limit_user = 1500
    all_users = []
    filter_user = ChannelParticipantsSearch('')

    while True:
        users = await client(GetParticipantsRequest(channel,filter_user,offset_user,limit_user, hash=0))
        if not users.users:
            break
        all_users.extend(users.users)
        offset_user += len(users.users)

    detailed_users = []

    for user in all_users:
        detailed_users.append([user.id,user.username, user.first_name, user.phone])

    for i in detailed_users:
        db_proccess(int(i[0]), str(i[1]), str(i[2]),str(i[3]))
    

def db_proccess(id:int, username:str, first_name:str, phone:str):
    # NAME YOUR DB
    with sq.connect("db.db") as con:
        cur = con.cursor()
        create = "CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, first_name TEXT, phone TEXT)"
        test_input = f"INSERT INTO users VALUES({id}, '{username}','{first_name}','{phone}')"
        cur.execute(create)
        try:
            cur.execute(test_input)
        except Exception as e:
            print("Somethind gone wrong...\nSkiping")
            pass


with client:
    client.loop.run_until_complete(main())
