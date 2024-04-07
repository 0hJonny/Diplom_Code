from .GenerationModel import GenerationModel
from .GenerationResponse import GenerationResponse
from models import ArticleAnnotation

class Gemma_2b(GenerationModel):
    def __init__(self):
        super().__init__()
        self.model_name = "gemma:2b"
        self.data = {
            "stream": False,  # Placeholder for stream option
            "options": {
                "temperature": 0.7,  # Placeholder for temperature option
                "repeat_penalty": 1.0,  # Placeholder for repeat_penalty option
                # "num_thread": 8  # Placeholder for num_thread option
            }
        }
    

    def annotate(self, article: ArticleAnnotation, stream=None, options=None) -> ArticleAnnotation:
        prompt = """
            Extract key points and sentences from the given news article, paying special attention to information that may be most significant for the reader. 
            Highlight the main facts, events, and ideas that could be crucial for understanding the content of the article. 
            Additionally, highlight information that may spark further interest from the reader or requires special attention. Use MarkDown Formatting.
            Article title: %s
            Article content: %s
            """
        prompt = prompt % (article.title, article.body)

        answer: GenerationResponse = self._generate_text(prompt=prompt, stream=stream, options=options)
        article.annotation = answer.response
        article.neural_networks["annotator"] = self.model_name
        
        return article

        
    def translate(self, article: ArticleAnnotation, stream=None, options=None) -> ArticleAnnotation:
        prompt = """
            Translate article to russian. 
            Article title: %s
            Article content: %s
            """
        prompt = prompt % (article.title, article.body)
        return self._generate_text(prompt=prompt, stream=stream, options=options)
        
    def categorize(self, article: ArticleAnnotation, stream=None, options=None) -> ArticleAnnotation:
        prompt = """
            Categorize article by theme. Write one word only!. Article title: %s
            Article content: %s
            """
        prompt = prompt % (article.title, article.body)
        
        answer = self._generate_text(prompt=prompt, stream=stream, options=options)
        
        article.theme_name = answer.response
        
        return article
        
    def extract_tags(self, article: ArticleAnnotation, stream=None, options=None) -> ArticleAnnotation:
        prompt = """
            Extract tags representing the main points of the article. Provide tags encapsulating core concepts, distinguishing features, or key takeaways. 
            Tags should be concise, reflecting one or two words of the main points of the article. Answer in format: [#tag1, #tag2,... #tags] like array of tags. 
            Example: Tags must has one or two words of main points of the Article. Write tags in camel style.
            Article title: %s
            Article content: %s
            """
        prompt = prompt % (article.title, article.body)
    
        answer: GenerationResponse = self._generate_text(prompt=prompt, stream=stream, options=options)

        # tags_line = answer.response.split()
        # article.tags = [tag.replace("#", '').replace('\n','') for tag in tags_line]
        article.tags = answer.response.replace('#', '').split('\n')

        return article
