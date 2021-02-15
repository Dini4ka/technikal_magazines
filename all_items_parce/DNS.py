from selenium import webdriver
from time import sleep
from selenium.webdriver.firefox.options import Options

class DNS():
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}
        opts = Options()
        opts.headless = True
        assert opts.headless
        self.driver = webdriver.Firefox(executable_path="geckodriver.exe", options=opts)
        self.pages = []
        self.items = []
        self.items_marks = []

    def find_items_links(self,link):
        self.driver.get(link)
        sleep(2)
        while (True):
            try:
                self.driver.execute_script('window.scrollBy(0,1500);')
                self.driver.find_element_by_class_name('pagination-widget__show-more-btn').click()
                sleep(2)
            except:
                break
        items_links = self.driver.find_elements_by_class_name('product-info__title-link')
        for item_links in items_links:
            self.items.append(item_links.find_element_by_tag_name('a').get_attribute('href'))

    def get_item_reviews(self):
        count = 0
        for link_main in self.items:
            count +=1
            print(str(count) + ' from ' + str(len(self.items)))
            dict = {}
            marks = []
            link = link_main + 'opinion/'
            self.driver.get(link)
            sleep(2)
            try:
                reviews_menu = self.driver.find_element_by_class_name('ow-counts')
                reviews = reviews_menu.find_elements_by_class_name('ow-counts__group')
                for review in reviews:
                    marks.append(review.text.split('\n')[0].split(' ')[0])
                marks = list(reversed(marks))
            except:
                marks = [0,0,0,0,0]
            dict[link_main] = marks
            self.items_marks.append(dict)
        self.driver.close()

    def getting_answers_from_file(self, links):
        count = 0
        for link_main in links:
            count +=1
            print(str(count) + ' from ' + str(len(links)))
            dict = {}
            marks = []
            link = link_main + 'opinion/'
            self.driver.get(link)
            sleep(2)
            try:
                reviews_menu = self.driver.find_element_by_class_name('ow-counts')
                reviews = reviews_menu.find_elements_by_class_name('ow-counts__group')
                for review in reviews:
                    marks.append(review.text.split('\n')[0].split(' ')[0])
                marks = list(reversed(marks))
            except:
                marks = [0, 0, 0, 0, 0]
            dict[link_main] = marks
            self.items_marks.append(dict)
        self.driver.close()

    def give_me_result(self):
        return self.items_marks

