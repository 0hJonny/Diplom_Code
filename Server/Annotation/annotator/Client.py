import requests
import os

from modules import Article as ArticleModel


class Client:
    def __init__(self):
        self.api_access_token:str = ""
        self.api_user_login:str = os.getenv("API_USER_LOGIN")
        self.api_user_password:str = os.getenv("API_USER_PASSWORD")
        self.api_base_url:str = os.getenv("FLASK_API")
        self.article:ArticleModel = None
        self.login()

    def login(self):
        login_url = f"{self.api_base_url}/login"
        login_data = {"username": self.api_user_login, "password":  self.api_user_password}
        login_response = requests.get(login_url, json=login_data)
        self.api_access_token = login_response.json().get("access_token")
        return login_response.status_code

    def get_articles_queue(self):
        headers = {"Authorization": f"Bearer {self.api_access_token}"}
        response = requests.get(f"{self.api_base_url}/articles/annotations", headers=headers)
        # self.articles_queue = response.json()
        return response.json()

    def get_article(self, article_id: int):
        headers = {"Authorization": f"Bearer {self.api_access_token}"}
        response = requests.get(f"{self.api_base_url}/articles/{article_id}", headers=headers)
        self.article = ArticleModel(*response.json())
        return response.status_code 

    def set_article(self, article: ArticleModel):
        self.article.theme_name = article.theme_name
        self.article.tags = article.tags.copy()
        self.article.annotation = article.annotation
        self.article.language_code = article.language_code
        
    def add_annotate(self, article: ArticleModel):
        self.set_article(article)
        headers = {"Authorization": f"Bearer {self.api_access_token}"}
        data = self.article.__dict__
        print(data)
        # response = requests.post(f"{self.api_base_url}/articles/annotations", json=data, headers=headers)
        # return response.status_code
