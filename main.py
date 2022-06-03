import datetime
import time
import json
from tqdm import tqdm
import requests
from yadisk import YaDisk


def get_token_vk():
    with open("token_vk.txt", encoding="utf-8") as token:
        text = token.read()
    return (text)


def get_token_ya():
    with open("token_ya.txt", encoding="utf-8") as token:
        text = token.read()
    return (text)

def create_folder_yandex():
    ya_token = get_token_ya()
    response = YaDisk(ya_token)
    folder_name = input('Введите имя папки: ')
    request_response = response.create_folder_yandex_(folder_name)
    if request_response:
        return(folder_name)
    else:
        return ('')


def import_yandex(url_list, folder_name):
    ya_token = get_token_ya()
    response = YaDisk(ya_token)
    for name, url_ in url_list.items():
        if name != 'size':
            flag = response.upload_file_(url_, '/'+folder_name+'/' + str(name))
            if flag == False:
                print(f'ОЙ...Что то пошло не так...\nОШИБКА загрзки {name}: {url_}')
                break


def request_vk_(URL):
    vk_token = get_token_vk()
    params = {
        'owner_id': '552934290',
        'album_id': 'profile',
        'photo_sizes': '1',
        'access_token': vk_token,
        'extended': '1',
        'v': '5.131'
    }
    request_vk = requests.get(URL, params=params)
    all_photo_ = request_vk.json()['response']
    all_photo = all_photo_['count']
    query_output = {}
    query_output['all_photo'] = all_photo
    query_output['request_vk'] = request_vk.json()

    return (query_output)


if __name__ == '__main__':
    hosts = 'https://cloud-api.yandex.net'
    URL = 'https://api.vk.com/method/photos.get'

    request_vk_ = request_vk_(URL)
    request_vk = request_vk_['request_vk']

    with open('request.json', 'w') as outfile:
        json.dump(request_vk, outfile, ensure_ascii=False, indent=2)
    print(f'json - фаил сохранен\nИмя файла:request.json\nДоступно для отправки на я.диск: {request_vk_["all_photo"]} ')

    items_teg = request_vk['response']
    all_photo = items_teg['items']
    url_list_ = {}
    url_list = []

    for all_size_one_photo in all_photo:
        list_size_one_photo = all_size_one_photo['sizes']
        unix_time = int(all_size_one_photo['date'])
        photo_upload_time = str(datetime.datetime.fromtimestamp(unix_time).strftime('%d-%m-%Y %H_%M_%S'))
        number_elements_list = len(list_size_one_photo)
        likes_photo = all_size_one_photo['likes']
        name_like = str(likes_photo['count']) +' ' + photo_upload_time
        if url_list_.get(name_like) == None:
            url_list_[name_like] = list_size_one_photo[number_elements_list - 1]['url']
            url_list_['size'] = list_size_one_photo[number_elements_list - 1]['type']
        else:
            url_list_[str(name_like) + '_'] = list_size_one_photo[number_elements_list - 1]['url']
            url_list_['size'] = list_size_one_photo[number_elements_list - 1]['type']
        url_list.append(url_list_)
        url_list_ = {}
    photo_upload = input('Сколько фото загрузить? ')
    all_photo_up = request_vk_['all_photo']
    try:
        if int(photo_upload) <= int(all_photo_up) and int(photo_upload) != 0:
            folder_name = create_folder_yandex()
            if folder_name != '':
                print(f'Папка создана')
                OK = input('Продолжить загрузку? (Y/N)')
                if OK.lower() == 'y':
                    new_mass_photo = []
                    for i in range(int(photo_upload)):
                        new_mass_photo.append(url_list[i])
                    for i in tqdm(new_mass_photo):
                        import_yandex(i,folder_name)
                        time.sleep(1)
                elif OK.lower() == 'y':
                    print('Загрузка прервана')
                else:
                    print('Неверный формат ввода')
        else:
            print('Ошибка ввода')
    except ValueError:
        print('Ошибка ввода')

    with open('result.json', 'w') as outfile:
        json.dump(new_mass_photo, outfile, ensure_ascii=False, indent=2)
    print(f'Информация о загруженных файлах сохранена.\nИмя файла: result.json')