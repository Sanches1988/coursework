import requests
import os
import datetime as dt


def get_token_id(file_name):
    with open(os.path.join(os.getcwd(), file_name), 'r') as file:
        token = file.readline().strip()
        id = file.readline().strip()
    return [token, id]

def time_convert(time):
    time_bc = dt.datetime.fromtimestamp(time)
    str_time = time_bc.strftime('%Y-%m-%d time %H-%M-%S')
    return str_time

def find_max_size(dict_search):
    max_size = 0
    for i in range(len(dict_search)):
        file_size = dict_search[i].get('width') * dict_search[i].get('height')
        if file_size > max_size:
            max_size = file_size
            need_elem = i
    return dict_search[need_elem].get('url'), dict_search[need_elem].get('type')

class VK_request:
    def __init__(self, token_list, version='5.131'):
        self.token = token_list[0]
        self.id = token_list[1]
        self.version = version
        self.start_params = {'access_token': self.token, 'v': self.version}
        self.json, self.export_dict = self.sort_info()

    def get_photo_info(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id,
                  'album_id': 'profile',
                  'photo_sizes': 1,
                  'extended': 1}
        photo_info = requests.get(url=url, params={**self.start_params, **params}).json()['response']
        return photo_info['count'], photo_info['items']

    def get_logs(self):
        photo_count, photo_items = self.get_photo_info()
        res = {}
        for i in range(photo_count):
            likes_count = photo_items[i]['likes']['count']
            url_download, picture_size = find_max_size(photo_items[i]['sizes'])
            time_warp = time_convert(photo_items[i]['date'])

            new_value = res.get(likes_count, [])
            new_value.append({'add_name': time_warp,
                              'url_picture': url_download,
                              'size': picture_size})
            res[likes_count] = new_value
        return res

    def sort_info(self):
        json_lst = []
        sorted_dict = {}
        picture_dict = self.get_logs()
        for elem in picture_dict.keys():
            for value in picture_dict[elem]:
                if len(picture_dict[elem]) == 1:
                    file_name = f'{elem}.jpeg'
                else:
                    file_name = f'{elem} {value["add_name"]}.jpeg'
                json_lst.append({'file name': file_name, 'size': value["size"]})
                sorted_dict[file_name] = picture_dict[elem][0]['url_picture']
        return json_lst, sorted_dict


class Yandex:
    def __init__(self, directory_name, token_list):
        self.token = token_list[0]
        self.url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        self.headers = {'Authorization': self.token}
        self.folder = self.create_directory(directory_name)

    def create_directory(self, directory_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': directory_name}
        if requests.get(url=url, headers=self.headers, params=params).status_code != 200:
            requests.put(url=url, headers=self.headers, params=params)
            print(f'Папка {directory_name} успешно создана в Я.Диске')
        else:
            print(f'Папка с именем {directory_name} уже существует.')
        return directory_name

    def in_directory(self, directory_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': directory_name}
        resource = requests.get(url=url, headers=self.headers, params=params).json()['_embedded']['items']
        in_folder_list = []
        for elem in resource:
            in_folder_list.append(elem['name'])
        return in_folder_list

    def create_copy(self, dict_files):
        files_in_folder = self.in_directory(self.folder)
        added_files_num = 0
        for k in dict_files.keys():
            if k not in files_in_folder:
                params = {'path': f'{self.folder}/{k}',
                          'url': dict_files[k],
                          'overwrite': 'false'}
                requests.post(self.url, headers=self.headers, params=params)
                print(f'Файл {k} добавлен')
                added_files_num += 1
            else:
                print(f'Такой файл {k} уже существует')
        print(f'Было добавлено {added_files_num} новых файлов')


token_id_VK = 'VKtoken.txt'
tokenYa = 'Yatoken.txt' 


if __name__ == '__main__':
    my_vk = VK_request(get_token_id(token_id_VK))
    my_yandex = Yandex('ВК фото', get_token_id(tokenYa))
    my_yandex.create_copy(my_vk.export_dict)

print(my_vk.json)

# my_yandex = Yandex('ВК фото', get_token_id(tokenYa))
# my_yandex.create_copy(my_vk.export_dict)