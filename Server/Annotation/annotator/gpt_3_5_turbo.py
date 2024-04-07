import g4f
from prompts import Prompt
from .Client import Client

class GPTAnnotator(Client):
    def __init__(self, article_id, language_code = "ru"):
        self.Client = Client()
        self.article_id = article_id
        self.Client.get_article(self.article_id)
        self.article_body = self.Client.article.body
        self.language_code = language_code
        self.prompt = Prompt(self.language_code, self.article_body)


    def _call_GPT(self, prompt):
        providers = [g4f.Provider.ChatgptNext,
                     g4f.Provider.ChatgptX,
                     g4f.Provider.FlowGpt,
                     g4f.Provider.GptTalkRu,
                     g4f.Provider.Koala,
                     g4f.Provider.Vercel]
        for provider in providers:
            print(provider)
            try:
                response = g4f.ChatCompletion.create(model = "gpt-3.5-turbo", provider=provider,
                                        messages=[{"role": "user", "content": f"{prompt}"}])
                return ''.join([f"{message}" for message in response])
            except Exception as e:
                print(e)

    def _call_Liao(self, prompt):
        try:
            response = g4f.ChatCompletion.create(model = "gpt-3.5-turbo", provider=g4f.Provider.Liaobots,
                                    messages=[{"role": "user", "content": f"{prompt}"}])
            return ''.join([f"{message}" for message in response])
        except Exception as e:
            print(e)
    
    
    def do_annotate(self):
        for step in ('annotation', 'themes', 'tags'):
            text_respone : str = None
            while not getattr(self.prompt, f'set_{step}')(text_respone):
                text_respone = self._call_GPT(getattr(self.prompt, step).get_prompt)
                print(text_respone)

        return True

    def do_summarize(self):
        self.Client.add_annotate(self.prompt.summarize())
        # pass