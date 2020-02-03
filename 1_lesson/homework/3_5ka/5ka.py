import json
from datetime import time
import requests


headers = {
    'User-agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'
    }


# TODO создать родительский класс

class CategoryObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        try:
            result = self.parent_group_code
        except AttributeError as e:
            result = self
        return result


class GroupObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        try:
            result = self.group_code
        except AttributeError as e:
            result = self
        return result


def get_data(url: str, params: dict) -> dict:
    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            break
        time.sleep(1)
    return response.json()


def parse_category():
    url = 'https://5ka.ru/api/v2/categories/'
    params = {}
    results = []
    while url:
        response = get_data(url, params)
        results = [CategoryObject(**itm) for itm in response]
        break
    return parse_group(results)


def parse_group(results):
    params = {}
    url = 'https://5ka.ru/api/v2/categories/'
    for category_code in results:
        response_group = get_data(url + str(category_code),  params)
        results_group = [GroupObject(**itm) for itm in response_group]
        #print('\n'.join(map(str, results_group)))
        parse_item(results_group)


def parse_item(results_group):
    url = 'https://5ka.ru/api/v2/special_offers/'
    for group_code in results_group:
        params = {'records_per_page': 100, 'page': 1, 'categories': group_code}
        response_item = get_data(url, params)
        # TODO переход на следующую страницу в случае, если есть пагинация
        if response_item['results']:
            with open(str(group_code) + '.json', 'w') as outfile:
                json.dump(response_item['results'], outfile)
            print(response_item)


parse_category()