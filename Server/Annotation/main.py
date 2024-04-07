

from utils import Client, QueueManager
from services import ArticleService
from models.GenerationModels import Mistral, Gemma_2b


def main():
    Manager = QueueManager()
    queue = Manager.get_queue()[0]
    for  article_id in queue:
        Worker = Client(article_id)
        Worker.article = ArticleService().extract_tags(Worker.article, model=Gemma_2b())
        Worker.article = ArticleService().categorize(Worker.article, model=Mistral())
        print(Worker.article)
        

if __name__ == "__main__":
    main()