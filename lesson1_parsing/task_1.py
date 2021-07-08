# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json; написать функцию, возвращающую список репозиториев.

import json
from pathlib import Path

import requests

url = 'https://api.github.com'
cred_path = Path(__file__).cwd().parent / 'cred.json'


def get_username():
    with open(cred_path, "r") as cred:
        return json.load(cred)['lesson1']['USERNAME']


default_username = get_username()


def get_request(username):
    return requests.get(f'{url}/users/{username}/repos').json()


def save_repos(request):
    with open('repos.json', 'w') as repos:
        json.dump(request, repos)


def print_repos():
    with open('repos.json', 'r') as repos:
        repos_info = json.load(repos)
    for repo in repos_info:
        print(repo['name'])


def pipeline(username=default_username):
    save_repos(get_request(username))
    print_repos()


if __name__ == "__main__":
    pipeline()
