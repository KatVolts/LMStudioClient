import base64
import os
from typing import List, Optional, Dict, Any, Union
from openai import OpenAI
from base_client import LLMClient

class LMStudioClient(LLMClient):
    def __init__(self, base_url="http://localhost:1234/v1", api_key="lm-studio"):
        self.client = OpenAI(base_url=base_url, api_key=api_key)

    def get_hosted_models(self):
        """Retrieves model IDs currently loaded in LM Studio."""
        try:
            response = self.client.models.list()
            return [model.id for model in response.data]
        except Exception as e:
            print(f"Error fetching models: {e}")
            return []

    def _encode_image(self, image_path):
        """Helper to convert local image to base64."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def query(self, 
              prompt: Optional[str] = None, 
              history: Optional[List[Dict]] = None, 
              image_path: Optional[str] = None,
              tools: Optional[List[Dict]] = None,
              tool_choice: Optional[str] = "auto",
              temperature: float = 0.7, 
              model_id=None, 
              system_instruction="You are a helpful assistant", 
              **kwargs):
        
        # 1. Auto-select model
        if not model_id:
            available = self.get_hosted_models()
            model_id = available[0] if available else "local-model"

        # 2. Build User Content
        user_content = None
        if prompt:
            if image_path:
                try:
                    base64_image = self._encode_image(image_path)
                    user_content = [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                except Exception as e:
                    return f"Error encoding image: {e}"
            else:
                user_content = prompt

        # 3. Manage History
        if history is None:
            messages = [{"role": "system", "content": system_instruction}]
            if user_content:
                messages.append({"role": "user", "content": user_content})
        else:
            if not history:
                history.append({"role": "system", "content": system_instruction})
            
            # Only append user message if content exists (skips for tool result follow-ups)
            if user_content:
                history.append({"role": "user", "content": user_content})
            messages = history

        try:
            # 4. Prepare Parameters
            params = {
                "model": model_id,
                "messages": messages,
                "temperature": temperature,
            }
            if tools:
                params["tools"] = tools
                params["tool_choice"] = tool_choice
            params.update(kwargs)

            # 5. API Call
            completion = self.client.chat.completions.create(**params)
            message_obj = completion.choices[0].message

            # 6. Handle Response
            if message_obj.tool_calls:
                # Convert to dict to prevent serialization errors
                msg_dict = message_obj.model_dump()
                
                # Fix for Jinja templates crashing on None content
                if msg_dict.get("content") is None:
                    msg_dict["content"] = ""
                
                if history is not None:
                    history.append(msg_dict)
                
                return message_obj.tool_calls
            else:
                response_text = message_obj.content
                if history is not None:
                    history.append({"role": "assistant", "content": response_text})
                return response_text

        except Exception as e:
            return f"Error during query: {e}"