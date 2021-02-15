from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import requests
import re

class Citilink():
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}
        self.pages = []
        self.items = []
        self.items_marks = []

    def getting_answers_from_file(self, links):
        opts = Options()
        opts.headless = True
        assert opts.headless
        driver = webdriver.Firefox(executable_path="geckodriver.exe", options=opts)
        dict = {}
        count = 0
        for link in links:
            count += 1
            print(str(count) + ' from ' + str(len(links)))
            main_link = link + 'otzyvy/'

            driver.get(main_link)
            try:
                reviews = driver.find_element_by_class_name('OpinionsRating__detail')
                marks = reviews.find_elements_by_class_name('OpinionsRatingDetail__percent')
                result = []
                for mark in marks:
                    result.append(re.findall('\d+', mark.text)[0])
            except:
                marks = driver.find_elements_by_class_name('OpinionsRatingDetail__percent')
                result = []
                for mark in marks:
                    result.append(re.findall('\d+', mark.text)[0])

            if result == []:
                result = ['0', '0', '0', '0', '0']
            result = list(reversed(result))
            dict[link] = result
            self.items_marks.append(dict)
        driver.close()
        return self.items_marks

    def getting_pages_links(self,link):
        getting_link = requests.get(link, headers=self.headers)
        html = getting_link.content
        soup = BeautifulSoup(html, "html.parser")
        all_categories = soup.find_all('div', class_='BrandCategories__brand-category-header')
        for category in all_categories:
            self.pages.append('https://www.citilink.ru/' + category.find('a')['href'])

    def getting_items_links(self):
        for page_link in self.pages:
            getting_link = requests.get(page_link, headers=self.headers)
            html = getting_link.content
            soup = BeautifulSoup(html, "html.parser")

            # Ищем ссылки на конкертные товары
            items_links = soup.find_all('div', class_='ProductCardVerticalLayout__wrapper-description ProductCardVertical__layout-description')
            for item_link in items_links:
                link = 'https://www.citilink.ru' + item_link.find('a')['href']
                if link not in self.items:
                    self.items.append(link)

            # Нашли меню со страницами
            soup.find('div', class_='PaginationWidget__wrapper-pagination')
            list_links = soup.find_all('a',
                                           class_ ='PaginationWidget__page PaginationWidget__page_next PaginationWidget__page-link')
            items_pages_on_category_page = []
            for list_link in list_links:
                items_pages_on_category_page.append(list_link['href'])

            # Перебираем встре страницы с товаром
            for item_page in items_pages_on_category_page:
                getting_link = requests.get(item_page, headers=self.headers)
                html = getting_link.content
                soup = BeautifulSoup(html, "html.parser")

                # Ищем ссылки на конкертные товары
                items_links = soup.find_all('div', class_='ProductCardVerticalLayout__wrapper-description ProductCardVertical__layout-description')
                for item_link in items_links:
                    link = 'https://www.citilink.ru' + item_link.find('a')['href']
                    if link not in self.items:
                        self.items.append(link)

                # Нашли меню со страницами
                soup.find('div', class_='PaginationWidget__wrapper-pagination')

                # Следующие страницы
                list_links = soup.find_all('a',
                                               class_='PaginationWidget__page PaginationWidget__page_next PaginationWidget__page-link')

                for list_link in list_links:
                    if list_link['href'] not in items_pages_on_category_page:
                        items_pages_on_category_page.append(list_link['href'])

    def getting_reviews(self):
        opts = Options()
        opts.headless = True
        assert opts.headless
        driver = webdriver.Firefox(executable_path="geckodriver.exe",  options=opts)

        count = 0
        for link in self.items:
            count +=1
            print(str(count) + ' from ' + str(len(self.items)) )
            main_link = link + 'otzyvy/'
            dict = {}
            driver.get(main_link)
            try:
                reviews = driver.find_element_by_class_name('OpinionsRating__detail')
                marks = reviews.find_elements_by_class_name('OpinionsRatingDetail__percent')
                result = []
                for mark in marks:
                    result.append(re.findall('\d+', mark.text)[0])
            except:
                marks = driver.find_elements_by_class_name('OpinionsRatingDetail__percent')
                result = []
                for mark in marks:
                    result.append(re.findall('\d+', mark.text)[0])

            if result == []:
                result = ['0','0','0','0','0']
            result = list(reversed(result))
            dict[link] = result
            self.items_marks.append(dict)
        driver.close()
        return self.items_marks

    def give_me_result(self):
        return self.items_marks
