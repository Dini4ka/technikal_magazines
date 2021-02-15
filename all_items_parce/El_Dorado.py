from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import requests

class El_Dorado():

    def __init__(self):
        self.items_link = []
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}
        self.items_marks = []

    def find_items_links(self,link):
        driver = webdriver.Firefox(executable_path="geckodriver.exe")
        driver.get(link)
        sleep(2)
        pages = []
        buttons_menu = driver.find_element_by_class_name('qkT05Iu')
        buttons = buttons_menu.find_elements_by_tag_name('li')
        for button in buttons:
            try:
                pages.append(int(button.text))
            except:
                pass
        for page in range(1, pages[-1]):
            driver.execute_script('window.scrollBy(0,1500);')
            driver.find_element_by_class_name('owhv_3_').click()
            sleep(2)
        items = driver.find_elements_by_css_selector('[data-dy="product"]')
        for item in items:
            self.items_link.append(item.find_element_by_tag_name('a').get_attribute('href'))
        driver.close()

    def get_item_reviews(self):
        count = 0
        for link_main in self.items_link:
            count +=1
            print(str(count) + ' from ' + str(len(self.items_link)))
            dict = {}

            # Подключаемся к странице товара
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}
            getting_link = requests.get(link_main + '?show=response', headers=headers)
            html = getting_link.content
            soup = BeautifulSoup(html, "html.parser")

            # Достаём меню с со страницами отзывов
            all_stars = [0, 0, 0, 0, 0]
            user_reviews_pages_menu = soup.find('div', class_='usersReviewsPager')
            try:

                # Ищем все ссылки на страницы с отзывами
                user_reviews_pages = user_reviews_pages_menu.find_all('a')
                user_reviews_pages_links = []


                # Забираем с начальной страницы загрузки все ссылки на "видимые" страницы
                for user_reviews_page in user_reviews_pages:
                    try:

                        # Если мы смогли извлечь ссылку, значит подходит
                        link = 'https://www.eldorado.ru' + user_reviews_page['href']
                        if link not in user_reviews_pages_links:
                            user_reviews_pages_links.append(link)
                    except:
                        pass


                # Если ни одной ссылки извлечено не было, значит всего одна страница с отзывами - т.е. текущая
                if len(user_reviews_pages_links) == 0:
                    reviews = soup.find_all('div', class_='usersReviewsListItem')
                    for review in reviews:
                        all_stars[len(review.find_all('div', class_='star starFull')) - 1] += 1
                    dict[link_main] = all_stars
                    self.items_marks.append(dict)
                    continue

                # Перебираем все страницы с отзывами, чтобы увидеть скрытые и добавить их
                for link in user_reviews_pages_links:
                    try:
                        getting_link = requests.get(link, headers=headers)
                        html = getting_link.content
                        soup = BeautifulSoup(html, "html.parser")
                    except:
                        continue

                    # Забираем все отзывы с текущей страницы
                    reviews = soup.find_all('div', class_='usersReviewsListItem')
                    for review in reviews:
                        all_stars[len(review.find_all('div', class_='star starFull')) - 1] += 1

                    # Ищем новый страницы
                    user_reviews_pages_menu = soup.find('div', class_='usersReviewsPager')
                    user_reviews_pages = user_reviews_pages_menu.find_all('a')
                    for user_reviews_page in user_reviews_pages:
                        try:
                            link = 'https://www.eldorado.ru' + user_reviews_page['href']
                            if link not in user_reviews_pages_links:
                                user_reviews_pages_links.append(link)
                        except:
                            pass

            except:
                all_stars = [0, 0, 0, 0, 0]
            dict[link_main] = all_stars
            self.items_marks.append(dict)

    def getting_answers_from_file(self, links):
        count = 0
        for link_main in links:
            dict = {}
            count +=1
            print(str(count) + ' from ' + str(len(links)))

            # Подключаемся к странице товара
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}
            getting_link = requests.get(link_main + '?show=response', headers=headers)
            html = getting_link.content
            soup = BeautifulSoup(html, "html.parser")

            # Достаём меню с со страницами отзывов
            all_stars = [0, 0, 0, 0, 0]
            user_reviews_pages_menu = soup.find('div', class_='usersReviewsPager')
            try:

                # Ищем все ссылки на страницы с отзывами
                user_reviews_pages = user_reviews_pages_menu.find_all('a')
                user_reviews_pages_links = []

                # Забираем с начальной страницы загрузки все ссылки на "видимые" страницы
                for user_reviews_page in user_reviews_pages:
                    try:

                        # Если мы смогли извлечь ссылку, значит подходит
                        link = 'https://www.eldorado.ru' + user_reviews_page['href']
                        if link not in user_reviews_pages_links:
                            user_reviews_pages_links.append(link)
                    except:
                        pass

                # Если ни одной ссылки извлечено не было, значит всего одна страница с отзывами - т.е. текущая
                if len(user_reviews_pages_links) == 0:
                    reviews = soup.find_all('div', class_='usersReviewsListItem')
                    for review in reviews:
                        all_stars[len(review.find_all('div', class_='star starFull')) - 1] += 1
                    dict[link_main] = all_stars
                    self.items_marks.append(dict)
                    continue

                # Перебираем все страницы с отзывами, чтобы увидеть скрытые и добавить их
                for link in user_reviews_pages_links:
                    try:
                        getting_link = requests.get(link, headers=headers)
                        html = getting_link.content
                        soup = BeautifulSoup(html, "html.parser")
                    except:
                        continue

                    # Забираем все отзывы с текущей страницы
                    reviews = soup.find_all('div', class_='usersReviewsListItem')
                    for review in reviews:
                        all_stars[len(review.find_all('div', class_='star starFull')) - 1] += 1

                    # Ищем новый страницы
                    user_reviews_pages_menu = soup.find('div', class_='usersReviewsPager')
                    user_reviews_pages = user_reviews_pages_menu.find_all('a')
                    for user_reviews_page in user_reviews_pages:
                        try:
                            link = 'https://www.eldorado.ru' + user_reviews_page['href']
                            if link not in user_reviews_pages_links:
                                user_reviews_pages_links.append(link)
                        except:
                            pass
            except:
                all_stars = [0, 0, 0, 0, 0]
            dict[link_main] = all_stars
            self.items_marks.append(dict)

    def give_me_result(self):
        return self.items_marks

