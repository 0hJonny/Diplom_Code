from .ServerInterface import ServerInterface
from models import ArticleAnnotation, User


class Client:
    def __init__(self, article_id: str):
        self.user = User()
        self.user.set_token(ServerInterface.login(self.user.get_login(), self.user.get_password())[0])
        self.get_article(article_id)
        
    def get_article(self, article_id: str):
        self.article = ArticleAnnotation.get_json(ServerInterface.get_article(article_id, self.user.get_token())[0])
