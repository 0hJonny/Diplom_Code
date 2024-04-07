from .ServerInterface import ServerInterface
from models import User


class QueueManager:
    def __init__(self):
        self.user = User()
        self.user.set_token(ServerInterface.login(self.user.get_login(), self.user.get_password())[0])
        
    def get_queue(self):
        return ServerInterface.get_articles_queue(self.user.get_token())
