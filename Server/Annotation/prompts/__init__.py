from .annotations import Annotations
from .themes import Themes
from .languages import Languages
from .tags import Tags


from modules import Article as ArticleModel

class Prompt:
    """Class for configuring the parameters of different classes"""

    def __init__(self, language, article_body):
        self.annotation = Annotations(language, article_body)
        self.themes = Themes()
        self.tags = Tags(article_body)
        self._language = language

    @property
    def language_code(self):
        """Returns the code of the language"""
        return self._language

    @property
    def language_name(self):
        """Returns the name of the language"""
        return Languages.get_lang_by_code(self._language)
    
    def set_themes(self, theme_name):
        input_string = theme_name
        if input_string is None:
            return False

        input_string = input_string.strip().lower().replace("theme: ", "").replace("'", "")
        theme_match = next((theme for theme, code in Themes.THEMES.items()
                            if input_string.lower() == theme.lower() or input_string.lower() in theme.lower()), None)
        if theme_match:
            self.themes.theme = theme_match
            return True
        return False
    
    def set_tags(self, tags):
        if tags:
            self.tags.add_tag(tags)
            return True
        else:
            return False

    def set_annotation(self, annotation):
        success = self.annotation.set_annotation(annotation)
        return success if annotation is not None else False

    def summarize(self) -> ArticleModel:
        article = ArticleModel(
            theme_name=self.themes.theme,
            annotation=self.annotation.annotation,
            language_code=self.language_code,
            tags=self.tags.get_tags()
        )
        return article


