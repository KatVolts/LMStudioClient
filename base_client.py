from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Union

class LLMClient(ABC):
    """
    Abstract base class defining the standard interface for LLM interactions.
    """
    @abstractmethod
    def query(self, 
              prompt: Optional[str] = None, 
              history: Optional[List[Dict]] = None, 
              image_path: Optional[str] = None,
              tools: Optional[List[Dict]] = None,
              tool_choice: Optional[str] = "auto",
              temperature: float = 0.7, 
              **kwargs) -> Union[str, Any]:
        pass