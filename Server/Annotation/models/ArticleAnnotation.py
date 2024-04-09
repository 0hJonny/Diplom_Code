import re

from dataclasses import dataclass, field

@dataclass
class ArticleAnnotation:
    id: str
    title: str
    body: str
    language_code: str = ""
    language_to_answer_code: str = ""
    language_to_answer_name: str = ""
    theme_name: str = ""
    tags: list[str] = field(default_factory=list)
    annotation: str = None
    neural_networks: dict[str, str] = field(default_factory=dict)

    def check_article_annotation(self):
        """Check if the article annotation is valid."""
        if self.body is None:
            return False
        if self.language_code is None:
            return False
        if self.language_to_answer_code is None:
            return False
        if self.language_to_answer_name is None:
            return False
        if self.theme_name is None:
            return False
        if self.tags is None:
            return False
        if self.annotation is None:
            return False
        if self.neural_networks is None:
            return False
        if not self.check_annotation():
            return False
        return True

    def check_annotation(self):

        # Регулярное выражение для поиска заголовков в формате "### Название раздела:"
        pattern = r'###\s*([^:\n]+):'
        
        # Поиск всех заголовков в тексте
        matches = re.findall(pattern, self.annotation)
        
        # Проверка наличия всех необходимых заголовков
        required_headings = [
            "Main Facts and Events",
            "Key Ideas",
            "Further Interest",
            "Important Keywords",
            "Highlighted Text"
        ]
        for heading in required_headings:
            if heading not in matches:
                return False
        
        # Если все заголовки найдены, возвращаем True
        return True


    def add_tag(self, tag: str):
        """Add a tag to the article."""
        if len(tag) <= 20 and tag not in self.tags:
            self.tags.append(tag)

    def add_neural_network(self, key: str, value: str):
        """Add a neural network to the article."""
        self.neural_networks[key] = value

    @classmethod
    def get_json(cls, json_data):
        return cls(
            id=json_data.get("id"),
            title=json_data.get("title"),
            body=json_data.get("body"),
            language_code=json_data.get("language_code"),
            language_to_answer_code=json_data.get("language_to_answer_code"),
            language_to_answer_name=json_data.get("language_to_answer_name"),
            theme_name=json_data.get("theme_name"),
            tags=json_data.get("tags", []),
            annotation=json_data.get("annotation"),
            neural_networks=json_data.get("neural_networks", {})
        )