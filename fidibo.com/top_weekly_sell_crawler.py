# import libs
import requests
from bs4 import BeautifulSoup
import csv

# get response of fidibo web page
URL = 'https://fidibo.com/'
r = requests.get(URL)

# set bs4 on parser tree
soup = BeautifulSoup(r.content, 'html5lib')

# get the links of most weekly sell books
links = [item.get('href') for item in soup.select('.all_ a')]

# list for saving dictionaries of book's data
books = []

# get important data of each book
for i in range(0, len(links), 2):
    link = URL+links[i]
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html5lib')
    book = {}
    book['name'] = soup.find('div', attrs = {'class':'col-sm-11'}).h1.text
    w_t = soup.find('div', attrs = {'class':'col-sm-11'}).find_all('a', attrs= {'data-ut-object-type':'HL_BOOKS_FULL'})
    book['author'] = w_t[0]['data-ut-object-title']
    if len(w_t) >= 2:
        book['translator'] = w_t[1]['data-ut-object-title']
        if len(w_t) >= 3 :
            book['speaker'] = w_t[2]['data-ut-object-title']
        else :
            book['speaker'] = ''
    else :
        book['translator'] = ''
        book['speaker'] = ''
    book['fidibo_price'] = soup.select('.book-price')[0].text
    info = soup.find('div', attrs = {'class':'book-tags text-center'}).text.split('\n')
    if len(info) == 12 :
        book['publisher'] = info[2].strip()
        book['price'] = ''
        book['date'] = info[5].strip()
        book['pages'] = ''
    elif len(info) == 13 :
        book['publisher'] = info[2].strip()
        book['price'] = ''
        book['date'] = info[5].strip()
        book['pages'] = info[10].strip()
    elif len(info) == 17 :
        book['publisher'] = info[2].strip()
        book['price'] = info[6].strip()
        book['date'] = info[9].strip()
        book['pages'] = info[14].strip()
    print(book['speaker'])
    books.append(book)

# save the data in a csv file
filename = 'top_week_books.csv'
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f,['name','author','translator','speaker','fidibo_price','publisher','price','date','pages'])
    w.writeheader()
    for book in books:
        w.writerow(book)