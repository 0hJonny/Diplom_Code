# Download the model before using.
# Check ollama/start.sh


from .GenerationModel import GenerationModel
from .GenerationResponse import GenerationResponse
from models import ArticleAnnotation

class Mistral(GenerationModel):
    def __init__(self):
        super().__init__()
        self.model_name = "mistral"
        self.data = {
            "stream": False,  # Placeholder for stream option
            "options": {
                "temperature": 0.1,  # Placeholder for temperature option
                "repeat_penalty": 1.05  # Placeholder for repeat_penalty option
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
            Translate article title to %s language. Safe the structure. 
            Article title: %s
            """
        prompt = prompt % (article.language_to_answer_name, article.title)

        answer = self._generate_text(prompt=prompt, stream=stream, options=options)

        article.title = answer.response

        prompt = """
            Translate article annotation to %s language. Safe the structure. 
            Article annotation: %s
            """
            
        if article.annotation is None:
            raise Exception("Annotation is None. Write annotation before translating.")

        prompt = prompt % (article.language_to_answer_name, article.annotation)

        answer = self._generate_text(prompt=prompt, stream=stream, options=options)

        article.annotation = answer.response

        article.neural_networks["translator"] = self.model_name
        
        return article
        
    def categorize(self, article: ArticleAnnotation, stream=None, options=None) -> ArticleAnnotation:
        prompt = """
            Classify the article to one of the topics: "technology", "crypto", "privacy", "security". Write one word only!. Article title: %s
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
            The tag is only one word.
            Example: Tags must has one or two words of main points of the Article. Write tags in camel style.
            Article title: %s
            Article content: %s
            """
        prompt = prompt % (article.title, article.body)
    
        answer: GenerationResponse = self._generate_text(prompt=prompt, stream=stream, options=options)

        tags_line = answer.response.strip().lstrip('[').rstrip(']').split(',')
        [article.add_tag(tag.replace("#", '').replace(' ', '')) for tag in tags_line]

        return article
