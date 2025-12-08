from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Union

class LLMClient(ABC):
    @abstractmethod
    def query(self, 
              prompt: str, 
              history: Optional[List[Dict]] = None, 
              image_path: Optional[str] = None,
              tools: Optional[List[Dict]] = None,
              tool_choice: Optional[str] = "auto",
              temperature: float = 0.7, 
              **kwargs) -> Union[str, any]:
        pass