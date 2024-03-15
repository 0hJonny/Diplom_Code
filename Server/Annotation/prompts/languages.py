

class Languages:
    LANGUAGES = {
        'English': 'en',
        'Chinese': 'zh',
        'Spanish': 'es',
        'Arabic': 'ar',
        'French': 'fr',
        'Russian': 'ru',
        'German': 'de',
        'Japanese': 'ja',
        'Portuguese': 'pt',
        'Hindi': 'hi'
    }

    @classmethod
    def names(cls):
        return list(cls.LANGUAGES.keys())

    @classmethod
    def codes(cls):
        return list(cls.LANGUAGES.values())
    
    @classmethod
    def get_lang_by_code(cls, code):
        for lang, lang_code in cls.LANGUAGES.items():
            if lang_code == code:
                return lang
