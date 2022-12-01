import requests
from pprint import pprint
import json

dict_photo_like = []
def get_photo (id):
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
        'count': 10
    }
    res = requests.get(photo_url, params=photo_params).json()
    print(f'Информация о пользователе {id} получена')

    for item in res['response']['items']:
        for items in item['sizes']:
            if items['type'] == 'z':
                dict_photo_like1 = {'file_name': item['likes']['count'], 'link': items['url'], 'size': items['type']}
                dict_photo_like.append(dict_photo_like1)
    with open('dict_photo_like.json', 'w') as outfile:
        json.dump(dict_photo_like, outfile)
    # pprint(dict_photo_like)
    create_directory(id)

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
    upload_file(name_dir)

def upload_file(dir_disk):
    with open('ya_token.txt', 'r') as file:
        yandex_token = file.read().strip()
    yandex_url = "https://cloud-api.yandex.net/v1/disk/resources"
    yandex_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'OAuth {yandex_token}'}

    for d in dict_photo_like:
        file_name = d['file_name']
        link = d['link']
        info = requests.post(f"{yandex_url}/upload/?path={dir_disk}/{file_name}.jpg&url={link}", headers=yandex_headers)
        # pprint(info.json())

        if info.status_code == 201:
            print(f"Файл '{file_name}' создан")
        elif info.status_code == 202:
            print(f"Файл '{file_name}' записан повторно")
        else:
            print(f"Error {info.status_code}")


if __name__ == '__main__':
    get_photo('33125771')





