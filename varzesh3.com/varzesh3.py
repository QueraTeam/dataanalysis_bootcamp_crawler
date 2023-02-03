from bs4 import BeautifulSoup
import requests
import csv
from requests import HTTPError, ConnectionError

def connect():
    URL = 'https://www.varzesh3.com/'
    try:
        response = requests.get(URL)
        print(f'HTTP response code: {response.status_code}')
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return response
    except HTTPError as HTTPErr:
        print(f'HTTP ERROR: {HTTPErr}')
    except ConnectionError as ConnectionErr:
        print(f'CONNECTION ERROR: {ConnectionErr}')


def csv_writer(file_name, data):
    with open(file_name + '.csv', 'w') as file:
        dict_writer = csv.DictWriter(file, data[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(data)

    
def extract_news(soup):
    news_list = list()
    news = soup.select('.widget-holder .widget.news .news-main-list ul li')
    for new in news:
        new_dict = {}
        new_dict['title'] = new.find('a').get('title')
        new_dict['url'] = new.find('a').get('href')
        new_dict['type'] = new.get('class')
        news_list.append(new_dict)
    csv_writer('news', news_list)


def extract_tables(soup):
    tables = soup.select('.table-holder .league-standing')
    for table in tables:
        rows = list()
        name = table.find('caption').get_text()
        headers = [column.get_text() for column in table.select('thead tr th')]
        teams = table.select('tbody tr')
        for team in teams:
            team_dict = {}
            for index, value in enumerate(team.select('td')):
                team_dict[headers[index]] = value.get_text()
            rows.append(team_dict)
        csv_writer(name, rows)


if __name__ == '__main__':
    response = connect()
    soup = BeautifulSoup(response.content, 'html.parser')
    extract_news(soup)
    extract_tables(soup)
    print("Done! :)")