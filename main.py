import json
from VK import VK_request
from Ya import Yandex


if __name__ == '__main__':
    my_vk = VK_request()
    my_yandex = Yandex('ВК фото')
    my_yandex.create_copy(my_vk.export_dict)


with open('json_file.json', 'w') as f:
    json.dump(my_vk.__dict__, f, ensure_ascii=False, indent=4)
