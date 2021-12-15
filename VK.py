import requests
import datetime as dt

token_vk = ""
test_vk_id = ""


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
    return dict_search[need_elem].get(
           'url'), dict_search[need_elem].get('type')


class VK_request:
    def __init__(self, version='5.131'):
        self.token = token_vk
        self.id = test_vk_id
        self.version = version
        self.start_params = {'access_token': self.token, 'v': self.version}
        self.json, self.export_dict = self.sort_info()

    def get_photo_info(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id,
                  'album_id': 'profile',
                  'photo_sizes': 1,
                  'extended': 1}
        photo_info = requests.get(
            url=url, params={**self.start_params, **params}).json()['response']
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
                json_lst.append({'file name': file_name,
                                 'size': value["size"]})
                sorted_dict[file_name] = picture_dict[elem][0]['url_picture']
        return json_lst, sorted_dict
