from datetime import datetime
import logging
import base64
from bs4 import BeautifulSoup
from parsers.base_parser import BaseParser
from parsers.model_cybernews import Article

logging.basicConfig(filename='CyberNews.log', level=logging.INFO)
logger = logging.getLogger(__name__)

class CyberNewsParser(BaseParser):
    def __init__(self, url: str, language_code: str):
        super().__init__(url=url)
        self.language_code: str = language_code 

    def _get_article(self, article: Article):
        self.url = article.post_href
        response = self._fetch_html()
                

        try:
            soup = BeautifulSoup(response, "lxml")
        except TypeError as e:
            logger.error(f"Can't parse the page {self.url}. Check the problem {e}")

        # Get article title
        try:
            div_date = soup.find('div', class_='article-info__date')
            if div_date:
                date_formats = ["Updated on: %B %d, %Y %I:%M %p", "Updated on: %B %d, %Y"]
                for date_format in date_formats:
                    try:
                        article.date = datetime.strptime(div_date.text.strip(), f"{date_format}")
                        break
                    except ValueError:
                        pass
                else:
                    logger.error(f"Can't parse date {div_date.text.strip()} from page {self.url}")
                    article.date = None
                article.date = article.date.strftime("%Y-%m-%dT%H:%M:%SZ%z")
            div_section_body = soup.find('div', class_='section__body')
            if div_section_body:
                h1_element = div_section_body.find('h1', class_='heading')
                if h1_element:
                    article.title = h1_element.text
            
        except AttributeError as e:
            logger.error(f"AttributeError Title: {e}\nProblem Link: {self.url}")

        # Get article author
        try:
            div_author = soup.find('a', class_='article-info__link')
            if div_author:
                article.author = div_author.text.replace('\n', '')
        except AttributeError as e:
            logger.error(f"AttributeError Author: {e}\nProblem Link: {self.url}")

        # Get article image
        try:
            img_element = soup.select_one('article > figure.thumbnail > img')
            if img_element:
                article.image = img_element.get('src')
                # Get bytes from image
                self.url = article.image
                response = self._fetch_html()
                self.url = article.post_href
                # Convert bytes to base64
                article.image = base64.b64encode(response).decode('utf-8')
        except AttributeError as e:
            logger.error(f"AttributeError Image: {e}\nProblem Link: {self.url}")
        
        # Get article content

        buffer = []

        content = soup.find("div", class_="content")
        if content is None:
            content = soup.find("article > div", class_="content")

        upper_target_break = soup.find("a", class_="article-info__link")

        under_target_div = content.find(id='more-from-cybernews')
        if under_target_div is None:  # If not found above
            under_target_div = content.find('div', class_='cybernews-responsive-2')

        # under_target_div = content.find('h2', class_='content__heading')

        if under_target_div is not None:
            try:
                text_array_from_page = under_target_div.find_all_previous(['a', 'p'])
            except AttributeError as e:
                logger.error(f"AttributeError: {e}\nProblem Link: {self.url}")
                return ""

        else:
            try:
                text_array_from_page = content.find_all(['a', 'p'], recursive=True)
            except AttributeError as e:
                logger.error(f"AttributeError: {e}\nProblem Link: {self.url}")
                return ""

        for element in text_array_from_page:
            if element == upper_target_break:
                break
            buffer.append(element.text.strip())

        article.body = "\n".join(reversed(buffer)) if under_target_div else "\n".join(buffer)

        if article.body == "":
            logger.error(f"Empty article body: {self.url}")
            
        return None not in article.__dict__.values()

    def _parse(self) -> bool:
        html_content = self._fetch_html()
        if html_content == None:
            logger.error("Failed to fetch HTML content.")
            return True

        soup = BeautifulSoup(html_content, "lxml")
        posts_container = soup.find("div", class_="cells_space_xl").parent

        # Initialize list to store all hrefs
        posts_hrefs = []

        # Focus article Part
        focus_articles = posts_container.find_all("a", class_="focus-articles__link")
        for article in focus_articles:
            focus_article_link = article.get('href')
            posts_hrefs.append(focus_article_link)

        # Parse elements from page
        posts_title_elements = posts_container.find_all("h3", class_="heading")
        for title_element in posts_title_elements:
            post_href = title_element.parent.get('href')  # Assuming href is stored in the parent element
            posts_hrefs.append(post_href)

        _same_articles = 0  # Reset _same_articles for each parse
        for post_href in posts_hrefs:
            if self._check_article_href(post_href):
                _same_articles += 1
                if _same_articles >= 13:
                    print("Reached maximum number of same articles.")
                    return True
                continue

            article = Article(language={"language_code": self.language_code}, post_href=post_href)
            if not self._get_article(article):
                continue

            logger.info(f"Current {self.url}\nTitle: {article.title}\t href: {post_href}\t page: {self.page_number}")
            # Send Data to the Server
            status = self._send_data_to_server(data=article.__dict__)
            if not status:
                print("Some error occurred during data sending.")
                return True
            
    def _pagination(self):
        self.page_number = 0
        base_url = self.url
        while True:
            self.page_number += 1
            if self.page_number != 1:
                self.url = f"{base_url}/page/{self.page_number}"
            else:
                self.url = base_url
            if self._parse():
                return True

    def start(self):
        return self._pagination()