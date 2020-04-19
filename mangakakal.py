import bs4
import requests
import logging
from collections import defaultdict
import pprint
from time import sleep

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s    %(message)s')


# https://manganelo.com/chapter/bqyp275111576304835/chapter_0

def hot_mangas(start_page):
    req = requests.get(start_page).content
    soup = bs4.BeautifulSoup(req, 'html.parser')
    mangas = soup.find_all('a', {'class': 'genres-item-name text-nowrap a-h'})
    # for i in mangas:
    #     i = str(i.get('href'))
    #     after_sym = i[i.rfind('/')::]
    #     # print(after_sym)
    #     i = 'https://manganelo.com/chapter' + after_sym + '/chapter_0'
    #     # print(i)
    result = []
    for i in mangas:
        i = i.get('href')
        result.append(i)
    return result


# არ დამიმთავრებია გადავწყვიტე რომ უკეთესი ვარიანტი არსებობს
print(hot_mangas('https://manganelo.com/genre-all?type=topview'))


def from_starter_page_links_and_titles_of_chapters(particular_manga):
    req = requests.get(particular_manga).content
    soup = bs4.BeautifulSoup(req, 'html.parser')
    mangas = soup.find_all('a', {'class': "chapter-name text-nowrap"})
    title_and_link = {}
    for i in mangas:
        title = i.get('title')
        href = i.get('href')
        title_and_link[title] = href
    return title_and_link


print(from_starter_page_links_and_titles_of_chapters('https://manganelo.com/manga/hyer5231574354229'))


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
    return links


# def go_to_next_chapter(soup):
#     link = soup.find('a', {'class': 'navi-change-chapter-btn-next a-h'}).get('href')
#     return link


def main():
    mangas = hot_mangas('https://manganelo.com/genre-all?type=topview')
    for manga in mangas:
        logging.debug(manga)
        links_and_titles = from_starter_page_links_and_titles_of_chapters(manga)
        for title, link in links_and_titles.items():
            logging.debug(f'{title, link}')
            link = manga_page_scrap(link)
            print(f'{title} --> {link}')




if __name__ == '__main__':
    main()
