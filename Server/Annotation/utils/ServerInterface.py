from typing import List, Tuple, Optional
import requests
import os

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
    def send_annotation(article_id: str, annotation: str, user_token: str) -> int:
        headers = {"Authorization": f"Bearer {user_token}"}
        data = {"article_id": article_id, "annotation": annotation}
        response = requests.post(f"{ServerInterface.api_base_url}/articles/articles/{article_id}", headers=headers, json=data)
        return response.status_code

    @staticmethod
    def login(username: str, password: str) -> Tuple[Optional[str], int]:
        login_url = f"{ServerInterface.api_base_url}/login"
        login_data = {"username": username, "password": password}
        login_response = requests.get(login_url, json=login_data)
        user_token = login_response.json().get("access_token")
        return user_token, login_response.status_code
