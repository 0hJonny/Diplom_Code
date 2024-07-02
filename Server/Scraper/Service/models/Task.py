from pydantic import BaseModel
from models.Article import Article

class Task(BaseModel):
    task_id: str
    url: str
    status: str = "pending"
    article: Article = None

