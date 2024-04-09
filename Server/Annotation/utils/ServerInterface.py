from typing import List, Tuple, Optional
import requests
import os

from models import ArticleAnnotation

class ServerInterface:
    api_base_url: str = os.getenv("FLASK_API")

    @staticmethod
    def get_articles_queue(user_token: str) -> List[dict]:
        headers = {"Authorization": f"Bearer {user_token}"}
        response = requests.get(f"{ServerInterface.api_base_url}/articles/annotations", headers=headers)
        return response.json()

    @staticmethod
    def get_article(article_id: str, user_token: str) -> Tuple[dict, int]:
        headers = {"Authorization": f"Bearer {user_token}"}
        response = requests.get(f"{ServerInterface.api_base_url}/articles/annotations/{article_id}", headers=headers)
        return response.json(), response.status_code

    @staticmethod
    def send_annotation(article_id: str, article: ArticleAnnotation, user_token: str) -> int:
        headers = {"Authorization": f"Bearer {user_token}"}
        data = article.__dict__
        response = requests.post(
            f"{ServerInterface.api_base_url}/articles/annotations/{article_id}",
            headers=headers,
            json=data,  # Convert ArticleAnnotation object to a dictionary before sending
        )
        return response.status_code

    @staticmethod
    def login(username: str, password: str) -> Tuple[Optional[str], int]:
        login_url = f"{ServerInterface.api_base_url}/login"
        login_data = {"username": username, "password": password}
        login_response = requests.get(login_url, json=login_data)
        user_token = login_response.json().get("access_token")
        return user_token, login_response.status_code
