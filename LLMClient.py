from abc import ABC, abstractmethod
from typing import List, Optional, Dict

class LLMClient(ABC):
    """
    A generic abstract base class for interacting with LLM providers.
    """

    @abstractmethod
    def query(self, 
              prompt: str, 
              history: Optional[List[Dict]] = None, 
              temperature: float = 0.7, 
              **kwargs) -> str:
        """
        Sends a prompt to the LLM.
        
        Args:
            prompt (str): The user input.
            history (list): A list of message dictionaries. Updates in-place.
            temperature (float): Controls randomness (0.0 to 1.0). Higher is more creative.
            **kwargs: Arbitrary keyword arguments.
            
        Returns:
            str: The text response from the model.
        """
        pass