import bs4
import requests
import logging
from collections import defaultdict
import pprint
from time import sleep

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s    %(message)s')


def hot_mangas(start_page):
    req = requests.get(start_page).content
    soup = bs4.BeautifulSoup(req, 'html.parser')
    mangas = soup.find_all('a', {'class': 'genres-item-name text-nowrap a-h'})
    for i in mangas:
        i = str(i.get('href')).replace('manga', 'chapter').join('/chapter_0')
        print(i)
hot_mangas('https://manganelo.com/genre-all?type=topview')

def manga_page_scrap(link):
    req = requests.get(link).content
    sleep(0.5)
    soup = bs4.BeautifulSoup(req, 'html.parser')
    img = soup.find_all('img')
    links = []
    for i in img:
        i = str(i.get('src'))
        if i.endswith('.jpg'):
            links.append(i)
    pprint.pprint(links)
    manga_page_scrap(go_to_next_chapter(soup=soup))


def go_to_next_chapter(soup):
    link = soup.find('a', {'class': 'navi-change-chapter-btn-next a-h'}).get('href')
    return link


# def main():
#     start = 'https://manganelo.com/chapter/bqyp275111576304835/chapter_0'
#     m = manga_page_scrap(start)


if __name__ == '__main__':
    main()
