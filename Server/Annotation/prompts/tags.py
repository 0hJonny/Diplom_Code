class Tags:
    def __init__(self, article_body):
        self.tags = []
        self.article_body = article_body

    def add_tag(self, tag_string):
        tag_string = tag_string.strip().lower().replace('tags: ', '').replace("'", "")
        for tag in tag_string.split(','):
            tag = tag.strip()
            if tag:
                self.tags.append(tag)
    
    def get_tags(self) -> list[str]:
        return self.tags

    @property
    def get_prompt(self):
        return f"Определи теги статьи.  Пиши только лишь теги. Используй форму вывода tags: 'tag1, tag2 ...'. \
        Тег должен отражать ключевые моменты статьи и быть достаточно общим. Не больше 7 тегов. Статья: {self.article_body}"
