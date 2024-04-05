from dataclasses import dataclass


@dataclass
class Article:
    title: str
    author: str
    post_href: str
    body: str
    image: str
