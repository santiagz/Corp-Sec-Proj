from telethon.sync import TelegramClient, events
from config import api_id, api_hash
from loguru import logger
from time import sleep

logger.add("def_cow.json", format="{time} {level} {message}", level="INFO", rotation="5 MB", compression="zip", serialize=True)

client = TelegramClient('sessions/name.session',api_id,api_hash)

@client.on(events.NewMessage(chats=("ChatWarsBot")))
async def my_handler(event):
    new_msg = event.message
    if new_msg.message.endswith("КОРОВАН."):
        logger.info("Detected!")
        sleep(26)
        msg = await client.get_messages("ChatWarsBot")
        if await msg[0].click(0) == None:
            await msg[0].click()
            logger.error("None was detected, replying click...")
        else:
            logger.info("Successfully defended cow from first time!")
    else:
        pass


client.start()
client.run_until_disconnected()
