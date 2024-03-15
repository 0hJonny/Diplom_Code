from dataclasses import dataclass, field

@dataclass
class Article:
    id: int = field(default_factory=lambda: 0)
    title: str = field(default_factory=lambda: "")
    created_at: str = field(default_factory=lambda: "")
    source_link: str = field(default_factory=lambda: "")
    image_link: str = field(default_factory=lambda: "")
    body: str = field(default_factory=lambda: "")
    theme_name: str = None
    tags: list[str] = field(default_factory=lambda: [])
    annotation: str | None = None
    language_code: str = ""

