import logging
from utils import Client, QueueManager
from services import ArticleService
from models.GenerationModels import OpenChat, Gemma_2b

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set the default logging level to DEBUG

# Create loggers
logger = logging.getLogger(__name__)
error_logger = logging.getLogger("error_logger")

# Create handlers
articles_handler = logging.FileHandler("logs/Articles.log")
error_handler = logging.FileHandler("logs/Error.log")

# Configure handlers
articles_handler.setLevel(logging.INFO)
error_handler.setLevel(logging.ERROR)

# Create formatters and add to handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
articles_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)

# Add handlers to loggers
logger.addHandler(articles_handler)
error_logger.addHandler(error_handler)

def main():
    Manager = QueueManager()
    # TODO CHECK FOR NULL VALUE
    queue = Manager.get_queue()
    for article_id in queue:
        Worker = Client(article_id[0])
        Worker.article = ArticleService().extract_tags(Worker.article, model=OpenChat())
        Worker.article = ArticleService().categorize(Worker.article, model=OpenChat())
        Worker.article = ArticleService().annotate(Worker.article, model=OpenChat())
        if Worker.article.language_to_answer_code != Worker.article.language_code:
            Worker.article = ArticleService().translate(Worker.article, model=OpenChat())
        if not Worker.send_article():
            error_logger.error("Article has not been annotated. Article: %s" % Worker.article.__dict__)
            break
        logger.info("Article has been annotated. Article: %s" % Worker.article.__dict__)

if __name__ == "__main__":
    main()
