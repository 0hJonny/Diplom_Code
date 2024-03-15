
class Annotations:
    def __init__(self, language : str, article_body : str):
        self.language : str = language
        self.article_body : str = article_body
        self.annotation : str = None
    
    @property
    def get_prompt(self):
        return (
            "Представь себя в роли редактора новостных статей. "
            "Напиши короткую аннотацию для статьи (тезисно), "
            "3-5 предложений, информативно. Отвечай на {} языке. "
            "Статья: {}"
        ).format(self.language, self.article_body)

    @property
    def get_annotation(self):
        return self.annotation

    def set_annotation(self, annotation):
        self.annotation = annotation
        return True
