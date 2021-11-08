from ya import Yandex
from vk import VK_request
import json

TOKEN_VK = "31d9be8fad58c49998fd1909dde2d9729eb9899136b79db75c2389f7f60610bde03a6aa8578d2f66e4a6e"
ID = "170907239"
TOKEN_YA = "AQAAAAAFHjZVAADLW7FYr7-e10sAvKQ_yQdr_n4"

if __name__ == '__main__':
    my_vk = VK_request(TOKEN_VK, ID)
    my_yandex = Yandex('ВК фото', TOKEN_YA)
    my_yandex.create_copy(my_vk.export_dict)

with open('json_file.json', 'w') as f:
    json.dump(my_vk.__dict__, f, ensure_ascii=False, indent=4)
