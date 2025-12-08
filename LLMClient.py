from abc import ABC, abstractmethod
from typing import List, Optional, Dict

class LLMClient(ABC):
    @abstractmethod
    def query(self, 
              prompt: str, 
              history: Optional[List[Dict]] = None, 
              image_path: Optional[str] = None,
              temperature: float = 0.7, 
              **kwargs) -> str:
        """
        Sends a prompt (and optional image) to the LLM.
        
        Args:
            prompt (str): The user input text.
            history (list): A list of message dictionaries. Updates in-place.
            image_path (str): Path to a local image file (optional).
            temperature (float): Controls randomness.
            **kwargs: Arbitrary keyword arguments.
        """
        pass