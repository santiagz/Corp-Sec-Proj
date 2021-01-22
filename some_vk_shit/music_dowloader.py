import vk_audio,vk_api,time
vk_session = vk_api.VkApi(login='number or email',password='password')
vk_session.auth()
vk = vk_audio.VkAudio(vk=vk_session)
data = vk.load(id)
audio_list = data.Audios

#TODO: change inputs to argparser and make download(url.mp3) func
#dubug
test_str1 = '344204774_456240014'
test_str2 = '344204774_456240013'
test_str3 = '344204774_456240012'
test_str4 = '344204774_456240011'
test_str5 = '344204774_456240010'
audio_arr = []

def id2mp3(ids:str):
    out = vk.get_by_id(ids)
    return("{url}".format(**out[0].toArray()))

def getTrackIds(i):
    return ("{owner_id}_{id}".format(**audio_list[i].toArray())) 
        #audio_arr.append("{owner_id}_{id}".format(**audio_list[i].toArray()))
        #print("{title} - {artist}; {owner_id}_{id}".format(**audio_list[i].toArray()))

inpt = input("How many tracks u wanna download? ")
inpt = int(inpt)
out = []
for i in range(0,inpt):
    out.append(id2mp3(getTrackIds(i)))
print(out)
