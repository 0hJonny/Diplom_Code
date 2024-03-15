

class Themes:
    THEMES = {
        'Technology': 'tech',
        'Crypto' : 'crypto',
        'Privacy' : 'privacy',
        'Security' : 'security'
    }

    def __init__(self):
        self.theme: str = None
        self.article_body: str = None


    @classmethod
    def get(cls, theme_name):
        return cls.THEMES.get(theme_name)


    @property
    def get_prompt(cls):
        themes_list = list(cls.THEMES.keys())
        themes_str = ', '.join(themes_list)
        themes_str = ', '.join([f"'{theme}'" for theme in cls.THEMES.keys()])
        return f"Определи тему статьи, выбери одну из предложенных: [{themes_str}]. Отвечай в формате theme: 'thame_name', соблюдай строго формат ответа. В ответе должна быть только тема. Статья {cls.article_body}"


