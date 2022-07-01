from bs4 import BeautifulSoup
import json

import requests


URL = r'https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D1%81%D0%BA%D0%B8%D0%B5_%D0%BD%D0%B0%D1%81%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D1%8B%D0%B5_%D0%BF%D1%83%D0%BD%D0%BA%D1%82%D1%8B_%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%B9_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D0%B8'


def get_data():
    soup = BeautifulSoup(requests.get(URL).text, "html.parser")
    table_body = soup.find('table').find('tbody')
    rows = table_body.find_all('tr')

    data = []
    for row in rows:
        tds = list(row.find_all('td'))
        if tds:
            data.append({
                'city': str(tds[1].text).strip(),
                'city_link': str(tds[1].find('a')['href']).strip(),
                'city_part': str(tds[2].text).strip(),
                'city_part_link': str(tds[2].find('a')['href']).strip(),
                'count': str(tds[4]['data-sort-value']).strip(),
            })
    
    return data


def get_city_info(city: str):
    data = get_data()

    for i in data:
        if str(i[1]).lower() == city.lower():
            print(i[1])
