import os
import undetected_chromedriver as uc
import requests
from bs4 import BeautifulSoup

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
        # UC options settings
        self.options = uc.ChromeOptions()
        self.options.arguments.extend(["--no-sandbox",
                                       "--disable-setuid-sandbox",
                                       "--disable-dev-shm-usage",
                                       "--disable-blink-features=AutomationControlled",
                                       "--disable-features=VizDisplayCompositor",
                                       "--disable-features=UseSurfaceLayerForVideo",
                                       "--force-color-profile=srgb",
                                       "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
                                       ])
        self.browser = uc.Chrome(options = self.options, headless=True,use_subprocess=False)
        
        # UC options ends
        self.url:str = url
        self.api_access_token:str = ""
        self.api_user_login:str = os.getenv("API_USER_LOGIN")
        self.api_user_password:str = os.getenv("API_USER_PASSWORD")
        self.api_base_url:str = os.getenv("DB_POST_API")
        # self._registration()
        self._login()
        def __del__(self):
                self.browser.quit()

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
        try:
            self.browser.get(self.url)
            self.browser.save_screenshot(f"screenshot.png")
            # response.raise_for_status()
            return self.browser.page_source
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"OOps: Something Else: {err}")
        return None


    def _send_data_to_server(self, data) -> bool:
        try:
            headers = {"Authorization": f"Bearer {self.api_access_token}"}
            response = requests.post(f"{self.api_base_url}/articles", json=data, headers=headers, timeout=5)
            response.raise_for_status()
            # print("Data sent successfully.")
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
            return False
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
            return True
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
            return True
        except requests.exceptions.RequestException as err:
            print(f"OOps: Something Else: {err}")
            return True

    def parse(self):
        html_content = self._fetch_html()
        if html_content:
            soup = BeautifulSoup(html_content, "lxml")
            return soup
        else:
            print("Failed to fetch HTML content.")
            return None
