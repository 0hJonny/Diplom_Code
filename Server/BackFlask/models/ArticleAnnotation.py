from dataclasses import dataclass

@dataclass
class ArticleAnnotation:
    id: int
    title: str
    created_at: str
    body: str
    theme_name: str
    tags: list[str]
    annotation: str | None
    neural_networks: dict[str, str]
    language_code: str

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "language_code": self.language
        }
    
    @classmethod
    def from_json(cls, json_data):
        return cls(
            id=json_data.get("id"),
            title=json_data.get("title"),
            created_at=json_data.get("created_at"),
            body=json_data.get("body"),
            theme_name=json_data.get("theme_name"),
            tags=json_data.get("tags", []),
            annotation=json_data.get("annotation"),
            neural_networks=json_data.get("neural_networks", {}),
            language_code=json_data.get("language_code")
        )