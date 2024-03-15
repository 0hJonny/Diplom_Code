from dotenv import load_dotenv
from annotator import GPTAnnotator, Client
from multiprocessing import Pool


def process_article(article_id):
    gpt = GPTAnnotator(*article_id)
    while not gpt.do_annotate():
        pass
    gpt.do_summarize()


def main():
    client = Client()
    articles_queue = client.get_articles_queue()
    print("Await of articles: ", len(articles_queue))
    with Pool(processes=2) as pool:
        pool.map(process_article, articles_queue)


if __name__ == "__main__":
    load_dotenv()
    main()