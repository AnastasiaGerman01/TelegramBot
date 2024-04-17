from config import DRIVER_PATH, URL
from selenium import webdriver
from selenium.webdriver.common.by import By
from db import find_all_search, process_laptops

class ParseLaptop:
    def __init__(self, url, xpath, bot = None):
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        self.driver.minimize_window()
        self.url = url
        self.bot = bot
        self.xpath = xpath

    def __del__(self):
        self.driver.close()

#Функция парсинга
    async def parse(self):
        #Запрашиваем все ключевые слова, введённые пользователем
        search_models = find_all_search()
        #Перебираем все страницы с 1 по 15 с вариантами предложений
        for page in range(1, 15):
            print("page = ", page)
            # print(self.url.format(page))
            self.driver.get(self.url.format(page))
            #Перебираем все элементы на странице
            for i in range(1,10):
                #Получаем доступ к одному из предложений
                element = self.driver.find_element(By.XPATH, self.xpath.format(i))
                # Получаем доступ к ссылке на данное предложение
                element_reference_class = self.driver.find_element(By.XPATH, self.xpath.format(i)+'/a')
                element_url = element_reference_class.get_attribute('href')
                element_title = element.text
                #Проверяем есть удовлетворяет ли предложение хотя бы одному кючевому слову, заданному пользователем
                for search_model in search_models:
                    if element_title.find(search_model.title) >= 0:
                        await process_laptops(element_title, element_url, search_model.chatid, self.bot)
                    
