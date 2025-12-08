from openai import OpenAI
from LLMClient import *

class LMStudioClient(LLMClient):
    def __init__(self, base_url="http://localhost:1234/v1", api_key="lm-studio"):
        self.client = OpenAI(base_url=base_url, api_key=api_key)

    def get_hosted_models(self):
        """
        Retrieves a list of currently loaded models.
        """
        try:
            response = self.client.models.list()
            return [model.id for model in response.data]
        except Exception as e:
            print(f"Error fetching models: {e}")
            return []

    def query(self, 
              prompt: str, 
              history: Optional[List[Dict]] = None, 
              temperature: float = 0.7, 
              model_id=None, 
              system_instruction="You are a helpful assistant", 
              **kwargs):
        """
        Sends a query to LM Studio with history and temperature support.
        """
        # 1. Handle Model Selection
        if not model_id:
            available = self.get_hosted_models()
            if available:
                model_id = available[0]
            else:
                return "Error: No hosted models found."

        # 2. Construct Messages
        if history is None:
            # Stateless mode: create a temporary list
            messages = [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ]
        else:
            # Stateful mode: maintain context
            if not history:
                history.append({"role": "system", "content": system_instruction})
            
            history.append({"role": "user", "content": prompt})
            messages = history

        try:
            # 3. API Call using the passed temperature
            params = {
                "model": model_id,
                "messages": messages,
                "temperature": temperature,
            }
            # Allow kwargs to override other params if necessary (e.g. max_tokens)
            params.update(kwargs)

            completion = self.client.chat.completions.create(**params)
            response_text = completion.choices[0].message.content

            # 4. Update History
            if history is not None:
                history.append({"role": "assistant", "content": response_text})

            return response_text

        except Exception as e:
            return f"Error during query: {e}"