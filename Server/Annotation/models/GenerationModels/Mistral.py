# Download the model before using.
# Check ollama/start.sh


import re
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
            Article title: {%s}
            Article content: {%s}

            Use my Markdown Formatting template.

            Template:

            ### Main Facts and Events:
            - [List the main facts and events mentioned in the article here]

            ### Key Ideas:
            - [Summarize the key ideas or arguments presented in the article]

            ### Further Interest:
            - [Highlight any information that may spark further interest or requires special attention]

            ### Important Keywords:
            - *Keywords*: [List any important keywords mentioned in the article here]

            ### Highlighted Text:
            - [Insert any highlighted text or quotes from the article here]
            """
        prompt = prompt % (article.title, article.body)

        answer: GenerationResponse = self._generate_text(prompt=prompt, stream=stream, options=options)

        article.annotation = answer.message["content"]
        article.add_neural_network("annotator", self.model_name)
        
        return article

        
    def translate(self, article: ArticleAnnotation, stream=None, options=None) -> ArticleAnnotation:
        prompt = """
            Title: %s
            Translate the title to %s language. Answer must contain only the title in form of [Title: Title].
            """
        prompt = prompt % (article.title, article.language_to_answer_name)

        answer = self._generate_text(prompt=prompt, stream=stream, options=options)

        answer = answer.message["content"]

        # Parse answer
        match = re.match(r'\s*\[Title: (.*)\]\s*$', answer.strip())
        if match:
            article.title = match.group(1)
        else:
            article.title = None

        prompt = """
            Translate article annotation to %s language. Safe the structure. 
            Article annotation: 
            '''
            %s
            '''
            """
            
        if article.annotation is None:
            raise Exception("Annotation is None. Write annotation before translating.")

        prompt = prompt % (article.language_to_answer_name, article.annotation)

        answer = self._generate_text(prompt=prompt, stream=stream, options=options)

        answer = answer.message["content"]

        index = answer.find('###')

        if index != -1:
            answer = answer[index:]
        article.annotation = answer

        article.add_neural_network("translator", self.model_name)
        
        return article
        
    def categorize(self, article: ArticleAnnotation, stream=None, options=None) -> ArticleAnnotation:
        prompt = """
            Article:
            '''
            Title: %s
            Content: %s
            '''
            Classify the article to one of the topics: 
            "technology", 
            "crypto", 
            "privacy", 
            "security".
            Use template to asnwer:
            Answer template: "Topic: topic 1"
            """
        prompt = prompt % (article.title, article.body)
        
        answer = self._generate_text(prompt=prompt, stream=stream, options=options)

        words = ["technology", "crypto", "privacy", "security"]

        answer = answer.message["content"].lower()
        print(answer)

        # Check if any of the words are present in the string
        for word in words:
            if word in answer:
                article.theme_name = word
                break
        else:
            article.theme_name = None

        return article
        
    def extract_tags(self, article: ArticleAnnotation, stream=None, options=None) -> ArticleAnnotation:
        prompt = """
            Article:
            '''
            Title: %s
            Content: %s
            '''
            What is tags of the Article? Tag is representing the main points of the article. 
            Tags should be concise, reflecting one or two words of the main points of the article.
            Answer in format: [tag1, tag2,... tags] like array of tags. 
            Example: Tags must has one or two words of main points of the Article.
            """
        prompt = prompt % (article.title, article.body)
    
        answer: GenerationResponse = self._generate_text(prompt=prompt, stream=stream, options=options)

        # Remove the square brackets from the string
        tags = answer.message["content"].strip("[]")


        # Split the string by comma to get individual tags
        tags_list = tags.split(",")

        # Remove leading and trailing whitespace from each tag
        [article.add_tag(tag.strip()) for tag in tags_list]

        return article