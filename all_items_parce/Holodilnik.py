from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
from bs4 import BeautifulSoup
import requests
import re

class Holodilnik():
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}
        self.pages = []
        self.items = []
        self.items_marks = []


    def getting_answers_from_file(self, links):
        count = 0
        for link in links:
            count += 1
            print(str(count) + ' from ' + str(len(links)))
            getting_link = requests.get(link, headers=self.headers)
            html = getting_link.content
            soup = BeautifulSoup(html, "html.parser")
            all_marks_menu = soup.find('td', class_='info')
            dict ={}
            marks = [0, 0, 0, 0, 0]
            try:
                comments = all_marks_menu.find_all('div', class_='rating_box')
                for comment in comments:
                    str_mark = comment.find('div', class_='rating')['style']
                    int_mark = int(re.findall('\d+', str_mark.split(' ')[1])[0]) // 20
                    marks[int_mark - 1] += 1
            except:
                pass
            dict[link] = marks
            self.items_marks.append(dict)
            sleep(5)

    def getting_items_links(self,link):
        getting_link = requests.get(link, headers=self.headers)
        html = getting_link.content
        soup = BeautifulSoup(html, "html.parser")
        pages = soup.find('ul', class_='pagination')
        page = pages.find_all('li', class_ ='page-item')
        last_page = page[-2].get_text()
        for i in range(1,int(last_page)+1):
            page_link = link + '&page=' + str(i)
            getting_link = requests.get(page_link, headers=self.headers)
            html = getting_link.content
            soup = BeautifulSoup(html, "html.parser")
            items = soup.find_all('div', class_= 'preview-product')
            for item in items:
                self.items.append(' http://' + item.find('div', class_='product-name').find('a')['href'][2:])

    def get_item_reviews(self):
        count = 0
        for link in self.items:
            count+=1
            print(str(count) + ' from ' + str(len(self.items)))
            getting_link = requests.get(link, headers=self.headers)
            html = getting_link.content
            soup = BeautifulSoup(html, "html.parser")
            all_marks_menu = soup.find('td', class_='info')
            dict ={}
            marks = [0, 0, 0, 0, 0]
            try:
                comments = all_marks_menu.find_all('div', class_='rating_box')
                for comment in comments:
                    str_mark = comment.find('div', class_='rating')['style']
                    int_mark = int(re.findall('\d+', str_mark.split(' ')[1])[0]) // 20
                    marks[int_mark - 1] += 1
            except:
                pass
            dict[link] = marks
            self.items_marks.append(dict)
            sleep(5)

    def give_me_result(self):
        return self.items_marks
