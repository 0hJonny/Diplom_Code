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