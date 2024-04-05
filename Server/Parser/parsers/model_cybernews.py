from dataclasses import dataclass


@dataclass
class Article:
    title: str = None
    author: str = None
    post_href: str = None
    body: str = None
    image: str = None
    language_code: str = None