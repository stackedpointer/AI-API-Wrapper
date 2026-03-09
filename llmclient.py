from openai import OpenAI

class LLMCLIENT:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
    def generate(self, messages):
        response = self.client.responses.create(model ="gpt-5-nano", input=messages)
        return response.output_text