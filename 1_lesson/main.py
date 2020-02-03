from datetime import time
import requests


headers = {
    'User-agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'
    }

api_url = 'https://5ka.ru/api/v2/special_offers/'
api_url_category = 'https://5ka.ru/api/v2/categories/'


class CategoryObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        try:
            result = self.parent_group_name
        except AttributeError as e:
            result = self
        return result


def get_data(url:str, params:dict) -> dict:
    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            break
        time.sleep(1)
    return response.json()


def parse_data():
    url = 'https://5ka.ru/api/v2/special_offers/'
    params = {'records_per_page': 100, 'page': 1, 'categories': ''}
    results = []
    while url:
        response = get_data(url, params)
        url = response['next']
        results.extend(response['results'])
        params = {}
    return results

parse_data()

print(1)
 


