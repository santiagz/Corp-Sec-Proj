import asyncio
from telethon.sync import TelegramClient, events
from config import api_id, api_hash
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import re

#your words
agr_words = ["#збираємось", "#йдемо", "#чекаємо", "#мусара", "#побачимось", "#пам‘ятай", "#приходьте!", "#скажіть", "#приносьте", "#сюрприз", "#збір", "#учасникам", "#підтримай", "#підтягуйтесь", "#підтримайте", "#приходь", "#приєднуйтесь", "#зустрінемося", "#чекаю", "#відстоюємо", "#відбивати", "#печерське", "#московська", "#володимирська", "#не-кидаємо", "#своїх", "#готуємось", "#затримали", "#відстояти", "#затриманого", "#відіб‘ємо", "#чекаємо", "#досить", "#беремо", "#фарба", "#зброя", "#фаер", "#райвідділок", "#поліція", "#поліції", "#зустрічі", "#друзі", "#до-поширення", "#СІЗО", "#закликаємо", "#закликаю", "#вимагаємо", "#кров", "#крові"]

def find_word(message):
    res = []
    r = [re.findall(i,message) for i in agr_words]
    for i in r:
        if i != []:
            res.append(i[0])
        else:
            pass
    return res

chat = ["GonorKyiv", "NVPatriot", "BKhodakovsky", "rock_in_ua", "tradition_and_order","revdiachat","revdiachannel","ASupersharij","D7_channel","selfdefense_sternenko","D7_comments"]

client = TelegramClient('YOUR_USERNAME',api_id,api_hash)

@client.on(events.NewMessage(chats=(chat)))
async def my_handler(event):
    new_msg = event.message
    parsed = find_word(new_msg.message)
    if parsed != []:
        smessage = ""
        prid = event.message.peer_id.channel_id
        channel_inf = await client.get_entity(PeerChannel(prid))
        date = event.message.date
        res_date = f"{date.day}.{date.month}.{date.year} {date.hour+3}:{date.minute+2}"
        smessage = "Название канала: "+channel_inf.title+f"\nСсылка на пост: https://t.me/{channel_inf.username}/{new_msg.id}"+"\n"
        smessage += "Время поста: "+res_date+"\n"
        smessage += f"Найденое слово: {parsed}\n\nПолый текс сообщения:\n{new_msg.message}"+"\n"
        await client.send_message("https://t.me/LINK_ON_CHANNEL", smessage)
    else:
        pass

client.start()
client.run_until_disconnected()
