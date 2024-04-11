from utils import Client, QueueManager
from services import ArticleService, Logger
from models.GenerationModels import OpenChat, Gemma_2b

# Configure logging


def main():
    logger = Logger()
    Manager = QueueManager()
    # TODO CHECK FOR NULL VALUE
    while queue := Manager.get_queue():
        for article_id in queue:
            Worker = Client(article_id[0])
            Worker.article = ArticleService().extract_tags(Worker.article, model=OpenChat())
            Worker.article = ArticleService().categorize(Worker.article, model=OpenChat())
            Worker.article = ArticleService().annotate(Worker.article, model=OpenChat())
            if Worker.article.language_to_answer_code != Worker.article.language_code:
                Worker.article = ArticleService().translate(Worker.article, model=OpenChat())
            if not Worker.send_article():
                logger.info("Article has not been annotated. Article: %s" % Worker.article.__dict__)
                break
            logger.error("Article has been annotated. Article: %s" % Worker.article.__dict__)

if __name__ == "__main__":
    main()
