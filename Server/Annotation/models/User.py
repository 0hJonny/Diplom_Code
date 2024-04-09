import os
from dataclasses import dataclass


@dataclass
class User:
    api_access_token:str = ""
    api_user_login:str = os.getenv("API_USER_LOGIN")
    api_user_password:str = os.getenv("API_USER_PASSWORD")
    api_base_url:str = os.getenv("FLASK_API")

    @classmethod
    def get_token(cls):
        return cls.api_access_token
    
    @classmethod
    def set_token(cls, token):
        cls.api_access_token = token
    
    @classmethod
    def get_login(cls):
        return cls.api_user_login
    
    @classmethod
    def get_password(cls):
        return cls.api_user_password
    
    @classmethod
    def get_base_url(cls):
        return cls.api_base_url