from utils import Client, QueueManager
from services import ArticleService, Logger
from models.GenerationModels import OpenChat, Gemma_2b, Gemma_7b, Mistral

# Configure logging


def main():
    logger = Logger()
    Manager = QueueManager()
    # TODO CHECK FOR NULL VALUE
    while queue := Manager.get_queue()["data"]:
        for article_id in queue:
            Worker = Client(article_id["id"])
            
            for attempt in range(3):
                try:
                    Worker.article = ArticleService().extract_tags(Worker.article, model=Gemma_7b())
                    Worker.article = ArticleService().categorize(Worker.article, model=Gemma_7b())
                    Worker.article = ArticleService().annotate(Worker.article, model=Gemma_7b())
                    if Worker.article.language_to_answer_code != Worker.article.language_code:
                        Worker.article = ArticleService().translate(Worker.article, model=Mistral())
                    if Worker.article.check_article_annotation():
                        if not Worker.send_article():
                            logger.error("Cannot send Article to server. Article: %s" % Worker.article.__dict__)
                        logger.info("Article has been sent to server. Article: %s" % Worker.article.__dict__)
                        break
                except TypeError:
                    logger.error(f"Attempt {attempt+1} failed. Article: {Worker.article.__dict__}")
                    if attempt == 2:
                        logger.error("All attempts failed. Get new article.")
                        continue
                    else:
                        logger.error("Next attempt.")

if __name__ == "__main__":
    main()
