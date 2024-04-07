from dataclasses import dataclass


@dataclass
class ArticleParser:
    title: str
    author: str
    post_href: str
    body: str
    image: str
