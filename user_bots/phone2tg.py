from telethon.sync import TelegramClient, events
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.contacts import DeleteContactsRequest
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon import functions, types
from config import api_id, api_hash
import asyncio

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

with TelegramClient("sessions/name.session",api_id, api_hash) as client:
    client(ImportChatInviteRequest("QLodgkw2yVQXBUkn"))
    hi = client.get_entity('https://t.me/joinchat/QLodgkw2yVQXBUkn')

    phone_list = stupid_make_phone_list("38098078XXXX")

    result = client(functions.contacts.ImportContactsRequest(
        contacts=[types.InputPhoneContact(
            client_id=1498215433,
            phone='+PHONENUMBER',
            first_name='1',
            last_name='1'
        )]
    ))
    uid = result.imported[0].user_id
    uusername = result.users[0].username
    phn = result.users[0].phone
    print(uid,uusername,phn)
    last_ent = client(functions.contacts.DeleteContactsRequest(id=[uid]))
    fn = last_ent.users[0].first_name
    ln = last_ent.users[0].last_name
    print(fn,ln)
