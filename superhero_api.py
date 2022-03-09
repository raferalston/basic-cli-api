import os
import json
import requests
import pprint

from get_all_heroes_data import get_data

#Pretty printer
pp = pprint.PrettyPrinter(indent=4)

#API data, get your key here: https://superheroapi.com/
API_KEY = 'YOURKEY'

#Data
directory_list = os.listdir()

if not 'heroes_data.json' in directory_list:
    get_data()

with open('heroes_data.json', 'r+') as f:
        heroes_data = json.loads(f.read())

class NotFoundError(Exception):
    pass

class SuperHeroAPI:
    def __init__(self, API=API_KEY, data=heroes_data):
        self._token = API
        self._data = data
        self._url = f'https://superheroapi.com/api/{self._token}'

    def get_all_heroes(self):
        return self._data
        
    def get_hero(self, name):
        name = self._parse_name(name)
        hero_id = self._get_id(name)
        return self._parse_api(self._url + f'/{hero_id}')

    def get_hero_image_url(self, name):
        name = self._parse_name(name)
        hero_id = self._get_id(name)
        return self._parse_api(self._url + f'/{hero_id}/image')['url']

    def get_hero_stats(self, name):
        name = self._parse_name(name)
        hero_id = self._get_id(name)
        return self._parse_api(self._url + f'/{hero_id}/powerstats')

    def _parse_name(self, name):
        return name.lower().title()

    def _get_id(self, name):
        data = self._data.get(name, False)
        if data:
            return data
        else:
            raise NotFoundError('Name not found')

    def _parse_api(self, url):
        response = requests.get(url, timeout=5)
        response.close()
        return response.json()

    def download_image(self, name):
        image_url = self.get_hero_image_url(name)
        with open(f'{name}.jpg', 'wb') as f:
            response = requests.get(image_url).content
            f.write(response)
    
    def beautiful_stats(self, name):
        stats = self.get_hero_stats(name)
        print(f'''Name: {stats['name']}
Int:  {stats['intelligence']}
Str:  {stats['strength']}
Spd:  {stats['speed']}
Pwr:  {stats['power']}
Cmbt: {stats['combat']}''')

