from urllib.error import HTTPError
import requests
from bs4 import BeautifulSoup
import pandas as pd


def handle_error(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except HTTPError as http_err:
        print('HTTP error occurred:  {}'.format(http_err))
    except ConnectionError as conn_err:
        print('Connection error occurred:  {}'.format(conn_err))
    except TimeoutError as timeout_err:
        print('Timeout error occurred:  {}'.format(timeout_err))
    except requests.exceptions as req_err:
        print('Request error occurred:  {}'.format(req_err))

def create_table(bs):
    author_book = bs.find_all(class_='book_bookAuthor__1n-U7')
    title_book = bs.find_all(class_='book_bookTitle__1VUnJ')
    author_book_series = pd.Series(author_book)
    title_book_series = pd.Series(title_book)
    table = pd.DataFrame({'Title': title_book_series, 'Author': author_book_series})
    print(table)

def scrape(url):
    handle_error(url)
    html = requests.get(url)
    bs = BeautifulSoup(html.content, 'html.parser')
    create_table(bs)


if __name__ == "__main__":
    url = "https://taaghche.com/filter?filter-collection=3130&filter-hasPhysicalBook=0&filter-target=4&order=1"
    scrape(url)
