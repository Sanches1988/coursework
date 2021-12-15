import requests
import time
from tqdm import tqdm

token_ya = ""


class Yandex:
    def __init__(self, directory_name):
        self.token = token_ya
        self.url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        self.headers = {'Authorization': self.token}
        self.folder = self.create_directory(directory_name)

    def create_directory(self, directory_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': directory_name}
        сreate_dir = requests.get(url=url,
                                  headers=self.headers,
                                  params=params).status_code != 200
        requests.put(url=url, headers=self.headers, params=params)
        return directory_name

    def in_directory(self, directory_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': directory_name}
        resource = requests.get(
            url=url, headers=self.headers,
            params=params).json()['_embedded']['items']
        in_folder_list = []
        for elem in resource:
            in_folder_list.append(elem['name'])
        return in_folder_list

    def create_copy(self, dict_files):
        files_in_folder = self.in_directory(self.folder)
        added_files_num = 0
        for k in tqdm(dict_files.keys()):
            time.sleep(1)
            if k not in files_in_folder:
                params = {'path': f'{self.folder}/{k}',
                          'url': dict_files[k],
                          'overwrite': 'false'}
                requests.post(self.url, headers=self.headers, params=params)
                added_files_num += 1
