import re

#set API and HASH
api_id = 11111
api_hash = "1234567890abcdef1234123"


agr_words = ["trigger"]

def find_word(message):
    res = []
    r = [re.findall(i,message) for i in agr_words]
    for i in r:
        if i != []:
            res.append(i[0])
        else:
            pass
    return res

chat = [-111111111,"another_chat"] #set Chats

client = TelegramClient('frankfrank1',api_id,api_hash) #set name of sesssion

@client.on(events.NewMessage(chats=(chat)))
async def my_handler(event):
    new_msg = event.message
    parsed = find_word(new_msg.message)
    if parsed != []:
        prid = event.message.peer_id.chat_id
        usrid = event.message.from_id.user_id

        date = event.message.date

        chat_inf = await client.get_entity(PeerChat(prid))
        user_inf = await client.get_entity(PeerUser(usrid))

        res_date = f"{date.day}.{date.month}.{date.year} {date.hour+3}:{date.minute+2}"
        smessage = ""
        smessage = "Название чата: "+chat_inf.title+"\n"
        smessage += "Имя отправителя: "+user_inf.first_name+" "+user_inf.last_name+" "+"\n"
        smessage += "Номер телефона: "+ user_inf.phone+"\n"
        smessage += "Username: "+ user_inf.username+"\n"
        smessage += "\nВремя отправки: "+res_date+"\n"
        smessage += f"Найденое слово: {parsed}\n\nПолый текс сообщения:\n{new_msg.message}"+"\n"
        await client.send_message(-123123123123123, smessage) #set Target for Notify
    else:
        pass

client.start()
client.run_until_disconnected()
