import logging
# from firebase import firebase
from time import sleep

import bs4
import requests

# firebase = firebase.FirebaseApplication('https://manga-aa86c.firebaseio.com/', None)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s    %(message)s')


# logging.disable(logging.CRITICAL)


# def from_starter_page_links_and_titles_of_chapters(particular_manga):
#     req = requests.get(particular_manga).content
#     soup = bs4.BeautifulSoup(req, 'html.parser')
#     sleep(0.1)
#     mangas = soup.find_all('a', {'class': "chapter-name text-nowrap"})
#     title_and_link = {}
#
#     for i in mangas:
#         title = i.get('title')
#         href = i.get('href')
#         title_and_link[title] = href
#     return title_and_link


def hot_mangas(start_page):
    r = requests.get(start_page)
    if r.status_code == 200:
        r = r.content
        soup = bs4.BeautifulSoup(r, 'html.parser')
        sleep(0.1)
        mangas = soup.find_all('a', {'class': 'genres-item-name text-nowrap a-h'})
        result = [i.get('href') for i in mangas]
        return result
    else:
        hot_mangas(start_page)
        print('hot manga fail')


def manga_page_scrap(link):
    r = requests.get(link)
    if r.status_code == 200:
        r = r.content
        sleep(0.35)
        soup = bs4.BeautifulSoup(r, 'html.parser')
        # return [i.get('src') for i in soup.find_all('img') if i.get('src').endswith('.jpg')]
        img = soup.find_all('img')
        links = []
        for i in img:
            i = str(i.get('src'))
            if i.endswith('.jpg'):
                links.append(i)
        return links
    else:
        manga_page_scrap(link)
        print('mangaPageScrap Fail')

def get_info(manga):
    r = requests.get(manga)
    if r.status_code == 200:
        r = r.content
        soup = bs4.BeautifulSoup(r, 'html.parser')
        sleep(0.35)
        front_photo = soup.find('img', {'class': 'img-loading'}).get('src')
        description = soup.find('div', {'id': 'panel-story-info-description'}).text
        alternative_names = soup.find('td', {'class': 'table-value'}).text
        step_1 = soup.find('table', {'class': 'variations-tableInfo'})
        name = soup.find('div', {'class': "story-info-right"})
        name = name.find('h1').text
        author = step_1.find('a', {'class': 'a-h'})
        author = author.text
        genres = step_1.find_all('td', {'class': 'table-value'})
        genres = genres[-1].get_text().replace("\n", "")

        chapter_nums = [i.text for i in soup.find_all('a', {'class': "chapter-name text-nowrap"})]
        chapters = reversed([[manga_page_scrap(i.get('href'))] for i in
                             soup.find_all('a', {'class': "chapter-name text-nowrap"})])

        return {'name': name, 'author': author, 'alternative_names': alternative_names,
                'description': description, 'front_photo': front_photo, 'genres': genres, 'chapters': chapters}
    else:
        get_info(manga)
        print('GEt_Info_Fail')


# def go_to_next_chapter(soup):
#     link = soup.find('a', {'class': 'navi-change-chapter-btn-next a-h'}).get('href')
#     return link
#            json.dump(,json_file,ensure_ascii=False)


def main():
    mangas = hot_mangas('https://manganelo.com/genre-all?type=topview')
    json_file = open('data.txt', 'w')
    for manga in mangas:
        manga_everything = get_info(manga)

        # print(manga_everything)
        # for chapter in manga_everything['chapters']:
        #     chapter_photos = manga_page_scrap(chapter)
        #     print(chapter_photos)


# firebase.post('/manga-aa86c/manga', some_data)

if __name__ == '__main__':
    main()
