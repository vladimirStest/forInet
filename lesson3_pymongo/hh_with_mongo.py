# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# записывающую собранные вакансии в созданную БД(добавление данных в БД по ходу сбора данных).
# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.
# Необязательно - возможность выбрать вакансии без указанных зарплат
# 3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.

import json
import re
from pprint import pprint

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def get_dom(html_string):
    return BeautifulSoup(html_string, "html.parser")


def get_element(html, attrs):
    return html.find(attrs=attrs)


class VacancyScraper:
    def __init__(self, vacancy, count_of_pages):
        self.count_of_pages = count_of_pages
        self.url = 'https://hh.ru/search/vacancy'
        self.params = {
            "area": "1",
            "fromSearchLine": 'true',
            "st": "searchVacancy",
            "text": vacancy
        }
        self.results = []
        self.FILE = "vacancies.json"

    def get_start_request(self):
        return get_dom(requests.get(self.url, params=self.params, headers=headers).text)

    def get_request(self, page):
        self.params["page"] = page
        return get_dom(requests.get(self.url, params=self.params, headers=headers).text)

    def check_count_of_pages(self):
        start_page = self.get_start_request()
        count_as_is = len(start_page.findAll(attrs={"data-qa": "pager-page"}))

        if self.count_of_pages <= count_as_is:
            return self.count_of_pages
        raise ValueError("Вы запрашиваете информацию со слишком большого количества страниц")

    @staticmethod
    def get_txt_of_element(html, attrs):
        try:
            return get_element(html, attrs).text.replace("\xa0", " ")
        except AttributeError:
            return None

    @staticmethod
    def get_salary_info(reg, salary, number):
        try:
            return ''.join(re.findall("[^\\.|\s]*", re.findall(reg, salary)[number]))
        except (TypeError, IndexError):
            return None

    def save_results(self):
        with open(self.FILE, 'w') as repos:
            json.dump(self.results, repos)

    def print_vacancies(self):
        with open(self.FILE, 'r') as vacancies:
            vacancy_info = json.load(vacancies)
            pprint(vacancy_info)

    def pipeline(self):
        self.check_count_of_pages()

        for page in range(self.count_of_pages):

            items = self.get_request(page).findAll(
                attrs={"class": "vacancy-serp-item"}
            )
            for vac in items:
                name = self.get_txt_of_element(vac, {"class": "resume-search-item__name"})
                salary = self.get_txt_of_element(vac, {"data-qa": "vacancy-serp__vacancy-compensation"})
                company = self.get_txt_of_element(vac, {"data-qa": "vacancy-serp__vacancy-employer"})
                city = re.split(r'[\s|,]+',
                                self.get_txt_of_element(vac, {"data-qa": "vacancy-serp__vacancy-address"}))[0]
                link = get_element(vac, {"data-qa": "vacancy-serp__vacancy-title"})['href']

                min_salary = self.get_salary_info(r'\d+[\\.|\s]\d+', salary, 0)
                max_salary = self.get_salary_info(r'\d+[\\.|\s]\d+', salary, 1)
                currency = self.get_salary_info(r'[a-zA-Zа-яА-ЯёЁ]+(?=[\\.|\s]*$)', salary, 0)

                added_dict = {'vacancy': name,
                              'min_salary': min_salary,
                              'max_salary': max_salary,
                              'currency': currency,
                              'company': company,
                              'city': city,
                              'link': link,
                              'site': self.url}
                self.results.append(added_dict)

        self.save_results()
        self.print_vacancies()


if __name__ == "__main__":
    vacancy = input(f'Введите искомую вакансию, узнайте наличие: \n')
    count_of_pages = int(input(f'Введите количество страниц с сайта: \n'))
    VacancyScraper(vacancy, count_of_pages).pipeline()
