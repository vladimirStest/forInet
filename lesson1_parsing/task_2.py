# Зарегистрироваться на https://openweathermap.org/api и написать функцию,
# которая получает погоду в данный момент для города,
# название которого получается через input. https://openweathermap.org/current

import json
from pathlib import Path
from pprint import pprint

import requests

url = 'https://api.openweathermap.org/data/2.5/weather'
cred_path = Path(__file__).cwd().parent / 'cred.json'

WEATHER_KEY = 'weather'


def get_api_key():
    with open(cred_path, "r") as cred:
        return json.load(cred)['lesson2']['API_KEY']


def get_request(city):
    params = {
        "q": city,
        "appid": get_api_key(),
    }
    return requests.get(url, params=params).json()


def print_repos(common):
    pprint(common[WEATHER_KEY])


def pipeline():
    weather = get_request(input(f'Введите город, узнайте погоду в нём: \n'))
    print_repos(weather)


if __name__ == "__main__":
    pipeline()
