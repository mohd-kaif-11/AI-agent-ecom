from gpt4all import GPT4All

class SQLTranslator:
    def __init__(self, model_path):
        self.model = GPT4All(model_path)

    def nl_to_sql(self, question, schema):
        prompt = f"Translate the following question to an SQL query for this schema:\n{schema}\nQuestion: {question}"
        response = self.model.generate(prompt)
        return response.strip()
