from bs4 import BeautifulSoup
import requests

class all_Items_Mvideo():
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}
        self.pages = []
        self.items = []
        self.items_marks = []

    def getting_answers_from_file(self, links):
        for item_link in links:
            res = {}
            link = item_link + '/reviews'
            getting_link = requests.get(link, headers=self.headers)
            html = getting_link.content
            soup = BeautifulSoup(html, "html.parser")
            try:
                reviews = soup.find('div', class_="review-ext-header review-ext-all")
                marks_block = reviews.find_all('li', class_="c-pseudo-tabs__item c-pseudo-tabs__item_multiselect")
                res_marks = [0, 0, 0, 0, 0]
                for mark_block in marks_block:
                    marks = mark_block.find_all('span')
                    if marks[0].get_text() == 'Рекомендуют':
                        continue
                    if marks[0].get_text() == 'Не нравится':
                        res_marks[0] = marks[1].get_text()
                        continue
                    if marks[0].get_text() == 'Ниже Среднего':
                        res_marks[1] = marks[1].get_text()
                        continue
                    if marks[0].get_text() == 'Нормально':
                        res_marks[2] = marks[1].get_text()
                        continue
                    if marks[0].get_text() == 'Хорошо':
                        res_marks[3] = marks[1].get_text()
                        continue
                    if marks[0].get_text() == 'Великолепно':
                        res_marks[4] = marks[1].get_text()
                        continue
                res[item_link] = res_marks
            except:
                res[item_link] = [0, 0, 0, 0, 0]
            self.items_marks.append(res)


    def getting_pages_links(self,link):
        getting_link = requests.get(link, headers=self.headers)
        html = getting_link.content
        soup = BeautifulSoup(html, "html.parser")
        pages = soup.find('div', class_='c-toggle-buttons')
        pages_link = pages.find_all('a')
        for page_link in pages_link:
            try:
                self.pages.append('https://www.mvideo.ru' + page_link['href'])
            except:
                pass
        for page in self.pages:
            getting_link = requests.get(page, headers=self.headers)
            html = getting_link.content
            soup = BeautifulSoup(html, "html.parser")
            pages = soup.find('div', class_='c-toggle-buttons')
            pages_link = pages.find_all('a')
            for page_link in pages_link:
                try:
                    str_link = 'https://www.mvideo.ru' + page_link['href']
                    if str_link not in self.pages:
                        self.pages.append('https://www.mvideo.ru' + page_link['href'])
                except:
                    pass

    def getting_items_links(self):
        for page_link in self.pages:
            getting_link = requests.get(page_link, headers=self.headers)
            html = getting_link.content
            soup = BeautifulSoup(html, "html.parser")
            main_page = soup.find('div', class_='search-results-area')
            items = main_page.find_all('a', class_="product-tile-picture-link")
            for item in items:
                item_link = 'https://www.mvideo.ru' + item['href']
                if item_link not in self.items:
                    self.items.append('https://www.mvideo.ru' + item['href'])

    def getting_reviews(self):
        o = 0
        for item_link in self.items:
            o +=1
            print(str(o) + ' from ' + str(len(self.items)) )
            res = {}
            link = item_link + '/reviews'
            getting_link = requests.get(link, headers=self.headers)
            html = getting_link.content
            soup = BeautifulSoup(html, "html.parser")
            try:
                reviews = soup.find('div', class_="review-ext-header review-ext-all")
                marks_block = reviews.find_all('li', class_="c-pseudo-tabs__item c-pseudo-tabs__item_multiselect")
                res_marks = [0, 0, 0, 0, 0]
                for mark_block in marks_block:
                    marks = mark_block.find_all('span')
                    if marks[0].get_text() == 'Рекомендуют':
                        continue
                    if marks[0].get_text() == 'Не нравится':
                        res_marks[0] = marks[1].get_text()
                        continue
                    if marks[0].get_text() == 'Ниже Среднего':
                        res_marks[1] = marks[1].get_text()
                        continue
                    if marks[0].get_text() == 'Нормально':
                        res_marks[2] = marks[1].get_text()
                        continue
                    if marks[0].get_text() == 'Хорошо':
                        res_marks[3] = marks[1].get_text()
                        continue
                    if marks[0].get_text() == 'Великолепно':
                        res_marks[4] = marks[1].get_text()
                        continue
                res[item_link] = res_marks
            except:
                res[item_link] = [0, 0, 0, 0, 0]
            self.items_marks.append(res)

    def give_me_result(self):
        return self.items_marks




