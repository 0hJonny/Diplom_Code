import os
import cloudscraper
import requests
from bs4 import BeautifulSoup
import time 
import random

"""
Класс BaseParser представляет собой базовый парсер, предназначенный для выполнения основных операций 
по получению и обработке данных из веб-ресурса. Класс включает методы для выполнения HTTP-запросов, 
парсинга HTML-контента с использованием библиотеки BeautifulSoup и отправки данных на сервер Flask.

- Конструктор класса принимает один аргумент `url:str`, который представляет собой URL-адрес ресурса, 
  который будет парситься.

- Метод _fetch_html() выполняет HTTP-запрос к указанному URL-адресу и возвращает HTML-контент страницы. 
  В случае возникновения ошибок при запросе, метод выводит сообщение об ошибке.

- Метод _send_data_to_server(data) предназначен для отправки данных на сервер. В данном примере он не реализован 
  полностью, но предоставляет место для реализации отправки данных в формате JSON на сервер Flask.

- Метод parse() выполняет парсинг HTML-контента с использованием библиотеки BeautifulSoup. 
  Если контент успешно получен, метод возвращает объект soup, который представляет собой дерево элементов HTML, 
  иначе выводит сообщение об ошибке и возвращает None.

Пример использования:
base_parser = BaseParser("https://example.com")
parsed_content = base_parser.parse()
"""


class BaseParser:
    def __init__(self, url: str):
        self.url:str = url
        self.scraper:cloudscraper = cloudscraper.create_scraper(delay=6, browser={"browser": "chrome", "device": "ipad"})
        self.api_access_token:str = ""
        self.api_user_login:str = os.getenv("API_USER_LOGIN")
        self.api_user_password:str = os.getenv("API_USER_PASSWORD")
        self.api_base_url:str = os.getenv("FLASK_API")
        # self._registration()
        self._login()

    # Регистрация пользователя
    def _registration(self):
        register_url = f"{self.api_base_url}/register"
        register_data = {"username": self.api_user_login, "password":  self.api_user_password}
        register_response = requests.post(register_url, json=register_data)
        print("Registration response:", register_response.text)


    # Авторизация пользователя и получение токена
    def _login(self):
        login_url = f"{self.api_base_url}/login"
        login_data = {"username": self.api_user_login, "password":  self.api_user_password}
        login_response = requests.get(login_url, json=login_data)
        self.api_access_token = login_response.json().get("access_token")

    def _fetch_html(self) -> bytes:
        max_attempts = 3
        for _ in range(max_attempts):
            time.sleep(random.uniform(1.041, 2.07))
            # time.sleep(random.uniform(0.041, 1.07))
            try:
                with self.scraper.get(self.url, timeout=5) as response:
                    response.raise_for_status()
                    return response.content
            except requests.exceptions.HTTPError as errh:
                print(f"HTTP Error: {errh}")
            except requests.exceptions.ConnectionError as errc:
                print(f"Error Connecting: {errc}")
            except requests.exceptions.Timeout as errt:
                print(f"Timeout Error: {errt}")
            except requests.exceptions.RequestException as err:
                print(f"OOps: Something Else: {err}")
            max_attempts -= 1
        return None
        
    def _handle_request_exceptions(self, exception):
        """
        Обрабатывает исключения при запросах.
        Возвращает True, если произошла ошибка, и False в противном случае.
        """
        if isinstance(exception, requests.exceptions.HTTPError):
            print(f"HTTP Error: {exception}")
        elif isinstance(exception, requests.exceptions.ConnectionError):
            print(f"Error Connecting: {exception}")
        elif isinstance(exception, requests.exceptions.Timeout):
            print(f"Timeout Error: {exception}")
        else:
            print(f"OOps: Something Else: {exception}")
        return True

    def _check_article_href(self, href: str) -> bool:
        try:
            headers = {"Authorization": f"Bearer {self.api_access_token}"}
            response = requests.get(f"{self.api_base_url}/articles/check", json={"article_href": href}, headers=headers, timeout=5)
            response.raise_for_status()
            return response.json().get("article_exists")
        except requests.exceptions.RequestException as e:
            return self._handle_request_exceptions(e)

    def _send_data_to_server(self, data) -> bool:
        try:
            headers = {"Authorization": f"Bearer {self.api_access_token}"}
            response = requests.post(f"{self.api_base_url}/articles", json=data, headers=headers, timeout=5)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return False
        

    def parse(self):
        html_content = self._fetch_html()
        if html_content:
            soup = BeautifulSoup(html_content, "lxml")
            return soup
        else:
            print("Failed to fetch HTML content.")
            return None
