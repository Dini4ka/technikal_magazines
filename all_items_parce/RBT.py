from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from time import sleep
import requests
import re

class RBT():
    def __init__(self):
        opts = Options()
        opts.headless = True
        assert opts.headless
        opts.add_argument("--enable-javascript")
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}
        self.driver = webdriver.Firefox(executable_path="geckodriver.exe", options=opts)
        self.pages = []
        self.items = []
        self.items_marks = []

    def getting_answers_from_file(self, links):
        count = 0
        for link in links:
            count +=1
            print(str(count) + ' from ' + str(len(links)))
            main_link = link +'otzyvy/'
            self.driver.get(main_link)
            if count == 1:
                sleep(15)
            else:
                sleep(10)
            dict = {}
            result = [0, 0, 0, 0, 0]
            try:
                id = self.driver.find_element_by_xpath('/html/body/div[2]/div[3]').get_attribute('data-item-id')
            except:
                print('no reviews')
                print(link)
                dict[link] = result
                self.items_marks.append(dict)
                continue
            try:
                pages_menu = self.driver.find_element_by_class_name('sp-pagination')
                max_page = pages_menu.find_elements_by_tag_name('a')[-1].get_attribute('data-sp-pagination-link')
            except:
                reviews = self.driver.find_elements_by_class_name('sp-review-rating')
                for review in reviews:
                    mark = len(review.find_elements_by_class_name('sp-star-on'))
                    result[mark - 1] += 1
                dict[link] = result
                self.items_marks.append(dict)
                continue
            for page in range(1, int(max_page) + 1):
                main_link = 'https://w-api2.aplaut.io/widgets/560533c15602351e2f000851/default/product/' + str(
                    id) + '/product-reviews.html?hostname=rbt.ru&page=' + str(page)
                getting_link = requests.get(main_link, headers=self.headers)
                html = getting_link.content
                soup = BeautifulSoup(html, "html.parser")
                reviews = soup.find_all('div', class_='sp-review-rating')
                for review in reviews:
                    mark = len(review.find_all('div', class_='sp-star-on'))
                    result[mark - 1] += 1
            dict[link] = result
            self.items_marks.append(dict)
        self.driver.close()


    def give_me_result(self):
        return self.items_marks
