from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict

class Article(BaseModel):
    title: str = None
    author: str = None
    post_href: str = None
    body: str = None
    image: str = None
    language: Dict[str, Optional[str]] = Field(default_factory=lambda: {"language_code": None})
    date: datetime = None

    @property
    def __bool__(self):
        if self.title and self.author and self.post_href and self.body:
            return self
        return None
