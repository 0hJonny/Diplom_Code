from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class ArticleWeb:
    id: str
    title: str
    timestamp: datetime
    category: str
    tags: List[str]
    content: str
    language_code: str
    image_source: Optional[str] = None