import logging
from bs4 import BeautifulSoup
from parsers.base_parser_uc import BaseParser
from parsers.model_cybernews import Article

logging.basicConfig(filename='CyberNews.log', level=logging.INFO)
logger = logging.getLogger(__name__)

class CyberNewsParser(BaseParser):
    def __init__(self, url: str):
        super().__init__(url=url)
        self.data = []


    def _get_title_body(self, url: str) -> str:
        self.url = url
        response = self._fetch_html()
        buffer = []

        try:
            soup = BeautifulSoup(response, "lxml")
        except TypeError as e:
            logger.error(f"Can't parse the page {self.url}. Check the problem {e}")
            return ""

        content = soup.find("div", class_="content")

        upper_target_break = soup.find("a", class_="article-info__link")

        under_target_div = content.find('h2', class_='content__heading')  ## Check other key class or element

        if under_target_div is not None:
            try:
                text_array_from_page = under_target_div.find_all_previous(['a', 'p'])
            except AttributeError as e:
                logger.error(f"AttributeError: {e}\nProblem Link: {self.url}")
                return ""

        else:
            try:
                text_array_from_page = content.find_all(['a', 'p'])
            except AttributeError as e:
                logger.error(f"AttributeError: {e}\nProblem Link: {self.url}")
                return ""
        # under_target_div = content.find("hr")
        # under_target_div = soup.find("div", "weekly-deal__title")
        # if under_target_div is None:
        #     under_target_div = content.find('h2', id='more-from-cybernews')

        for element in text_array_from_page:
            if element == upper_target_break:
                break
            buffer.append(element.text.strip())

        buffer_text = "\n".join(reversed(buffer)) if under_target_div else "\n".join(buffer)

        return buffer_text

    def _parse(self) -> bool:
        html_content = self._fetch_html()
        _same_articles = 0
        if html_content:
            soup = BeautifulSoup(html_content, "lxml")
            posts_container = soup.find("div", "cells_space_xl").parent

            posts_title = posts_container.find_all("h3", class_="heading")
            posts_body = posts_container.find_all("div", class_="cells_responsive")

            # parse elements
            for title_element, body_element in zip(posts_title, posts_body):
                post_title = title_element.text
                post_href = title_element.parent.get('href')
                author = body_element.find("a", class_="text").text.strip()
                try:
                    image_href = body_element.find("img", class_="image").get("data-src")
                except AttributeError as error:
                    image_href = None
                    logger.error(f"{error}")
                body = self._get_title_body(url=post_href)

                if body == "":
                    continue

                self.data = Article(title=post_title,
                                    author=author,
                                    post_href=post_href,
                                    body=body,
                                    image_href=image_href)
                logger.info(f"Current {self.url}\nTitle: {post_title}\t href: {post_href}")
                # Send Data to the Server
                status = self._send_data_to_server(data=self.data.__dict__)
                if status is True or _same_articles >= 13:
                    print(f"Some Error ({status})")
                    return True
                elif status is False:
                    _same_articles += 1
        else:
            logger.error("Failed to fetch HTML content.")
            return True

    def _pagination(self):
        base_url = self.url
        page_number = 1
        while True:
            if page_number != 1:
                self.url = f"{base_url}/page/{page_number}"
            else:
                self.url = base_url
            page_number += 1
            if self._parse():
                return True

    def start(self):
        return self._pagination()