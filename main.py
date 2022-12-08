import requests
from pprint import pprint
import json

def users_info(id): #получаем информацию о пользователе
    with open('vk_token.txt', 'r') as f:
        token = f.read().strip()
    # id = 69717407
    URL = 'https://api.vk.com/method/users.get'
    params = {
        'user_ids': id,
        'access_token': token, # токен и версия api являются обязательными параметрами во всех запросах к vk
        'v':'5.131',
        'fields': 'education,sex'
    }
    res = requests.get(URL, params=params).json()
    info = res['response']
    # dict_name_user = {}
    for info in res['response']:
        dict_name_user1 = {'first_name': info['first_name'], 'last_name': info['last_name'], 'id': info['id']}
        # dict_name_user.append(dict_name_user1)
    print(f'Информация о пользоваетеле {dict_name_user1["first_name"]} {dict_name_user1["last_name"]} получена')
    return get_photo (dict_name_user1["id"])

def get_photo (id): #Получение информации о фото пользователя
    dict_photo_like = []
    count = int(input('Скольео фотограй вы хотите скачать: '))
    with open('vk_token.txt', 'r') as f:
        vk_token = f.read().strip()
    photo_url = 'https://api.vk.com/method/photos.get'
    photo_params = {
        'access_token': vk_token,
        'v': '5.131',
        'owner_id': id,
        'album_id': 'profile',
        'rev': 0,
        'extended': 1,
        'photo_sizes': 1,
        'count': count
    }
    res = requests.get(photo_url, params=photo_params).json()

    for item in res['response']['items']:
        for items in item['sizes']:
            if items['type'] == 'z':
                dict_photo_like1 = {'file_name': item['likes']['count'], 'link': items['url'], 'size': items['type']}
                dict_photo_like.append(dict_photo_like1)
    with open('dict_photo_like.json', 'w') as outfile:
        json.dump(dict_photo_like, outfile)
    pprint(dict_photo_like)
    return create_directory(input('Введите название директории в Яндекс Диске, в которую будет закачен файл: '))
#     # pprint(dict_photo_like)
#     # create_directory(id)
#
def create_directory(name_dir):
    with open('ya_token.txt', 'r') as file:
        yandex_token = file.read().strip()
    yandex_url = "https://cloud-api.yandex.net/v1/disk/resources"
    yandex_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'OAuth {yandex_token}'}

    rez = requests.put(f'{yandex_url}?path={name_dir}', headers=yandex_headers)
    # print(rez.status_code)
    if rez.status_code == 201:
        print(f"Каталог '{name_dir}' создан")
    elif rez.status_code == 409:
        print(f"Такой каталог '{name_dir}' уже создан")
    else:
        print(f"Error {rez.status_code}")
    return upload_file(name_dir)
#
def upload_file(dir_disk):
    with open('ya_token.txt', 'r') as file:
        yandex_token = file.read().strip()
    yandex_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    yandex_headers = {
        'Content-Type': 'application/json',
        # 'Accept': 'application/json',
        'Authorization': f'OAuth {yandex_token}'}

    with open("dict_photo_like.json", "r", encoding='utf-8') as read_file:
        dict_photo_like = json.load(read_file)

    for d in dict_photo_like:
        file_name = d['file_name']
        link = d['link']
        params = {"path": f'{dir_disk}/{file_name}', "url": link, "overwrite": "true"}
        response = requests.post(yandex_url, params=params, headers=yandex_headers, )

        if response.status_code == 201:
            print(f"Файл '{file_name}' создан")
        elif response.status_code == 202:
            print(f"Файл '{file_name}' записан повторно")
        else:
            print(f"Error {response.status_code}")


if __name__ == '__main__':
    pprint(users_info(input('Введите ID пользователя Вконтакте: ')))

# 69717407
# 34044962
# 667783273
# 265526713


