#TZ - get and set by user id count of cigarets
# must te shown info like "1.10.19 - You rolled {n} cigarets {time}"
#TODO fix except in set_count
#TODO "delete count" func by id
from aiogram import Bot, types
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher

from aiogram.utils.exceptions import MessageTextIsEmpty
import logging
from config import TOKEN
from messages import MESSAGES
import sqlite3 as sq

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def db_worker(id, date, count):
   with sq.connect("db.db") as con:
        cur = con.cursor()
        create = "CREATE TABLE IF NOT EXISTS users (id INTEGER, date TEXT, count INTEGER)"
        test_input = f"INSERT INTO users VALUES({id},'{date}', {count})"
        cur.execute(create)
        cur.execute(test_input)

def db_selector(id):
    with sq.connect("db.db") as con:
        cur = con.cursor()
        select = f"SELECT SUM(count) FROM users WHERE id = {id};"
        cur.execute(select)
        result = cur.fetchall()
        return result[0][0]

@dp.message_handler(commands=["start","help"])
async def proc_start_help(msg:types.Message):
    await bot.send_message(msg.chat.id, MESSAGES['start'])


@dp.message_handler(commands=["get_count"])
async def proc_get_count(msg:types.Message):
    summ = db_selector(msg.from_user.id)
    await msg.reply(f"To sum up - you rolled/smoked {summ} cigarets") #Add time here


@dp.message_handler(commands=["set_count"])
async def proc_set_count(msg:types.Message):
    whois = msg.from_user.id
    date = msg.date
    print(whois, date)
    argument = msg.get_args()
    #Check if it`s int
    argument = int(argument)
    db_worker(whois, date, argument)
    await msg.reply(f"Saved {argument}")
    
if __name__ == '__main__':
    executor.start_polling(dp)
