from dataclasses import dataclass

@dataclass
class Annotation:
    id: int
    title: str
    created_at: str
    source_link: str
    image_link: str
    body: str
    theme_name: str
    tags: list[str]
    annotation: str | None
    language_code: str
