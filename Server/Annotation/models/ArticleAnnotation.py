from dataclasses import dataclass, field

@dataclass
class ArticleAnnotation:
    id: str
    title: str
    body: str
    language_code: str = ""
    theme_name: str = ""
    tags: list[str] = field(default_factory=list)
    annotation: str = None
    neural_networks: dict[str, str] = field(default_factory=dict)

    @classmethod
    def get_json(cls, json_data: dict):
        return cls(*json_data)
    
    
    def to_json(self):
        return {
            "id": getattr(self, 'id', None),
            "title": getattr(self, 'title', None),
            "created_at": getattr(self, 'created_at', None),
            "body": getattr(self, 'body', None),
            "theme_name": getattr(self, 'theme_name', None),
            "tags": getattr(self, 'tags', []),
            "annotation": getattr(self, 'annotation', None),
            "neural_networks": getattr(self, 'neural_networks', {}),
            "language_code": getattr(self, 'language_code', None)
        }
    
    def add_tag(self, tag: str):
        """Add a tag to the article."""
        if tag not in self.tags:
            self.tags.append(tag)

    def add_neural_network(self, key: str, value: str):
        """Add a neural network to the article."""
        self.neural_networks[key] = value