import vk_api, urllib, os
vk_session = vk_api.VkApi(login='phone_number or email',password='password')
vk_session.auth()
vk = vk_session.get_api() 

#TODO:change inputs to argparser!
pathname = input("Give a name for directory: ")
userdir = os.mkdir(pathname)
cnt = input("How many pictures u wanna take?")
cnt = int(cnt)

response = vk.photos.get(owner_id=int(344204774), album_id="saved", rev=1, photo_sizes=0, count=cnt)
for i in range(len(response["items"])):
    photo_url = str(response["items"][i]["sizes"][len(response["items"][i]["sizes"])-1]["url"])
    urllib.request.urlretrieve(photo_url, pathname + '/' + str(response["items"][i]['id']) + '.jpg')
