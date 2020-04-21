import bs4
import requests
import logging
# from firebase import firebase
from time import sleep

# firebase = firebase.FirebaseApplication('https://manga-aa86c.firebaseio.com/', None)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s    %(message)s')


# logging.disable(logging.CRITICAL)


# https://manganelo.com/chapter/bqyp275111576304835/chapter_0

def hot_mangas(start_page):
    req = requests.get(start_page).content
    soup = bs4.BeautifulSoup(req, 'html.parser')
    sleep(0.1)
    mangas = soup.find_all('a', {'class': 'genres-item-name text-nowrap a-h'})

    dict_title_linkHome = {}
    for i in mangas:
        logging.debug(i)

        title = i.get('title')
        i = i.get('href')
        dict_title_linkHome[title] = i
    return dict_title_linkHome


def from_starter_page_links_and_titles_of_chapters(particular_manga):
    req = requests.get(particular_manga).content
    soup = bs4.BeautifulSoup(req, 'html.parser')
    sleep(0.1)
    mangas = soup.find_all('a', {'class': "chapter-name text-nowrap"})
    title_and_link = {}

    for i in mangas:
        title = i.get('title')
        href = i.get('href')
        title_and_link[title] = href
    return title_and_link


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
    for manga_name, manga_home_link in mangas.items():

        links_and_titles = from_starter_page_links_and_titles_of_chapters(manga_home_link)
        for title, link in links_and_titles.items():
            link = manga_page_scrap(link)
            print(f'{title} --> {link}')


# firebase.post('/manga-aa86c/manga', some_data)

if __name__ == '__main__':
    main()
