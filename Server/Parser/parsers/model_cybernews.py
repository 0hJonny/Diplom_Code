from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Article:
    title: str = None
    author: str = None
    post_href: str = None
    body: str = None
    image: str = None
    language: dict = field(default_factory=lambda: {"language_code": None})
    date: datetime = None

@property
def __bool__(self):
    if self.title is not None and self.author is not None and self.post_href is not None and self.body is not None:
        return self
    return None

