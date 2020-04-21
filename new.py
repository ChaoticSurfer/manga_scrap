import bs4
import requests
import logging
from time import sleep

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s    %(message)s')


def hot_mangas(start_page):
    req = requests.get(start_page).content
    soup = bs4.BeautifulSoup(req, 'html.parser')
    sleep(0.1)
    mangas = soup.find_all('a', {'class': 'genres-item-name text-nowrap a-h'})
    res = []
    for i in mangas:
        res.append(i.get('href'))
    return res


# mangas = hot_mangas('https://manganelo.com/genre-all?type=topview')


def get_info(manga):
    req = requests.get(manga).content
    soup = bs4.BeautifulSoup(req, 'html.parser')
    sleep(0.1)

    front_photo = soup.find('img', {'class': 'img-loading'}).get('src')
    descriptiom = soup.find('div', {'id': 'panel-story-info-description'}).text

    alternative_names = soup.find('td', {'class': 'table-value'}).text
    author = ''
    name = soup.find('div', {'class': 'story-info-right'}).text

    mangas = [i.get('href') for i in soup.find_all('a', {'class': "chapter-name text-nowrap"})]
    genres = [i for i in soup.find_all('td', {'class': 'table-value'})]
    print(name, 4, '\n\n\n-----------------------------------------------------------------')
    print(genres, 6, '\n\n\n-----------------------------------------------------------------')
    print(soup.find_all('td', {'class': 'table-value'}),'\n\n-------------------------------------------------------')

    result = {}


get_info('https://manganelo.com/manga/hyer5231574354229')
# for i in mangas:

#     i = str(i.get('href'))
#     after_sym = i[i.rfind('/')::]
#     # print(after_sym)
#     i = 'https://manganelo.com/chapter' + after_sym + '/chapter_0'
#     # print(i)
