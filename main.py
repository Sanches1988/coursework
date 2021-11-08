from ya import Yandex
from vk import VK_request
import json

TOKEN_VK = ""
ID = ""
TOKEN_YA = ""

if __name__ == '__main__':
    my_vk = VK_request(TOKEN_VK, ID)
    my_yandex = Yandex('ВК фото', TOKEN_YA)
    my_yandex.create_copy(my_vk.export_dict)

with open('json_file.json', 'w') as f:
    json.dump(my_vk.__dict__, f, ensure_ascii=False, indent=4)
