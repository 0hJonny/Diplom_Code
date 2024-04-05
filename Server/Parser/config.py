# config.py

"""
Этот код представляет собой словарь, в котором ключами являются названия ресурсов,
а значениями - соответствующие им URL-адреса.
Словарь используется для хранения информации о различных веб-ресурсах,
которые могут быть использованы в проекте для парсинга данных.

This code represents a dictionary where keys are the names of resources,
and values are their corresponding URLs.
The dictionary is used to store information about various web resources
that

Example:
    RESOURCES = {
    "category": {
        "example_site": "https://example.com",
        # Add other resources
    },
    # Add other resource categories and their subcategories accordingly
}

"""

SOURCES = [{
    "name" : "CyberNews",
    "language_code" : "en",
    "urls" : ["https://cybernews.com/tech",
              "https://cybernews.com/crypto",
              "https://cybernews.com/privacy",
              "https://cybernews.com/security",
              "https://cybernews.com/editorial"]}]