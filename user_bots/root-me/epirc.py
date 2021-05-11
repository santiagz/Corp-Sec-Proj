""" IRC user_bot to pwn first 4 tasks"""
from pwn import *
from math import sqrt
from base64 import b64decode
from codecs import decode
from zlib import decompress
import re
import time


def ep1(session):
    session.send("PRIVMSG candy :!ep1\n")
    time.sleep(0.1)
    session.send("PRIVMSG kijabo ama running!\n")
    data = session.recvuntil("ama running")
    data = str(data.decode("UTF-8"))
    r = re.findall("\d+ \/ \d+",data)[0]
    nums = r.split("/")
    nums[0] = int(nums[0])
    nums[1] = int(nums[1])
    print(nums)
    res = round(sqrt(nums[0]) * nums[1],2)
    session.send(f"PRIVMSG candy !ep1 -rep {str(res)}\n")
    time.sleep(0.1)
    session.recvline()
    last_msg = session.recvline()
    return str(last_msg.decode("UTF-8"))


def ep2(session):
    session.send("PRIVMSG candy :!ep2\n")
    time.sleep(0.1)
    session.send("PRIVMSG kijabo ama running!\n")
    data = session.recvuntil("ama running")
    data = str(data.decode("UTF-8"))
    r = re.findall("PRIVMSG kijabo :\w+",data)[0]
    encdata = r.split(":")[1]+"=="
    decdata = b64decode(encdata)
    decdata = decdata.decode("UTF-8")

    #print("encoded:",encdata)
    session.send(f"PRIVMSG candy !ep2 -rep {str(decdata)}\n")
    time.sleep(0.1)
    session.recvline()
    last_msg = session.recvline()
    return str(last_msg.decode("UTF-8"))

def ep3(session):
    session.send("PRIVMSG candy :!ep3\n")
    time.sleep(0.1)
    session.send("PRIVMSG kijabo ama running!\n")
    data = session.recvuntil("ama running")
    data = str(data.decode("UTF-8"))
    r = re.findall("PRIVMSG kijabo :\w+",data)[0]
    encdata = r.split(":")[1]
    res = decode(encdata,"rot_13")
    session.send(f"PRIVMSG candy !ep3 -rep {str(res)}\n")
    time.sleep(0.1)
    session.recvline()
    last_msg = session.recvline()
    return str(last_msg.decode("UTF-8"))

def ep4(session):
    session.send("PRIVMSG candy :!ep4\n")
    time.sleep(0.1)
    session.send("PRIVMSG kijabo ama running!\n")
    data = session.recvuntil("ama running")
    data = str(data.decode("UTF-8"))
    r = re.findall("PRIVMSG kijabo :\w+",data)[0]
    encdata = r.split(":")[1]
    print("enc:",encdata)
    try:
        decdata = b64decode(encdata)
        res = decompress(decdata)
        res = res.decode("UTF-8")
        session.send(f"PRIVMSG candy !ep4 -rep {str(res)}\n")
        time.sleep(0.1)
        session.recvline()
        last_msg = session.recvline()
        return str(last_msg.decode("UTF-8"))
    except Exception:
        return "Fake data..."


s = remote("irc.root-me.org",6667)
s.send("NICK kijabo\n")
s.send("USER kijabo 8 x : root-me_challenge\n")
time.sleep(1)
s.send("JOIN #root-me_challenge\n")
print(ep4(s))
